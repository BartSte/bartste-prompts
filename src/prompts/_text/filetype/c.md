## Filetype: C

When writing C code, you MUST follow these principles:

- Use ANSI C standard libraries unless specific platform features are required
- Follow secure coding practices:
  - Validate all pointer dereferences
  - Use bounded string functions (strncpy instead of strcpy)
  - Check return values of all system calls
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
- Use proper error handling:
  - Check return values from system calls
  - Use errno for system error reporting
  - Provide meaningful error messages
- Follow consistent memory management:
  - Free allocated memory in reverse allocation order
  - Use const for pointers that shouldn't modify data
  - Document ownership of transferred pointers
- When testing C code:
  - Use Check framework patterns
  - Isolate tests using test fixtures
  - Test edge cases and error conditions
