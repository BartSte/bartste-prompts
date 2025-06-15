## Filetype: Lua

When writing Lua docstrings, you MUST follow these principles:

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
