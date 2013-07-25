from groundstation.objects.root_object import RootObject
from groundstation.objects.update_object import UpdateObject


def update_object(data, parents=[]):
    return UpdateObject(parents, data)


def root_object(id, channel, protocol):
    return RootObject(id, channel, protocol)
