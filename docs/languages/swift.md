<!--
Document: Swift Development Standards
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Swift Development Standards

This document outlines the standards and best practices for Swift development at Bayat.

## Code Style and Formatting

### General Guidelines
- Follow the [Swift API Design Guidelines](https://swift.org/documentation/api-design-guidelines/)
- Use SwiftLint to enforce consistent style
- Maximum line length should be 120 characters
- Use 4 spaces for indentation, not tabs
- Files should be encoded in UTF-8
- Files should end with a newline
- Avoid trailing whitespace

### Naming Conventions
1. **General Naming**:
   - Use clear, descriptive names that communicate purpose
   - Favor clarity over brevity
   - Avoid abbreviations and acronyms unless widely known
   - Use camelCase for all names (except for type names)

2. **Types and Protocols**:
   - Use PascalCase for type names (classes, structures, enumerations, and protocols)
   - Name protocols to describe capabilities or behaviors (e.g., `Equatable`, `Codable`)
   - Name types as nouns

3. **Methods and Functions**:
   - Use verbs for methods and functions that perform actions
   - Name mutating methods using imperative verb phrases (e.g., `sort()`, `append()`)
   - Name non-mutating counterparts using past participles (e.g., `sorted()`, `appended()`)

4. **Variables and Properties**:
   - Use nouns for properties and variables
   - Use `is` prefix for Boolean properties (e.g., `isEnabled`, `isValid`)
   - Name computed properties to express what they compute, not how

5. **Enumerations**:
   - Use singular names for enumeration types
   - Use lowerCamelCase for enumeration cases
   - Consider omitting type name from case when context is clear

### File Organization
1. **File Structure**:
   - One type per file unless types are closely related
   - Name files after their main type (e.g., `UserManager.swift`)
   - Group related types together in the file system
   - Place extensions in the same file as the type they extend if small

2. **Code Organization within a File**:
   - Follow a consistent order of section declarations:
     1. Type declaration
     2. Properties
     3. Initializers
     4. Public methods
     5. Private methods
     6. Protocol conformances
   - Use `// MARK:` comments to organize code sections
   - Group related methods and properties together

## Language Features and Idioms

### Optionals
1. **Optional Handling**:
   - Avoid forced unwrapping (`!`) in production code
   - Use optional binding (`if let`, `guard let`) to unwrap optionals
   - Use optional chaining (`?.`) when appropriate
   - Use `nil` coalescing operator (`??`) for default values

2. **Implicitly Unwrapped Optionals**:
   - Use sparingly, primarily for IBOutlets or properties initialized in `viewDidLoad`
   - Document why a property is implicitly unwrapped
   - Consider refactoring to avoid implicitly unwrapped optionals

### Access Control
1. **Visibility Modifiers**:
   - Use appropriate access control modifiers (`public`, `internal`, `fileprivate`, `private`)
   - Favor minimal accessibility; start with `private` and increase visibility as needed
   - Document public API thoroughly
   - Mark classes as `final` unless designed for inheritance

2. **Access Control for Extensions**:
   - Use consistent access level for extension methods as their types
   - Use `fileprivate` for utility methods used only within the file

### Type Safety
1. **Strong Typing**:
   - Leverage Swift's type system for safety
   - Use enumerations for states and options
   - Avoid stringly-typed code
   - Use custom types to clarify intent (e.g., `typealias` or struct wrappers)

2. **Type Inference**:
   - Let the compiler infer types when clear from context
   - Include explicit types for public API and complex expressions
   - Use type annotations for empty collections and ambiguous types

### Memory Management
1. **ARC and Retain Cycles**:
   - Be aware of potential retain cycles
   - Use weak and unowned references appropriately
   - Document closures that capture `self` strongly
   - Avoid memory leaks by properly breaking retain cycles

2. **Value vs. Reference Types**:
   - Prefer structs over classes when possible
   - Use classes when identity or inheritance is required
   - Be aware of copy semantics for value types
   - Document performance implications for large value types

### Error Handling
1. **Error Types**:
   - Define domain-specific error types (typically enumerations)
   - Conform to `Error` protocol
   - Provide meaningful error messages
   - Use appropriate error cases for different failure modes

2. **Error Propagation**:
   - Use `throws` and `rethrows` appropriately
   - Use `do-catch` blocks to handle errors
   - Avoid silently ignoring errors
   - Provide context when converting errors between domains

3. **Result Type**:
   - Use `Result<Success, Failure>` for asynchronous operations
   - Provide clear success and error types
   - Handle both success and failure cases
   - Use `Result` for operations that can fail even when using callbacks

### Concurrency
1. **Async/Await**:
   - Use Swift's structured concurrency model when available
   - Properly mark `async` functions and methods
   - Use `Task` for launching async work
   - Handle cancellation appropriately

2. **Dispatch Queues**:
   - Use appropriate queues for appropriate work (main queue for UI, background queues for processing)
   - Be explicit about which queue work is performed on
   - Avoid thread contention and deadlocks
   - Consider thread safety for shared resources

3. **Actor Model**:
   - Use actors to manage shared mutable state
   - Respect actor isolation boundaries
   - Be aware of potential deadlocks when actors call other actors
   - Document actor usage patterns

## Architectural Patterns

### MVVM (Model-View-ViewModel)
1. **Components**:
   - **Model**: Domain data and business logic
   - **View**: UI elements and layout (UIViewController, UIView, SwiftUI View)
   - **ViewModel**: Transforms model data for display and handles view logic

2. **Best Practices**:
   - Keep views simple and focused on UI concerns
   - Make view models testable with clear inputs and outputs
   - Use data binding (Combine, RxSwift, or closures) to connect view and view model
   - Keep models independent of UI concerns

### Other Patterns
1. **Coordinator Pattern**:
   - Use coordinators for navigation logic
   - Decouple view controllers from each other
   - Handle deep linking and complex flows using coordinators
   - Document the responsibility of each coordinator

2. **Dependency Injection**:
   - Use constructor injection for required dependencies
   - Consider property injection for optional dependencies
   - Use dependency containers for complex dependency graphs
   - Test with mock dependencies

## SwiftUI

### View Structure
1. **View Composition**:
   - Break complex views into smaller, reusable components
   - Use `ViewModifier` for reusable view modifications
   - Leverage `@ViewBuilder` for dynamic view construction
   - Keep view bodies readable and focused

2. **State Management**:
   - Use appropriate property wrappers (`@State`, `@Binding`, `@ObservedObject`, `@EnvironmentObject`)
   - Minimize state duplication
   - Prefer value semantics for view models with `@ObservableObject`
   - Document state dependencies

### SwiftUI and UIKit Integration
1. **Bridging**:
   - Use `UIViewRepresentable` and `UIViewControllerRepresentable` appropriately
   - Keep representable wrappers thin
   - Handle updates and coordination properly
   - Document UIKit dependencies

## Testing

### Unit Testing
1. **Test Coverage**:
   - Aim for high test coverage for business logic
   - Test edge cases and error conditions
   - Keep tests independent from each other
   - Follow AAA pattern (Arrange, Act, Assert)

2. **Mocking and Stubbing**:
   - Use protocols for easier mocking
   - Create test-specific implementations for dependencies
   - Consider using a mocking framework for complex cases
   - Document mock behaviors

3. **Test Organization**:
   - Name tests clearly to describe what they test
   - Group related tests together
   - Use descriptive assertions
   - Test both success and failure paths

### UI Testing
1. **XCTest UI Testing**:
   - Make UI elements accessible for testing
   - Create screen abstractions (Page Objects)
   - Make tests robust against minor UI changes
   - Test key user flows

2. **Snapshot Testing**:
   - Use snapshot tests for UI verification
   - Be aware of platform differences in rendering
   - Document snapshot test requirements
   - Update snapshots when UI intentionally changes

## Performance

### Optimization
1. **General Principles**:
   - Measure before optimizing
   - Use Instruments for profiling
   - Focus on hot paths and user-visible performance
   - Document performance implications

2. **Common Optimizations**:
   - Reduce memory allocations
   - Minimize work on the main thread
   - Batch UI updates
   - Use appropriate data structures for operations

## Dependency Management

### Swift Package Manager
1. **Package Structure**:
   - Organize code into modules with clear dependencies
   - Document module boundaries and responsibilities
   - Version packages according to semantic versioning
   - Specify version constraints appropriately

2. **Dependency Selection**:
   - Evaluate dependencies for maintenance and compatibility
   - Consider license implications
   - Prefer well-maintained, actively developed packages
   - Document rationale for external dependencies

### Alternative Solutions
1. **CocoaPods**:
   - Maintain an up-to-date Podfile
   - Pin versions for stability
   - Document pod-specific setup requirements
   - Keep pods updated regularly

2. **Carthage**:
   - Use Carthage for frameworks not available via SPM
   - Document build requirements
   - Include Carthage bootstrapping in documentation

## Documentation

### Code Documentation
1. **Comments and Documentation**:
   - Use documentation comments (`///`) for public API
   - Document parameters, return values, and thrown errors
   - Include examples for complex functionality
   - Keep documentation up to date with code changes

2. **README and Project Documentation**:
   - Maintain clear setup instructions
   - Document architectural decisions
   - Include visual diagrams for complex systems
   - Document build and deployment processes

## Resources
- [Swift API Design Guidelines](https://swift.org/documentation/api-design-guidelines/)
- [Swift.org Documentation](https://swift.org/documentation/)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [SwiftLint](https://github.com/realm/SwiftLint)
- [Swift Style Guide](https://google.github.io/swift/)

## Appendix: SwiftLint Configuration

```yaml
disabled_rules:
  # Customize based on project needs
  - line_length
  - trailing_whitespace
  - todo

opt_in_rules:
  - empty_count
  - explicit_init
  - closure_spacing
  - overridden_super_call
  - redundant_nil_coalescing
  - private_outlet
  - nimble_operator
  - attributes
  - operator_usage_whitespace
  - closure_end_indentation
  - first_where
  - sorted_imports
  - object_literal
  - number_separator
  - prohibited_super_call
  - fatal_error_message

included:
  - Sources
  - Tests

excluded:
  - Carthage
  - Pods
  - vendor

line_length:
  warning: 120
  error: 200
  ignores_comments: true
  ignores_urls: true

file_length:
  warning: 400
  error: 1000

type_name:
  min_length: 3
  max_length: 50

identifier_name:
  min_length: 2
  max_length: 50
  excluded:
    - id
    - URL
    - x
    - y

reporter: "xcode"
``` 