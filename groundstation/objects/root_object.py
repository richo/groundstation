import root_object_pb2

class RootObject(object):
    data_members = ["id", "channel", "protocol"]
    def __init__(self, id, channel, protocol):
        super(RootObject, self).__init__()
        self.id = id
        self.channel = channel
        self.protocol = protocol

    @staticmethod
    def from_object(obj):
        """Convert an object straight from Git into a RootObject"""
        protobuf = root_object_pb2.RootObject()
        protobuf.ParseFromString(obj)
        return RootObject(protobuf.id, protobuf.channel, protobuf.protocol)

    def as_object(self):
        """Convert a RootObject into data suitable to write into the database
        as a Git object"""
        protobuf = root_object_pb2.RootObject()
        for member in self.data_members:
            setattr(protobuf, member, getattr(self, member))
        return protobuf.SerializeToString()
