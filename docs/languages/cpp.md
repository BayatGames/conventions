<!--
Document: C++ Coding Standards
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# C++ Coding Standards

This document outlines the coding standards and best practices for C++ development across all Bayat projects. Following these guidelines ensures code consistency, quality, and maintainability.

## Table of Contents

- [C++ Version](#c-version)
- [Code Style](#code-style)
- [Naming Conventions](#naming-conventions)
- [Memory Management](#memory-management)
- [Project Structure](#project-structure)
- [Build System](#build-system)
- [Headers and Includes](#headers-and-includes)
- [Error Handling](#error-handling)
- [Performance Considerations](#performance-considerations)
- [Concurrency](#concurrency)
- [Security Best Practices](#security-best-practices)
- [Testing](#testing)
- [Documentation](#documentation)
- [Tools and IDE Configuration](#tools-and-ide-configuration)

## C++ Version

- Use C++17 for all new projects
- C++14 is the minimum supported version for existing projects
- Document C++ version requirements in project README and build files
- Use C++20 features only when they provide significant benefits and are supported by all target compilers

## Code Style

All C++ code should follow a consistent style based on the Google C++ Style Guide with the following adaptations:

### Formatting

- Use 2 spaces for indentation (no tabs)
- Maximum line length of 100 characters
- Use clang-format for automated code formatting
- Avoid excessive horizontal spacing (no multiple spaces for alignment)
- Place opening braces on the same line as control statements
- Place opening braces for function/method definitions on a new line
- Use `nullptr` instead of `NULL` or `0`
- Use `auto` when it improves readability, but don't overuse it

### Example Style

```cpp
// Good C++ style example
#include <string>
#include <vector>

namespace bayat {
namespace utils {

class StringProcessor {
 public:
  StringProcessor();
  ~StringProcessor();

  // Process a string and return a modified version
  std::string Process(const std::string& input);

 private:
  bool IsValid(const std::string& text) const;
  std::vector<std::string> cached_results_;
};

StringProcessor::StringProcessor() 
{
  // Constructor implementation
}

std::string StringProcessor::Process(const std::string& input) 
{
  if (!IsValid(input)) {
    return "";
  }

  std::string result = input;
  // Process the string...
  for (auto& c : result) {
    if (c == ' ') {
      c = '_';
    }
  }

  cached_results_.push_back(result);
  return result;
}

}  // namespace utils
}  // namespace bayat
```

### Clang-Format Configuration

Use the following `.clang-format` file as a baseline:

```yaml
---
Language: Cpp
BasedOnStyle: Google
AccessModifierOffset: -1
AlignAfterOpenBracket: Align
AlignConsecutiveAssignments: false
AlignConsecutiveDeclarations: false
AlignEscapedNewlines: Left
AlignOperands: true
AlignTrailingComments: true
AllowAllParametersOfDeclarationOnNextLine: true
AllowShortBlocksOnASingleLine: false
AllowShortCaseLabelsOnASingleLine: false
AllowShortFunctionsOnASingleLine: Inline
AllowShortIfStatementsOnASingleLine: false
AllowShortLoopsOnASingleLine: false
AlwaysBreakAfterReturnType: None
AlwaysBreakBeforeMultilineStrings: true
AlwaysBreakTemplateDeclarations: Yes
BinPackArguments: true
BinPackParameters: true
BreakBeforeBinaryOperators: None
BreakBeforeBraces: Custom
BraceWrapping:
  AfterClass: false
  AfterControlStatement: false
  AfterEnum: false
  AfterFunction: true
  AfterNamespace: false
  AfterStruct: false
  AfterUnion: false
  AfterExternBlock: false
  BeforeCatch: false
  BeforeElse: false
  IndentBraces: false
  SplitEmptyFunction: true
  SplitEmptyRecord: true
  SplitEmptyNamespace: true
BreakBeforeInheritanceComma: false
BreakInheritanceList: BeforeColon
BreakBeforeTernaryOperators: true
BreakConstructorInitializersBeforeComma: false
BreakConstructorInitializers: BeforeColon
BreakStringLiterals: true
ColumnLimit: 100
CommentPragmas: '^ IWYU pragma:'
CompactNamespaces: false
ConstructorInitializerAllOnOneLineOrOnePerLine: true
ConstructorInitializerIndentWidth: 4
ContinuationIndentWidth: 4
Cpp11BracedListStyle: true
DerivePointerAlignment: false
FixNamespaceComments: true
IncludeBlocks: Preserve
IncludeCategories:
  - Regex: '^<.*\.h>'
    Priority: 1
  - Regex: '^<.*'
    Priority: 2
  - Regex: '.*'
    Priority: 3
IncludeIsMainRegex: '([-_](test|unittest))?$'
IndentCaseLabels: true
IndentPPDirectives: None
IndentWidth: 2
IndentWrappedFunctionNames: false
KeepEmptyLinesAtTheStartOfBlocks: false
MaxEmptyLinesToKeep: 1
NamespaceIndentation: None
PenaltyBreakAssignment: 2
PenaltyBreakBeforeFirstCallParameter: 1
PenaltyBreakComment: 300
PenaltyBreakFirstLessLess: 120
PenaltyBreakString: 1000
PenaltyExcessCharacter: 1000000
PenaltyReturnTypeOnItsOwnLine: 200
PointerAlignment: Left
ReflowComments: true
SortIncludes: true
SortUsingDeclarations: true
SpaceAfterCStyleCast: false
SpaceAfterTemplateKeyword: true
SpaceBeforeAssignmentOperators: true
SpaceBeforeCpp11BracedList: false
SpaceBeforeCtorInitializerColon: true
SpaceBeforeInheritanceColon: true
SpaceBeforeParens: ControlStatements
SpaceBeforeRangeBasedForLoopColon: true
SpaceInEmptyParentheses: false
SpacesBeforeTrailingComments: 2
SpacesInAngles: false
SpacesInContainerLiterals: false
SpacesInCStyleCastParentheses: false
SpacesInParentheses: false
SpacesInSquareBrackets: false
Standard: Cpp11
TabWidth: 2
UseTab: Never
```

## Naming Conventions

### Files

- Header files: `.h` extension
- Source files: `.cpp` extension
- Use all lowercase with underscores for filenames
- Match source file name to the main class/functionality it implements
- Example: `string_processor.h` and `string_processor.cpp`

### Directories

- Use lowercase with underscores
- Group related files into directories based on functionality
- Example: `core/`, `rendering/`, `physics/`

### Types

- Use CamelCase for class, struct, enum, and typedef names
- Example: `class StringProcessor`, `struct UserConfig`

### Variables

- Use snake_case for variable names
- Class member variables should have a trailing underscore
- Example: `std::string user_name;`, `int frame_count_;`
- Use descriptive names that indicate purpose
- Boolean variables should be named as predicates (e.g., `is_valid`, `has_data`)

### Constants

- Use kCamelCase for constants (with k prefix)
- Example: `const int kMaxBufferSize = 1024;`

### Functions

- Use CamelCase for functions and methods
- Accessor methods should match the property name
- Example: `void ProcessData()`, `int count() const`

### Namespaces

- Use lowercase for namespace names
- Use company or project name as the top-level namespace
- Example: `namespace bayat { namespace rendering { ... } }`

### Enums

- Enum names should use CamelCase
- Enum values should use kCamelCase (with k prefix)
- Example:

  ```cpp
  enum class LogLevel {
    kDebug,
    kInfo,
    kWarning,
    kError,
    kFatal
  };
  ```

## Memory Management

### General Guidelines

- Prefer automatic variables and RAII (Resource Acquisition Is Initialization)
- Avoid raw pointers when ownership semantics are required
- Use smart pointers to express ownership
- Explicitly delete copy/move constructors and assignment operators when not needed
- Be consistent with memory allocation (e.g., don't mix `new`/`delete` with `malloc`/`free`)

### Smart Pointers

- Use `std::unique_ptr` for exclusive ownership
- Use `std::shared_ptr` for shared ownership
- Use `std::weak_ptr` to break reference cycles with `std::shared_ptr`
- Prefer using `std::make_unique` and `std::make_shared` over direct constructor calls

Example:

```cpp
// Prefer this:
auto user = std::make_unique<User>("John", 30);

// Over:
std::unique_ptr<User> user(new User("John", 30));
```

### Resource Management

- Use RAII to manage resources (files, memory, mutexes, etc.)
- Create wrapper classes that handle resource cleanup in destructors
- Avoid naked `new` and `delete` operations
- Use containers and smart pointers to manage collections and object lifetimes

Example:

```cpp
class FileHandler {
 public:
  explicit FileHandler(const std::string& filename) {
    file_ = std::fopen(filename.c_str(), "r");
    if (!file_) {
      throw std::runtime_error("Failed to open file");
    }
  }

  ~FileHandler() {
    if (file_) {
      std::fclose(file_);
    }
  }

  // Prevent copying
  FileHandler(const FileHandler&) = delete;
  FileHandler& operator=(const FileHandler&) = delete;

  // Allow moving
  FileHandler(FileHandler&& other) noexcept : file_(other.file_) {
    other.file_ = nullptr;
  }
  
  FileHandler& operator=(FileHandler&& other) noexcept {
    if (this != &other) {
      if (file_) {
        std::fclose(file_);
      }
      file_ = other.file_;
      other.file_ = nullptr;
    }
    return *this;
  }

  // File operations...
  std::string ReadLine();

 private:
  FILE* file_;
};
```

## Project Structure

Organize C++ projects with the following directory structure:

```
project_name/
├── CMakeLists.txt          # Main CMake configuration
├── README.md               # Project documentation
├── LICENSE                 # License information
├── .gitignore              # Git ignore file
├── .clang-format           # Clang-format configuration
├── src/                    # Source code
│   ├── CMakeLists.txt      # Source build configuration
│   ├── main.cpp            # Application entry point
│   ├── core/               # Core functionality
│   │   ├── core.h          # Core public interface
│   │   ├── subsystem1.h    # Subsystem 1 header
│   │   └── subsystem1.cpp  # Subsystem 1 implementation
│   └── module2/            # Another module
│       ├── module2.h       # Module 2 public interface
│       └── module2.cpp     # Module 2 implementation
├── include/                # Public headers
│   └── project_name/       # Project-specific headers
│       ├── api.h           # Main API header
│       └── types.h         # Common types
├── tests/                  # Test directory
│   ├── CMakeLists.txt      # Test build configuration
│   ├── core/               # Core module tests
│   │   └── subsystem1_test.cpp
│   └── module2/            # Module 2 tests
│       └── module2_test.cpp
├── examples/               # Example applications
│   ├── CMakeLists.txt      # Examples build configuration
│   └── example1.cpp        # Example 1
├── docs/                   # Documentation
│   └── api.md              # API documentation
└── third_party/            # Third-party dependencies
    └── some_library/       # Third-party library
```

## Build System

### CMake

- Use CMake as the primary build system
- Set minimum required CMake version to 3.14 or higher
- Use target-based approach with modern CMake
- Define targets with clear properties and dependencies
- Use separate CMakeLists.txt files for different directories
- Prefer to use find_package for dependencies when available

Example CMakeLists.txt:

```cmake
cmake_minimum_required(VERSION 3.14)
project(ProjectName VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Build options
option(BUILD_TESTS "Build tests" ON)
option(BUILD_EXAMPLES "Build examples" ON)

# Add third-party dependencies
find_package(Boost REQUIRED COMPONENTS system filesystem)

# Define library target
add_library(${PROJECT_NAME}
  src/core/subsystem1.cpp
  src/module2/module2.cpp
)

# Set include directories
target_include_directories(${PROJECT_NAME}
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
  PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# Link dependencies
target_link_libraries(${PROJECT_NAME}
  PUBLIC
    Boost::system
    Boost::filesystem
)

# Compiler flags
target_compile_options(${PROJECT_NAME}
  PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/W4 /WX>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -Wpedantic -Werror>
)

# Build tests if enabled
if(BUILD_TESTS)
  enable_testing()
  add_subdirectory(tests)
endif()

# Build examples if enabled
if(BUILD_EXAMPLES)
  add_subdirectory(examples)
endif()

# Installation rules
install(TARGETS ${PROJECT_NAME}
  EXPORT ${PROJECT_NAME}Targets
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin
  INCLUDES DESTINATION include
)

install(DIRECTORY include/
  DESTINATION include
)
```

### Compiler Flags

- Enable high warning levels (`-Wall -Wextra -Wpedantic` or `/W4`)
- Treat warnings as errors in CI builds (`-Werror` or `/WX`)
- Enable debug information in debug builds
- Enable optimizations in release builds
- Consider enabling sanitizers in debug/test builds

## Headers and Includes

### Include Guards

- Use `#pragma once` for all header files
- Alternatively, use traditional include guards with project-specific prefix

Example:

```cpp
// Using #pragma once
#pragma once

// Or using traditional include guards
#ifndef BAYAT_MODULE_HEADER_H_
#define BAYAT_MODULE_HEADER_H_

// Header contents...

#endif  // BAYAT_MODULE_HEADER_H_
```

### Include Order

- Group and order includes as follows:
  1. Related header (e.g., `foo.cpp` includes `foo.h` first)
  2. C system headers (e.g., `<cstdlib>`)
  3. C++ standard library headers (e.g., `<iostream>`)
  4. Other libraries' headers
  5. Your project's headers
- Within each group, order alphabetically
- Use angle brackets for system and external headers (`<header>`)
- Use quotes for project headers (`"header.h"`)

Example:

```cpp
// In foo.cpp
#include "foo.h"  // Related header

#include <cstdlib>  // C system header
#include <cstring>

#include <iostream>  // C++ standard library header
#include <string>
#include <vector>

#include <boost/algorithm/string.hpp>  // Other libraries

#include "base/common.h"  // Project headers
#include "foo/bar.h"
```

### Forward Declarations

- Use forward declarations when possible to reduce compilation dependencies
- Include the full header when using derived classes, template details, or inlined functions

Example:

```cpp
// Forward declarations
namespace bayat {
class User;  // Forward declaration
}  // namespace bayat

// Later in the code
void ProcessUser(const bayat::User* user);
```

## Error Handling

### Exceptions

- Use exceptions for exceptional conditions that cannot be handled locally
- Document exception safety guarantees for functions and methods
- Catch exceptions by reference
- Catch specific exceptions before more general ones
- Provide meaningful error messages in exceptions
- Consider creating a hierarchy of custom exception classes for your project

Example:

```cpp
class DatabaseError : public std::runtime_error {
 public:
  explicit DatabaseError(const std::string& message)
      : std::runtime_error("Database error: " + message) {}
};

class ConnectionError : public DatabaseError {
 public:
  explicit ConnectionError(const std::string& message)
      : DatabaseError("Connection failed: " + message) {}
};

void ConnectToDatabase() {
  try {
    // Connection logic...
    if (!connection_established) {
      throw ConnectionError("Could not connect to database server");
    }
  } catch (const ConnectionError& e) {
    // Handle specific error
    LogError(e.what());
    throw;  // Rethrow for caller to handle
  } catch (const DatabaseError& e) {
    // Handle more general database error
    LogError(e.what());
    // Attempt recovery...
  } catch (const std::exception& e) {
    // Handle standard library exceptions
    LogFatalError(e.what());
    throw;
  }
}
```

### Error Codes

- Use error codes when exceptions are not appropriate (e.g., performance-critical code)
- Use `std::error_code` or custom error code types
- Provide clear documentation for error code meanings
- Consider using Boost.System or similar libraries for error code management

### Assertions

- Use `assert()` to check for conditions that should never happen
- Use runtime checks for conditions that might fail due to external factors
- Consider using a more feature-rich assertion library for production code

## Performance Considerations

### General Guidelines

- Write clean, readable code first, then optimize if necessary
- Measure performance before and after optimizations
- Focus on algorithmic improvements before micro-optimizations
- Use appropriate data structures for the task
- Minimize memory allocations in performance-critical paths
- Avoid copies of large objects

### Optimizations

- Use move semantics where appropriate
- Use references for function parameters to avoid copying
- Consider using `constexpr` for compile-time evaluation
- Use reserve() for vectors and other containers when size is known
- Prefer pre-increment (++i) over post-increment (i++) for iterators
- Use range-based for loops when possible

Example:

```cpp
// Less efficient
void ProcessNames(std::vector<std::string> names) {  // Copies the entire vector
  for (int i = 0; i < names.size(); i++) {  // Less idiomatic
    // Process each name
  }
}

// More efficient
void ProcessNames(const std::vector<std::string>& names) {  // Reference, no copy
  names.reserve(names.size() + 10);  // Reserve space if adding elements
  
  for (const auto& name : names) {  // Range-based for loop, no copy of string
    // Process each name
  }
}
```

## Concurrency

### Threading

- Use `std::thread` for basic threading needs
- Use `std::async` and `std::future` for task-based parallelism
- Document thread safety for classes and functions
- Be explicit about which resources are shared between threads
- Use thread-local storage when appropriate

### Synchronization

- Use `std::mutex` and `std::lock_guard` for basic synchronization
- Use `std::unique_lock` when more flexibility is needed
- Use `std::shared_mutex` for reader-writer locks
- Prefer higher-level synchronization mechanisms over raw locks
- Use `std::atomic` for simple shared variables
- Always lock in the same order to avoid deadlocks

Example:

```cpp
class ThreadSafeCounter {
 public:
  ThreadSafeCounter() = default;

  // Multiple threads can read the counter's value.
  unsigned int Get() const {
    std::shared_lock<std::shared_mutex> lock(mutex_);
    return value_;
  }

  // Only one thread can increment the counter at a time.
  void Increment() {
    std::unique_lock<std::shared_mutex> lock(mutex_);
    ++value_;
  }

  // Only one thread can reset the counter at a time.
  void Reset() {
    std::unique_lock<std::shared_mutex> lock(mutex_);
    value_ = 0;
  }

 private:
  mutable std::shared_mutex mutex_;
  unsigned int value_ = 0;
};
```

### Asynchronous Programming

- Use `std::future` and `std::promise` for asynchronous operations
- Consider using a task-based concurrency library for complex scenarios
- Document the execution context (which thread) for callbacks and handlers
- Be careful with capturing variables in lambdas for async operations

Example:

```cpp
std::future<int> ComputeValueAsync() {
  return std::async(std::launch::async, []() {
    // Perform expensive computation
    std::this_thread::sleep_for(std::chrono::seconds(2));
    return 42;
  });
}

void UseAsyncValue() {
  auto future = ComputeValueAsync();
  
  // Do other work while computation is running
  
  // Wait for result when needed
  try {
    int result = future.get();  // Will block until result is available
    std::cout << "Result: " << result << std::endl;
  } catch (const std::exception& e) {
    std::cerr << "Computation failed: " << e.what() << std::endl;
  }
}
```

## Security Best Practices

### Input Validation

- Validate all inputs, especially those from external sources
- Use secure string handling to prevent buffer overflows
- Validate array indices before use
- Check integer operations for overflow and underflow

### Memory Safety

- Avoid raw memory operations when possible
- Use bounds-checking containers and iterators
- Initialize all variables before use
- Use memory sanitizers in testing

### Secure Coding Patterns

- Use constant-time comparison for sensitive data like passwords
- Sanitize sensitive data in memory when no longer needed
- Don't log sensitive information
- Use secure random number generators for cryptographic purposes

Example:

```cpp
// Insecure - vulnerable to timing attacks
bool VerifyPasswordInsecure(const std::string& stored_hash, const std::string& input) {
  return stored_hash == ComputeHash(input);  // Variable-time comparison
}

// Secure - constant-time comparison
bool VerifyPasswordSecure(const std::string& stored_hash, const std::string& input) {
  const std::string computed_hash = ComputeHash(input);
  if (stored_hash.length() != computed_hash.length()) {
    return false;
  }
  
  // Constant-time comparison
  int result = 0;
  for (size_t i = 0; i < stored_hash.length(); ++i) {
    result |= stored_hash[i] ^ computed_hash[i];
  }
  return result == 0;
}
```

## Testing

### Unit Testing

- Use Google Test, Catch2, or Boost.Test for unit testing
- Test each class and function in isolation
- Mock external dependencies using Google Mock or similar
- Organize tests to mirror the structure of the source code
- Name test files with a `_test` suffix (e.g., `string_processor_test.cpp`)

Example (using Google Test):

```cpp
#include <gtest/gtest.h>
#include "string_processor.h"

namespace bayat {
namespace utils {
namespace {

TEST(StringProcessorTest, ProcessReplaceSpacesWithUnderscores) {
  StringProcessor processor;
  std::string input = "hello world";
  std::string expected = "hello_world";
  
  EXPECT_EQ(processor.Process(input), expected);
}

TEST(StringProcessorTest, ProcessEmptyString) {
  StringProcessor processor;
  std::string input = "";
  
  EXPECT_EQ(processor.Process(input), "");
}

}  // namespace
}  // namespace utils
}  // namespace bayat
```

### Integration Testing

- Test interactions between components
- Test with realistic data and environments
- Test both success and failure paths
- Use fixtures for complex test setup

### Test Coverage

- Aim for at least 80% code coverage
- Focus on testing complex logic and edge cases
- Use coverage tools like gcov/lcov or OpenCppCoverage
- Include coverage reports in CI pipelines

## Documentation

### Code Documentation

- Use Doxygen-style comments for classes, functions, and methods
- Document parameters, return values, exceptions, and side effects
- Include usage examples for complex interfaces
- Keep documentation close to the code (in header files)

Example:

```cpp
/**
 * @brief Processes a string according to defined rules.
 *
 * This function takes an input string and processes it by replacing
 * spaces with underscores and performing other transformations.
 *
 * @param input The string to process
 * @return The processed string
 * @throws std::invalid_argument If the input string is invalid
 *
 * @note This function is not thread-safe
 *
 * @code
 * StringProcessor processor;
 * std::string result = processor.Process("Hello World");
 * // result is now "Hello_World"
 * @endcode
 */
std::string Process(const std::string& input);
```

### API Documentation

- Provide comprehensive documentation for public APIs
- Include getting started guides and tutorials
- Document versioning and compatibility guarantees
- Use clear examples for common use cases
- Document performance characteristics and thread safety

### Project Documentation

- Maintain a README.md with project overview
- Include build instructions
- Document dependencies and system requirements
- Provide contribution guidelines
- Include license information

## Tools and IDE Configuration

### Recommended Tools

- Compiler: GCC, Clang, or MSVC
- Build System: CMake
- Package Manager: Conan or vcpkg
- Code Formatter: clang-format
- Static Analyzer: clang-tidy, Cppcheck
- Dynamic Analysis: Valgrind, AddressSanitizer
- Documentation: Doxygen
- Unit Testing: Google Test, Catch2
- CI/CD: GitHub Actions, GitLab CI, Jenkins

### IDE Configuration

#### Visual Studio Code

Recommended extensions:

- C/C++ (Microsoft)
- CMake Tools
- CMake
- CodeLLDB
- clangd
- C++ TestMate

Settings (settings.json):

```json
{
  "C_Cpp.clang_format_fallbackStyle": "Google",
  "C_Cpp.clang_format_style": "file",
  "C_Cpp.default.cppStandard": "c++17",
  "C_Cpp.formatting": "clangFormat",
  "editor.formatOnSave": true,
  "cmake.configureOnOpen": true,
  "cmake.buildDirectory": "${workspaceFolder}/build"
}
```

#### Visual Studio

- Enable C++17 features
- Use clang-format for formatting
- Enable static analysis
- Configure /W4 warning level

#### CLion

- Enable clang-format
- Configure CMake integration
- Enable Clang-Tidy integration
- Use Google style as base formatting style

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 2025-03-20 | Initial version |
