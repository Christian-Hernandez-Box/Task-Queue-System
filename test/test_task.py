import pytest
from datetime import datetime
from src.task import Task, TaskStatus, TaskPriority


class TestTaskCreation:
    """Test task creation and initialization"""

    def test_create_task_with_default_priority(self):
        """Test creating a task with default priority"""
        task = Task("Download file")
        assert task.name == "Download file"
        assert task.status == TaskStatus.PENDING
        assert task.priority == TaskPriority.MEDIUM
        assert task.id is not None
        assert isinstance(task.timestamp, datetime)

    def test_create_task_with_custom_priority(self):
        """Test creating a task with custom priority"""
        task = Task("Fix bug", priority=TaskPriority.HIGH)
        assert task.name == "Fix bug"
        assert task.priority == TaskPriority.HIGH

    def test_create_task_with_critical_priority(self):
        """Test creating a critical priority task"""
        task = Task("Server down", priority=TaskPriority.CRITICAL)
        assert task.priority == TaskPriority.CRITICAL

    def test_task_id_is_unique(self):
        """Test that each task gets a unique ID"""
        task1 = Task("Task 1")
        task2 = Task("Task 2")
        assert task1.id != task2.id

    def test_task_timestamp_is_created(self):
        """Test that task timestamp is set on creation"""
        before = datetime.now()
        task = Task("Test task")
        after = datetime.now()
        assert before <= task.timestamp <= after

    def test_create_task_with_empty_name_raises_error(self):
        """Test that empty name raises ValueError"""
        with pytest.raises(ValueError, match="non-empty string"):
            Task("")

    def test_create_task_with_whitespace_name_raises_error(self):
        """Test that whitespace-only name raises ValueError"""
        with pytest.raises(ValueError, match="non-empty string"):
            Task("   ")

    def test_create_task_with_non_string_name_raises_error(self):
        """Test that non-string name raises ValueError"""
        with pytest.raises(ValueError, match="non-empty string"):
            Task(123)

    def test_create_task_with_invalid_priority_raises_error(self):
        """Test that invalid priority raises ValueError"""
        with pytest.raises(ValueError, match="TaskPriority enum"):
            Task("Valid task", priority="high")


class TestTaskStatusTransitions:
    """Test task status transitions"""

    def test_task_starts_as_pending(self):
        """Test that new task starts as PENDING"""
        task = Task("New task")
        assert task.is_pending()

    def test_start_processing_transition(self):
        """Test transition from PENDING to PROCESSING"""
        task = Task("Task to process")
        task.start_processing()
        assert task.status == TaskStatus.PROCESSING
        assert task.is_processing() is True

    def test_complete_task_transition(self):
        """Test transition from PROCESSING to COMPLETED"""
        task = Task("Task to complete")
        task.start_processing()
        task.complete()
        assert task.status == TaskStatus.COMPLETED
        assert task.is_completed() is True

    def test_fail_task_from_processing(self):
        """Test failing a task from PROCESSING status"""
        task = Task("Task to fail")
        task.start_processing()
        task.fail("Connection timeout")
        assert task.status == TaskStatus.FAILED
        assert task.is_failed() is True

    def test_fail_task_from_pending(self):
        """Test failing a task from PENDING status"""
        task = Task("Pending task")
        task.fail("Invalid input")
        assert task.status == TaskStatus.FAILED

    def test_cannot_start_processing_twice(self):
        """Test that cannot start processing an already processing task"""
        task = Task("Task")
        task.start_processing()
        with pytest.raises(ValueError, match="Cannot start processing"):
            task.start_processing()

    def test_cannot_complete_pending_task(self):
        """Test that cannot complete a PENDING task"""
        task = Task("Task")
        with pytest.raises(ValueError, match="Cannot complete"):
            task.complete()

    def test_cannot_complete_failed_task(self):
        """Test that cannot complete a FAILED task"""
        task = Task("Task")
        task.fail()
        with pytest.raises(ValueError, match="Cannot complete"):
            task.complete()

    def test_cannot_fail_completed_task(self):
        """Test that cannot fail a COMPLETED task"""
        task = Task("Task")
        task.start_processing()
        task.complete()
        with pytest.raises(
            ValueError, match="Cannot fail a task that is already completed"
        ):
            task.fail()


