# Lua Development Standards

This document outlines the standards and best practices for Lua development at Bayat.

## Code Style and Formatting

### General Guidelines
- Maximum line length should be 80 characters
- Use 2 spaces for indentation, not tabs
- Files should be encoded in UTF-8
- Files should end with a newline
- Use spaces around operators
- No trailing whitespace
- Use empty lines to separate logical sections of code

### Naming Conventions
1. **Variables and Functions**:
   - Use snake_case for variable and function names (e.g., `player_score`, `calculate_total`)
   - Use descriptive names that reflect purpose or meaning
   - Local variables and private functions should start with lowercase
   - Boolean variables should use prefixes like `is_`, `has_`, or `should_` (e.g., `is_valid`)

2. **Constants**:
   - Use SCREAMING_SNAKE_CASE for constants (e.g., `MAX_PLAYERS`, `DEFAULT_TIMEOUT`)
   - Define constants at the top of the file or module

3. **Modules and Classes**:
   - Use PascalCase for "classes" (tables that are meant to be used with a metatable)
   - Use snake_case for modules (e.g., `player_manager.lua`)
   - Module names should match their filenames

4. **Private Members**:
   - Prefix private functions and variables with an underscore (e.g., `_private_helper`)
   - Keep truly private functions local to the module

### Code Organization
1. **File Structure**:
   - Organize files by functionality
   - One primary "class" or module per file
   - Keep files reasonably sized (under 500 lines when possible)
   - Standard order:
     - Module declaration/imports/requires
     - Constants
     - Local functions
     - Module table definition
     - Public functions
     - Return statement for the module

2. **Module Structure**:
   - Use the module pattern: 
     ```lua
     local MyModule = {}
     
     -- Functions and variables defined here
     
     return MyModule
     ```
   - Import other modules with local variables:
     ```lua
     local other_module = require("other_module")
     ```

## Tables and Data Structures

1. **Table Formatting**:
   - Format tables consistently:
     ```lua
     -- Single line for short tables
     local point = { x = 10, y = 20 }
     
     -- Multiple lines for longer tables
     local config = {
       name = "Application",
       version = "1.0.0",
       settings = {
         fullscreen = true,
         resolution = "1920x1080"
       }
     }
     ```
   - Use trailing commas in multiline tables for easier additions and version control
   - Align keys and values in table definitions when it improves readability

2. **Table Usage**:
   - Use tables as the primary data structure
   - Prefer table.insert() and table.remove() for array operations
   - Use ipairs() for array-like tables and pairs() for associative tables
   - Avoid mixing array and hash table styles unless necessary

## Object-Oriented Programming

1. **Class Pattern**:
   - Use a consistent class pattern with metatables:
     ```lua
     local MyClass = {}
     MyClass.__index = MyClass
     
     function MyClass.new(args)
       local self = setmetatable({}, MyClass)
       -- Initialize object
       return self
     end
     
     function MyClass:method()
       -- Method implementation
     end
     
     return MyClass
     ```

2. **Inheritance**:
   - Implement inheritance through metatables:
     ```lua
     local Parent = require("parent")
     
     local Child = {}
     Child.__index = Child
     setmetatable(Child, Parent)
     
     function Child.new(args)
       local self = Parent.new(args)
       setmetatable(self, Child)
       -- Initialize child-specific properties
       return self
     end
     ```

## Error Handling

1. **Error Reporting**:
   - Use Lua's error mechanism appropriately:
     ```lua
     if not condition then
       error("Meaningful error message", 2)  -- 2 means report error at caller's level
     end
     ```
   - Include contextual information in error messages
   - Use assert() for validating arguments and preconditions:
     ```lua
     function my_function(required_arg)
       assert(required_arg, "required_arg is mandatory")
       -- Function implementation
     end
     ```

