<!--
Document: Rust Development Standards
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Rust Development Standards

This document outlines the standards and best practices for Rust development at Bayat.

## Code Style and Formatting

### General Guidelines

- Follow Rust standard style using `rustfmt` with the default settings
- Maximum line length should be 100 characters
- Use 4 spaces for indentation, not tabs
- Files should be encoded in UTF-8
- Files should end with a newline

### Naming Conventions

1. **Types and Traits**:
   - Use PascalCase for types, traits, and enum variants (e.g., `OrderProcessor`, `Serialize`)
   - Use descriptive names that reflect the purpose or behavior
   - Prefer concise but clear names

2. **Functions and Methods**:
   - Use snake_case for functions and methods (e.g., `process_order`, `find_by_id`)
   - Use verbs for functions that perform actions
   - Use nouns for functions that return values

3. **Variables and Parameters**:
   - Use snake_case for variables and parameters (e.g., `order_count`, `user_name`)
   - Use descriptive names that reflect the purpose or meaning
   - Boolean variables should use `is_`, `has_`, or `should_` prefixes (e.g., `is_valid`)

4. **Constants and Statics**:
   - Use SCREAMING_SNAKE_CASE for constants and static variables (e.g., `MAX_CONNECTIONS`)
   - Make names descriptive of their purpose

5. **Modules**:
   - Use snake_case for module names (e.g., `order_processing`, `user_management`)
   - Avoid single-letter module names or overly generic names

### Code Organization

1. **Module Structure**:
   - Follow the Rust module system conventions
   - Use `mod.rs` or separate files based on project complexity
   - Organize code in modules by functionality or domain
   - Maintain a clean hierarchy to enable clear `use` statements

2. **File Structure**:
   - Standard order: imports, module declarations, constants, types, traits, implementations
   - Group `use` statements by crate
   - Place Rust standard library imports first, then external crates, then local imports
   - Separate import groups with a blank line

## Language Features and Idioms

### Error Handling

1. **Result and Option**:
   - Use `Result<T, E>` for operations that can fail
   - Use `Option<T>` for values that may be absent
   - Prefer using `?` operator for error propagation
   - Avoid `unwrap()` and `expect()` in production code

2. **Custom Error Types**:
   - Define domain-specific error types
   - Implement the `std::error::Error` trait for custom errors
   - Use the `thiserror` crate for deriving error implementations
   - Provide meaningful error messages

3. **Error Conversion**:
   - Implement `From` for converting between error types
   - Use the `anyhow` crate for flexible error handling in applications
   - Add context to errors using `.context()` or `.with_context()`

### Memory Management

1. **Ownership**:
   - Follow Rust's ownership model strictly
   - Prefer passing references over transferring ownership when appropriate
   - Use clear lifetimes to express relationships
   - Document lifetime requirements in function and type documentation

2. **Borrowing**:
   - Prefer immutable borrows (`&T`) over mutable borrows (`&mut T`) when possible
   - Keep mutable borrows as short and localized as possible
   - Avoid nested borrows that could lead to complex lifetime relationships

3. **Smart Pointers**:
   - Use `Box<T>` for heap allocation with single ownership
   - Use `Rc<T>` for shared ownership in single-threaded contexts
   - Use `Arc<T>` for shared ownership in multi-threaded contexts
   - Use interior mutability patterns (`RefCell`, `Mutex`, `RwLock`) judiciously

### Concurrency

1. **Thread Safety**:
   - Leverage Rust's type system to ensure thread safety
   - Use `Send` and `Sync` traits appropriately
   - Prefer message passing over shared state when possible
   - Document thread safety guarantees in public APIs

2. **Async/Await**:
   - Use `async`/`await` for asynchronous code
   - Use `tokio` or `async-std` as the async runtime
   - Avoid mixing futures from different runtimes
   - Be mindful of `!Send` futures in async code

3. **Synchronization Primitives**:
   - Use appropriate synchronization primitives (`Mutex`, `RwLock`, etc.)
   - Prefer `parking_lot` crate equivalents for better performance
   - Minimize locked sections to reduce contention
   - Be aware of potential deadlocks in lock ordering

### Generics and Traits

1. **Generic Code**:
   - Use generics to create flexible, reusable components
   - Constrain generic parameters with trait bounds
   - Use `where` clauses for complex trait bounds
   - Provide type aliases for complex generic types

2. **Trait Design**:
   - Follow the Rust trait design patterns
   - Use traits for behavior abstraction
   - Design traits around behavior, not data
   - Implement standard traits (`Debug`, `Display`, `Clone`, etc.) when appropriate

3. **Trait Objects**:
   - Use trait objects (`dyn Trait`) for runtime polymorphism
   - Be aware of the performance implications of dynamic dispatch
   - Ensure traits intended for trait objects are object-safe
   - Consider alternatives like enum dispatch when performance is critical

## Testing

### Unit Testing

