# Flow Control and Rate Limiting Algorithms Homework

This repository contains solutions for homework tasks on flow control and rate limiting algorithms.

## Tasks
- **Task 1**: Implement a Rate Limiter using the Sliding Window algorithm to restrict message frequency in a chat system.
- **Task 2**: Implement a Rate Limiter using the Throttling algorithm to enforce a minimum interval between messages in a chat system.

## Files
- `sliding_window_limiter.py`: Solution for Task 1.
- `throttling_limiter.py`: Solution for Task 2.
- `requirements.txt`: Dependency list for the project.

## Requirements
- Python 3.x
- No additional libraries are required for these scripts (they use standard Python modules: `time`, `random`, `collections.deque`, `typing`).
- Install dependencies (if needed for other tasks):
  ```bash
  pip3 install -r requirements.txt
  ```

## Usage
Run each script to test:
```bash
python3 sliding_window_limiter.py
python3 throttling_limiter.py
```

## Notes
- Both scripts simulate message flow with a 10-second restriction per user.
- Output matches the expected format with success/failure indicators and wait times.
- Scripts are tested on Python 3.11.