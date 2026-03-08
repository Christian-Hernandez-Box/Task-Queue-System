from src.queue import Queue
from src.task import Task, TaskStatus

class Worker:
    """
    A worker that processes tasks from a queue sequentially in FIFO order.
    
    The worker manages the lifecycle of tasks:
    - Takes tasks from the queue
    - Updates task status as processing progresses
    - Handles successful completion or failures
    
    Attributes:
        queue (Queue): The queue of tasks to process
        processed_tasks (list): List of completed/failed tasks
        current_task (Task): Currently processing task
    
    Time Complexity:
    - process_next_task(): O(n) where n is queue size (due to dequeue)
    - process_all_tasks(): O(n*m) where n is number of tasks, m is avg processing time
    
    Space Complexity: O(n) for storing processed tasks
    """

    def __init__(self, queue=None):
        """
        Initialize a worker with an optional queue.
        
        Args:
            queue (Queue, optional): Queue of tasks to process. Creates new if not provided.
        """
        self.queue = queue if queue is not None else Queue()
        self.processed_tasks = []
        self.current_task = None

    def add_task(self, task):
        """
        Add a task to the worker's queue.
        
        Args:
            task (Task): Task to add to queue
            
        Raises:
            ValueError: If task is not a Task instance
            
        Time Complexity: O(1)
        """
        if not isinstance(task, Task):
            raise ValueError("Can only add Task instances to the queue")
        self.queue.enqueue(task)

    def has_tasks(self):
        """
        Check if there are tasks in the queue.
        
        Returns:
            bool: True if queue has tasks, False otherwise
            
        Time Complexity: O(1)
        """
        return not self.queue.is_empty()
    
    def queue_size(self):
        """
        Get the number of tasks remaining in queue.
        
        Returns:
            int: Number of tasks in queue
            
        Time Complexity: O(1)
        """
        return self.queue.size()
    
    def process_next_task(self):
        """
        Dequeue and process the next task from the queue.
        
        Task lifecycle:
        1. PENDING → PROCESSING (start processing)
        2. PROCESSING → COMPLETED (upon successful completion)
        
        Returns:
            Task: The task that was processed
            
        Raises:
            IndexError: If queue is empty
            
        Time Complexity: O(n) where n is queue size (due to dequeue pop(0))
        """
        if not self.has_tasks():
            raise IndexError("Cannot process task from empty queue")
        
        task = self.queue.dequeue()
        self.current_task = task

        # Update task status
        task.start_processing()
        task.complete()

        # Track processed task
        self.processed_tasks.append(task)

        return task
    
    def process_task_with_callback(self, callback):
        """
        Process next task with a custom callback function.
        
        The callback receives the task and should return True for success,
        False for failure. Callback can raise exceptions on error.
        
        Args:
            callback (callable): Function that processes a task.
                               Should accept Task as argument.
                               Should return True on success, False on failure.
        
        Returns:
            Task: The processed task
            
        Raises:
            IndexError: If queue is empty
            ValueError: If callback is not callable
            
        Time Complexity: O(n) where n is queue size
        """
        if not callable(callback):
            raise ValueError("Callback must be callable")
        
        if not self.has_tasks():
            raise IndexError("Cannot process task from empty queue")
        
        task = self.queue.dequeue()
        self.current_task = task

        try:
            task.start_processing()

            # Execute custom processing logic
            success = callback(task)

            if success:
                task.complete()
            else:
                task.fail("Task callback returned False")

        except Exception as e:
            task.fail(f"Exception during processing: {str(e)}")

        self.processed_tasks.append(task)
        return task
    
    def process_all_tasks(self):
        """
        Process all remaining tasks in the queue.
        
        Processes tasks sequentially until queue is empty.
        
        Returns:
            list: All processed tasks
            
        Time Complexity: O(n*m) where n is number of tasks, m is avg processing time
        """
        results = []

        while self.has_tasks():
            task = self.process_next_task()
            results.append(task)

        return results
    
    def process_all_tasks_with_callback(self, callback):
        """
        Process all remaining tasks with a custom callback.
        
        Args:
            callback (callable): Function that processes each task
        
        Returns:
            list: All processed tasks
            
        Time Complexity: O(n*m) where n is number of tasks, m is avg processing time
        """
        results = []

        while self.has_tasks():
            task = self.process_task_with_callback(callback)
            results.append(task)

        return results
    
    def get_completed_tasks(self):
        """
        Get all tasks that have been completed.
        
        Returns:
            list: Tasks with COMPLETED status
            
        Time Complexity: O(n) where n is processed_tasks length
        """
        return [task for task in self.processed_tasks if task.is_completed()]
    
    def get_failed_tasks(self):
        """
        Get all tasks that have failed.
        
        Returns:
            list: Tasks with FAILED status
            
        Time Complexity: O(n) where n is processed_tasks length
        """
        return [task for task in self.processed_tasks if task.is_failed()]
    
    def get_processed_tasks(self):
        """
        Get all processed tasks.
        
        Returns:
            list: All processed tasks
            
        Time Complexity: O(1)
        """
        return self.processed_tasks.copy()
    
    def get_stats(self):
        """
        Get statistics about processed tasks.
        
        Returns:
            dict: Statistics including completed, failed, and total counts
            
        Time Complexity: O(n) where n is processed_tasks length
        """
        completed = len(self.get_completed_tasks())
        failed = len(self.get_failed_tasks())
        total = len(self.processed_tasks)

        return {
            "total_processed": total,
            "completed": completed,
            "failed": failed,
            "pending_in_queue": self.queue_size(),
            "success_rate": completed / total if total > 0 else 0
        }
    
    def __str__(self):
        """String representation of worker."""
        return f"Worker(queue_size={self.queue_size()}, processed={len(self.processed_tasks)})"
    
    def __repr__(self):
        """Developer-friendly representation of worker."""
        return self.__str__()