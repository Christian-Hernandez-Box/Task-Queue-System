"""
Task Queue System - Demo Application

This module demonstrates how to use the Task Queue System in action.
Shows task creation, queue management, and worker processing.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.queue import Queue
from src.task import Task, TaskPriority
from src.worker import Worker


def main():
    """
    Main demo function showing a complete workflow of the Task Queue System.
    """
    print("\n" + "=" * 60)
    print("TASK QUEUE SYSTEM - DEMO")
    print("=" * 60 + "\n")

    # Create a worker with a new queue
    print("📋 Creating worker with task queue...\n")
    worker = Worker()

    # Add tasks with different priorities
    print("➕ Adding tasks to queue:\n")
    tasks_to_add = [
        ("Download file from server", TaskPriority.HIGH),
        ("Process user data", TaskPriority.MEDIUM),
        ("Send notification email", TaskPriority.LOW),
        ("Backup database", TaskPriority.CRITICAL),
        ("Update cache", TaskPriority.MINIMAL),
    ]

    for task_name, priority in tasks_to_add:
        task = Task(task_name, priority=priority)
        worker.add_task(task)
        print(f"   ✓ Added: {task_name} ({priority.name} priority)")

    print(f"\n📦 Queue now contains {worker.queue_size()} tasks\n")

    # Process all tasks
    print("⚙️  Processing all tasks...\n")
    results = worker.process_all_tasks()

    # Display results
    print("✅ Task Processing Results:\n")
    for i, task in enumerate(results, 1):
        status_symbol = "✓" if task.is_completed() else "✗"
        print(f"   {i}. {status_symbol} {task.name}")
        print(f"      Status: {task.status.value.upper()}")
        print(f"      Priority: {task.priority.name}")
        print()

    # Show statistics
    print("📊 Processing Statistics:\n")
    stats = worker.get_stats()
    print(f"   Total Processed: {stats['total_processed']}")
    print(f"   Completed Tasks: {stats['completed']}")
    print(f"   Failed Tasks: {stats['failed']}")
    print(f"   Success Rate: {stats['success_rate'] * 100:.1f}%")
    print(f"   Remaining in Queue: {stats['pending_in_queue']}")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60 + "\n")


def demo_with_callback():
    """
    Demo showing how to process tasks with custom callback logic.
    This example shows conditional task processing.
    """
    print("\n" + "=" * 60)
    print("TASK QUEUE SYSTEM - CALLBACK DEMO")
    print("=" * 60 + "\n")

    worker = Worker()

    # Add some tasks
    print("➕ Adding tasks...\n")
    for i in range(5):
        task = Task(f"Task {i}")
        worker.add_task(task)
        print(f"   ✓ Added Task {i}")

    print(f"\n📦 Queue contains {worker.queue_size()} tasks\n")

    # Custom processing logic: fail tasks with even numbers
    def custom_processor(task):
        """
        Custom task processor that:
        - Completes odd-numbered tasks (1, 3, 5...)
        - Fails even-numbered tasks (0, 2, 4...)
        """
        task_num = int(task.name.split()[-1])
        return task_num % 2 != 0  # True for odd numbers

    print("⚙️  Processing tasks with custom logic...\n")
    print("   Logic: Odd-numbered tasks succeed, even-numbered tasks fail\n")

    results = worker.process_all_tasks_with_callback(custom_processor)

    # Display results
    print("✅ Results:\n")
    for task in results:
        status_symbol = "✓" if task.is_completed() else "✗"
        print(f"   {status_symbol} {task.name} - {task.status.value.upper()}")

    # Show statistics
    print("\n📊 Statistics:\n")
    stats = worker.get_stats()
    print(f"   Completed: {stats['completed']}")
    print(f"   Failed: {stats['failed']}")
    print(f"   Success Rate: {stats['success_rate'] * 100:.1f}%")

    print("\n" + "=" * 60)
    print("CALLBACK DEMO COMPLETE")
    print("=" * 60 + "\n")


def demo_single_task_processing():
    """
    Demo showing step-by-step single task processing.
    """
    print("\n" + "=" * 60)
    print("TASK QUEUE SYSTEM - STEP-BY-STEP DEMO")
    print("=" * 60 + "\n")

    worker = Worker()

    # Create and add a single task
    print("➕ Creating a single task...\n")
    task = Task("Important operation", priority=TaskPriority.CRITICAL)
    worker.add_task(task)
    print(f"   Task: {task.name}")
    print(f"   Priority: {task.priority.name}")
    print(f"   Initial Status: {task.status.value}")

    print(f"\n📦 Queue Size: {worker.queue_size()}")

    # Process the task
    print("\n⚙️  Processing task...\n")
    processed_task = worker.process_next_task()

    print(f"   Final Status: {processed_task.status.value.upper()}")
    print(f"   Completed: {processed_task.is_completed()}")

    print(f"\n📦 Queue Size After: {worker.queue_size()}")

    print("\n" + "=" * 60)
    print("STEP-BY-STEP DEMO COMPLETE")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    # Run all demos
    main()
    demo_with_callback()
    demo_single_task_processing()

    print("\n💡 Tip: Run individual demos by importing and calling:")
    print(
        "   from src.main import main, demo_with_callback, demo_single_task_processing"
    )
    print("   main()")
    print()
