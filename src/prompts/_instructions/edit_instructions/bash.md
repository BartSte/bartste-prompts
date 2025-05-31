## Filetype: Bash

When writing Bash scripts, you MUST follow these principles:

- Add shebang line: `#!/usr/bin/env bash`
- Enable strict mode at script start:
  ```bash
  set -euo pipefail
  ```
- Document functions with args and flags:
  ```bash
  # @brief Create a new directory and enter it
  # @param -p PARENT  Parent directory
  # @param DIRNAME    Directory to create
  mkcd() {{
      # ...
  }}
  ```
- Follow POSIX compatibility guidelines:
  - Use `#!/bin/sh` for portable scripts
  - Avoid bashisms in POSIX mode
  - Test with shellcheck
- Variable handling:
  - UPPER_CASE for global variables
  - lower_case for local variables
  - readonly for constants
- Error handling:
  - Trap EXIT signals for cleanup
  - Use `|| true` to ignore expected errors
  - Provide usage messages for invalid args
- When testing Bash scripts:
  - Use bats-core testing framework
  - Test exit codes and output
  - Mock external dependencies
