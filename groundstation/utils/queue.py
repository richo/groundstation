class Queue(list):
    """A queue structure which maintains a list of N recent items, resizable
    dynamically"""

    def __init__(self, size):
        self.size = size

    def append(self, obj):
        if obj not in self:
            super(Queue, self).append(obj)
        self.trim()

    def trim(self):
        while len(self) > self.size:
            self.pop(0)

    @property
    def size(self):
        return self.size

    @size.setter
    def set_size(self, size):
        self.size = size
        self.trim()
