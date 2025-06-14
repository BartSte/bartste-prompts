## Filetype: C

When writing docstrings for C, you MUST follow these principles:

- Document functions using Doxygen-style comments:

```c
/**
 * @brief Adds two integers
 * @param a First operand
 * @param b Second operand
 * @return Sum of a and b
 */
int add(int a, int b) {{
    return a + b;
}}
```
