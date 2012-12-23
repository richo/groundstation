import uuid

class Node(object):
    def __init__(self):
        self.name = str(uuid.uuid1())
