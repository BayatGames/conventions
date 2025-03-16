# Kotlin Development Standards

This document outlines the standards and best practices for Kotlin development at Bayat.

## Code Style and Formatting

### General Guidelines
- Follow the [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- Use ktlint or detekt for automated style enforcement
- Maximum line length should be 120 characters
- Use 4 spaces for indentation, not tabs
- Files should be encoded in UTF-8
- Files should end with a newline
- Use trailing commas in multi-line declarations

### Naming Conventions
1. **Classes and Interfaces**:
   - Use PascalCase for class names (e.g., `UserRepository`, `PaymentService`)
   - Name classes as nouns or noun phrases
   - Use adjectives for interfaces that define behavior (e.g., `Sortable`, `Pageable`)

2. **Functions and Properties**:
   - Use camelCase for function and property names (e.g., `getUserById()`, `isActive`)
   - Name functions as verbs or verb phrases
   - Use `is`, `has`, or `should` prefixes for Boolean properties
   - Name top-level constants using SCREAMING_SNAKE_CASE

3. **Parameters and Local Variables**:
   - Use camelCase for parameters and local variables
   - Avoid single-letter names except for obvious cases (e.g., loop indices)
   - Prefer descriptive names that convey purpose

4. **Packages**:
   - Use lowercase package names
   - Use the reverse domain name pattern (e.g., `io.bayat.module.feature`)
   - Keep package names concise
   - Group related classes in the same package

5. **Companion Objects**:
   - Use descriptive names for companion objects when they have a specific purpose
   - Default companion objects should not have a name

### Code Organization
1. **File Structure**:
   - Prefer one class per file
   - Name the file after the primary class or interface it contains
   - Extensions to an existing class should be in a separate file with a descriptive name
   - Group related extension functions in the same file

2. **Class Structure**:
   - Order class contents in a logical manner:
     1. Properties
     2. Initializers
     3. Public methods
     4. Internal methods
     5. Private methods
     6. Companion object
     7. Nested/inner classes
   - Use `//region` and `//endregion` comments for logical grouping if needed

3. **Package Structure**:
   - Organize packages by feature, not by type
   - Keep a clear separation between public API and internal implementation
   - Use `internal` visibility modifier appropriately
   - Group related functionality within packages

## Language Features and Idioms

### Kotlin-Specific Features
1. **Null Safety**:
   - Avoid using `!!` operator unless absolutely necessary
   - Use nullable types (`T?`) only when a value can legitimately be null
   - Prefer `?.` (safe call) and `?:` (elvis) operators for null handling
   - Consider using `requireNotNull()` or `checkNotNull()` for mandatory parameters

2. **Extensions**:
   - Use extension functions to extend functionality of existing classes
   - Prefer extension functions over utility classes
   - Keep extensions focused and single-purpose
   - Document extensions that might not be obvious

3. **Scope Functions**:
   - Use `let` for executing code blocks on non-null objects
   - Use `apply` for object configuration
   - Use `run` when you need both the receiver and a result value
   - Use `also` for side effects outside the object configuration
   - Use `with` when working with an object multiple times

4. **Smart Casts**:
   - Leverage type checking with `is` operator for smart casts
   - Use `as?` for safe casts that might fail
   - Avoid unnecessary type checking when the compiler can infer the type

5. **Collections**:
   - Prefer immutable collections (`listOf`, `setOf`, `mapOf`) when contents won't change
   - Use mutable collections (`mutableListOf`, etc.) only when necessary
   - Leverage collection functions like `map`, `filter`, `reduce` for transformations
   - Use sequences for large collections to improve performance

### Functional Programming
1. **Higher-Order Functions**:
   - Use higher-order functions for code reuse
   - Keep lambdas concise and readable
   - Use function references (`::functionName`) instead of lambdas for simple cases
   - Document complex higher-order functions

2. **Lambda Syntax**:
   - Use trailing lambda syntax when the lambda is the last parameter
   - Use multi-line lambda syntax for complex lambdas
   - Use named parameters for clarity when needed
   - Move complex lambdas to separate functions when they become unwieldy

3. **Immutability**:
   - Prefer `val` over `var` whenever possible
   - Use immutable data structures by default
   - Make classes immutable when appropriate
   - Use data classes for simple data containers

### Coroutines
1. **Structured Concurrency**:
   - Follow structured concurrency principles
   - Use appropriate coroutine scope for the context
   - Always handle exceptions in coroutines
   - Use `supervisorScope` when children should fail independently

2. **Dispatchers**:
   - Choose the appropriate dispatcher for the task (IO, Default, Main)
   - Document dispatcher requirements for suspending functions
   - Be mindful of thread confinement, especially for UI operations
   - Don't block the Main dispatcher with long-running operations

3. **Flow**:
   - Use Flow for asynchronous data streams
   - Collect flows in the appropriate coroutine scope
   - Use cold flows for most use cases
   - Be mindful of flow backpressure for large data streams

4. **Error Handling**:
   - Use `try-catch` blocks within coroutines
   - Consider using `CoroutineExceptionHandler` for top-level error handling
   - Document how errors are propagated in suspending functions
   - Avoid swallowing exceptions without proper handling

## Architecture and Design Patterns

### Clean Architecture
1. **Layer Separation**:
   - Separate code into distinct layers (presentation, domain, data)
   - Define clear boundaries between layers
   - Use dependency inversion to maintain layer independence
   - Avoid leaking implementation details across layer boundaries

2. **Domain Layer**:
   - Keep business logic in the domain layer
   - Use entities to represent core business objects
   - Define use cases for business operations
   - Keep domain layer independent of framework specifics

3. **Data Layer**:
   - Implement repository interfaces from the domain layer
   - Handle data sources and transformations
   - Use data models specific to the data layer
   - Map between data models and domain entities

4. **Presentation Layer**:
   - Use MVVM or MVI pattern for UI logic
   - Keep ViewModels focused on presentation logic
   - Use LiveData or StateFlow for observable UI state
   - Handle UI events appropriately

### Dependency Injection
1. **General Principles**:
   - Use constructor injection as the primary method
   - Define clear module boundaries
   - Document dependencies and their lifecycles
   - Use appropriate scoping for dependencies

2. **Frameworks**:
   - Use Dagger Hilt for Android applications
   - Use Koin for simpler projects or non-Android Kotlin applications
   - Follow framework-specific best practices
   - Configure DI in a centralized location

## Testing

### Unit Testing
1. **Testing Framework**:
   - Use JUnit 5 for unit tests
   - Use MockK for mocking
   - Use appropriate assertion libraries (e.g., AssertJ, Truth)
   - Follow the AAA pattern (Arrange, Act, Assert)

2. **Test Organization**:
   - Name tests descriptively
   - Group related tests together
   - Use nested tests for complex test scenarios
   - Keep tests independent of each other

3. **Mocking**:
   - Mock dependencies, not the system under test
   - Use relaxed mocks when appropriate
   - Verify critical interactions
   - Use spies judiciously

### Coroutine Testing
1. **Test Dispatchers**:
   - Use `TestCoroutineDispatcher` for controlling coroutine execution
   - Set the main dispatcher to a test dispatcher during tests
   - Use `runBlockingTest` for testing suspending functions
   - Be aware of test timeouts when testing coroutines

2. **Flow Testing**:
   - Use `Flow.test()` extension function for testing flows
   - Verify emissions and their order
   - Test error cases and completion
   - Use `TestCoroutineScheduler` for time-based operators

## Documentation

### Code Documentation
1. **KDoc**:
   - Document all public APIs with KDoc comments
   - Document non-obvious behavior
   - Include examples for complex functionality
   - Document limitations and edge cases

2. **Class and Function Documentation**:
   - Describe the purpose and responsibility of each class
   - Document parameters, return values, and exceptions
   - Document thread safety considerations
   - Keep documentation up-to-date with code changes

3. **Code Comments**:
   - Use comments to explain "why", not "what"
   - Comment complex algorithms or business rules
   - Avoid redundant comments that just repeat the code
   - Use TODO comments for future improvements with tracking information

## Android-Specific Guidelines

### Jetpack Components
1. **Architecture Components**:
   - Use ViewModel for UI-related data handling
   - Use LiveData or StateFlow for observable data
   - Use Room for database operations
   - Use Navigation component for app navigation

2. **Compose**:
   - Follow Compose best practices
   - Keep composables small and focused
   - Use appropriate state management techniques
   - Extract reusable composables

3. **Work Manager**:
   - Use WorkManager for background tasks
   - Define clear work constraints
   - Handle work failures gracefully
   - Document work requirements

### Resource Management
1. **Resource Organization**:
   - Follow Android resource naming conventions
   - Organize resources by type and feature
   - Use resource qualifiers appropriately
   - Extract dimensions, colors, and strings into resources

2. **Performance Considerations**:
   - Be mindful of resource usage
   - Optimize layouts for performance
   - Use appropriate view recycling patterns
   - Profile and optimize critical paths

## Build and Dependency Management

### Gradle Configuration
1. **Project Structure**:
   - Use Gradle Kotlin DSL for build scripts
   - Organize multi-module projects appropriately
   - Define dependencies in a centralized location
   - Use version catalogs for dependency management

2. **Dependency Management**:
   - Keep dependencies up to date
   - Audit dependencies for security vulnerabilities
   - Minimize transitive dependencies
   - Document dependency purpose and alternatives

## Code Quality

### Static Analysis
1. **Tools**:
   - Use ktlint for style checking
   - Use detekt for code quality analysis
   - Configure SonarQube for comprehensive analysis
   - Include static analysis in CI pipeline

2. **Quality Gates**:
   - Define clear quality thresholds
   - Enforce code quality in CI
   - Track and improve metrics over time
   - Document exceptions to rules

## References
- [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- [Kotlin Official Documentation](https://kotlinlang.org/docs/home.html)
- [Kotlin Coroutines Guide](https://kotlinlang.org/docs/coroutines-guide.html)
- [Android Kotlin Style Guide](https://developer.android.com/kotlin/style-guide) 