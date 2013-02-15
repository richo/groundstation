from groundstation.objects.root_object import RootObject
from groundstation.objects.update_object import UpdateObject

def hydrate_object(protobuf):
    obj = RootObject.from_object(protobuf)
    if not obj.protocol:
        obj = UpdateObject.from_object(protobuf)
    return obj
