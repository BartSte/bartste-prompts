## Filetype: Zsh

When writing Zsh scripts, you MUST follow these principles:

- Add shebang line: `#!/usr/bin/env zsh`
- Enable strict mode at script start:
  ```zsh
  set -euo pipefail
  emulate -L zsh
  ```
- Document functions with args and flags:
  ```zsh
  # @brief Print formatted message
  # @param -c COLOR  Set text color
  # @param MESSAGE   Message to display
  function print_message() {{
      # ...
  }}
  ```
- Follow security best practices:
  - Quote all variable expansions
  - Use [[ ]] for conditional tests
  - Sanitize user input
- Use zsh-specific features judiciously:
  - Array operations
  - Globbing qualifiers
  - Completion system
- Error handling:
  - Use TRAP* functions for error signals
  - Check exit codes of external commands
  - Provide meaningful error messages
- When testing Zsh scripts:
  - Use shunit2 or zunit frameworks
  - Test individual functions with subshells
  - Verify exit codes and output
