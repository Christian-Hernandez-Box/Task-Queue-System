import pytest
from src.queue import Queue
from src.task import Task, TaskStatus, TaskPriority
from src.worker import Worker


class TestWorkerInitialization:
    """Test worker creation and initialization"""

    def test_create_worker_with_new_queue(self):
        """Test creating a worker with a new queue"""
        worker = Worker()
        assert worker.queue is not None
        assert worker.has_tasks() is False
        assert worker.queue_size() == 0
        assert len(worker.processed_tasks) == 0

    def test_create_worker_with_existing_queue(self):
        """Test creating a worker with an existing queue"""
        queue = Queue()
        task = Task("Existing task")
        queue.enqueue(task)

        worker = Worker(queue)
        assert worker.queue is queue
        assert worker.has_tasks() is True
        assert worker.queue_size() == 1

    def test_worker_current_task_starts_none(self):
        """Test that current_task is None initially"""
        worker = Worker()
        assert worker.current_task is None


class TestWorkerTaskAddition:
    """Test adding tasks to worker"""

    def test_add_single_task(self):
        """Test adding a single task"""
        worker = Worker()
        task = Task("Test task")
        worker.add_task(task)

        assert worker.has_tasks() is True
        assert worker.queue_size() == 1

    def test_add_multiple_tasks(self):
        """Test adding multiple tasks"""
        worker = Worker()
        tasks = [Task(f"Task {i}") for i in range(5)]

        for task in tasks:
            worker.add_task(task)

        assert worker.queue_size() == 5

    def test_add_non_task_raises_error(self):
        """Test that adding non-Task object raises ValueError"""
        worker = Worker()
        with pytest.raises(ValueError, match="Task instances"):
            worker.add_task("not a task")

    def test_add_none_raises_error(self):
        """Test that adding None raises ValueError"""
        worker = Worker()
        with pytest.raises(ValueError, match="Task instances"):
            worker.add_task(None)


class TestWorkerProcessing:
    """Test basic task processing"""

    def test_process_single_task(self):
        """Test processing a single task"""
        worker = Worker()
        task = Task("Task to process")
        worker.add_task(task)

        processed_task = worker.process_next_task()

        assert processed_task is task
        assert processed_task.is_completed() is True
        assert worker.has_tasks() is False
        assert len(worker.processed_tasks) == 1

    def test_process_multiple_tasks_fifo(self):
        """Test processing multiple tasks in FIFO order"""
        worker = Worker()
        tasks = [Task(f"Task {i}") for i in range(3)]

        for task in tasks:
            worker.add_task(task)

        for i, expected_task in enumerate(tasks):
            processed_task = worker.process_next_task()
            assert processed_task is expected_task
            assert processed_task.is_completed()

    def test_process_next_task_updates_status(self):
        """Test that processing updates task status correctly"""
        worker = Worker()
        task = Task("Status check")
        worker.add_task(task)

        assert task.is_pending() is True

        worker.process_next_task()

        assert task.is_pending() is False
        assert task.is_completed() is True

    def test_process_next_task_from_empty_queue_raises_error(self):
        """Test that processing from empty queue raises IndexError"""
        worker = Worker()
        with pytest.raises(IndexError, match="empty queue"):
            worker.process_next_task()

    def test_current_task_is_updated(self):
        """Test that current_task is updated when processing"""
        worker = Worker()
        task = Task("Current task")
        worker.add_task(task)

        assert worker.current_task is None
        worker.process_next_task()
        assert worker.current_task is task


class TestWorkerProcessingWithCallback:
    """Test task processing with custom callbacks"""

    def test_process_with_success_callback(self):
        """Test processing with callback that returns True"""
        worker = Worker()
        task = Task("Callback task")
        worker.add_task(task)

        def success_callback(t):
            return True

        processed_task = worker.process_task_with_callback(success_callback)
        assert processed_task.is_completed() is True

    def test_process_with_failure_callback(self):
        """Test processing with callback that returns False"""
        worker = Worker()
        task = Task("Failing task")
        worker.add_task(task)

        def failure_callback(t):
            return False

        processed_task = worker.process_task_with_callback(failure_callback)
        assert processed_task.is_failed() is True
        assert "returned False" in processed_task.failure_reason

    def test_process_with_exception_callback(self):
        """Test processing with callback that raises exception"""
        worker = Worker()
        task = Task("Exception task")
        worker.add_task(task)

        def exception_callback(t):
            raise RuntimeError("Custom error")

        processed_task = worker.process_task_with_callback(exception_callback)
        assert processed_task.is_failed() is True
        assert "Custom error" in processed_task.failure_reason

    def test_process_with_non_callable_raises_error(self):
        """Test that non-callable callback raises ValueError"""
        worker = Worker()
        task = Task("Task")
        worker.add_task(task)

        with pytest.raises(ValueError, match="callable"):
            worker.process_task_with_callback("not callable")

    def test_callback_receives_task(self):
        """Test that callback receives the task as argument"""
        worker = Worker()
        task = Task("Callback receiver")
        worker.add_task(task)

        received_task = None

        def capture_callback(t):
            nonlocal received_task
            received_task = t
            return True

        worker.process_task_with_callback(capture_callback)
        assert received_task is task


