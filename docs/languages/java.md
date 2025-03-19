<!--
Document: Java Development Standards
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Java Development Standards

This document outlines the standards and best practices for Java development at Bayat.

## Code Style and Formatting

### General Guidelines
- Follow the [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html) with specific Bayat modifications noted in this document
- Use 4 spaces for indentation, not tabs
- Maximum line length should be 100 characters
- Files should be encoded in UTF-8
- Files should end with a newline

### Naming Conventions
1. **Classes and Interfaces**:
   - Use PascalCase (e.g., `OrderProcessor`, `CustomerRepository`)
   - Classes should be nouns
   - Interfaces should be adjectives or nouns
   - Generic types should use single uppercase letters (e.g., `T`, `E`, `K`, `V`)

2. **Methods**:
   - Use camelCase (e.g., `processOrder()`, `findCustomerById()`)
   - Methods should be verbs or verb phrases
   - Test methods should be named descriptively (e.g., `shouldThrowExceptionWhenInvalidInput()`)

3. **Variables**:
   - Use camelCase (e.g., `orderCount`, `customerName`)
   - Constants should be UPPER_SNAKE_CASE (e.g., `MAX_RETRY_COUNT`)
   - Boolean variables should use "is", "has", "can" prefixes (e.g., `isValid`, `hasPermission`)

4. **Packages**:
   - Use lowercase, with hierarchical naming (e.g., `io.bayat.module.submodule`)
   - Avoid underscores or other special characters

### Code Organization
1. **Class Structure**:
   - Order of elements: static fields, instance fields, constructors, methods
   - Public methods before protected and private methods
   - Group related methods together
   - Maximum class size should be 2000 lines (prefer smaller)
   - Maximum method size should be 75 lines (prefer smaller)

2. **Package Structure**:
   - `io.bayat.project.feature` as the base package pattern
   - Feature packages should be organized by domain concepts
   - Utility classes in a `util` package
   - Constants in a `constants` package
   - Exceptions in an `exception` package

## Language Features and Patterns

### Java Version
- Default to Java 17 LTS for new projects
- Consider Java 21 (or latest LTS) for projects specifically needing newer features
- Maintain backward compatibility as required by the project

### Recommended Features
1. **Java 8+ Features**:
   - Prefer lambda expressions for functional interfaces
   - Use Stream API for collection operations where appropriate
   - Use Optional to represent absent values (not for performance-critical code)
   - Use method references instead of lambdas where possible
   - Utilize default methods in interfaces when applicable

2. **Java 9+ Features**:
   - Use the module system for large applications
   - Utilize factory methods for collections (`List.of()`, `Map.of()`, etc.)
   - Use try-with-resources for all AutoCloseable resources

3. **Java 10+ Features**:
   - Use `var` for local variables when the type is obvious
   - Avoid `var` when it reduces readability or type clarity

4. **Java 14+ Features**:
   - Use pattern matching for instanceof where applicable
   - Use records for simple data carriers
   - Use switch expressions for multi-way conditionals

### Discouraged Practices
- Avoid raw types (use generics)
- Minimize use of checked exceptions for control flow
- Avoid unnecessary object creation
- Don't use `null` to represent optional values or absence
- Avoid finalizers and object.finalize()
- Avoid excessive inheritance hierarchies (prefer composition)
- Don't use `public` fields (use accessor methods)

## Common Design Patterns

### Recommended Patterns
1. **Creational Patterns**:
   - Builder Pattern for complex object construction
   - Factory Method for object creation logic
   - Dependency Injection for service components

2. **Structural Patterns**:
   - Adapter for interface compatibility
   - Decorator for adding behavior dynamically
   - Composite for tree structures

3. **Behavioral Patterns**:
   - Strategy for encapsulating algorithms
   - Observer for event handling
   - Command for action encapsulation

### Dependency Injection
- Use constructor injection as the primary DI approach
- Field injection should be avoided except in tests
- Use Spring Framework annotations consistently

## Error Handling

### Exception Usage
1. **Exception Types**:
   - Use unchecked exceptions (runtime) for programming errors
   - Use checked exceptions only when the caller should handle the exception
   - Create custom exception hierarchies for the application domain

2. **Exception Handling**:
   - Always include a cause when wrapping exceptions
   - Use specific catch blocks before general ones
   - Log exceptions appropriately before handling/rethrowing
   - Clean up resources in finally blocks or try-with-resources

3. **Logging**:
   - Use SLF4J API for logging
   - Include context information in log messages
   - Use appropriate log levels (ERROR, WARN, INFO, DEBUG, TRACE)
   - Don't log sensitive information

