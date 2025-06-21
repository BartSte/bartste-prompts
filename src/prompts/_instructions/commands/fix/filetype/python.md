## Filetype: Python

### Fixing Python Bugs

You must follow these Python-specific rules when fixing bugs:

1. **Bug Types**:

   - Syntax errors (indentation, missing colons, etc.)
   - Runtime exceptions (NameError, TypeError, ValueError, etc.)
   - Logical errors (incorrect calculations, conditionals)
   - Concurrency issues (threading, asyncio)
   - Resource leaks (unclosed files/sockets)
   - Python version incompatibilities

2. **Pythonic Solutions**:

   - Prefer context managers for resource handling
   - Use built-in exceptions appropriately
   - Leverage Python's duck typing
   - Follow PEP 8 style guidelines
   - Write defensive code with type hints

### Common Python Bugs and Fixes

**Syntax Error**:

```python
# Before
def calculate(a b):
    return a + b

# After
def calculate(a, b):
    return a + b
```

**TypeError**:

```python
# Before
def greet(name):
    return "Hello " + name

greet(42)

# After
def greet(name: str | int) -> str:
    return "Hello " + str(name)
```

**Resource Leak**:

```python
# Before
f = open('file.txt')
content = f.read()
return content

# After
with open('file.txt') as f:
    return f.read()
```

**Logical Error**:

```python
# Before
def is_even(n):
    return n % 2 = 0

# After
def is_even(n: int) -> bool:
    return n % 2 == 0
```

**Concurrency Issue**:

```python
# Before
counter = 0

def increment():
    global counter
    counter += 1

# After
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    with lock:
        counter += 1
```
