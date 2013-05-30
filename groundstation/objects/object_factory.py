from groundstation.objects.base_object_pb2 import BaseObject, \
    ROOT as TYPE_ROOT, \
    UPDATE as TYPE_UPDATE, \
    UNSET as TYPE_UNSET
from groundstation.objects.root_object import RootObject
from groundstation.objects.update_object import UpdateObject


def type_of(protobuf):
    base = BaseObject()
    base.ParseFromString(protobuf)
    return base.type


def hydrate_object(protobuf):
    # Test if it's strongly typed first
    _type = type_of(protobuf)
    if _type == TYPE_ROOT:
        return RootObject.from_object(protobuf)
    elif _type == TYPE_UPDATE:
        return UpdateObject.from_object(protobuf)
    elif _type == TYPE_UNSET:
        # Use existing heuristic
        obj = RootObject.from_object(protobuf)
        if not obj.protocol:
            obj = UpdateObject.from_object(protobuf)
        return obj
    else:
        raise Exception("Unknown type; %s" % (str(_type)))
