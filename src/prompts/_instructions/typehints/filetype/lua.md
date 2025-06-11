## Filetype: Lua

When writing Lua code, you MUST follow these principles:

- Prefer local variables over global ones. Always declare variables with `local` unless there's a specific reason to use globals.
- Use proper table construction patterns:
  - Use `{{}}` for tables with sequential indexes (arrays)
  - Use table constructors with explicit keys for dictionaries
  - Prefer `table.insert()` for adding to arrays
- Handle nil values properly using `if` checks or the `or` operator
- Use Lua's error handling appropriately:
  - Use `assert()` for validating critical preconditions
  - Use `pcall()`/`xpcall()` for handling recoverable errors
- Use metatables judiciously - only when truly needed for inheritance or operator overloading
- Follow string handling best practices:
  - Use `string.format()` for complex string construction
  - Prefer `..` operator for simple concatenations
  - Be aware of string interning with large numbers of unique strings
- Use module pattern for code organization:

  ```lua
  local M = {{}}

  function M.new(init_val)
      local obj = {{value = init_val or 0}}
      setmetatable(obj, {{__index = M}})
      return obj
  end

  function M:increment()
      self.value = self.value + 1
  end

  return M
  ```

- Write detailed docstrings using LuaDoc-style annotations:

  ```lua
  --- A simple counter class
  ---@class Counter
  ---@field value number The current count value
  local Counter = {{}}

  --- Create a new Counter instance
  -- @param init_val number (optional) Initial value
  -- @return Counter instance
  function Counter.new(init_val)
      -- ...
  end
  ```

- Add type hint annotations using LDT (Lua Development Tools) format:

  ```lua
  --- Add two numbers
  ---@param a number
  ---@param b number
  ---@return number
  local function add(a, b)
      return a + b
  end

  --- A coordinate tuple
  ---@type Coord
  ---@field x number
  ---@field y number
  ```

- Follow Lua style guidelines:
  - 2 space indentation
  - snake_case for variables and functions
  - PascalCase for class-like tables
  - UPPER_CASE for constants
  - Avoid semicolons at line endings
- When testing Lua code:
  - Use busted test framework patterns where applicable
  - Follow arrange-act-assert structure
  - Use descriptive test names with `describe` and `it` blocks
