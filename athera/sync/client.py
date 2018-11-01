import os
import logging
import grpc
from athera.sync.sirius.services import service_pb2
from athera.sync.sirius.services import service_pb2_grpc

ONE_MB = 1048576
 
class Client(object):
    """
    Client to query the remote grpc file sync service, Sirius.
    """
    CHUNK_SIZE = 2*ONE_MB

    def __init__(self, url, chunk_size=CHUNK_SIZE):
        
        self.url = url
        self.chunk_size = chunk_size
        self.channel = grpc.insecure_channel(self.url)
        self.stub = service_pb2_grpc.SiriusStub(self.channel)

    def get_mounts(self, token, group_id):
        """
        Using the provided credentials, which identify a user, provide the mounts for the supplied group.
        """

        request = service_pb2.MountsRequest()
        
        metadata = [(b'auth-jwt', token),
                    (b'group-id', group_id)]

        try:
            mounts = self.stub.Mounts(request, metadata=metadata)
            return (mounts, None)
        except grpc.RpcError as e:
            logging.debug("grpc.RpcError %s", e)
            return (None, e.message)

    # def get_files(self, token, group_id, mount_id, path="/"):
    #     """
    #     Using the provided credentials, group and mount, provide a list of files at the (optional) supplied path.
    #     """
    #     request = sirius.services.service_pb2.FilesRequest(mount_id=mount_id, path=path)
    #     metadata = [(b'auth-jwt', token),
    #                 (b'group-id', group_id)]

    #     try:
    #         files = self.stub.FileList(request, metadata=metadata)
    #         return (files, None)
    #     except grpc.RpcError as e:
    #         logging.debug("grpc.RpcError %s", e)
    #         return (None, e.message)


    # def get_file_contents(self, token, group_id, mount_id, path):
    #     """
    #     Data access for a single file defined in path, relative to the remote mount root
    #     """
    #     request = sirius.services.service_pb2.FileContentsRequest(mount_id=mount_id, path=path, chunk_size=self.chunk_size)
    #     metadata = [(b'auth-jwt', token),
    #                 (b'group-id', group_id)]

    #     try:
    #         fileContents = self.stub.FileContentsStream(request, metadata=metadata)
    #         return (fileContents, None)
    #     except grpc.RpcError as e:
    #         logging.debug("grpc.RpcError %s", e)
    #         return (None, e.message)