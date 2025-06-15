## Filetype: Python

When writing python docstrings, you also MUST follow these principles:

- Add docstrings to the code that using Google docstrings. For example:

```python
class Point:
    """Represents a 2D Point."""

    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        """Init.
        Args:
          x: the x coordinate.
          y: the y coordinate.
        """
        self.x = x
        self.y = y

def add(a: int, b: int) -> int:
  """Adds two numbers.

  Args:
      a: the first number.
      b: the second number.

  Returns:
      Sum of the two numbers.
  """
  return a + b
```
