import pytest
from src.queue import Queue


class TestQueueBasicOperations:
    """Test basic queue operations: enqueue, dequeue, peek, is_empty, size"""
    
    def test_create_empty_queue(self):
        """Test that a new queue is empty"""
        queue = Queue()
        assert queue.is_empty() is True
        assert queue.size() == 0
    
    def test_enqueue_single_item(self):
        """Test enqueueing a single item"""
        queue = Queue()
        queue.enqueue("task1")
        assert queue.size() == 1
        assert queue.is_empty() is False
    
    def test_enqueue_multiple_items(self):
        """Test enqueueing multiple items"""
        queue = Queue()
        items = ["task1", "task2", "task3"]
        for item in items:
            queue.enqueue(item)
        assert queue.size() == 3
    
    def test_dequeue_single_item(self):
        """Test dequeueing a single item"""
        queue = Queue()
        queue.enqueue("task1")
        item = queue.dequeue()
        assert item == "task1"
        assert queue.is_empty() is True
    
    def test_dequeue_fifo_order(self):
        """Test that dequeue returns items in FIFO order"""
        queue = Queue()
        items = ["first", "second", "third"]
        for item in items:
            queue.enqueue(item)
        
        for expected_item in items:
            assert queue.dequeue() == expected_item
    
    def test_peek_does_not_remove(self):
        """Test that peek returns item without removing it"""
        queue = Queue()
        queue.enqueue("task1")
        assert queue.peek() == "task1"
        assert queue.size() == 1  # Item should still be there
    
    def test_peek_returns_front_item(self):
        """Test that peek returns the front item"""
        queue = Queue()
        queue.enqueue("first")
        queue.enqueue("second")
        assert queue.peek() == "first"


class TestQueueEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_dequeue_empty_queue_raises_error(self):
        """Test that dequeueing from empty queue raises IndexError"""
        queue = Queue()
        with pytest.raises(IndexError, match="Cannot dequeue from an empty queue"):
            queue.dequeue()
    
    def test_peek_empty_queue_raises_error(self):
        """Test that peeking at empty queue raises IndexError"""
        queue = Queue()
        with pytest.raises(IndexError, match="Cannot peek at an empty queue"):
            queue.peek()
    
    def test_enqueue_dequeue_cycle(self):
        """Test multiple enqueue/dequeue cycles"""
        queue = Queue()
        
        # First cycle
        queue.enqueue("a")
        assert queue.dequeue() == "a"
        assert queue.is_empty() is True
        
        # Second cycle
        queue.enqueue("b")
        queue.enqueue("c")
        assert queue.dequeue() == "b"
        assert queue.dequeue() == "c"
    
    def test_queue_with_different_data_types(self):
        """Test queue with different data types"""
        queue = Queue()
        queue.enqueue(42)
        queue.enqueue("string")
        queue.enqueue([1, 2, 3])
        queue.enqueue({"key": "value"})
        
        assert queue.dequeue() == 42
        assert queue.dequeue() == "string"
        assert queue.dequeue() == [1, 2, 3]
        assert queue.dequeue() == {"key": "value"}
    
    def test_queue_with_none_value(self):
        """Test queue can store None values"""
        queue = Queue()
        queue.enqueue(None)
        assert queue.peek() is None
        assert queue.dequeue() is None


class TestQueueLargeOperations:
    """Test queue with large number of items"""
    
    def test_large_enqueue_dequeue(self):
        """Test queue with 1000 items"""
        queue = Queue()
        n = 1000
        
        # Enqueue 1000 items
        for i in range(n):
            queue.enqueue(i)
        assert queue.size() == n
        
        # Dequeue all items
        for i in range(n):
            assert queue.dequeue() == i
        assert queue.is_empty() is True
    
    def test_size_accuracy(self):
        """Test that size() remains accurate after many operations"""
        queue = Queue()
        
        for i in range(100):
            queue.enqueue(i)
            assert queue.size() == i + 1
        
        for i in range(100):
            queue.dequeue()
            assert queue.size() == 99 - i


class TestQueueStringRepresentation:
    """Test string representations of queue"""
    
    def test_str_representation(self):
        """Test string representation of queue"""
        queue = Queue()
        queue.enqueue("a")
        queue.enqueue("b")
        assert str(queue) == "Queue(['a', 'b'])"
    
    def test_repr_representation(self):
        """Test repr representation of queue"""
        queue = Queue()
        queue.enqueue(1)
        assert repr(queue) == "Queue([1])"