class Queue:
    """A FIFO (First-In-First-Out) Queue implementation using a Python list."""
    
    def __init__(self):
        """Initialize an empty queue."""
        self.items = []

    def enqueue(self, item):
        """Add an item to the rear of the queue."""
        self.items.append(item)

    def dequeue(self):
        """Remove and return the item at the front of the queue."""
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue")
        return self.items.pop(0)
    
    def peek(self):
        """Return the item at the front of the queue without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek at an empty queue")
        return self.items[0]
    
    def is_empty(self):
        """Check if the queue is empty."""
        return len(self.items) == 0
    
    def size(self):
        """Return the number of items in the queue."""
        return len(self.items)
    
    def __str__(self):
        """String representation of the queue."""
        return f"Queue({self.items})"
    
    def __repr__(self):
        """Developer-friendly representation of the queue."""
        return self.__str__()