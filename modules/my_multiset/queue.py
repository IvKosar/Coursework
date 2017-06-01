# Data structure Queue

class Queue():
    """
    Representation of queue data structure
    """

    def __init__(self):
        self._items = list()
        self._size = 0

    def size(self):
        """
        :return: size of queue
        """
        return self._size

    def isEmpty(self):
        """
        Check whether Queue has elements

        :return: bool
        """
        return self._items == list()

    def enqueue(self, item):
        """
        Add item to the tail of Queue

        :param item: element to add
        :return: None
        """
        self._items.append(item)
        self._size += 1

    def dequeue(self):
        """
        Remove first element from Queue
        :return: item
        """
        if self.isEmpty(): return None

        self._size -= 1
        return self._items.pop(0)

    def peek(self):
        """
        Get first element of Queue

        :return:
        """
        if self.isEmpty(): return None
        return self._items[0]

    def __str__(self):
        return str(self._items)