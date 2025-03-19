<!--
Document: TypeScript Coding Conventions
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# TypeScript Coding Conventions

This document outlines the TypeScript coding conventions and standards for all Bayat projects. It builds upon our \1\2) with additional TypeScript-specific guidelines.

## Table of Contents

- [TypeScript Version](#typescript-version)
- [Type Definitions](#type-definitions)
- [Interfaces and Types](#interfaces-and-types)
- [Classes](#classes)
- [Generics](#generics)
- [Enums](#enums)
- [Null and Undefined](#null-and-undefined)
- [Type Assertions](#type-assertions)
- [TSConfig Standards](#tsconfig-standards)
- [Documentation](#documentation)
- [Testing TypeScript Code](#testing-typescript-code)
- [Migration Strategies](#migration-strategies)

## TypeScript Version

- Specify TypeScript version in `package.json` 
- Document the minimum supported TypeScript version in README.md
- Stay within one major version of the latest stable release

## Type Definitions

### General Type Guidelines

- Prefer explicit typing over implicit (inferred) typing for function parameters and return types
- Use type inference for local variables when types are obvious
- Use `unknown` instead of `any` when possible
- Avoid type assertions except when necessary
- Use union types to represent values that could be one of several types

```typescript
// Good
function calculateTotal(items: Item[], taxRate: number): number {
  // Type of total inferred as number
  let total = 0;
  
  for (const item of items) {
    total += item.price;
  }
  
  return total * (1 + taxRate);
}

// Avoid
function calculateTotal(items, taxRate) {
  let total = 0;
  
  for (const item of items) {
    total += item.price;
  }
  
  return total * (1 + taxRate);
}
```

### Type Annotations

- Use `: Type` syntax for variable and parameter type annotations
- Use `: => Type` syntax for function return type annotations
- Place type annotations after parameter/variable names
- Add spaces around the colon in type annotations

```typescript
// Good
const age: number = 30;
function greet(name: string): string {
  return `Hello, ${name}!`;
}

// Avoid
const age:number = 30;
function greet(name:string):string {
  return `Hello, ${name}!`;
}
```

## Interfaces and Types

### When to Use Interface vs Type

- Use `interface` for object definitions that can be extended or implemented
- Use `type` for unions, primitives, tuples, or when you need to use operations like mapped types
- Prefer `interface` over `type` for public API definitions
- Be consistent in your codebase

```typescript
// Interface for object definitions that may be extended
interface User {
  id: number;
  name: string;
  email: string;
}

// Extended interface
interface AdminUser extends User {
  permissions: string[];
}

// Type for union types
type Status = 'pending' | 'active' | 'closed';

// Type for complex types that use mapped types or other operations
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};
```

### Naming Conventions

- Use PascalCase for interface and type names
- Do not use "I" prefixes for interface names (e.g., use `User` not `IUser`)
- Use declarative, descriptive names
- Suffix interface with a noun or adjective describing its purpose

```typescript
// Good
interface Button {
  label: string;
  onClick: () => void;
}

interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

// Avoid
interface IButton {
  label: string;
  onClick: () => void;
}

interface Response<T> {
  data: T;
  status: number;
  message: string;
}
```

### Property Definitions

- Use optional properties (`?`) rather than properties that can be undefined
- Use readonly modifier for properties that should not be modified after creation
- Group required properties before optional properties
- Add JSDoc comments for complex properties

```typescript
interface User {
  // Required properties
  id: number;
  name: string;
  
  // Optional properties
  email?: string;
  phoneNumber?: string;
  
  // Readonly properties
  readonly createdAt: Date;
}
```

## Classes

### Class Members

- Use visibility modifiers (`public`, `private`, `protected`) for all class members
- Use `private` instead of JavaScript's `#` private fields for consistency
- Use the `readonly` modifier for properties that should not change after initialization
- Define member visibility in this order: public, protected, private

```typescript
class Product {
  // Public properties
  public name: string;
  public readonly id: string;
  
  // Protected properties
  protected category: string;
  
  // Private properties
  private _price: number;
  
  constructor(name: string, id: string, category: string, price: number) {
    this.name = name;
    this.id = id;
    this.category = category;
    this._price = price;
  }
  
  // Public methods
  public getFormattedPrice(): string {
    return `$${this._price.toFixed(2)}`;
  }
  
  // Protected methods
  protected calculateDiscount(percent: number): number {
    return this._price * (1 - percent / 100);
  }
  
  // Private methods
  private validatePrice(price: number): boolean {
    return price > 0;
  }
}
```

### Abstract Classes and Inheritance

- Use abstract classes for base classes that should not be instantiated directly
- Prefer composition over inheritance when possible
- Be explicit about which methods can be overridden by using the `protected` modifier
- Use explicit abstract method and property declarations

```typescript
abstract class Shape {
  protected color: string;
  
  constructor(color: string) {
    this.color = color;
  }
  
  abstract calculateArea(): number;
  
  public getColor(): string {
    return this.color;
  }
}

class Circle extends Shape {
  private radius: number;
  
  constructor(color: string, radius: number) {
    super(color);
    this.radius = radius;
  }
  
  calculateArea(): number {
    return Math.PI * this.radius * this.radius;
  }
}
```

## Generics

### Generic Type Parameters

- Use PascalCase single-letter names (e.g., `T`, `K`, `V`) for simple generic type parameters
- Use descriptive names for complex generic type parameters (e.g., `TItem`, `TKey`, `TValue`)
- Use constraints to limit generic types when necessary
- Set meaningful defaults for generic types when appropriate

```typescript
// Simple generic type
function identity<T>(value: T): T {
  return value;
}

// Descriptive generic types with constraints
interface Repository<TEntity extends { id: string }> {
  findById(id: string): Promise<TEntity | null>;
  save(entity: TEntity): Promise<void>;
}

// Generic with default
interface ApiClient<TError = Error> {
  fetch<TData>(url: string): Promise<TData | TError>;
}
```

## Enums

### Enum Definitions

- Use PascalCase for enum names
- Use PascalCase for enum members
- Prefer const enums for better performance when applicable
- Use string or number values explicitly when they have meaning

```typescript
// Numbered enum (default)
enum Direction {
  North,
  East,
  South,
  West
}

// String enum (preferred for readability and debugging)
enum HttpStatus {
  OK = "OK",
  NotFound = "NOT_FOUND",
  InternalServerError = "INTERNAL_SERVER_ERROR"
}

// Const enum for performance
const enum LogLevel {
  Debug,
  Info,
  Warning,
  Error
}
```

### Using Enums

- Import enums directly rather than referencing individual values
- Use dot notation to access enum values
- When using TypeScript with strict mode, always handle all enum cases in switch statements

```typescript
import { HttpStatus } from './http-status';

function handleResponse(status: HttpStatus): void {
  switch (status) {
    case HttpStatus.OK:
      // Handle OK response
      break;
    case HttpStatus.NotFound:
      // Handle not found
      break;
    case HttpStatus.InternalServerError:
      // Handle server error
      break;
    default:
      // Ensure exhaustiveness checking
      const exhaustiveCheck: never = status;
      throw new Error(`Unhandled status: ${exhaustiveCheck}`);
  }
}
```

## Null and Undefined

### Strict Null Checking

- Enable `strictNullChecks` in TSConfig
- Use `undefined` for uninitialized values
- Use `null` for intentionally absent values
- Use optional chaining (`?.`) and nullish coalescing (`??`) operators
- Be explicit about null/undefined in function return types

```typescript
// Function that might return undefined
function findUser(id: string): User | undefined {
  return users.find(user => user.id === id);
}

// Handling possible undefined return
const user = findUser('123');
const userName = user?.name ?? 'Guest';

// Function with explicit null return
function getUserById(id: string): User | null {
  const user = database.query(`SELECT * FROM users WHERE id = ${id}`);
  return user || null;
}
```

## Type Assertions

### When to Use Type Assertions

- Use type assertions only when you know more about the type than TypeScript does
- Prefer type guards over type assertions
- Use `as` syntax over angle brackets (`<>`) for consistency with JSX
- Use `unknown` as an intermediate step when asserting to a specific type from `any`

```typescript
// Type assertion when you know the type
const button = document.getElementById('submit') as HTMLButtonElement;

// Prefer type guards when possible
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function processValue(value: unknown): void {
  if (isString(value)) {
    // TypeScript knows value is a string here
    console.log(value.toUpperCase());
  }
}

// Safer assertions using unknown
const data: unknown = JSON.parse(responseText);
const user = (data as unknown) as User;
```

## TSConfig Standards

### Recommended Configuration

Establish standard TSConfig settings for projects:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "node",
    "esModuleInterop": true,
    "strict": true,
    "strictNullChecks": true,
    "noImplicitAny": true,
    "noImplicitThis": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  }
}
```

### Project-Specific Configurations

- Document any deviations from the standard configuration
- Use `extends` to build on the base configuration
- Create environment-specific configurations when necessary (browser vs. Node.js)

## Documentation

### JSDoc for TypeScript

- Use JSDoc comments for public APIs
- Leverage TypeScript's type system to reduce redundant documentation
- Focus on documenting "why" rather than "what" when the type signature is clear
- Document constraints and edge cases not obvious from types

```typescript
/**
 * Represents a user in the system
 */
interface User {
  /** Unique identifier for the user */
  id: string;
  
  /** User's full name */
  name: string;
  
  /** User's email address */
  email: string;
}

/**
 * Retrieves a user by their ID
 * 
 * @param id - The user's unique identifier
 * @returns The user object if found, null otherwise
 * 
 * @throws {ApiError} If the API request fails
 */
async function getUserById(id: string): Promise<User | null> {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    if (error.status === 404) {
      return null;
    }
    throw new ApiError('Failed to fetch user', error);
  }
}
```

## Testing TypeScript Code

### Type Testing

- Use `dtslint` or similar tools to test type definitions
- Write tests that would fail to compile if types are incorrect
- Test edge cases in generic types

### Unit Testing

- Use TypeScript-compatible testing frameworks (Jest, Vitest, etc.)
- Configure testing tools to use the same TypeScript settings as your project
- Test type guards and custom type predicates explicitly

```typescript
// Type guard
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'name' in obj &&
    'email' in obj
  );
}

// Testing the type guard
describe('isUser', () => {
  it('returns true for valid user objects', () => {
    const user = { id: '123', name: 'John', email: 'john@example.com' };
    expect(isUser(user)).toBe(true);
  });
  
  it('returns false for non-user objects', () => {
    const notUser = { id: '123', name: 'John' };
    expect(isUser(notUser)).toBe(false);
  });
});
```

## Migration Strategies

### JavaScript to TypeScript Migration

- Use incremental migration approaches
- Start with `allowJs: true` in TSConfig
- Add `.ts` files alongside `.js` files
- Add type definitions for existing JavaScript libraries
- Use `@ts-check` and JSDoc types for JavaScript files before conversion

### Loose to Strict TypeScript Migration

- Enable strict flags incrementally:
  1. `noImplicitAny`
  2. `strictNullChecks`
  3. `strictFunctionTypes`
  4. `strictBindCallApply`
  5. `strictPropertyInitialization`
  6. `noImplicitThis`
  7. `alwaysStrict`
- Use `// @ts-ignore` sparingly during migration
- Document technical debt with `// TODO:` comments

## Additional Resources

- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
- [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)
- [Microsoft TypeScript Coding Guidelines](https://github.com/microsoft/TypeScript/wiki/Coding-guidelines)

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | YYYY-MM-DD | Initial version | 