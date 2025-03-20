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
- Use union types instead of optional parameters where meaningful

## React Conventions

- Use functional components with hooks
- Use TypeScript interfaces for component props
- Prefer explicit type imports over global imports

## Code Organization

- One class/interface per file
- Group imports by: external, internal, relative
- Organize functions by lifecycle or importance

## Error Handling

- Use typed error classes
- Handle async errors with try/catch or promise chaining

## Related Files

- [TypeScript](docs/languages/typescript.md)
- [JavaScript](docs/languages/javascript.md)
- [React](docs/frameworks/react.md)
