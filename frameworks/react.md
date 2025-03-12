# React Development Conventions

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Component Architecture](#component-architecture)
4. [State Management](#state-management)
5. [Styling](#styling)
6. [Performance Optimization](#performance-optimization)
7. [Testing](#testing)
8. [TypeScript Integration](#typescript-integration)
9. [Hooks Usage](#hooks-usage)
10. [Error Handling](#error-handling)
11. [Accessibility](#accessibility)
12. [Security Best Practices](#security-best-practices)
13. [Code Style](#code-style)
14. [Documentation](#documentation)

## Introduction

This document outlines the standard conventions and best practices for React application development at Bayat. These guidelines aim to ensure consistency, maintainability, and scalability across all React projects.

## Project Structure

### Folder Organization

```
src/
├── assets/        # Static files like images, fonts, etc.
├── components/    # Reusable UI components
│   ├── common/    # Shared components across features
│   └── features/  # Feature-specific components
├── config/        # Configuration files
├── contexts/      # React Context definitions
├── hooks/         # Custom React hooks
├── layouts/       # Layout components
├── pages/         # Page components
├── services/      # API services and data fetching
├── store/         # State management (Redux, Zustand, etc.)
├── styles/        # Global styles, themes, variables
├── types/         # TypeScript type definitions
└── utils/         # Utility functions
```

### File Naming

- **Components**: Use PascalCase for component files and directories
  - Example: `Button.tsx`, `UserProfile.tsx`
- **Non-component files**: Use camelCase
  - Example: `useAuth.ts`, `apiService.ts`
- **Test files**: Use the same name as the file they test with `.test` or `.spec` suffix
  - Example: `Button.test.tsx`, `useAuth.spec.ts`
- **Style files**: Use the same name as the component they style
  - Example: `Button.module.css`, `UserProfile.styles.ts`

## Component Architecture

### Component Organization

- Follow the single responsibility principle
- Prefer functional components with hooks over class components
- Break down complex components into smaller, reusable pieces
- Keep components under 250 lines of code when possible

### Component Types

1. **Presentational Components**: Focus on UI and receive data via props
2. **Container Components**: Manage state and data fetching, passing data to presentational components
3. **Layout Components**: Handle structural layout and positioning
4. **Page Components**: Represent entire pages and compose other components
5. **HOCs/Render Props**: For cross-cutting concerns when hooks aren't sufficient

### Props

- Use destructuring for props
- Define prop types with TypeScript interfaces or PropTypes
- Provide default props when applicable
- Keep required props to a minimum
- Use prop spreading sparingly and only when necessary

```tsx
// Good
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'small' | 'medium' | 'large';
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

const Button = ({ 
  variant = 'primary', 
  size = 'medium', 
  label, 
  onClick, 
  disabled = false 
}: ButtonProps) => {
  // Component implementation
};
```

## State Management

### Local State

- Use `useState` for simple component-level state
- Use `useReducer` for complex state logic within a component

### Global State

- For small to medium apps, use React Context with hooks
- For larger applications, consider:
  - Redux (with Redux Toolkit)
  - Zustand
  - Jotai
  - Recoil

### State Management Rules

- Keep state as local as possible
- Lift state up only when necessary
- Use memoization to prevent unnecessary re-renders
- Avoid prop drilling by using context or state management libraries
- Structure state to minimize deep nesting

## Styling

### Approach Options

1. **CSS Modules**: Preferred for component-specific styling
2. **Styled Components/Emotion**: For dynamic styling based on props
3. **Tailwind CSS**: Acceptable for rapid prototyping and consistent design systems
4. **Global CSS**: Only for app-wide styles (reset, variables, typography)

### Styling Guidelines

- Follow responsive design principles
- Use design tokens for colors, spacing, typography
- Create theme variables for light/dark mode
- Implement mobile-first approach
- Avoid inline styles
- Use relative units (rem, em) over pixels when possible

## Performance Optimization

### Key Techniques

- Implement code splitting with dynamic imports
- Use React.memo for expensive pure components
- Apply useMemo and useCallback for referential equality
- Employ virtualization for long lists (react-window, react-virtualized)
- Use image optimization techniques
- Implement lazy loading for components and assets
- Avoid unnecessary re-renders with proper key usage

```tsx
// Good example of React.memo with useCallback
const MemoizedComponent = React.memo(({ onItemClick, items }) => {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id} onClick={() => onItemClick(item.id)}>
          {item.name}
        </li>
      ))}
    </ul>
  );
});

// Parent component
const Parent = () => {
  const [items, setItems] = useState([]);
  
  const handleItemClick = useCallback((id) => {
    // Handle click logic
  }, [/* dependencies */]);
  
  return <MemoizedComponent onItemClick={handleItemClick} items={items} />;
};
```

## Testing

### Testing Levels

1. **Unit Tests**: For individual components and utilities
2. **Integration Tests**: For component interactions
3. **E2E Tests**: For critical user flows

### Testing Libraries

- Jest as the test runner
- React Testing Library for component testing
- Cypress or Playwright for E2E testing
- MSW for API mocking

### Testing Guidelines

- Write tests that mirror user behavior
- Test component behavior, not implementation details
- Aim for meaningful test coverage, not just metrics
- Mock external dependencies
- Use test-driven development when appropriate

```tsx
// Good example of a component test
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
  it('renders with the correct label', () => {
    render(<Button label="Click me" onClick={jest.fn()} />);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
  
  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button label="Click me" onClick={handleClick} />);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

## TypeScript Integration

- Use TypeScript for all new React projects
- Define interfaces for component props, state, and context
- Use discriminated unions for complex state
- Leverage utility types (Partial, Omit, Pick, etc.)
- Create reusable type definitions
- Avoid using `any` and `as` type assertions

```tsx
// Good example of TypeScript usage
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
}

interface UserCardProps {
  user: User;
  onEdit?: (id: string) => void;
  editable?: boolean;
}

const UserCard = ({ user, onEdit, editable = false }: UserCardProps) => {
  // Component implementation
};
```

## Hooks Usage

### Custom Hooks Guidelines

- Extract reusable logic into custom hooks
- Name hooks with 'use' prefix
- Keep hooks focused on a single concern
- Document hook parameters and return values
- Handle errors gracefully within hooks

```tsx
// Good example of a custom hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);
  
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);
  
  return debouncedValue;
}
```

### Built-in Hooks Best Practices

- **useState**: Split complex state into multiple useState calls
- **useEffect**: Specify dependencies accurately to prevent infinite loops
- **useContext**: Create custom hooks to consume context
- **useReducer**: Use for complex state logic
- **useCallback/useMemo**: Apply only when performance optimizations are needed

## Error Handling

- Implement error boundaries for component-level error catching
- Use try/catch for async operations
- Create standardized error display components
- Log errors to monitoring services
- Provide user-friendly error messages
- Implement recovery mechanisms where possible

```tsx
// Error boundary example
class ErrorBoundary extends React.Component {
  state = { hasError: false, error: null };
  
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    // Log to error monitoring service
    logErrorToService(error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorDisplay error={this.state.error} />;
    }
    
    return this.props.children;
  }
}
```

## Accessibility

- Follow WCAG 2.1 AA standards at minimum
- Use semantic HTML elements
- Implement proper keyboard navigation
- Provide ARIA attributes when necessary
- Ensure sufficient color contrast
- Test with screen readers
- Support reduced motion preferences

```tsx
// Good accessibility example
const ActionButton = ({ onClick, label, isDisabled = false }) => {
  return (
    <button
      onClick={onClick}
      disabled={isDisabled}
      aria-disabled={isDisabled}
      aria-label={label}
    >
      {label}
    </button>
  );
};
```

## Security Best Practices

- Sanitize user input
- Prevent XSS via proper escaping
- Use React's built-in protections against injection
- Implement proper authentication and authorization
- Protect against CSRF
- Follow least privilege principle for API calls
- Keep dependencies updated for security patches

## Code Style

- Follow ESLint and Prettier configurations
- Use consistent naming conventions
- Apply functional programming principles where appropriate
- Write self-documenting code
- Keep functions pure when possible
- Use destructuring for props and state
- Apply consistent patterns across the codebase

## Documentation

- Document component props with JSDoc comments
- Create Storybook stories for UI components
- Maintain a component library documentation
- Document complex logic and algorithms
- Keep README files updated
- Include setup instructions for new developers
- Document state management approaches

```tsx
/**
 * Button component for common actions
 * 
 * @param {Object} props - Component props
 * @param {string} props.label - Button text
 * @param {'primary' | 'secondary' | 'tertiary'} [props.variant='primary'] - Visual style variant
 * @param {'small' | 'medium' | 'large'} [props.size='medium'] - Button size
 * @param {() => void} props.onClick - Click handler function
 * @param {boolean} [props.disabled=false] - Whether the button is disabled
 * @param {React.ReactNode} [props.icon] - Optional icon to display
 */
const Button = ({ 
  label, 
  variant = 'primary', 
  size = 'medium', 
  onClick, 
  disabled = false,
  icon
}) => {
  // Implementation
};
``` 