2. **Error Handling**:
   - Use pcall() or xpcall() to catch errors:
     ```lua
     local success, result = pcall(function()
       -- Function that might throw an error
     end)
     
     if not success then
       -- Handle error
       print("Error: " .. result)
     end
     ```
   - Return error values for non-exceptional conditions:
     ```lua
     function find_user(id)
       if not valid_id(id) then
         return nil, "Invalid user ID"
       end
       -- Find user
       return user
     end
     ```

## Performance Considerations

1. **Memory Management**:
   - Avoid creating tables in tight loops
   - Reuse tables when possible using table.clear() (Lua 5.4+) or custom clear function
   - Be aware of garbage collection events and their impact on performance
   - Use weak tables for caches to allow garbage collection of unused objects

2. **Algorithm Efficiency**:
   - Use local variables for performance-critical code
   - Avoid global lookups in tight loops
   - Precompute values when possible
   - Be mindful of table access patterns and string concatenation
   - Use string.format() for complex string formatting
   - Consider performance trade-offs when using closures

## Documentation

1. **Code Comments**:
   - Use `--` for single-line comments
   - Use `--[[` and `]]` for multi-line comments
   - Document the purpose of all functions, parameters, and return values
   - Explain non-obvious code sections
   - Use consistent comment style:
     ```lua
     ---
     -- Brief description of function
     -- @param name (type) Description of parameter
     -- @return (type) Description of return value
     --
     function my_function(name)
       -- Implementation
     end
     ```

2. **Module Documentation**:
   - Include a header comment at the top of each file describing the module's purpose
   - Document dependencies and usage examples
   - Consider using LuaDoc or similar documentation tools for API documentation

## Testing

1. **Unit Testing**:
   - Use a testing framework like Busted, LuaUnit, or Telescope
   - Write tests for all public functions
   - Organize tests to match the module structure
   - Test edge cases and error conditions

2. **Test Organization**:
   - Keep tests in a separate directory (e.g., `tests/`)
   - Name test files to match the modules they test (e.g., `test_player_manager.lua`)
   - Use descriptive test names that indicate what is being tested

## Modules and Dependencies

1. **Module Structure**:
   - Use proper module pattern:
     ```lua
     local MyModule = {}
     
     -- Module functions defined here
     
     return MyModule
     ```
   - Avoid global variables
   - Keep module interfaces clean and focused
   - Document dependencies in the module header

2. **Dependency Management**:
   - Use require() with relative paths for local modules
   - Specify version dependencies in a project manifest
   - Consider using LuaRocks for dependency management
   - Minimize external dependencies

## Security Considerations

1. **Input Validation**:
   - Validate all inputs, especially from external sources
   - Sanitize data used in sensitive operations
   - Be cautious with functions like loadstring() and setfenv()
   - Avoid using insecure serialization methods

2. **Environment Security**:
   - Use sandboxing techniques for untrusted code
   - Limit access to sensitive system functions
   - Carefully review any use of os.execute(), io operations, and network functions

## Lua Version Compatibility

1. **Version-Specific Features**:
   - Clearly document which Lua version your code targets
   - Be aware of language differences between Lua 5.1, 5.2, 5.3, and 5.4
   - Use conditional code or compatibility libraries when supporting multiple Lua versions
   - Document any version-specific features or dependencies

2. **Compatibility Libraries**:
   - Consider using compatibility libraries like compat-5.3
   - Test code on all supported Lua versions

## Game Development (If Applicable)

1. **Game Engine Integration**:
   - Follow engine-specific best practices (Unity, LÖVE, etc.)
   - Understand the lifecycle and performance characteristics of the engine
   - Use appropriate design patterns for your engine

2. **Game-Specific Patterns**:
   - Use component-based design when appropriate
   - Consider using an entity-component system for complex games
   - Separate game logic from rendering code
   - Implement proper game state management

## Version Control

1. **Commit Guidelines**:
   - Follow the project's commit message format
   - Make logical, focused commits
   - Ensure code runs without errors before committing
   - Document breaking changes clearly 