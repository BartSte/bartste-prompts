## Filetype: Python

When writing python code, you also MUST follow these principles:

- Add type hints to where possible. You MUST follow these principles:
  - Where possible, use builtin types instead of those from `typing` (for example, `list` instead of `List`)
  - Where possible, import types from `collections.abc`.
  - Do not use `Optional` but use ` | None` instead
  - Try to avoid dynamic imports and relative imports.

- Add docstrings to the code. Use Google docstrings. For example:

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
    """Add two numbers.

    Args:
        a: the first number.
        b: the second number.

    Returns:
        Sum of the two numbers.
    """
    return a + b
  ```

- When writing unittests follow these principles:
  - Make use of the `unittest` framework's `TestCase` class to construct your test cases.
  - Try to focus on testing against the actual implementation
  - Tests are located in the `tests` folder mirroring the structure of the `src` folder, where each module is prepended with `test_`. For example, the tests for `src/module/abc/example.py` would be located in `tests/test_module/test_abc/test_example.py`, or `tests/test_abc/test_example.py` if there is only one `module` folder.
