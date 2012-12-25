import uuid

class Node(object):
    def __init__(self):
        self.uuid = uuid.uuid1()
        self.name = str(self.uuid)
