## Command: unittests

Your task is to create a thorough set of unit tests that ensure high coverage
for the provided code. Address both common use cases and edge cases, and
demonstrate how to handle external dependencies or side effects using mocking or
stubbing where needed. Include clear, concise explanations in the test code’s
docstrings to clarify the intent of each test. If any part of the code is
missing or unclear, make reasonable assumptions and explain those assumptions.

Place these tests in another file than the source files, following these
conventions:

- The file holding the unittests is named `test_<original_file_name>.<ext>` (for
  example, if the source file is `file.abc`, the test file should be named
  `test_file.abc`.)
- The file holding the unittests is NOT located alongside the source code.
  Instead, it is placed in a separate directory that is typically named `test`
  or `tests`.
