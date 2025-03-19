<!--
Document: Dart Development Standards
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Dart Development Standards

This document outlines the standards and best practices for Dart development at Bayat.

## Code Style and Formatting

### General Guidelines
- Follow the official [Dart Style Guide](https://dart.dev/guides/language/effective-dart/style)
- Use `dart format` or the Flutter/Dart IDE formatter with default settings
- Maximum line length should be 80 characters
- Use 2 spaces for indentation, not tabs
- Files should be encoded in UTF-8
- Files should end with a newline

### Naming Conventions
1. **Classes, Enums, Typedefs, and Extensions**:
   - Use UpperCamelCase (e.g., `HttpRequest`, `UserRepository`)
   - Be descriptive and avoid abbreviations
   - For extensions, name them based on what they add or the type they extend (e.g., `StringExtension`)

2. **Libraries, Packages, Directories, and Source Files**:
   - Use lowercase_with_underscores (e.g., `dart_style`, `user_repository.dart`)
   - Make file names match the primary class or functionality they contain
   - Prefix library names with the package name for public libraries

3. **Variables, Constants, and Parameters**:
   - Use lowerCamelCase for variables and parameters (e.g., `itemCount`, `userName`)
   - Use descriptive names that reflect the purpose
   - For boolean variables, consider using prefixes like `is`, `has`, or `should` (e.g., `isEnabled`)

4. **Private Members**:
   - Use a leading underscore for private members (e.g., `_privateField`, `_privateMethod()`)
   - Follow the same casing conventions otherwise (lowerCamelCase)

5. **Constants**:
   - Use lowerCamelCase for constant variables (e.g., `const pi = 3.14`)
   - Static and top-level constants follow the same naming convention

### Code Organization
1. **File Structure**:
   - One primary class, enum, or mixin per file
   - Group related functionality in the same directory
   - Follow the standard Dart project structure:
     ```
     lib/                 # Main package code
       src/               # Implementation code
       [module_name]/     # Feature-specific modules
     test/                # Test files
     bin/                 # Executable files
     ```

2. **Import Directives Order**:
   - Dart SDK imports first
   - Package imports next
   - Relative imports last
   - Within each group, sort imports alphabetically
   - Add a blank line between each import group
   - Example:
     ```dart
     import 'dart:async';
     import 'dart:math';
     
     import 'package:flutter/material.dart';
     import 'package:provider/provider.dart';
     
     import '../models/user.dart';
     import 'utils.dart';
     ```

## Documentation

1. **Code Comments**:
   - Use `///` for documentation comments (dartdoc)
   - Use `//` for implementation comments
   - Write comments in complete sentences with proper grammar
   - Document all public APIs

2. **Class and Member Documentation**:
   - Document the purpose of all public classes, methods, and properties
   - Specify parameter types, return values, and thrown exceptions
   - Use Markdown syntax within documentation comments
   - Example:
     ```dart
     /// Returns a [User] object with the given ID.
     ///
     /// Throws a [NotFoundException] if the user is not found.
     /// 
     /// Parameters:
     /// - [id] The unique identifier for the user
     User getUserById(String id) { ... }
     ```

## Null Safety

1. **Type Safety**:
   - All new code should use sound null safety
   - Minimize the use of nullable types (`Type?`)
   - Use late variables only when initialization is guaranteed

2. **Handling Null Values**:
   - Use the null-aware operators (`?.`, `??`, `??=`, `!`) appropriately
   - Avoid using the `!` operator when possible
   - Consider using `if (value != null)` checks over the `!` operator for clarity

## Error Handling

1. **Exceptions**:
   - Define custom exception classes for specific error cases
   - Use `try/catch` blocks for exceptional conditions, not for control flow
   - Propagate exceptions to appropriate layers
   - Avoid catching general `Exception` types; catch specific exceptions

2. **Async Code**:
   - Always handle errors in async code either with try/catch or `.catchError()`
   - Ensure `Future` chains have proper error handling
   - Consider using `async`/`await` for improved readability

## State Management

1. **Recommended Approaches**:
   - For Flutter applications:
     - Use Provider, Riverpod, Bloc/Cubit, or Redux depending on project complexity
     - Use StatefulWidget when the state is local to a single widget
     - Document the state management approach in project README

2. **Best Practices**:
   - Separate business logic from UI code
   - Keep state immutable when possible
   - Minimize the scope of state

## Testing

1. **Unit Tests**:
   - Aim for high test coverage of business logic
   - Use the `test` package for Dart code and `flutter_test` for Flutter code
   - Structure tests using `group` and `test` functions
   - Use descriptive test names that describe the behavior being tested

2. **Mock Objects**:
   - Use the `mockito` package or `mocktail` for mocks
   - Create mock classes for external dependencies

3. **Widget Tests (for Flutter)**:
   - Test widget rendering and behavior
   - Test user interactions

4. **Integration Tests**:
   - Implement integration tests for critical user flows
   - Use `integration_test` package for Flutter applications

## Performance Optimization

1. **General Guidelines**:
   - Avoid expensive operations in the UI thread
   - Use asynchronous operations for potentially long-running tasks
   - Optimize list rendering by using appropriate widgets (e.g., ListView.builder)
   - Minimize rebuilds by using const constructors where appropriate

2. **Memory Management**:
   - Close streams when they're no longer needed
   - Dispose controllers and other resources in the `dispose` method
   - Be careful of memory leaks due to closures that capture objects

3. **Measurement and Profiling**:
   - Use the Dart DevTools for profiling and debugging
   - Establish performance benchmarks for critical code paths
   - Measure performance changes when optimizing code

## Packages and Dependencies

1. **Dependency Management**:
   - Specify version constraints in pubspec.yaml
   - Prefer using caret syntax (`^`) for version constraints
   - Document the purpose of all dependencies
   - Keep dependencies up to date

2. **Package Selection**:
   - Prefer established packages with good documentation and support
   - Evaluate package quality, maintenance, and community support
   - Consider licensing and compatibility
   - Balance functionality with package size

## Security

1. **Data Security**:
   - Use secure storage solutions for sensitive data (e.g., `flutter_secure_storage`)
   - Never hard-code sensitive information such as API keys
   - Use environment-specific configurations for different environments

2. **Code Security**:
   - Validate all user inputs
   - Sanitize data from external sources
   - Use HTTPS for network communications
   - Implement proper authentication and authorization

## Internationalization and Accessibility

1. **Internationalization (i18n)**:
   - Use the `intl` package for internationalization
   - Externalize user-facing strings
   - Support right-to-left (RTL) layouts

2. **Accessibility**:
   - Ensure proper contrast ratios for text
   - Provide appropriate semantic labels for UI elements
   - Support screen readers with semantic labels
   - Test with accessibility tools

## Version Control

1. **Commit Guidelines**:
   - Follow the project's commit message format
   - Make atomic commits that represent a logical change
   - Verify that the code compiles and tests pass before committing

2. **Pull Requests**:
   - Include descriptive titles and descriptions
   - Reference related issues in descriptions
   - Keep PRs focused on a single issue or feature

## CI/CD Integration

1. **Recommended Practices**:
   - Run static analysis (`dart analyze`) in CI
   - Execute all tests in CI
   - Automate build and deployment processes
   - Use code coverage tools to maintain or improve test coverage 