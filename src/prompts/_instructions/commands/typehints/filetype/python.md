## Filetype: Python

### Adding Type Hints to Python Code

You must follow these Python-specific rules when adding type hints:

1. **Basic Annotations**:

   - Add parameter types in function definitions: `def func(arg: type)`
   - Add return types: `def func(...) -> return_type:`
   - Annotate variables: `var: type = value`

2. **Precision**:

   - Use built-in types (`list`, `dict`) instead of `typing` aliases (`List`, `Dict`)
   - For complex types, import from `collections.abc` (e.g., `Iterable`, `Sequence`)
   - Use `| None` instead of `Optional` for nullable types
   - For union types, use `Type1 | Type2`

3. **Docstrings**:

   - When docstrings exist, update parameter/return type information
   - Remove redundant type information from docstrings
   - Keep docstring content when it provides additional context

4. **Special Cases**:

   - Use `Any` only when necessary
   - For callback functions, use `Callable[[ArgTypes], ReturnType]`
   - For classes, annotate instance variables at class level and NOT in the
     `__init__`. So the following is good:

     ```python
     class Foo:
         bar: int
         def __init__(self):
             self.bar = 1
     ```

     and the following is bad:

     ```python
     class Foo:
         def __init__(self):
             self.bar: int = 1
     ```

### Examples

**Function without type hints**:

```python
def greet(name):
    return f"Hello, {name}"
```

**With type hints**:

```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```

**Class without type hints**:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

**With type hints**:

```python
class Point:
    x: int
    y: int
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
```

**Union type**:

```python
def parse_input(value: str | int) -> float:
    return float(value)
```

**Nullable parameter**:

```python
def send_message(msg: str, recipient: str | None = None) -> bool:
    ...
```

**Collections**:

```python
from collections.abc import Sequence

def process_items(items: Sequence[str]) -> list[tuple[int, str]]:
    ...
```

**Generic Type**:

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    items: list[T]

    def __init__(self) -> None:
        self.items = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()
```