class TestWorkerBatchProcessing:
    """Test processing all tasks at once"""

    def test_process_all_tasks(self):
        """Test processing all tasks in queue"""
        worker = Worker()
        tasks = [Task(f"Task {i}") for i in range(5)]

        for task in tasks:
            worker.add_task(task)

        results = worker.process_all_tasks()

        assert len(results) == 5
        assert worker.has_tasks() is False
        assert len(worker.processed_tasks) == 5

        for result in results:
            assert result.is_completed()

    def test_process_all_tasks_empty_queue(self):
        """Test processing all tasks from empty queue"""
        worker = Worker()
        results = worker.process_all_tasks()
        assert results == []

    def test_process_all_with_callback(self):
        """Test batch processing with callback"""
        worker = Worker()
        tasks = [Task(f"Task {i}") for i in range(3)]

        for task in tasks:
            worker.add_task(task)

        def custom_callback(t):
            return t.name != "Task 1"  # Fail task 1

        results = worker.process_all_tasks_with_callback(custom_callback)

        assert len(results) == 3
        assert results[0].is_completed()  # Task 0
        assert results[1].is_failed()  # Task 1
        assert results[2].is_completed()  # Task 2


class TestWorkerQuerying:
    """Test querying worker state"""

    def test_has_tasks_empty(self):
        """Test has_tasks on empty queue"""
        worker = Worker()
        assert worker.has_tasks() is False

    def test_has_tasks_with_items(self):
        """Test has_tasks with items in queue"""
        worker = Worker()
        worker.add_task(Task("Task"))
        assert worker.has_tasks() is True

    def test_queue_size(self):
        """Test queue_size method"""
        worker = Worker()
        assert worker.queue_size() == 0

        for i in range(3):
            worker.add_task(Task(f"Task {i}"))
        assert worker.queue_size() == 3

    def test_get_completed_tasks(self):
        """Test getting completed tasks"""
        worker = Worker()
        worker.add_task(Task("Task 1"))
        worker.add_task(Task("Task 2"))

        worker.process_all_tasks()

        completed = worker.get_completed_tasks()
        assert len(completed) == 2

    def test_get_failed_tasks(self):
        """Test getting failed tasks"""
        worker = Worker()
        worker.add_task(Task("Task 1"))
        worker.add_task(Task("Task 2"))

        def fail_all(t):
            return False

        worker.process_all_tasks_with_callback(fail_all)

        failed = worker.get_failed_tasks()
        assert len(failed) == 2

    def test_get_processed_tasks(self):
        """Test getting all processed tasks"""
        worker = Worker()
        tasks = [Task(f"Task {i}") for i in range(3)]
        for task in tasks:
            worker.add_task(task)

        worker.process_all_tasks()

        processed = worker.get_processed_tasks()
        assert len(processed) == 3


class TestWorkerStatistics:
    """Test worker statistics"""

    def test_get_stats_empty(self):
        """Test stats with no processed tasks"""
        worker = Worker()
        stats = worker.get_stats()

        assert stats["total_processed"] == 0
        assert stats["completed"] == 0
        assert stats["failed"] == 0
        assert stats["pending_in_queue"] == 0
        assert stats["success_rate"] == 0

    def test_get_stats_all_completed(self):
        """Test stats with all tasks completed"""
        worker = Worker()
        for i in range(5):
            worker.add_task(Task(f"Task {i}"))

        worker.process_all_tasks()
        stats = worker.get_stats()

        assert stats["total_processed"] == 5
        assert stats["completed"] == 5
        assert stats["failed"] == 0
        assert stats["success_rate"] == 1.0

    def test_get_stats_mixed_success_failure(self):
        """Test stats with mixed success and failure"""
        worker = Worker()
        for i in range(5):
            worker.add_task(Task(f"Task {i}"))

        def every_other_fails(t):
            return int(t.name.split()[-1]) % 2 == 0

        worker.process_all_tasks_with_callback(every_other_fails)
        stats = worker.get_stats()

        assert stats["total_processed"] == 5
        assert stats["completed"] == 3
        assert stats["failed"] == 2
        assert stats["success_rate"] == 0.6


class TestWorkerStringRepresentation:
    """Test worker string representations"""

    def test_str_representation(self):
        """Test string representation of worker"""
        worker = Worker()
        worker.add_task(Task("Task 1"))
        worker.add_task(Task("Task 2"))

        worker_str = str(worker)
        assert "Worker" in worker_str
        assert "queue_size=2" in worker_str

    def test_repr_representation(self):
        """Test repr representation of worker"""
        worker = Worker()
        worker.add_task(Task("Task"))

        worker_repr = repr(worker)
        assert "Worker" in worker_repr


class TestWorkerIntegration:
    """Test complete workflows with worker"""

    def test_full_workflow_with_mixed_tasks(self):
        """Test complete workflow with various tasks"""
        worker = Worker()

        # Add tasks with different priorities
        worker.add_task(Task("Critical", priority=TaskPriority.CRITICAL))
        worker.add_task(Task("Normal", priority=TaskPriority.MEDIUM))
        worker.add_task(Task("Low", priority=TaskPriority.LOW))

        assert worker.queue_size() == 3

        # Process all
        results = worker.process_all_tasks()

        assert len(results) == 3
        assert all(task.is_completed() for task in results)
        assert worker.has_tasks() is False

        stats = worker.get_stats()
        assert stats["success_rate"] == 1.0

    def test_workflow_with_custom_processing(self):
        """Test workflow with custom task processing logic"""
        worker = Worker()

        # Add tasks
        for i in range(5):
            worker.add_task(Task(f"Task {i}"))

        # Custom logic: fail tasks with even numbers
        def process_task(task):
            task_num = int(task.name.split()[-1])
            return task_num % 2 != 0  # True for odd, False for even

        results = worker.process_all_tasks_with_callback(process_task)

        stats = worker.get_stats()
        assert stats["completed"] == 2  # Tasks 1, 3
        assert stats["failed"] == 3  # Tasks 0, 2, 4
