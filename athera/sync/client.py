import os
import logging
import grpc
from athera.sync.sirius.services import service_pb2
from athera.sync.sirius.services import service_pb2_grpc
import sys
import io 

MAX_CHUNK_SIZE = 1024 * 1024  # 1Mb

class Client(object):
    # ToDo: CloseConnection for every method
    # ToDo: Before performing any api call, check if token is expired; if so: REFRESH IT
    """
    Client to query the remote grpc file sync service, Sirius.
    """

    def __init__(self, url, token):
        
        self.url = url
        # self.chunk_size = chunk_size
        credentials = grpc.ssl_channel_credentials()
        self.channel = grpc.secure_channel(self.url, credentials)
        self.stub = service_pb2_grpc.SiriusStub(self.channel)
        self.token = token
        

    def get_mounts(self, group_id):
        """
        Using the provided credentials, which identify a user, provide the mounts for the supplied group.
        """

        request = service_pb2.MountsRequest()
        
        metadata = [('authorization', "bearer: {}".format(self.token)),
                    ('active-group', group_id)]

        try:
            mountsResponse = self.stub.Mounts(request, metadata=metadata)
            return mountsResponse.mounts, None
        except grpc.RpcError as e:
            logging.debug("grpc.RpcError %s", e)
            return None, e
        except AttributeError as e:
            return None, e

    def get_files(self, group_id, mount_id, path="/"): # ToDo: User provide a buffer
        """
        Using the provided credentials, group and mount, provide a list of files at the (optional) supplied path.
        """
        request = service_pb2.FilesListRequest(mount_id=mount_id, path=path)
        metadata = [('authorization', "bearer: {}".format(self.token)),
                    ('active-group', group_id)]

        try:
            response = self.stub.FilesList(request, metadata=metadata, timeout=10)
            for resp in response:
                yield resp, None
        except grpc.RpcError as e:
            yield None, e

    def download_to_file(self, group_id, mount_id, destination_file, path="/", chunk_size=MAX_CHUNK_SIZE): # ToDo: User provide a buffer
        """
        Download a file by chunks of up to 1 Mb
        """
        if chunk_size > MAX_CHUNK_SIZE: # We limit the chunk size to 1Mb
            chunk_size = MAX_CHUNK_SIZE
        request = service_pb2.FileContentsRequest(mount_id=mount_id, path=path, chunk_size=chunk_size)
        metadata = [('authorization', "bearer: {}".format(self.token)),
                    ('active-group', group_id)]
        total_bytes = 0
        try:
            response = self.stub.FileContents(request, metadata=metadata, timeout=10)
            for resp in response:
                total_bytes += resp.bytes_remaining
                destination_file.write(resp.bytes)
            logging.debug("Successfully wrote {} bytes into {}".format(total_bytes, destination_file.name))
        except grpc.RpcError as e:
            return e
        except AttributeError as e:
            return e

    def upload_to_file(self, group_id, mount_id, file_to_upload, destination_path, chunk_size=MAX_CHUNK_SIZE):
        """
        Upload a file by chunks of up to 1 Mb
        Mount_id allows you to select on which mount you would like to upload your file
        file_to_upload is a filestream of the file to upload, read access is enough.
        destination_path is the path on the mount at which the file will be uploaded
        """
        if chunk_size > MAX_CHUNK_SIZE: # 
            chunk_size = MAX_CHUNK_SIZE
        
        metadata = [
            ('authorization', "bearer: {}".format(self.token)),
            ('active-group', group_id),
            ('mount-id', mount_id),
            ('path', destination_path),
        ]

        try:
            response = self.stub.FileUpload(
                self._retrieve_file_bytes(file_to_upload, chunk_size),
                metadata=metadata,
                timeout=10
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