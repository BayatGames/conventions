# Ruby Development Standards

This document outlines the standards and best practices for Ruby development at Bayat.

## Code Style and Formatting

### General Guidelines
- Follow the [Ruby Style Guide](https://rubystyle.guide/)
- Use RuboCop to enforce style consistency
- Maximum line length should be 100 characters
- Use 2 spaces for indentation, not tabs
- Files should be encoded in UTF-8
- Files should end with a newline
- Avoid unnecessary comments

### Naming Conventions
1. **Classes and Modules**:
   - Use PascalCase for class and module names (e.g., `OrderProcessor`, `UserAuthentication`)
   - Name classes as nouns or noun phrases
   - Use descriptive, meaningful names that reflect purpose
   - Avoid acronyms unless commonly understood

2. **Methods and Variables**:
   - Use snake_case for methods, variables, and symbols (e.g., `process_order`, `user_count`)
   - Name methods to reflect their behavior
   - Methods that return boolean values should end with a question mark (e.g., `valid?`, `active?`)
   - Methods that are potentially dangerous should end with an exclamation mark (e.g., `save!`, `delete!`)

3. **Constants**:
   - Use SCREAMING_SNAKE_CASE for constants (e.g., `MAX_LOGIN_ATTEMPTS`, `DEFAULT_TIMEOUT`)
   - Place constants at the top of the class/module definition
   - Use descriptive names that indicate purpose

4. **Predicates**:
   - Methods that return boolean values should end with a question mark
   - Name should reflect what is being asked (e.g., `empty?`, `valid?`)
   - Avoid negation in predicate names (use `present?` instead of `not_empty?`)

5. **File Names**:
   - Use snake_case for file names
   - File names should match the main class/module name they contain
   - Test files should end with `_spec.rb` or `_test.rb` depending on the testing framework

### Code Organization
1. **File Structure**:
   - One class/module per file as a general rule
   - Name the file after the primary class or module it contains
   - Group related classes in directories
   - Follow the standard Ruby project layout

2. **Class Structure**:
   - Order of declarations:
     1. Module includes
     2. Constant definitions
     3. Attribute macros (attr_*)
     4. Other macros (has_many, etc.)
     5. Class methods
     6. Constructor
     7. Instance methods
     8. Private/protected methods
   - Group related methods together
   - Keep files under 300 lines when possible
   - Keep methods under 20 lines when possible

## Language Features and Idioms

### Ruby Idioms
1. **Collections**:
   - Use Ruby's built-in enumerable methods (e.g., `map`, `select`, `reduce`)
   - Prefer functional-style collection manipulation over imperative loops
   - Use block parameters with descriptive names
   - Use `&:method_name` shorthand for simple method calls

2. **String Manipulation**:
   - Use string interpolation instead of concatenation
   - Use heredocs for multi-line strings
   - Use single quotes for strings without interpolation
   - Use double quotes for strings with interpolation or escape characters

3. **Conditionals and Control Flow**:
   - Use the ternary operator for simple conditions
   - Use `if`/`unless` modifiers for simple single-line conditions
   - Avoid nested conditionals when possible
   - Use `case` statements for multiple conditions on the same variable

4. **Method Definitions**:
   - Use keyword arguments for methods with multiple optional parameters
   - Provide default values for optional arguments
   - Use method-level rescue clauses for specific error handling
   - Use guard clauses to reduce nesting

5. **Blocks, Procs, and Lambdas**:
   - Use `{ ... }` for single-line blocks and `do ... end` for multi-line blocks
   - Use stabby lambda syntax (`->`) for creating lambdas
   - Understand the difference between procs and lambdas
   - Use block arguments for methods that yield

### Advanced Features
1. **Metaprogramming**:
   - Use metaprogramming judiciously
   - Document metaprogramming techniques thoroughly
   - Prefer simpler solutions when they provide adequate functionality
   - Be aware of the performance implications

2. **DSLs (Domain Specific Languages)**:
   - Create clear, well-documented DSLs
   - Follow consistent patterns within a DSL
   - Consider the readability for developers unfamiliar with the DSL
   - Provide helpful error messages for DSL users

3. **Module Extension and Inclusion**:
   - Use `include` for adding instance methods
   - Use `extend` for adding class methods
   - Use `prepend` when you need to override methods and call super
   - Understand the method lookup chain

## Ruby on Rails Guidelines

### General Rails Principles
1. **Convention over Configuration**:
   - Follow Rails conventions unless there's a compelling reason not to
   - Use standard directory structure
   - Follow naming conventions for models, controllers, and views
   - Use Rails generators appropriately

2. **MVC Architecture**:
   - Keep controllers skinny
   - Keep models fat but well-organized
   - Use service objects for complex business logic
   - Keep views simple and use partials for reusability

3. **Configuration**:
   - Use environment variables for sensitive configuration
   - Use Rails credentials for managing secrets
   - Use config/initializers for application configuration
   - Keep environment-specific configuration in the appropriate files

### Models
1. **ActiveRecord**:
   - Define associations at the top of the model class
   - Define validations after associations
   - Use scopes for common queries
   - Keep callback chains simple and side-effect free

2. **Validations**:
   - Validate at the model level
   - Use custom validators for complex validations
   - Include descriptive error messages
   - Test validations thoroughly

3. **Queries**:
   - Use ActiveRecord query methods over raw SQL when possible
   - Use eager loading (`includes`, `preload`, `eager_load`) to avoid N+1 queries
   - Use scopes to encapsulate common query conditions
   - Index frequently queried columns

### Controllers
1. **RESTful Design**:
   - Follow RESTful routing conventions
   - Keep controllers focused on the standard CRUD actions
   - Use nested resources appropriately
   - Use custom actions sparingly and with purpose

2. **Filters**:
   - Use before_action filters for repeated setup code
   - Keep filters focused on a single concern
   - Extract complex filter logic to methods
   - Limit filter scope with `only` and `except`

3. **Response Handling**:
   - Respond to different formats consistently
   - Use HTTP status codes appropriately
   - Set flash messages for user feedback
   - Redirect after successful POST, PUT, or DELETE requests

### Views
1. **Templates**:
   - Keep view templates simple
   - Extract partials for reusable components
   - Minimize logic in templates
   - Use helper methods for complex view logic

2. **Helpers**:
   - Create focused helper methods
   - Group related helpers together
   - Test complex helpers
   - Avoid helpers with complex logic

3. **Asset Pipeline/Webpacker**:
   - Organize JavaScript and CSS files appropriately
   - Use the asset pipeline or Webpacker as appropriate for the project
   - Minimize asset size for production
   - Follow documentation for the current Rails version

### Background Jobs
1. **Job Design**:
   - Keep jobs small and focused
   - Make jobs idempotent when possible
   - Handle errors properly
   - Set appropriate timeouts and retries

2. **Job Processing**:
   - Use Sidekiq or ActiveJob for background processing
   - Use job priority levels appropriately
   - Monitor job queues in production
   - Test job behavior and error handling

## Testing

### RSpec Guidelines
1. **Describe and Context Blocks**:
   - Use descriptive names for describe and context blocks
   - Use `describe` for methods or classes being tested
   - Use `context` for specific conditions or states
   - Nest contexts to build up complex test scenarios

2. **Examples**:
   - Write descriptive example names
   - Keep examples focused on a single assertion when possible
   - Use expectation matchers for clear assertions
   - Follow the Arrange, Act, Assert pattern

3. **Test Data**:
   - Use factories (FactoryBot) for test data creation
   - Create only the data needed for the test
   - Use traits for common variations
   - Clean up test data after tests

4. **Mocking and Stubbing**:
   - Use mocks and stubs judiciously
   - Test the real implementation when practical
   - Mock external services consistently
   - Reset mocks after tests

### Testing Practices
1. **Test Coverage**:
   - Write tests for all business logic
   - Target 90%+ test coverage for models
   - Test edge cases and error conditions
   - Use tools like SimpleCov to monitor coverage

2. **Integration Testing**:
   - Write integration tests for critical user flows
   - Use feature specs with Capybara for UI testing
   - Test API endpoints
   - Balance unit and integration tests appropriately

3. **Test Performance**:
   - Keep tests fast
   - Use profiling tools to identify slow tests
   - Use DatabaseCleaner with appropriate strategy
   - Consider using test parallelization for large test suites

## Documentation

### Code Documentation
1. **YARD/RDoc**:
   - Document public APIs using YARD or RDoc
   - Include examples in documentation
   - Document parameters, return values, and exceptions
   - Keep documentation up to date with code changes

2. **Comments**:
   - Use comments to explain "why" not "what"
   - Document complex algorithms or business rules
   - Keep comments current with code changes
   - Use TODO comments with tracking information

3. **README and Wiki**:
   - Maintain comprehensive README files
   - Document setup procedures
   - Include examples of common usage
   - Keep documentation for different audiences (developers, end users)

## Performance and Optimization

### Performance Considerations
1. **Database**:
   - Index frequently queried columns
   - Optimize complex queries
   - Use eager loading to avoid N+1 queries
   - Paginate large result sets

2. **Memory Usage**:
   - Be aware of memory allocation patterns
   - Avoid large in-memory data structures
   - Use streaming for large data processing
   - Monitor memory usage in production

3. **Caching**:
   - Use fragment caching for view components
   - Use low-level caching for expensive computations
   - Set appropriate cache expiration
   - Invalidate caches when underlying data changes

### Profiling and Benchmarking
- Use rack-mini-profiler for request profiling
- Use memory_profiler for memory allocation profiling
- Use benchmark-ips for performance comparisons
- Record baselines before optimization

## Dependency Management

### Gems
1. **Selection Criteria**:
   - Prefer well-maintained gems with active communities
   - Evaluate security history
   - Consider license compatibility
   - Assess documentation quality

2. **Gemfile Organization**:
   - Group gems logically in the Gemfile
   - Specify version constraints
   - Document gem purpose with comments
   - Regularly update dependencies

3. **Bundler**:
   - Use Bundler for dependency management
   - Keep Gemfile.lock in version control
   - Use `bundle update` judiciously
   - Use bundle binstubs for development

## Code Quality

### Static Analysis
1. **RuboCop**:
   - Use RuboCop for style enforcement
   - Customize RuboCop configuration for project needs
   - Address code offenses systematically
   - Run RuboCop in CI pipeline

2. **Additional Tools**:
   - Use Brakeman for security analysis
   - Use Rails Best Practices for Rails-specific checks
   - Use Reek for code smell detection
   - Integrate code quality checks into the development workflow

### Code Review
- Conduct peer code reviews
- Focus on correctness, readability, and maintainability
- Use automated tools to catch style issues
- Document code review process

## Security

### Common Concerns
1. **Authentication and Authorization**:
   - Use established authentication gems like Devise or Clearance
   - Implement proper authorization with Pundit or CanCanCan
   - Use secure password storage
   - Implement appropriate session management

2. **Input Validation**:
   - Validate all input data
   - Use strong parameters in Rails controllers
   - Sanitize data for display
   - Prevent SQL injection through proper query methods

3. **OWASP Guidelines**:
   - Follow OWASP security recommendations
   - Protect against XSS, CSRF, and other common vulnerabilities
   - Implement proper error handling without leaking information
   - Regularly update dependencies for security patches

## References
- [Ruby Style Guide](https://rubystyle.guide/)
- [The Ruby Programming Language](https://www.ruby-lang.org/en/documentation/)
- [Rails Guides](https://guides.rubyonrails.org/)
- [Thoughtbot Guides](https://github.com/thoughtbot/guides/tree/main/ruby)
- [RSpec Documentation](https://rspec.info/documentation/)
- [Ruby Security](https://guides.rubyonrails.org/security.html) 