<!--
Document: PHP Development Standards
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# PHP Development Standards

This document outlines the standards and best practices for PHP development at Bayat.

## Code Style and Formatting

### General Guidelines
- Follow [PSR-12](https://www.php-fig.org/psr/psr-12/) coding style standard
- Use PHP_CodeSniffer to enforce style consistency
- Maximum line length should be 120 characters
- Use 4 spaces for indentation, not tabs
- Files should be encoded in UTF-8 without BOM
- Files should end with a newline
- Use strict type declarations (`declare(strict_types=1);`) in all files

### Naming Conventions
1. **Classes and Interfaces**:
   - Use PascalCase for class names (e.g., `OrderProcessor`, `UserRepository`)
   - Use PascalCase for interface names with "Interface" suffix (e.g., `LoggerInterface`)
   - Name trait with PascalCase with "Trait" suffix (e.g., `LoggableTrait`)
   - Abstract classes should be prefixed with "Abstract" (e.g., `AbstractController`)

2. **Methods and Functions**:
   - Use camelCase for method and function names (e.g., `getUserById()`, `processOrder()`)
   - Methods should be named for their behavior, typically using a verb
   - Use verb phrases that describe the action (e.g., `calculateTotal()`, `sendEmail()`)
   - Prefix boolean methods with "is", "has", or "should" (e.g., `isValid()`, `hasPermission()`)

3. **Variables and Properties**:
   - Use camelCase for variable and property names (e.g., `$userName`, `$orderTotal`)
   - Be descriptive with variable names
   - Use plural names for arrays or collections
   - Avoid abbreviations unless they are widely understood

4. **Constants**:
   - Use UPPER_SNAKE_CASE for constants (e.g., `MAX_LOGIN_ATTEMPTS`)
   - Define constants in classes when they're related to that class
   - Use descriptive names that indicate the purpose

5. **Namespaces**:
   - Use PascalCase for namespace segments
   - Follow PSR-4 autoloading standard
   - Use vendor/organization name as the top-level namespace
   - Structure namespaces based on functionality or domain concepts

### File Organization
1. **File Structure**:
   - One class per file
   - Filename should match the class name
   - Group related classes in directories
   - Follow PSR-4 directory structure

2. **Code Organization**:
   - Order class elements consistently:
     1. Constants
     2. Properties
     3. Constructor
     4. Public methods
     5. Protected methods
     6. Private methods
   - Group related methods together
   - Keep files under 500 lines when possible
   - Keep methods under 50 lines when possible

## Language Features and Best Practices

### PHP Version
- Use PHP 8.1+ for new projects
- Use PHP 7.4+ for maintenance of existing projects
- Document minimum PHP version requirements in project README

### Modern PHP Features
1. **Type Declarations**:
   - Always use type declarations for parameters, return types, and properties
   - Use union types when necessary
   - Use nullable types (`?Type`) for optional values
   - Use void return type when a function doesn't return a value

2. **PHP 7.4+ Features**:
   - Use typed properties
   - Use arrow functions for simple callbacks
   - Use null coalescing assignment operator (`??=`)
   - Use spread operator when appropriate

3. **PHP 8.0+ Features**:
   - Use named arguments for better readability
   - Use constructor property promotion
   - Use match expressions instead of switch statements
   - Use attributes for metadata

4. **PHP 8.1+ Features**:
   - Use readonly properties for immutable data
   - Use enums for type-safe enumeration values
   - Use pure intersection types where appropriate
   - Use first-class callable syntax

### Error Handling
1. **Exceptions**:
   - Create custom exception classes for specific error cases
   - Use exception hierarchy to categorize exceptions
   - Include helpful context in exception messages
   - Use try-catch blocks judiciously

2. **Error Reporting**:
   - Set appropriate error reporting levels for each environment
   - Log errors appropriately
   - Never display errors in production
   - Handle errors gracefully with user-friendly messages

3. **Validation**:
   - Validate all input data
   - Use type declarations and assertions
   - Fail early when invalid data is detected
   - Return clear validation error messages

### Security Best Practices
1. **Input Validation and Sanitization**:
   - Validate all user input
   - Use prepared statements for database queries
   - Sanitize output appropriately for context (HTML, JSON, etc.)
   - Use input filtering functions

2. **Authentication and Authorization**:
   - Use secure password hashing (password_hash)
   - Implement proper session management
   - Apply the principle of least privilege
   - Use CSRF protection

3. **Common Vulnerabilities**:
   - Protect against XSS (Cross-Site Scripting)
   - Prevent SQL injection
   - Avoid file inclusion vulnerabilities
   - Protect against CSRF (Cross-Site Request Forgery)

## Object-Oriented Programming

### Class Design
1. **SOLID Principles**:
   - Single Responsibility Principle: Classes should have one reason to change
   - Open/Closed Principle: Open for extension, closed for modification
   - Liskov Substitution Principle: Subtypes should be substitutable for their base types
   - Interface Segregation: Many specific interfaces are better than one general interface
   - Dependency Inversion: Depend on abstractions, not concretions

2. **Design Patterns**:
   - Use Factory pattern for object creation
   - Use Repository pattern for data access
   - Use Strategy pattern for interchangeable algorithms
   - Use Observer pattern for event handling
   - Document pattern usage in comments

3. **Composition**:
   - Favor composition over inheritance
   - Use traits for shared behavior
   - Keep inheritance hierarchies shallow
   - Apply interface-based programming

### Dependency Management
1. **Dependency Injection**:
   - Use constructor injection for required dependencies
   - Use setter injection for optional dependencies
   - Consider using a dependency injection container
   - Document dependencies for each class

2. **Service Container**:
   - Use a service container in larger applications
   - Configure services in a central location
   - Define service interfaces for major components
   - Use lazy loading for resource-intensive services

## Framework-Specific Guidelines

### Laravel
1. **General Practices**:
   - Follow Laravel naming conventions
   - Use Laravel's built-in features instead of reinventing the wheel
   - Keep controllers thin, move business logic to services
   - Use Laravel's validation system for input validation

2. **Eloquent**:
   - Define relationships in model classes
   - Use Eloquent scopes for common query conditions
   - Use model factories for testing
   - Define fillable or guarded properties for mass assignment protection

3. **Structure**:
   - Organize code by feature/module in larger applications
   - Use service providers for bootstrapping components
   - Use middleware for cross-cutting concerns
   - Use form requests for complex validation

### Symfony
1. **General Practices**:
   - Follow Symfony best practices
   - Use Symfony components as designed
   - Leverage the service container
   - Structure the application according to Symfony recommendations

2. **Components**:
   - Use Doctrine properly for database operations
   - Use Symfony forms for handling form submission
   - Use the security component for authentication/authorization
   - Use events and event listeners appropriately

3. **Configuration**:
   - Use environment variables for environment-specific configuration
   - Use YAML for service configuration
   - Keep configuration DRY
   - Follow Symfony configuration conventions

## Testing

### Unit Testing
1. **PHPUnit**:
   - Write automated tests using PHPUnit
   - Aim for high test coverage of business logic
   - Follow the AAA pattern (Arrange, Act, Assert)
   - Use data providers for testing multiple scenarios

2. **Test Organization**:
   - Name test methods descriptively
   - Organize tests to mirror the structure of the code being tested
   - Use setUp and tearDown methods for common test setup
   - Keep tests independent from each other

3. **Mocking**:
   - Use PHPUnit's built-in mocking framework or Mockery
   - Mock external dependencies
   - Test both success and failure paths
   - Avoid excessive mocking

### Integration Testing
- Test interactions between components
- Use an in-memory database for database tests when possible
- Test the complete request/response cycle in web applications
- Create fixtures for test data

## Documentation

### Code Documentation
1. **PHPDoc**:
   - Use PHPDoc to document classes, methods, and properties
   - Document parameters, return types, and exceptions
   - Include descriptive summaries
   - Keep documentation up to date with code changes

2. **Comments**:
   - Use comments to explain "why", not "what"
   - Document complex algorithms or business rules
   - Avoid redundant comments
   - Use TODO comments with tracking information

### API Documentation
- Document all public APIs
- Use OpenAPI/Swagger for REST APIs
- Include examples and use cases
- Document authentication requirements

## Performance

### Optimization
1. **General Principles**:
   - Profile before optimizing
   - Focus on bottlenecks identified through profiling
   - Consider both memory and CPU usage
   - Document performance considerations

2. **Common Optimizations**:
   - Use caching appropriately
   - Optimize database queries
   - Minimize external service calls
   - Use appropriate data structures

### Caching
- Use APCu for opcode caching
- Implement data caching where appropriate
- Cache expensive operations
- Invalidate cache when data changes

## Build and Deployment

### Composer
1. **Package Management**:
   - Use Composer for dependency management
   - Specify version constraints appropriately
   - Keep composer.json and composer.lock in version control
   - Run `composer update` only when needed

2. **Project Organization**:
   - Follow PSR-4 for autoloading
   - Use `composer scripts` for common tasks
   - Document installation and setup procedures
   - Specify PHP extensions required

### Deployment
- Use automated deployment processes
- Include database migrations in the deployment process
- Use environment-specific configuration
- Consider using Docker for consistent environments

## Code Quality

### Static Analysis
1. **Tools**:
   - Use PHPStan or Psalm for static analysis
   - Configure appropriate rule levels
   - Address reported issues systematically
   - Integrate static analysis into CI pipeline

2. **Quality Metrics**:
   - Monitor code complexity
   - Keep cyclomatic complexity low
   - Track test coverage
   - Use automated tools to enforce quality standards

### Code Review
- Conduct peer code reviews
- Focus on business logic correctness, security, and maintainability
- Use code review checklists
- Document code review findings and resolutions

## References
- [PHP Standards Recommendations](https://www.php-fig.org/psr/)
- [PHP: The Right Way](https://phptherightway.com/)
- [Laravel Best Practices](https://github.com/alexeymezenin/laravel-best-practices)
- [Symfony Best Practices](https://symfony.com/doc/current/best_practices.html)
- [PHP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/PHP_Configuration_Cheat_Sheet.html) 