# Task Queue System

A foundational implementation of a queue-based task processing system, demonstrating core data structures and software engineering practices.

## Project Overview

This project implements a **Task Queue System** similar to print queues or background job processors. It serves as a hands-on learning experience for understanding queues, task management, and building testable software.

### Learning Objectives

- ✅ Implement a **Queue data structure** from scratch
- ✅ Understand FIFO (First-In-First-Out) principles
- ✅ Practice **unit testing** with pytest
- ✅ Document **time/space complexity** analysis
- ✅ Build a functional queue-based system
- ✅ Reflect on learnings through a learning journal

## Project Structure

```
Task-Queue-System/
├── src/
│   ├── __init__.py
│   ├── queue.py           # Queue implementation
│   ├── task.py            # Task object definition
│   └── worker.py          # Task processing logic
├── tests/
│   ├── __init__.py
│   ├── test_queue.py      # Queue unit tests
│   ├── test_task.py       # Task unit tests
│   └── test_edge_cases.py # Edge case testing
├── docs/
│   ├── COMPLEXITY.md      # Time/space complexity analysis
│   ├── LEARNING_JOURNAL.md # Reflection & discoveries
│   └── README.md          # Architecture documentation
├── requirements.txt
├── .gitignore
└── README.md
```

## Features

- Custom Queue implementation (no built-in libraries)
- Task creation and management
- FIFO task processing
- Comprehensive unit tests
- Error handling for edge cases

## Getting Started

### Prerequisites
- Python 3.8+

### Installation

```bash
pip install -r requirements.txt
```

### Running Tests

```bash
pytest tests/
```

### Running with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

## Usage

*To be implemented*

## Acceptance Criteria

### Core Implementation
- [ ] Queue Data Structure: Implement custom queue with `enqueue()`, `dequeue()`, `peek()`, `is_empty()`, `size()` methods
- [ ] Task Object: Create Task class with properties (id, name, status, priority, timestamp)
- [ ] Worker Logic: Implement worker that processes tasks from queue sequentially
- [ ] No Built-in Libraries: Use only Python primitives (lists, dicts) - no `collections.deque`

### Testing
- [ ] Unit Tests: Write tests for queue operations (enqueue, dequeue, edge cases)
- [ ] Task Tests: Validate task creation and status transitions
- [ ] Edge Cases: Test empty queue, single item, multiple items, invalid operations
- [ ] Test Coverage: Aim for 90%+ code coverage with pytest

### Documentation
- [ ] Complexity Analysis: Document time/space complexity for all queue operations
- [ ] Learning Journal: Reflect on discoveries, challenges, and key learnings
- [ ] Code Comments: Clear inline documentation explaining logic
- [ ] Architecture Docs: Explain system design and how components interact

### Project Structure
- [ ] Follow provided directory structure with `src/`, `tests/`, `docs/`
- [ ] Populate `requirements.txt` with pytest dependency
- [ ] Add `.gitignore` for Python artifacts
- [ ] Update main README with project overview and setup instructions

## Documentation

- **[Complexity Analysis](docs/COMPLEXITY.md)** - Time and space complexity of queue operations
- **[Learning Journal](docs/LEARNING_JOURNAL.md)** - Insights and discoveries during development

## Key Concepts Covered

1. **Data Structures**: Queue implementation with enqueue/dequeue operations
2. **Testing**: Unit tests with pytest framework
3. **Documentation**: Code comments, complexity analysis, and learning reflections
4. **Software Design**: Task management and worker patterns

## Definition of Done

✅ All acceptance criteria met  
✅ Code review complete  
✅ Tests passing at 90%+ coverage  
✅ Documentation complete and accurate
