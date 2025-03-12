# Code Documentation Standards

This document outlines the standards and best practices for documenting code across all Bayat projects. Following these guidelines ensures that code is well-documented, maintainable, and understandable by all team members.

## Table of Contents

- [Documentation Principles](#documentation-principles)
- [Inline Documentation](#inline-documentation)
  - [Comments](#comments)
  - [Docstrings and Function Headers](#docstrings-and-function-headers)
- [Language-Specific Standards](#language-specific-standards)
  - [JavaScript/TypeScript](#javascripttypescript)
  - [Python](#python)
  - [C#](#c)
  - [C++](#c-1)
  - [Java](#java)
- [Class and Module Documentation](#class-and-module-documentation)
- [Code Examples](#code-examples)
- [Documentation Tools](#documentation-tools)
- [Documentation Tests](#documentation-tests)
- [Documentation Review Process](#documentation-review-process)
- [Versioning and Maintenance](#versioning-and-maintenance)

## Documentation Principles

All code documentation at Bayat should adhere to the following core principles:

1. **Clarity**: Use clear, concise language that is easily understood by all team members
2. **Completeness**: Cover all required aspects without unnecessary verbosity
3. **Consistency**: Use consistent terminology, format, and style throughout
4. **Accuracy**: Ensure documentation accurately reflects the current code behavior
5. **Necessity**: Document what is needed for usage, not implementation details unless they are critical
6. **Proximity**: Keep documentation as close to the code as possible
7. **Maintainability**: Design documentation to be easily updated alongside code changes

## Inline Documentation

### Comments

Use inline comments to explain complex logic, important decisions, or non-obvious code.

**Do:**
- Comment on "why" rather than "what" when the code itself is clear
- Add comments for complex algorithms or business logic
- Document workarounds, temporary solutions, or known limitations
- Use TODO comments for future enhancements (with ticket numbers)

**Don't:**
- Add comments that repeat what the code obviously does
- Leave outdated or incorrect comments
- Add commented-out code into production codebase

**Examples:**

```javascript
// Good comment
// Cache result to avoid expensive recalculation during animation loop
const cachedValue = expensiveCalculation(input);

// Bad comment - obvious from code
// Set value to 5
const value = 5;

// Good TODO with ticket reference
// TODO(BAY-1234): Implement pagination for this endpoint
```

### Docstrings and Function Headers

Every public function, method, class, and module should have a docstring or header comment that explains:

1. **Purpose**: What the function/class does
2. **Parameters**: Description of each parameter and their requirements
3. **Return Value**: What the function returns (if applicable)
4. **Exceptions/Errors**: What errors can be raised or returned
5. **Examples**: Usage examples where appropriate

## Language-Specific Standards

### JavaScript/TypeScript

Use JSDoc for documenting JavaScript and TypeScript code:

```javascript
/**
 * Calculates the total price including tax
 * 
 * @param {Object[]} items - The items to calculate total for
 * @param {number} items[].price - The price of each item
 * @param {number} [items[].quantity=1] - The quantity of each item
 * @param {number} taxRate - The tax rate as a decimal (e.g., 0.1 for 10%)
 * @returns {number} The total price including tax
 * @throws {Error} If any item has an invalid price
 * 
 * @example
 * // Returns 33
 * calculateTotal([{price: 10}, {price: 20}], 0.1);
 */
function calculateTotal(items, taxRate) {
  // Implementation
}
```

For TypeScript, leverage type definitions along with JSDoc:

```typescript
/**
 * User profile information
 */
interface UserProfile {
  /** Unique identifier */
  id: string;
  /** User's full name */
  name: string;
  /** User's email address */
  email: string;
  /** User's profile picture URL */
  pictureUrl?: string;
}

/**
 * Fetches a user's profile from the API
 * 
 * @param userId - The ID of the user to fetch
 * @returns The user's profile data
 * @throws {ApiError} If the user cannot be found or the request fails
 */
async function fetchUserProfile(userId: string): Promise<UserProfile> {
  // Implementation
}
```

### Python

Use Google-style docstrings for Python code:

```python
def process_user_data(user_id: int, data: dict) -> tuple[bool, Optional[str]]:
    """Process user data and update the user profile.
    
    This function validates the provided data, updates the user profile
    in the database, and triggers any necessary side effects.
    
    Args:
        user_id: The ID of the user to update
        data: Dictionary containing user data fields to update
            Supported fields: name, email, preferences
    
    Returns:
        A tuple where:
        - The first element is a boolean indicating success
        - The second element is an error message if successful is False,
          otherwise None
    
    Raises:
        ValueError: If the data contains invalid values
        UserNotFoundError: If the user_id does not exist
    
    Example:
        >>> success, error = process_user_data(123, {"name": "John Doe"})
        >>> if success:
        ...     print("User updated successfully")
        ... else:
        ...     print(f"Failed to update user: {error}")
    """
    # Implementation
```

### C#

Use XML documentation comments for C# code:

```csharp
/// <summary>
/// Processes a payment transaction.
/// </summary>
/// <remarks>
/// This method handles the full payment flow including authorization,
/// capture, and receipt generation.
/// </remarks>
/// <param name="amount">The payment amount in cents.</param>
/// <param name="cardToken">The tokenized payment card.</param>
/// <param name="customerId">The ID of the customer making the payment.</param>
/// <returns>
/// A <see cref="PaymentResult"/> containing the transaction details and status.
/// </returns>
/// <exception cref="ArgumentException">
/// Thrown when <paramref name="amount"/> is less than or equal to zero.
/// </exception>
/// <exception cref="PaymentDeclinedException">
/// Thrown when the payment is declined by the payment processor.
/// </exception>
public async Task<PaymentResult> ProcessPaymentAsync(
    long amount,
    string cardToken,
    string customerId)
{
    // Implementation
}
```

### C++

Use Doxygen-style comments for C++ code:

```cpp
/**
 * @brief Calculates the distance between two points
 * 
 * @param p1 The first point
 * @param p2 The second point
 * @return double The Euclidean distance between p1 and p2
 * 
 * @throws std::invalid_argument If either point has invalid coordinates
 * 
 * @note This function uses double precision for all calculations
 * 
 * @see Point2D for the point structure definition
 */
double calculateDistance(const Point2D& p1, const Point2D& p2)
{
    // Implementation
}
```

### Java

Use Javadoc for Java code:

```java
/**
 * Processes an order and returns the order confirmation.
 * 
 * <p>This method handles the entire order processing workflow, including
 * inventory checks, payment processing, and notification dispatch.
 * 
 * @param order The order to process, must not be null
 * @param paymentMethod The payment method to use for this order
 * @param options Additional options for order processing (can be null)
 * @return An OrderConfirmation object with the details of the processed order
 * @throws InsufficientInventoryException if any item in the order is out of stock
 * @throws PaymentFailedException if payment processing fails
 * 
 * @see OrderConfirmation
 * @since 2.1.0
 */
public OrderConfirmation processOrder(
    Order order,
    PaymentMethod paymentMethod,
    OrderOptions options) {
    // Implementation
}
```

## Class and Module Documentation

Each class or module should be documented with:

1. **Purpose**: What the class/module is responsible for
2. **Usage**: How to use the class/module (with examples)
3. **Dependencies**: Any external dependencies
4. **Lifecycle**: Any initialization or cleanup requirements
5. **Thread Safety**: Thread safety guarantees (if applicable)

Example (Python):

```python
"""User management module.

This module provides functionality for managing user accounts,
including creation, authentication, and profile management.

Usage:
    from users import UserManager
    
    # Create a user manager
    user_manager = UserManager(db_connection)
    
    # Create a new user
    user_id = user_manager.create_user("john@example.com", "password123")
    
    # Authenticate a user
    user = user_manager.authenticate("john@example.com", "password123")

Dependencies:
    - Database connection (postgres or mysql)
    - Email service for sending verification emails
    
Thread Safety:
    This module is thread-safe and can be used from multiple threads.
"""
```

## Code Examples

Include code examples where appropriate:

- Provide examples for complex or non-obvious usage patterns
- Include examples for main use cases of public APIs
- Show both success and error handling cases
- Keep examples concise but complete
- Ensure examples are correct and actually work
- Update examples when the API changes

Example (JavaScript):

```javascript
/**
 * User authentication service
 * 
 * @example
 * // Basic login
 * const authService = new AuthService();
 * try {
 *   const user = await authService.login('user@example.com', 'password');
 *   console.log(`Logged in as ${user.name}`);
 * } catch (error) {
 *   console.error('Login failed:', error.message);
 * }
 * 
 * @example
 * // Login with two-factor authentication
 * const authService = new AuthService();
 * try {
 *   // First step: request verification code
 *   await authService.requestTwoFactorCode('user@example.com', 'password');
 *   
 *   // Second step: verify code
 *   const user = await authService.verifyTwoFactorCode('123456');
 *   console.log(`Logged in as ${user.name}`);
 * } catch (error) {
 *   console.error('Two-factor authentication failed:', error.message);
 * }
 */
class AuthService {
  // Implementation
}
```

## Documentation Tools

Use the following documentation generation tools based on the language:

- **JavaScript/TypeScript**: JSDoc, TypeDoc
- **Python**: Sphinx, pydoc
- **C#**: DocFX, Sandcastle
- **C++**: Doxygen
- **Java**: Javadoc

For all projects, ensure that:

1. Documentation building is part of the CI/CD pipeline
2. Generated documentation is published to a central location
3. Documentation coverage is monitored
4. Links to the documentation are included in the README

## Documentation Tests

Test your documentation to ensure it remains accurate:

1. **Doctest**: For languages that support it (Python, Rust), use doctest to verify examples
2. **Compilation Tests**: Ensure code examples compile and execute correctly
3. **Link Validation**: Verify that all links in documentation are valid
4. **Example Testing**: Run examples in CI to ensure they work

Example Python doctest:

```python
def add(a, b):
    """Add two numbers and return the result.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
        
    Examples:
        >>> add(1, 2)
        3
        >>> add(-1, 1)
        0
    """
    return a + b
```

## Documentation Review Process

Documentation should be reviewed along with code:

1. **Accuracy**: Does the documentation accurately describe the code?
2. **Completeness**: Are all public APIs documented?
3. **Clarity**: Is the documentation clear and understandable?
4. **Examples**: Are examples correct and helpful?
5. **Grammar and Style**: Does the documentation follow style guidelines?

Reviewers should treat documentation deficiencies as seriously as code issues.

## Versioning and Maintenance

Keep documentation in sync with code:

1. **Version Specific**: Ensure documentation is specific to the version it describes
2. **Update with Code**: Update documentation whenever the related code changes
3. **Deprecation Notices**: Clearly mark deprecated features in documentation
4. **Change Log**: Maintain a change log of API changes
5. **Documentation Review**: Review documentation as part of regular maintenance

For API documentation, include:

- When features were introduced
- Compatibility notes
- Migration guides for breaking changes

Example deprecation notice:

```javascript
/**
 * Processes a payment
 * 
 * @param {Object} paymentInfo Payment information
 * @returns {Promise<PaymentResult>} The payment result
 * 
 * @deprecated Since version 2.3.0. Use processPaymentV2() instead.
 * This method will be removed in version 3.0.0.
 * 
 * @example
 * // Old way (deprecated)
 * const result = await processPayment({ amount: 1000 });
 * 
 * // New way
 * const result = await processPaymentV2({ amount: 1000, currency: 'USD' });
 */
```