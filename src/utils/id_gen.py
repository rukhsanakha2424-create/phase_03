class IDGenerator:
    """Simple ID generator for in-memory tasks."""
    def __init__(self):
        self._current_id = 0

    def next_id(self) -> int:
        self._current_id += 1
        return self._current_id
