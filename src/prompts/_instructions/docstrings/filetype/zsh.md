## Filetype: Zsh

When writing zsh docstrings, you MUST follow these principles:

- Document functions with args and flags:

```zsh
# @brief Print formatted message
# @param -c COLOR  Set text color
# @param MESSAGE   Message to display
function print_message() {{
    # ...
}}
```
