# JavaScript Coding Conventions

This document outlines the JavaScript coding conventions and standards for all Bayat projects. Following these guidelines ensures code consistency, readability, and maintainability across all JavaScript codebases.

## Table of Contents

- [Syntax and Formatting](#syntax-and-formatting)
- [Language Features](#language-features)
- [Naming Conventions](#naming-conventions)
- [Code Organization](#code-organization)
- [Documentation](#documentation)
- [Performance Considerations](#performance-considerations)
- [Testing](#testing)
- [Module Management](#module-management)
- [Browser Compatibility](#browser-compatibility)
- [Security Best Practices](#security-best-practices)
- [Tools and Enforcement](#tools-and-enforcement)

## Syntax and Formatting

### General Guidelines

- Use 2 spaces for indentation
- Line length should not exceed 80 characters
- Use semicolons at the end of statements
- Use single quotes for string literals
- Add trailing commas in multi-line object and array literals
- Surround operators with spaces
- Place open braces on the same line as their statement
- Place else statements on the same line as the closing brace

```javascript
// Good
function calculateArea(width, height) {
  const area = width * height;
  
  if (area > 100) {
    return 'Large';
  } else if (area > 20) {
    return 'Medium';
  } else {
    return 'Small';
  }
}

// Avoid
function calculateArea(width,height){
  const area=width*height;
  
  if(area>100)
  {
    return "Large";
  }
  else if(area>20)
  {
    return "Medium";
  }
  else
  {
    return "Small";
  }
}
```

### File Structure

- Each file should contain a single logical component (class, service, etc.)
- Place imports at the top of the file
- Group imports by type (third-party libraries, then project imports)
- Place exports at the bottom of the file for CommonJS modules

```javascript
// Third-party imports
import React from 'react';
import PropTypes from 'prop-types';

// Project imports
import { formatCurrency } from '../utils/formatters';
import Button from '../components/Button';

// Component code here...

export default MyComponent;
```

## Language Features

### Variable Declarations

- Use `const` by default
- Use `let` only when reassignment is necessary
- Avoid using `var`
- Declare variables at the top of their scope
- Declare one variable per line

```javascript
// Good
const firstName = 'John';
const lastName = 'Doe';
let age = 30;

// Later in the code
age = 31;

// Avoid
var firstName = 'John', lastName = 'Doe';
var age = 30;
```

### Modern JavaScript Features

- Prefer arrow functions for anonymous functions
- Use template literals instead of string concatenation
- Use object shorthand for object literals
- Use array and object destructuring
- Use the spread operator for object and array manipulation
- Use default parameters when appropriate
- Use optional chaining and nullish coalescing when appropriate

```javascript
// Good
const user = {
  name,
  age,
  getFullProfile() {
    return `${this.name} (${this.age})`;
  }
};

const { id, status } = response;
const newItems = [...items, newItem];
const updatedUser = { ...user, age: user.age + 1 };
const displayName = user?.name ?? 'Guest';

// Avoid
const user = {
  name: name,
  age: age,
  getFullProfile: function() {
    return this.name + ' (' + this.age + ')';
  }
};

const id = response.id;
const status = response.status;
const newItems = items.concat([newItem]);
const updatedUser = Object.assign({}, user, { age: user.age + 1 });
const displayName = user && user.name ? user.name : 'Guest';
```

### Asynchronous Code

- Prefer async/await over Promise chains when appropriate
- Handle errors with try/catch blocks for async/await
- Avoid deeply nested Promise chains
- Always return in Promise chains to ensure proper chaining

```javascript
// Good
async function fetchUserData(userId) {
  try {
    const response = await api.fetchUser(userId);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw error;
  }
}

// Or with Promise chains
function fetchUserData(userId) {
  return api.fetchUser(userId)
    .then(response => response.data)
    .catch(error => {
      console.error('Failed to fetch user:', error);
      throw error;
    });
}

// Avoid
function fetchUserData(userId) {
  return new Promise((resolve, reject) => {
    api.fetchUser(userId).then(response => {
      resolve(response.data);
    }).catch(error => {
      console.error('Failed to fetch user:', error);
      reject(error);
    });
  });
}
```

## Naming Conventions

### General Guidelines

- Use descriptive names that reveal intent
- Use camelCase for variables, functions, and methods
- Use PascalCase for classes, interfaces, and React components
- Use UPPER_SNAKE_CASE for constants
- Avoid single-letter names except for loop iterators
- Boolean variables should start with "is", "has", "should", etc.

### Specific Naming Patterns

| Element | Case | Example |
|---------|------|---------|
| Variables | camelCase | `userName`, `itemCount` |
| Functions | camelCase | `calculateTotal`, `fetchData` |
| Classes/Constructors | PascalCase | `UserProfile`, `PaymentProcessor` |
| Components | PascalCase | `Button`, `UserCard` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT`, `API_BASE_URL` |
| Private properties | camelCase with underscore prefix | `_privateValue`, `_cache` |
| File names | kebab-case | `user-profile.js`, `payment-utils.js` |

## Code Organization

### Function Design

- Keep functions small and focused (under 30 lines of code)
- Follow the Single Responsibility Principle
- Functions should do one thing and do it well
- Limit parameters to 3 or fewer; use object parameters for more
- Return early to avoid deep nesting

```javascript
// Good
function validateUser(user) {
  if (!user) {
    return { valid: false, error: 'User is required' };
  }
  
  if (!user.name) {
    return { valid: false, error: 'Name is required' };
  }
  
  if (!user.email || !isValidEmail(user.email)) {
    return { valid: false, error: 'Valid email is required' };
  }
  
  return { valid: true };
}

// Avoid
function validateUser(user) {
  let isValid = true;
  let error = null;
  
  if (user) {
    if (user.name) {
      if (user.email && isValidEmail(user.email)) {
        // Valid user
      } else {
        isValid = false;
        error = 'Valid email is required';
      }
    } else {
      isValid = false;
      error = 'Name is required';
    }
  } else {
    isValid = false;
    error = 'User is required';
  }
  
  return { valid: isValid, error: error };
}
```

### Error Handling

- Be explicit about error handling
- Use custom error classes for application-specific errors
- Provide meaningful error messages
- Log errors with proper context
- Don't swallow errors without good reason

```javascript
class APIError extends Error {
  constructor(message, status, data) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.data = data;
  }
}

async function fetchData(endpoint) {
  try {
    const response = await fetch(endpoint);
    
    if (!response.ok) {
      const data = await response.json().catch(() => null);
      throw new APIError(
        `API request failed with status ${response.status}`,
        response.status,
        data
      );
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof APIError) {
      // Handle API-specific errors
      console.error(`API Error (${error.status}):`, error.message);
    } else {
      // Handle network or other errors
      console.error('Network Error:', error.message);
    }
    throw error;
  }
}
```

## Documentation

### Comments

- Write comments that explain "why", not "what"
- Use JSDoc for public APIs and complex functions
- Keep comments up-to-date with code changes
- Use `// TODO:` comments for planned changes

### JSDoc

Document complex functions and public APIs with JSDoc:

```javascript
/**
 * Calculates the total price with tax and discounts applied
 * 
 * @param {number} basePrice - The base price of the item
 * @param {number} taxRate - The tax rate as a decimal (e.g., 0.07 for 7%)
 * @param {Object} [options] - Additional options
 * @param {number} [options.discount=0] - Discount as a decimal
 * @param {boolean} [options.roundToNearestCent=true] - Whether to round to nearest cent
 * @returns {number} The final price
 * @throws {Error} If basePrice or taxRate is negative
 */
function calculateTotalPrice(basePrice, taxRate, options = {}) {
  const { discount = 0, roundToNearestCent = true } = options;
  
  if (basePrice < 0 || taxRate < 0) {
    throw new Error('Price and tax rate must be non-negative');
  }
  
  let total = basePrice * (1 - discount) * (1 + taxRate);
  
  if (roundToNearestCent) {
    total = Math.round(total * 100) / 100;
  }
  
  return total;
}
```

## Performance Considerations

### General Guidelines

- Minimize DOM manipulation
- Batch DOM updates when possible
- Use appropriate data structures for operations
- Avoid premature optimization
- Profile performance issues before optimizing
- Cache expensive computation results

### Specific Recommendations

- Use `requestAnimationFrame` for animations
- Debounce or throttle event handlers for performance-critical events
- Virtualize long lists to minimize DOM elements
- Remove event listeners when components are unmounted
- Use web workers for CPU-intensive operations
- Lazy-load resources and components when possible

```javascript
// Debouncing example
function debounce(func, wait) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

// Usage
const handleResize = debounce(() => {
  // Handle resize logic
}, 200);

window.addEventListener('resize', handleResize);
```

## Testing

### Unit Testing

- Write tests for all non-trivial functions
- Use Jest (or another testing framework) for unit tests
- Follow the AAA pattern: Arrange, Act, Assert
- Mock external dependencies
- Test edge cases and error scenarios

```javascript
// Example test using Jest
describe('calculateTotalPrice', () => {
  test('calculates price with tax and no discount', () => {
    // Arrange
    const basePrice = 100;
    const taxRate = 0.07;
    
    // Act
    const result = calculateTotalPrice(basePrice, taxRate);
    
    // Assert
    expect(result).toBe(107);
  });
  
  test('applies discount before tax', () => {
    // Arrange
    const basePrice = 100;
    const taxRate = 0.07;
    const options = { discount: 0.1 }; // 10% discount
    
    // Act
    const result = calculateTotalPrice(basePrice, taxRate, options);
    
    // Assert
    expect(result).toBe(96.3); // (100 * 0.9) * 1.07 = 96.3
  });
  
  test('throws error for negative price', () => {
    expect(() => calculateTotalPrice(-10, 0.07)).toThrow();
  });
});
```

### Integration and End-to-End Testing

- Use Cypress, Playwright, or similar for E2E tests
- Test critical user flows
- Set up CI/CD pipeline for automated testing
- Use realistic test data

## Module Management

### ES Modules

- Prefer ES modules (`import`/`export`) over CommonJS (`require`)
- Use named exports for multiple functions/classes
- Use default exports for main component/class
- Be consistent with import style
- Avoid side effects in modules

```javascript
// utils.js
export function formatDate(date) {
  // Implementation
}

export function formatCurrency(amount) {
  // Implementation
}

// component.js
import React from 'react';
import { formatCurrency } from './utils';

function PriceDisplay({ amount }) {
  return <div>{formatCurrency(amount)}</div>;
}

export default PriceDisplay;
```

## Browser Compatibility

- Define browser support targets in the project README
- Use appropriate polyfills for unsupported features
- Use transpilation (Babel) for syntax compatibility
- Test on targeted browsers

## Security Best Practices

- Sanitize user input to prevent XSS attacks
- Use Content Security Policy (CSP) headers
- Avoid using `eval()` or `new Function()`
- Validate data on the server, not just the client
- Use HTTPS for all API calls
- Follow OWASP security guidelines

```javascript
// Avoid direct HTML insertion
// Bad
element.innerHTML = userProvidedContent;

// Good (with a sanitization library)
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userProvidedContent);

// Or avoid HTML insertion altogether
element.textContent = userProvidedContent;
```

## Tools and Enforcement

- Use ESLint for static code analysis
- Configure Prettier for consistent formatting
- Set up automatic linting in CI/CD pipeline
- Use TypeScript for type checking when appropriate
- Add pre-commit hooks to enforce standards

### Recommended ESLint Configuration

```javascript
// .eslintrc.js
module.exports = {
  "extends": [
    "eslint:recommended",
    "plugin:import/errors",
    "plugin:prettier/recommended"
  ],
  "plugins": ["import"],
  "env": {
    "browser": true,
    "es6": true,
    "node": true,
    "jest": true
  },
  "parserOptions": {
    "ecmaVersion": 2020,
    "sourceType": "module"
  },
  "rules": {
    "no-console": ["warn", { "allow": ["error", "warn"] }],
    "no-var": "error",
    "prefer-const": "error",
    "eqeqeq": ["error", "always"]
  }
};
```

## Additional Resources

- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html)
- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [JavaScript Clean Code Best Practices](https://github.com/ryanmcdermott/clean-code-javascript)

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | YYYY-MM-DD | Initial version | 