1. **Test Organization**:
   - Place tests in a `#[cfg(test)]` module at the bottom of the file
   - Use nested modules to organize different test categories
   - Name test functions descriptively
   - Follow the "Arrange, Act, Assert" pattern

2. **Testing Framework**:
   - Use Rust's built-in testing framework
   - Use `#[test]` attribute for test functions
   - Use `#[should_panic]` for tests that should panic
   - Use `assert!`, `assert_eq!`, and `assert_ne!` macros

3. **Test Coverage**:
   - Aim for high test coverage of business logic
   - Test both success and failure paths
   - Test edge cases and boundary conditions
   - Use test utilities and fixtures to reduce duplication

### Integration Testing

- Place integration tests in the `tests/` directory
- Structure integration tests to test larger components
- Use test fixtures for setting up complex test scenarios
- Mock external services when necessary

### Property-Based Testing

- Use `proptest` or `quickcheck` for property-based testing
- Define properties that should hold for your functions
- Test with a wide range of inputs, including edge cases
- Shrink failing test cases to minimal counterexamples

## Performance

### Optimization

1. **General Principles**:
   - Optimize for correctness first, then performance
   - Measure before optimizing (`criterion`, `flamegraph`)
   - Consider time, memory, and binary size trade-offs
   - Document performance characteristics of critical code

2. **Memory Optimization**:
   - Be aware of data structure layouts and sizes
   - Use `#[repr(C)]` or `#[repr(packed)]` when necessary
   - Consider custom allocators for specialized needs
   - Use stack allocation over heap allocation when possible

3. **Algorithmic Optimization**:
   - Choose appropriate algorithms and data structures
   - Use iterators and iterator combinators efficiently
   - Leverage zero-cost abstractions
   - Avoid redundant allocations

### Profiling and Benchmarking

- Use `criterion` for benchmarking
- Use `perf` or `flamegraph` for profiling
- Establish baseline performance metrics
- Create regression tests for performance-critical code

## Documentation

### Code Documentation

1. **Doc Comments**:
   - Document all public items with `///` or `//!` comments
   - Include examples in documentation
   - Document panics, errors, and safety considerations
   - Keep documentation up to date with code changes

2. **Internal Comments**:
   - Use regular comments (`//`) for implementation details
   - Comment complex algorithms or non-obvious code
   - Avoid redundant comments that repeat the code
   - Use `TODO` or `FIXME` comments for future work

3. **Rustdoc**:
   - Use Markdown formatting in doc comments
   - Group related items with module-level documentation
   - Include examples that are tested by `cargo test`
   - Document unsafe code extensively

## Dependency Management

### Crate Selection

1. **Evaluation Criteria**:
   - Prefer mature, well-maintained crates
   - Check for recent updates and active maintenance
   - Evaluate documentation quality and examples
   - Consider license compatibility

2. **Versioning**:
   - Use semantic versioning for dependencies
   - Specify version requirements explicitly
   - Use caret requirements (`^1.2.3`) for most dependencies
   - Pin exact versions for critical dependencies

### Workspace Organization

- Use Cargo workspaces for multi-crate projects
- Maintain a clear dependency hierarchy
- Share common dependencies across workspace members
- Use internal crates for code organization

## Build and Release

### Cargo Configuration

1. **Project Setup**:
   - Use `cargo-edit` for dependency management
   - Configure appropriate metadata in `Cargo.toml`
   - Define features for optional functionality
   - Set up development and release profiles

2. **CI/CD Integration**:
   - Run tests on CI for multiple platforms
   - Configure linting checks (`clippy`)
   - Verify formatting with `rustfmt`
   - Set up test coverage reporting

### Release Process

- Use semantic versioning for releases
- Create release tags in version control
- Generate changelogs for each release
- Automate the release process when possible

## Code Quality

### Static Analysis

1. **Clippy**:
   - Run `clippy` regularly
   - Enable all clippy lints by default
   - Document suppressed lints with reasons
   - Update code to address clippy warnings

2. **Rustfmt**:
   - Use `rustfmt` for consistent formatting
   - Run `rustfmt` before committing
   - Use a consistent configuration in `.rustfmt.toml`
   - Automate formatting in CI

3. **Other Tools**:
   - Use `cargo-audit` for security vulnerability checking
   - Use `cargo-deny` for license compliance
   - Use `cargo-bloat` to identify binary size issues
   - Consider `cargo-udeps` for unused dependencies

### Unsafe Code

- Minimize use of unsafe code
- Document why unsafe is necessary
- Encapsulate unsafe code in safe abstractions
- Extensively test unsafe code
- Use `unsafe` blocks as small as possible

## References

- [The Rust Programming Language](https://doc.rust-lang.org/book/)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
- [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)
- [Rustonomicon](https://doc.rust-lang.org/nomicon/) (for unsafe Rust)

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 2025-03-20 | Initial version |
