## Filetype: C++

When writing C++ docstrings, you MUST follow these principles:

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
