import os
import logging
import grpc
from athera.sync.sirius.services import service_pb2
from athera.sync.sirius.services import service_pb2_grpc
import sys
import io 

ONE_MB = 1024 * 1024
MAX_CHUNK_SIZE = 1 * ONE_MB

REGION_URLS = {
    "us-west1": "us-west1.files.athera.io:443",
    "europe-west1": "files.athera.io:443",
    "australia-southeast1": "australia-southeast1.files.athera.io:443"
}

class Client(object):
    """
    Client to query the remote grpc file sync service, Sirius.
    
    Improvements:
    * Check if token is expired before performing API call. If so, refresh it.
    """

    def __init__(self, region, token):
        """ 
        'region': The ingress point for the data. Use the region geographically closest to you.
                  Other regions may have to perform a 'rescan' on the mount_id to detect the newly uploaded file.
        'token':  JSON Web Token. See athera.auth.generate_jwt.py on how to generate a JWT.
        """
        
        self.url = REGION_URLS.get(region)
        if not self.url:
            raise ValueError("Unknown region. Please use one of the following: {}".format(REGION_URLS.keys()))

        self.credentials = grpc.ssl_channel_credentials()
        self.token = token
        channel = grpc.secure_channel(self.url, self.credentials)
        self.stub = service_pb2_grpc.SiriusStub(channel)
       

    def get_mounts(self, group_id):
        """
        Provide a ist of the mounts available to the supplied group, including those inherited from ancestor groups.
        
        Returns of list of sirius.types.Mount objects.

        sirius.types.Mount:
            id              // (str) The id of the storage mount
            name            // (str) The name of the mount
            mount_location  // (str) The mount root path (where it will appear in Athera sessions)
            group_id        // (str) The id of the mount belongs to

        """

        request = service_pb2.MountsRequest()
        
        metadata = [('authorization', "bearer: {}".format(self.token)),
                    ('active-group', group_id)]
                
        try:
            mountsResponse = self.stub.Mounts(request, metadata=metadata)
            return mountsResponse.mounts, None
        except grpc.RpcError as e:
            logging.debug("grpc.RpcError %s", e)
            return [], e
        except AttributeError as e:
            return [], e

    def get_files(self, group_id, mount_id, path="/"):
        """
        Using the provided group and mount, provide a list of files at the (optional) supplied path.

        Returns a generator of sirius.services.FilesListResponse objects.

        sirius.services.FilesListResponse:
            path        // (str) The location where the listing has been done (relative to the mount root)
            mount_id    // (str) The id of the mount being queried
            file        // (sirius.types.File) A protobuf object. See below

        sirius.types.File:
            path        // (str) The full path of the file (relative to the mount root)
            name        // (str) Name
            mount_id    // (str) The id of the mount being queried
            size        // (int) Size of the object in bytes
            type        // (sirius.types.File.Type) See below
            
        sirius.types.File.Type:
            // A protobuf enumeration type.
            enum Type {
                UNKNOWN = 0;
                DIRECTORY = 1;
                FILE = 2;
                SEQUENCE = 3;
            }
        """
        request = service_pb2.FilesListRequest(mount_id=mount_id, path=path)
        metadata = [('authorization', "bearer: {}".format(self.token)),
                    ('active-group', group_id)]
        try:
            response = self.stub.FilesList(request, metadata=metadata)
            for resp in response:
                yield resp, None
        except grpc.RpcError as e:
            yield None, e

    def download_to_file(self, group_id, mount_id, destination_file, path="/", chunk_size=MAX_CHUNK_SIZE): 
        """
        Download a file in chunks of up to 1 Mb.

        'destination_file': A file-like object to which the downloaded data will be written.

        Returns an error if 'path' is not a file.
        """
        if chunk_size > MAX_CHUNK_SIZE: # We limit the chunk size to 1Mb
            raise ValueError("chunk_size exceeds maximum value of {} bytes ({}M)".format(MAX_CHUNK_SIZE, MAX_CHUNK_SIZE / ONE_MB))

        request = service_pb2.FileContentsRequest(mount_id=mount_id, path=path, chunk_size=chunk_size)
        metadata = [('authorization', "bearer: {}".format(self.token)),
                    ('active-group', group_id)]
                    
        total_bytes = 0
        try:
            response = self.stub.FileContents(request, metadata=metadata)
            for resp in response:
                destination_file.write(resp.bytes)
                total_bytes += resp.bytes

            logging.debug("Successfully wrote {} bytes into {}".format(total_bytes, destination_file.name))
        except grpc.RpcError as e:
            return e
        except AttributeError as e:
            return e

    def upload_file(self, group_id, mount_id, file_to_upload, destination_path, chunk_size=MAX_CHUNK_SIZE):
        """
        Upload a file by chunks of up to 1 Mb.

        'mount_id':         Storage Mount to upload file to.
        'file_to_upload':   The file object of the file to upload, read access is enough.
        'destination_path': The path on the mount where the file will be uploaded (relative to the mount root).

        An example:
        * The final location needs to be '/data/org/default-my-org/uploads/movie1.mov'
        * The mount provides the root path of '/data/org/default-my-org'
        * Therefore, the 'destination_path' would need to be 'uploads/movie1.mov'
        """
        if chunk_size > MAX_CHUNK_SIZE:
            raise ValueError("chunk_size exceeds maximum value of {} bytes ({}M)".format(MAX_CHUNK_SIZE, MAX_CHUNK_SIZE / ONE_MB))
        
        metadata = [
            ('authorization', "bearer: {}".format(self.token)),
            ('active-group', group_id),
            ('mount-id', mount_id),
            ('path', destination_path),
        ]

        try:
            response = self.stub.FileUpload(
                self._retrieve_file_bytes(file_to_upload, chunk_size),
                metadata=metadata
            )
            return response, None
        except grpc.RpcError as e:
            return None, e
        except AttributeError as e:
            return None, e

    def _retrieve_file_bytes(self, file, chunk_size):
        chunk = file.read(chunk_size)
        while chunk != b"":
            yield service_pb2.FileUploadRequest(
                chunk_size=chunk_size,
                bytes=chunk,
            )
            chunk = file.read(chunk_size)