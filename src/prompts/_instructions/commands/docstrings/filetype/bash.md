## Filetype: Bash

When writing docstrings for Bash scripts, you MUST follow these principles:

- Document functions with args and flags:

```bash
# @brief Create a new directory and enter it
# @param -p PARENT  Parent directory
# @param DIRNAME    Directory to create
mkcd() {{
    # ...
}}
```