## Concurrency

### Thread Safety
1. **Immutability**:
   - Make classes immutable when possible
   - Use final fields for immutable objects
   - Ensure proper visibility with volatile or atomic variables

2. **Synchronization**:
   - Prefer higher-level concurrency utilities over `synchronized` keyword
   - Use `java.util.concurrent` package classes
   - Avoid blocking operations in critical sections
   - Document thread-safety characteristics

3. **Executors and Thread Pools**:
   - Use ExecutorService instead of raw threads
   - Size thread pools appropriately for the workload
   - Shut down executors properly
   - Handle rejected executions gracefully

## Testing

### Unit Testing
1. **Testing Framework**:
   - Use JUnit 5 for unit tests
   - Use Mockito for mocking dependencies
   - Use AssertJ for fluent assertions

2. **Test Structure**:
   - Follow the AAA pattern (Arrange, Act, Assert)
   - One concept per test
   - Use descriptive test names
   - Aim for test independence

3. **Coverage Requirements**:
   - Minimum 80% code coverage for business logic
   - Test both positive and negative cases
   - Test boundary conditions
   - Test exception paths

### Integration Testing
- Use Spring Boot Test for integration tests
- Use TestContainers for external dependencies
- Clean up test resources after tests
- Avoid testing the same logic in both unit and integration tests

## Documentation

### Code Documentation
1. **Javadoc**:
   - All public APIs must have Javadoc comments
   - Document parameters, returns, exceptions thrown
   - Include example usage when appropriate
   - Keep comments updated when code changes

2. **Comments**:
   - Comment complex algorithms and business logic
   - Avoid obvious comments that repeat the code
   - Use TODO comments for future improvements (with ticket reference)
   - Document API contracts and invariants

## Build and Dependency Management

### Maven Configuration
1. **Project Structure**:
   - Follow standard Maven directory structure
   - Use Maven wrapper for consistent builds
   - Organize multi-module projects appropriately

2. **Dependency Management**:
   - Use Maven BOM (Bill of Materials) for version management
   - Specify dependency versions explicitly
   - Minimize transitive dependencies
   - Use appropriate dependency scopes

3. **Build Configuration**:
   - Configure compilation for appropriate Java version
   - Use standardized plugins for common tasks
   - Externalize configuration from pom.xml where appropriate

### Gradle Configuration
- Use Gradle Kotlin DSL for build scripts
- Follow conventions for directory structure
- Use version catalogs for dependency management
- Apply appropriate Gradle plugins for quality checks

## Frameworks and Libraries

### Spring Framework
1. **Spring Boot**:
   - Use Spring Boot for new applications
   - Follow Spring Boot conventions and defaults
   - Use Spring Initializr for project setup
   - Use starter dependencies when available

2. **Spring Components**:
   - Use appropriate stereotypes (@Component, @Service, @Repository)
   - Favor constructor injection
   - Use Spring profiles for environment-specific configuration
   - Externalize configuration using @ConfigurationProperties

### Persistence
1. **JPA/Hibernate**:
   - Follow JPA entity design best practices
   - Use appropriate fetch strategies
   - Map relationships correctly
   - Use query methods or JPQL for simple queries

2. **Spring Data**:
   - Use Spring Data repositories
   - Apply appropriate query methods
   - Use specifications for complex queries
   - Configure auditing for entity tracking

## Code Quality

### Static Analysis
1. **Tools**:
   - Use SonarQube for code quality analysis
   - Configure SpotBugs for bug detection
   - Use Checkstyle for style enforcement
   - Apply PMD for common programming flaws detection

2. **Quality Gates**:
   - No critical or blocker issues
   - Maintain or improve technical debt ratio
   - Maintain minimum test coverage
   - Code duplication under 5%

### Performance
1. **Optimization**:
   - Optimize only after profiling
   - Consider memory usage and garbage collection
   - Use appropriate collection implementations
   - Cache expensive computations

2. **Benchmarking**:
   - Use JMH for micro-benchmarks
   - Document performance characteristics
   - Test with realistic data volumes
   - Consider performance during code reviews

## References
- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- [Effective Java by Joshua Bloch](https://www.oreilly.com/library/view/effective-java-3rd/9780134686097/)
- [Spring Framework Documentation](https://docs.spring.io/spring-framework/reference/index.html)
- [Oracle Java Coding Guidelines](https://www.oracle.com/java/technologies/javase/codeconventions-contents.html) 