class TestTaskStatusChecks:
    """Test task status checking methods"""

    def test_is_pending_method(self):
        """Test is_pending() method"""
        task = Task("Task")
        assert task.is_pending() is True
        task.start_processing()
        assert task.is_pending() is False

    def test_is_processing_method(self):
        """Test is_processing() method"""
        task = Task("Task")
        assert task.is_processing() is False
        task.start_processing()
        assert task.is_processing() is True

    def test_is_completed_method(self):
        """Test is_completed() method"""
        task = Task("Task")
        assert task.is_completed() is False
        task.start_processing()
        task.complete()
        assert task.is_completed() is True

    def test_is_failed_method(self):
        """Test is_failed() method"""
        task = Task("Task")
        assert task.is_failed() is False
        task.fail()
        assert task.is_failed() is True


class TestTaskPriorities:
    """Test task priority levels"""

    def test_all_priority_levels(self):
        """Test all priority levels can be assigned"""
        priorities = [
            TaskPriority.CRITICAL,
            TaskPriority.HIGH,
            TaskPriority.MEDIUM,
            TaskPriority.LOW,
            TaskPriority.MINIMAL,
        ]

        for priority in priorities:
            task = Task("Task", priority=priority)
            assert task.priority == priority

    def test_priority_comparison(self):
        """Test that tasks can be compared by priority"""
        critical_task = Task("Critical", priority=TaskPriority.CRITICAL)
        low_task = Task("Low", priority=TaskPriority.LOW)

        assert critical_task < low_task  # Critical has lower value (higher importance)


class TestTaskEquality:
    """Test task equality and comparison"""

    def test_tasks_equal_if_same_id(self):
        """Test that tasks are equal if they have the same ID"""
        task1 = Task("Task A")
        task2 = task1  # Same object
        assert task1 == task2

    def test_tasks_not_equal_if_different_id(self):
        """Test that tasks are not equal if they have different IDs"""
        task1 = Task("Task A")
        task2 = Task("Task A")  # Same name but different ID
        assert task1 != task2

    def test_task_equality_with_non_task_object(self):
        """Test comparing task with non-task object"""
        task = Task("Task")
        assert task != "not a task"
        assert task != 123


class TestTaskStringRepresentation:
    """Test task string representations"""

    def test_str_representation(self):
        """Test string representation of task"""
        task = Task("Download file", priority=TaskPriority.HIGH)
        task_str = str(task)
        assert "Download file" in task_str
        assert "pending" in task_str
        assert "HIGH" in task_str

    def test_repr_representation(self):
        """Test repr representation of task"""
        task = Task("Process data")
        task_repr = repr(task)
        assert "Task" in task_repr
        assert "Process data" in task_repr


class TestTaskFailureReason:
    """Test task failure reason tracking"""

    def test_fail_with_reason(self):
        """Test failing task with a reason"""
        task = Task("Task")
        task.fail("Network timeout")
        assert task.failure_reason == "Network timeout"

    def test_fail_with_default_reason(self):
        """Test failing task without providing a reason"""
        task = Task("Task")
        task.fail()
        assert task.failure_reason == "Unknown error"


class TestTaskLifecycle:
    """Test complete task lifecycle"""

    def test_successful_task_lifecycle(self):
        """Test a task going through successful lifecycle"""
        task = Task("Download and process", priority=TaskPriority.HIGH)
        assert task.is_pending()

        task.start_processing()
        assert task.is_processing()

        task.complete()
        assert task.is_completed()

    def test_failed_task_lifecycle(self):
        """Test a task going through failure lifecycle"""
        task = Task("Risky operation", priority=TaskPriority.CRITICAL)
        assert task.is_pending()

        task.start_processing()
        assert task.is_processing()

        task.fail("Connection lost")
        assert task.is_failed()

    def test_pending_to_failed_lifecycle(self):
        """Test task failing directly from PENDING status"""
        task = Task("Invalid task")
        assert task.is_pending()

        task.fail("Invalid parameters")
        assert task.is_failed()
