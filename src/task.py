from enum import Enum
from datetime import datetime
from uuid import uuid4


class TaskStatus(Enum):
    """Enumeration of possible task statuses."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskPriority(Enum):
    """Enumeration of task priority levels (1 = highest, 5 = lowest)."""

    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    MINIMAL = 5


class Task:
    """
    Represents a task that can be queued and processed.

    Attributes:
        id (str): Unique identifier for the task
        name (str): Name/description of the task
        status (TaskStatus): Current status of the task
        priority (TaskPriority): Priority level of the task
        timestamp (datetime): When the task was created

    Time Complexity: O(1) for all operations
    Space Complexity: O(1)
    """

    def __init__(self, name, priority=TaskPriority.MEDIUM):
        """
        Initialize a new Task.

        Args:
            name (str): Name/description of the task
            priority (TaskPriority): Priority level (default: MEDIUM)

        Raises:
            ValueError: If name is empty or priority is invalid
        """
        if not name or not isinstance(name, str) or name.strip() == "":
            raise ValueError("Task name must be a non-empty string")

        if not isinstance(priority, TaskPriority):
            raise ValueError("Priority must be a TaskPriority enum value")

        self.id = str(uuid4())
        self.name = name
        self.status = TaskStatus.PENDING
        self.priority = priority
        self.timestamp = datetime.now()

    def start_processing(self):
        """
        Transition task status from PENDING to PROCESSING.

        Raises:
            ValueError: If task is not in PENDING status

        Time Complexity: O(1)
        """
        if self.status != TaskStatus.PENDING:
            raise ValueError(
                f"Cannot start processing a task with status: {self.status.value}"
            )
        self.status = TaskStatus.PROCESSING

    def complete(self):
        """
        Transition task status from PROCESSING to COMPLETED.

        Raises:
            ValueError: If task is not in PROCESSING status

        Time Complexity: O(1)
        """
        if self.status != TaskStatus.PROCESSING:
            raise ValueError(f"Cannot complete a task with status: {self.status.value}")
        self.status = TaskStatus.COMPLETED

    def fail(self, reason="Unknown error"):
        """
        Transition task to FAILED status with optional reason.

        Args:
            reason (str): Reason why the task failed

        Raises:
            ValueError: If task is already COMPLETED

        Time Complexity: O(1)
        """
        if self.status == TaskStatus.COMPLETED:
            raise ValueError("Cannot fail a task that is already completed")

        self.status = TaskStatus.FAILED
        self.failure_reason = reason

    def is_pending(self):
        """Check if task is in PENDING status."""
        return self.status == TaskStatus.PENDING

    def is_processing(self):
        """Check if task is in PROCESSING status."""
        return self.status == TaskStatus.PROCESSING

    def is_completed(self):
        """Check if task is in COMPLETED status."""
        return self.status == TaskStatus.COMPLETED

    def is_failed(self):
        """Check if task is in FAILED status."""
        return self.status == TaskStatus.FAILED

    def __str__(self):
        """String representation of the task."""
        return f"Task(id={self.id[:8]}..., name={self.name}, status={self.status.value}, priority={self.priority.name})"

    def __repr__(self):
        """Developer-friendly representation of the task."""
        return self.__str__()

    def __lt__(self, other):
        """
        Compare tasks by priority (for sorting).
        Lower priority value = higher importance.
        """
        if not isinstance(other, Task):
            return NotImplemented
        return self.priority.value < other.priority.value

    def __eq__(self, other):
        """Check equality based on task id."""
        if not isinstance(other, Task):
            return NotImplemented
        return self.id == other.id
