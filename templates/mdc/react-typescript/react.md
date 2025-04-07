# React Development Conventions

## Component Structure

- Use functional components with hooks
- One component per file
- Keep components small and focused on a single responsibility
- Follow naming pattern: `ComponentName.tsx`

## Prop Definitions

- Use TypeScript interfaces for component props
- Name prop interfaces following the pattern: `IComponentNameProps`
- Destructure props in function parameters
- Provide default values for optional props

```typescript
interface IButtonProps {
  text: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

const Button = ({ text, onClick, variant = 'primary' }: IButtonProps) => {
  // Component implementation
};
```

## Hooks Usage

- Follow the Rules of Hooks
- Custom hooks should be prefixed with `use`
- Extract complex logic into custom hooks
- Keep `useEffect` dependencies explicit and complete

## React Best Practices

- Use React fragments to avoid unnecessary divs
- Use keys derived from data, not indexes, in lists
- Memoize callbacks with useCallback for child components
- Memoize expensive calculations with useMemo
- Utilize React.memo for pure components
- Implement accessibility best practices (e.g., semantic HTML, ARIA attributes)

## State Management

- Use local state (useState) for component-specific state
- Use context for shared state across components
- Prefer composition over deep prop drilling
- Consider state management libraries for complex applications

## Event Handling

- Name handlers with the pattern: `handleEventName`
- Prefer inline arrow functions for simple handlers
- Use useCallback for handlers passed to child components

## Performance Considerations

- Lazy load components with React.lazy and Suspense
- Use windowing for long lists (react-window or react-virtualized)
- Avoid unnecessary re-renders by memoizing components and callbacks
- Profile component performance using React DevTools
