## Filetype: Python

### Refactoring Python Code

You must follow these Python-specific rules when refactoring:

1. **Code Structure**:

   - Follow PEP 8 style guidelines
   - Break large functions into smaller, focused functions
   - Use Pythonic constructs (list comprehensions, context managers)
   - Apply SOLID principles (especially Single Responsibility Principle)

2. **Readability**:

   - Use meaningful names for variables/functions/classes
   - Keep functions under 15 lines
   - Remove unused imports and variables
   - Replace magic numbers with constants

3. **Error Handling**:

   - Use built-in exceptions where appropriate
   - Avoid broad except clauses
   - Use context managers for resource handling

4. **Comments and Docstrings**:

   - Remove outdated comments
   - Update docstrings to match functionality
   - Use Google-style docstrings for public APIs

5. **Type Hints**:
   - Add type hints to public interfaces
   - Use built-in types (list, dict) instead of typing aliases
   - Use `| None` instead of Optional

### Examples

**Before (Poor Structure)**:

```python
def d(data):
    r = {}
    for k, v in data.items():
        if type(v) == dict:
            r[k] = d(v)
        elif type(v) == list:
            r[k] = [d(i) if type(i) == dict else i for i in v]
        else:
            r[k] = v
    return r
```

**After (Well-Structured)**:

```python
def deep_copy(data: dict) -> dict:
    """Recursively copy nested dictionaries and lists.

    Args:
        data: Input dictionary to copy

    Returns:
        Deep copy of input dictionary
    """
    copy = {}
    for key, value in data.items():
        if isinstance(value, dict):
            copy[key] = deep_copy(value)
        elif isinstance(value, list):
            copy[key] = [deep_copy(item) if isinstance(item, dict) else item
                         for item in value]
        else:
            copy[key] = value
    return copy
```

**Before (Poor Error Handling)**:

```python
def fetch(url):
    import requests
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None
```

**After (Robust Error Handling)**:

```python
import requests
from requests.exceptions import RequestException

def fetch_json(url: str) -> dict | None:
    """Fetch JSON data from URL with proper error handling.

    Args:
        url: API endpoint URL

    Returns:
        JSON response or None on failure
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except RequestException as e:
        logging.error(f"Request failed: {e}")
        return None
    else:
        return response.json()
```

**Before (Violates SOLID)**:

```python
class Report:
    def __init__(self, data):
        self.data = data

    def generate(self):
        # complex report generation
        pass

    def save_pdf(self):
        # PDF saving logic
        pass

    def send_email(self):
        # email sending logic
        pass
```

**After (SOLID Compliant)**:

```python
class ReportGenerator:
    def __init__(self, data: dict):
        self.data = data

    def generate(self) -> str:
        """Generate report content"""
        # generation logic
        return "Report content"

class ReportExporter:
    @staticmethod
    def save_pdf(content: str, filename: str) -> None:
        """Export report to PDF file"""
        # saving logic

    @staticmethod
    def send_email(content: str, recipients: list[str]) -> None:
        """Email report to recipients"""
        # email logic
```
