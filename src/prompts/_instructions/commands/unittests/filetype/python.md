## Filetype: Python

### General coding principles

- Add type hints wherever possible.
  - Prefer built-in types (`list`, `dict`, …) over those from `typing`.
  - Import abstract collections (e.g. `Iterable`, `Mapping`) from `collections.abc`.
  - Use the PEP-604 union syntax (`str | None`) instead of `Optional[str]`.
  - Avoid dynamic or relative imports.
- Add Google-style docstrings to every public class, function, and method.

### Unit-testing guidelines

1. **Framework**

   - Use the standard `unittest` framework `TestCase`.

2. **Real I/O first, mock as needed**

   - Write black-box tests that exercise the true implementation with concrete inputs/outputs.
   - When a test would be **slow, flaky, or environment-dependent**—for example:
     - Network requests (`requests`, sockets, HTTP clients)
     - Time or randomness (`time.sleep`, `datetime.now`, `random.*`)
     - Filesystem outside a `tmp_path` or `tempfile` sandbox
       – then replace only the problematic call sites with `unittest.mock`.
   - For **every external dependency you mock**, include **at least one** example that demonstrates correct use of `patch`, `MagicMock`, `side_effect`, or `autospec=True`.

3. **File structure**

```
src/<module>/
  __init__.py
  foo.py
  bar/
    __init__.py
    baz.py

tests/
  __init__.py
  test_foo.py
  test_bar/
    __init__.py
    test_baz.py
```

As can be seen, test are kept separate from the source directory. Here the
`tests` directory has the same package structure as the `src` directory where
each directory and file are prefixed with `test_` (when applicable).

4. **Coverage & quality**

- Target ≥ 80 % branch coverage.
- Keep each test independent and idempotent.
- Prefer explicit assertions (`assertEqual`, `assertRaises`, `assertTrue`, …).
- Clean up any resources you create (use `tempfile`, `setUp`/`tearDown`, or context managers).

5. **Example skeleton**

```python
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock


from mypkg.foo import parse_csv, fetch_data

# ---------- Real I/O tests ----------
class ParseCsvRealIOTest(unittest.TestCase):
    def test_parse_csv_valid(self) -> None:
        """parse_csv returns a list of dicts for a simple CSV."""
        tmp_dir = Path(self.assertTrue.__self__.__class__.__name__)  # quick temp dir
        csv_file = tmp_dir / "sample.csv"
        csv_file.write_text("a,b\n1,2")
        expected = [{"a": "1", "b": "2"}]
        self.assertEqual(parse_csv(csv_file), expected)

# ---------- Mock-based tests ----------
class FetchDataMockedTest(unittest.TestCase):
    @patch("mypkg.foo.requests.get", autospec=True)
    def test_fetch_data_happy_path(self, mock_get: MagicMock) -> None:
        """fetch_data returns decoded JSON when the HTTP call succeeds."""
        mock_get.return_value.json.return_value = {"id": 1}
        self.assertEqual(fetch_data(1), {"id": 1})
        mock_get.assert_called_once_with("https://api.example.com/items/1")


```
