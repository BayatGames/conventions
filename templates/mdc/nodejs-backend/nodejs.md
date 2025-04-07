# Node.js Development Conventions

## Project Structure

```plaintext
src/
├── config/          # Configuration files
├── controllers/     # Route controllers
├── middleware/      # Express middleware
├── models/          # Database models
├── routes/          # Express routes
├── services/        # Business logic
├── utils/           # Utility functions
├── validation/      # Input validation
├── app.js           # Express app setup
└── server.js        # Server entry point
```

## Naming Conventions

- **Files**: Use lowercase with hyphens for multi-word filenames
  - `user-service.js`
  - `auth-middleware.js`
- **Functions**: Use camelCase
  - `getUserById()`
  - `validateAuthToken()`
- **Classes**: Use PascalCase
  - `UserService`
  - `DatabaseConnection`
- **Constants**: Use UPPER_SNAKE_CASE
  - `DEFAULT_TIMEOUT`
  - `API_BASE_URL`

## Asynchronous Code

- Use async/await for asynchronous operations
- Handle promise rejections with try/catch
- Avoid callback hell
- Be consistent with error propagation

```javascript
// Preferred
async function getUserData(userId) {
  try {
    const user = await User.findById(userId);
    if (!user) {
      throw new NotFoundError('User not found');
    }
    return user;
  } catch (error) {
    logger.error('Error fetching user:', error);
    throw error;
  }
}

// Avoid
function getUserData(userId, callback) {
  User.findById(userId, (err, user) => {
    if (err) {
      return callback(err);
    }
    if (!user) {
      return callback(new Error('User not found'));
    }
    callback(null, user);
  });
}
```

## Error Handling

- Create custom error classes for different error types
- Use middleware for centralized error handling
- Include appropriate HTTP status codes
- Log errors with sufficient context

## Module Exports

- Use named exports for multiple functions
- Use default exports for single class/function modules
- Destructure imports to improve readability

```javascript
// Export multiple functions
export const createUser = () => {};
export const updateUser = () => {};

// Or with CommonJS
module.exports = {
  createUser: () => {},
  updateUser: () => {}
};
```

## Configuration Management

- Use environment variables for configuration
- Keep secrets out of the code
- Use a configuration service/module
- Validate configuration on startup

## Dependency Management

- Use npm or yarn consistently for package management
- Keep dependencies updated
- Use `package-lock.json` or `yarn.lock` for reproducible builds
- Review dependencies for security vulnerabilities
