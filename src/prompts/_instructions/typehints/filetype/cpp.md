## Filetype: C++

When writing C++ code, you MUST follow these principles:

- Prefer modern C++ features (C++17/20) where available
- Follow RAII principles for resource management
- Use smart pointers (unique_ptr, shared_ptr) instead of raw pointers
- Document classes and functions using Doxygen-style:
  ```cpp
  /// @brief Matrix class for linear algebra operations
  class Matrix {{
  public:
      /// @brief Construct identity matrix
      /// @param size Matrix dimension
      explicit Matrix(size_t size);
  }};
  ```
- Follow type safety guidelines:
  - Use static_cast over C-style casts
  - Prefer enum class over plain enum
  - Use nullptr instead of NULL
- Exception safety:
  - Provide basic exception guarantee at minimum
  - Use noexcept where appropriate
  - Document exception guarantees in comments
- Template metaprogramming:
  - Provide concept constraints in C++20+
  - Document template requirements
  - Prefer static_assert for type checking
- When testing C++ code:
  - Use Catch2 or Google Test frameworks
  - Test template specializations
  - Verify exception behavior
