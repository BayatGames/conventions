# C Development Standards

This document outlines the standards and best practices for C development at Bayat.

## Code Style and Formatting

### General Guidelines
- Follow the K&R style for code formatting
- Maximum line length should be 80 characters
- Use 4 spaces for indentation, not tabs
- Files should be encoded in UTF-8
- Files should end with a newline
- Comments should be written in grammatically correct English
- Use `/* */` for multi-line comments and `//` for single-line comments

### Naming Conventions
1. **Functions**:
   - Use snake_case for function names (e.g., `calculate_total`, `find_element`)
   - Use descriptive names that clearly indicate the purpose
   - Prefix module/component-specific functions with a component identifier (e.g., `net_connect`, `mem_allocate`)

2. **Variables**:
   - Use snake_case for variable names (e.g., `item_count`, `user_input`)
   - Use meaningful names that reflect the purpose or meaning
   - Boolean variables should use `is_`, `has_`, or `can_` prefixes (e.g., `is_valid`)
   - For loop counters or temporary variables, single letters like `i`, `j`, `k` are acceptable

3. **Constants and Macros**:
   - Use SCREAMING_SNAKE_CASE for constants and macros (e.g., `MAX_BUFFER_SIZE`, `PI_VALUE`)
   - Don't use Hungarian notation

4. **Structures and Typedefs**:
   - Use PascalCase for structure type names (e.g., `NetworkConnection`, `UserData`)
   - Use snake_case for structure members
   - Use `_t` suffix for typedef names (e.g., `size_t`, `net_conn_t`)

5. **Enums**:
   - Use PascalCase for enum type names
   - Use SCREAMING_SNAKE_CASE for enum values
   - Prefix enum values with a common prefix (e.g., `COLOR_RED`, `COLOR_BLUE`)

### Code Organization
1. **File Structure**:
   - Header files should use `.h` extension
   - Implementation files should use `.c` extension
   - Place standard library includes first, then custom includes
   - Use include guards in all header files using `#ifndef`, `#define`, and `#endif`
   - Separate logical code sections with comments

2. **Standard order for file content**:
   - Include directives
   - Macro definitions
   - Type definitions (structs, enums, typedefs)
   - Function prototypes
   - Global variables (minimize use)
   - Function implementations

## Memory Management

### Best Practices
1. **Allocation and Deallocation**:
   - Always check the return values of `malloc()`, `calloc()`, and `realloc()`
   - Free all allocated memory when no longer needed
   - Use a consistent memory management pattern throughout the codebase
   - Consider implementing or using custom memory management routines for specific purposes

2. **Preventing Memory Leaks**:
   - Ensure that resources are released in all code paths, including error conditions
   - Use tool support (Valgrind, AddressSanitizer) to check for memory leaks
   - Document ownership and lifetime of allocated memory in function documentation

3. **Buffer Management**:
   - Always check for buffer overflow conditions
   - Prefer safer alternatives to unsafe functions (e.g., use `strncpy()` instead of `strcpy()`)
   - Never use gets(), prefer fgets() with appropriate buffer size checks

## Error Handling

1. **Error Codes**:
   - Use consistent error codes across the application
   - Return error codes from functions rather than using global error variables where possible
   - Document all possible error codes a function can return

2. **Error Reporting**:
   - Implement a consistent error reporting mechanism
   - Consider using a logging system to record errors
   - Handle errors at the appropriate level, avoiding error propagation when the error can be handled locally

## Documentation

1. **Code Comments**:
   - Document the purpose of all functions in header files
   - Document non-obvious implementation details in implementation files
   - Use consistent comment style for API documentation

2. **Function Documentation**:
   - Document all parameters, return values, and error conditions
   - Specify any side effects or preconditions
   - Format:
     ```c
     /**
      * Brief description of function
      *
      * @param param1 Description of first parameter
      * @param param2 Description of second parameter
      * @return Description of return value
      */
     ```

## Testing

1. **Unit Testing**:
   - Write tests for all public functions
   - Use a consistent testing framework (e.g., Unity, CUnit)
   - Test edge cases and error conditions

2. **Integration Testing**:
   - Test interaction between modules
   - Test with realistic data sets

## Security Considerations

1. **Input Validation**:
   - Validate all input, especially user input
   - Check array bounds before access
   - Use secure coding practices to avoid common vulnerabilities

2. **Secure Functions**:
   - Prefer secure alternatives to unsafe standard library functions
   - Avoid functions prone to buffer overflows (gets(), scanf() without limits, etc.)
   - Consider using security-focused static analysis tools

## Performance Optimization

1. **General Guidelines**:
   - Optimize for readability and correctness first, then performance
   - Profile code to identify actual bottlenecks before optimizing
   - Document performance-critical code sections

2. **Algorithm Selection**:
   - Choose appropriate algorithms based on data size and usage patterns
   - Consider space-time tradeoffs based on the application requirements

## Dependencies

1. **Library Usage**:
   - Prefer standard libraries when possible
   - Document all external dependencies
   - Consider portability when selecting libraries

2. **Version Management**:
   - Specify compatible versions for all dependencies
   - Test with the specific versions used in production

## Platform-Specific Considerations

1. **Portability**:
   - Use standard C (C99 or C11) for maximum portability
   - Isolate platform-specific code in dedicated modules
   - Use conditional compilation for platform-specific code (#ifdef)
   - Document platform-specific assumptions

2. **Endianness**:
   - Be aware of endianness issues when working with binary data
   - Use appropriate conversion functions when necessary

## Tools and Environment

1. **Recommended Tools**:
   - Compiler: GCC, Clang
   - Static Analysis: Cppcheck, Clang Static Analyzer
   - Memory Checking: Valgrind, AddressSanitizer
   - Formatting: clang-format
   - Build System: Make, CMake

2. **Compiler Warnings**:
   - Compile with high warning levels (e.g., `-Wall -Wextra` for GCC)
   - Treat warnings as errors in CI/CD pipelines

## Version Control

1. **Commit Guidelines**:
   - Follow the project's commit message format
   - Group related changes in a single commit
   - Ensure the code compiles and passes tests before committing 