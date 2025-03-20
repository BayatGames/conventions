# TypeScript Conventions

## Naming Conventions

- **Interfaces**: PascalCase, prefixed with 'I'

  ```typescript
  interface IUserProfile {}
  ```

- **Types**: PascalCase

  ```typescript
  type UserState = 'active' | 'inactive';
  ```

- **Classes**: PascalCase

  ```typescript
  class UserService {}
  ```

- **Variables & Functions**: camelCase

  ```typescript
  const userData = {};
  function getUserProfile() {}
  ```

- **Constants**: UPPER_SNAKE_CASE

  ```typescript
  const MAX_RETRY_ATTEMPTS = 3;
  ```

- **Private Properties**: camelCase with underscore prefix

  ```typescript
  private _userToken = '';
  ```

## Type Definitions

- Always define return types for public functions
- Use type inference for local variables where obvious
- Avoid `any` type; use `unknown` when type is uncertain
- Use union types instead of optional parameters where appropriate
- Create reusable type definitions for complex structures

## Code Organization

- One class/interface per file
- Group imports by: external, internal, relative
- Organize functions by lifecycle or importance
- Define types close to where they're used

## Error Handling

- Use typed error classes
- Handle async errors with try/catch or promise chaining
- Provide meaningful error messages

## Best Practices

- Use readonly for immutable properties
- Prefer interfaces for object shapes used across the codebase
- Use enums for predefined sets of values
- Use generics for reusable components and functions
