# Frontend Architecture Standards

This document outlines the standards and best practices for frontend architecture across all Bayat projects. Following these guidelines ensures consistency, maintainability, and scalability of frontend applications.

## Table of Contents

- [Core Principles](#core-principles)
- [Application Architecture](#application-architecture)
- [State Management](#state-management)
- [Component Design](#component-design)
- [Code Organization](#code-organization)
- [Performance Optimization](#performance-optimization)
- [Testing Strategy](#testing-strategy)
- [Build and Bundling](#build-and-bundling)
- [Styling Architecture](#styling-architecture)
- [Routing Standards](#routing-standards)
- [API Integration](#api-integration)
- [Security Practices](#security-practices)
- [Accessibility Standards](#accessibility-standards)
- [Internationalization](#internationalization)
- [Error Handling](#error-handling)
- [Monitoring and Analytics](#monitoring-and-analytics)
- [Documentation](#documentation)

## Core Principles

All frontend architectures at Bayat should adhere to these core principles:

1. **Component-Based**: Design systems as composable, reusable components
2. **Single Responsibility**: Each component should do one thing well
3. **Separation of Concerns**: Separate business logic, presentation, and state management
4. **Unidirectional Data Flow**: Data flows in one direction for predictability
5. **Performance First**: Optimize for fast initial load and interaction
6. **Accessibility by Default**: Ensure applications are usable by everyone
7. **Responsive Design**: Applications work across all device sizes
8. **Testable Code**: Architecture supports comprehensive testing
9. **Maintainable**: Code is organized for long-term maintenance
10. **Framework Agnostic Core**: Core business logic should be framework-agnostic where possible

## Application Architecture

### Approved Architecture Patterns

Choose the appropriate architecture pattern based on project requirements:

| Pattern | Best For | Key Characteristics |
|---------|----------|---------------------|
| **Component-Based** | Most applications | Composable, reusable components |
| **Atomic Design** | Design system implementations | Hierarchy of components (atoms, molecules, organisms, etc.) |
| **Micro-Frontend** | Large applications with multiple teams | Independent frontend applications composed together |
| **JAMstack** | Content-heavy applications | JavaScript, APIs, and Markup architecture |
| **Server-Side Rendering** | SEO-critical applications | Render initial HTML on the server |
| **Static Site Generation** | Content sites with infrequent updates | Pre-render pages at build time |

### Reference Architecture

Standard layered architecture for frontend applications:

```
├── UI Layer (Components)
│   ├── Pages/Screens
│   ├── Layouts
│   ├── UI Components
│   └── Design System
├── Application Layer
│   ├── State Management
│   ├── Routing
│   ├── Forms
│   └── Services
├── Domain Layer
│   ├── Business Logic
│   ├── Models/Entities
│   └── Validation
└── Infrastructure Layer
    ├── API Clients
    ├── Storage
    ├── Authentication
    └── Analytics
```

### Technology Selection

Approved frontend technologies:

| Category | Approved Technologies | Notes |
|----------|----------------------|-------|
| **Frameworks** | React, Angular, Vue.js | React preferred for new projects |
| **State Management** | Redux, MobX, Zustand, React Context | Choose based on complexity |
| **CSS Approaches** | CSS Modules, Styled Components, Tailwind CSS | Tailwind preferred for new projects |
| **Build Tools** | Webpack, Vite, Next.js | Vite preferred for new projects |
| **Testing** | Jest, React Testing Library, Cypress | Combination recommended |

## State Management

### State Categories

Organize application state into these categories:

1. **UI State**: Temporary visual states (e.g., open/closed, loading, validation)
2. **Application State**: Session-level state (e.g., current user, theme preferences)
3. **Domain State**: Business data (e.g., products, orders, users)
4. **Server Cache**: Local cache of server data (e.g., API responses)

### State Management Patterns

Choose the appropriate state management pattern based on complexity:

| State Type | Simple Applications | Medium Complexity | High Complexity |
|------------|---------------------|-------------------|-----------------|
| UI State | Component State | Context API | Redux Toolkit |
| Application State | Context API | Context + Hooks | Redux Toolkit |
| Domain State | Context API | React Query/SWR | Redux Toolkit + Middleware |
| Server Cache | Fetch + useEffect | React Query/SWR | Redux Toolkit Query |

### State Management Best Practices

1. **Minimize State**: Store only necessary data in state
2. **Single Source of Truth**: Avoid duplicating state
3. **Immutability**: Never directly mutate state
4. **Normalize Complex Data**: Flatten nested data structures
5. **Colocation**: Keep state close to where it's used
6. **Persistence**: Use local storage for persistent state
7. **Hydration**: Restore state on page reload when needed

## Component Design

### Component Hierarchy

Organize components in a clear hierarchy:

1. **Page Components**: Represent entire pages/routes
2. **Container Components**: Manage data and state
3. **Feature Components**: Implement specific features
4. **UI Components**: Reusable UI elements
5. **Design System Components**: Primitive UI components

### Component Guidelines

1. **Props Interface**: Define clear prop interfaces for all components
2. **Prop Validation**: Validate all component props
3. **Default Props**: Provide sensible defaults
4. **Composition**: Favor composition over inheritance
5. **Pure Components**: Make components pure where possible
6. **Memoization**: Use memoization for expensive calculations
7. **Error Boundaries**: Implement error boundaries for fault isolation

### Component Example (React)

```tsx
// Button.tsx
import React, { memo } from 'react';
import classNames from 'classnames';
import './Button.css';

export type ButtonVariant = 'primary' | 'secondary' | 'tertiary';
export type ButtonSize = 'small' | 'medium' | 'large';

export interface ButtonProps {
  /** Button label content */
  children: React.ReactNode;
  /** Visual variant of the button */
  variant?: ButtonVariant;
  /** Size of the button */
  size?: ButtonSize;
  /** Disabled state */
  disabled?: boolean;
  /** Click handler */
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  /** Additional class names */
  className?: string;
  /** Button type attribute */
  type?: 'button' | 'submit' | 'reset';
}

/**
 * Primary button component for user interaction
 */
const Button = ({
  children,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  onClick,
  className,
  type = 'button',
  ...rest
}: ButtonProps) => {
  return (
    <button
      type={type}
      className={classNames(
        'btn',
        `btn--${variant}`,
        `btn--${size}`,
        { 'btn--disabled': disabled },
        className
      )}
      disabled={disabled}
      onClick={onClick}
      {...rest}
    >
      {children}
    </button>
  );
};

// Use memo for performance optimization
export default memo(Button);
```

## Code Organization

### Project Structure

Follow this standard project structure:

```
src/
├── assets/              # Static assets
├── components/          # Shared components
│   ├── ui/              # UI components
│   └── features/        # Feature components
├── config/              # Application configuration
├── hooks/               # Custom hooks
├── layouts/             # Page layouts
├── pages/               # Page components
├── services/            # External service integrations
├── store/               # State management
├── styles/              # Global styles
├── types/               # TypeScript type definitions
├── utils/               # Utility functions
├── App.tsx              # Application root
└── main.tsx             # Entry point
```

### Feature-Based Organization

For larger applications, consider a feature-based structure:

```
src/
├── common/             # Shared code
│   ├── components/     # Shared components
│   ├── hooks/          # Shared hooks
│   └── utils/          # Shared utilities
├── features/           # Feature modules
│   ├── auth/           # Authentication feature
│   │   ├── components/ # Feature-specific components
│   │   ├── hooks/      # Feature-specific hooks
│   │   ├── services/   # Feature-specific services
│   │   ├── store/      # Feature-specific state
│   │   └── index.ts    # Feature entry point
│   ├── products/       # Products feature
│   └── checkout/       # Checkout feature
├── layouts/            # Application layouts
├── pages/              # Route pages
├── store/              # Root store configuration
├── App.tsx             # Application root
└── main.tsx            # Entry point
```

### Naming Conventions

Use consistent naming conventions:

- **Files**: PascalCase for components, camelCase for utilities
- **Components**: PascalCase (e.g., `Button.tsx`)
- **Hooks**: camelCase with `use` prefix (e.g., `useAuth.ts`)
- **Context**: PascalCase with `Context` suffix (e.g., `AuthContext.tsx`)
- **Constants**: UPPER_SNAKE_CASE
- **Types/Interfaces**: PascalCase with descriptive names
- **CSS Modules**: Same name as component with `.module.css` extension

## Performance Optimization

### Performance Metrics

Track these key performance metrics:

1. **First Contentful Paint (FCP)**: Under 1.8s
2. **Largest Contentful Paint (LCP)**: Under 2.5s
3. **First Input Delay (FID)**: Under 100ms
4. **Cumulative Layout Shift (CLS)**: Under 0.1
5. **Time to Interactive (TTI)**: Under 3.8s
6. **Total Blocking Time (TBT)**: Under 200ms

### Performance Optimization Techniques

Implement these optimization strategies:

1. **Code Splitting**: Split code by routes and large components
2. **Lazy Loading**: Defer loading of non-critical resources
3. **Tree Shaking**: Eliminate unused code
4. **Bundle Analysis**: Regularly analyze bundle size
5. **Resource Optimization**: Optimize images and assets
6. **Caching Strategy**: Implement effective caching
7. **Critical CSS**: Inline critical CSS
8. **Web Vitals Monitoring**: Monitor core web vitals

### Example Code Splitting (React)

```tsx
import React, { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import Loading from './components/Loading';

// Lazy load route components
const Home = lazy(() => import('./pages/Home'));
const Products = lazy(() => import('./pages/Products'));
const ProductDetail = lazy(() => import('./pages/ProductDetail'));
const Checkout = lazy(() => import('./pages/Checkout'));

const App = () => {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
        <Route path="/products/:id" element={<ProductDetail />} />
        <Route path="/checkout" element={<Checkout />} />
      </Routes>
    </Suspense>
  );
};
```

## Testing Strategy

### Testing Levels

Implement comprehensive testing across these levels:

1. **Unit Tests**: Test individual components and functions
2. **Integration Tests**: Test interactions between components
3. **Component Tests**: Test component rendering and behavior
4. **End-to-End Tests**: Test complete user flows
5. **Visual Regression Tests**: Test UI appearance
6. **Performance Tests**: Test loading and runtime performance
7. **Accessibility Tests**: Test for accessibility compliance

### Testing Coverage Standards

Maintain these minimum test coverage levels:

- **Core Components**: 90% statement coverage
- **Business Logic**: 90% statement coverage
- **Utility Functions**: 95% statement coverage
- **UI Components**: Key interactions and states tested
- **Critical User Flows**: 100% end-to-end test coverage

### Testing Examples

Unit test example (Jest + React Testing Library):

```tsx
// Button.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button component', () => {
  test('renders with default props', () => {
    render(<Button>Click me</Button>);
    const button = screen.getByRole('button', { name: /click me/i });
    
    expect(button).toBeInTheDocument();
    expect(button).toHaveClass('btn btn--primary btn--medium');
    expect(button).not.toBeDisabled();
  });
  
  test('applies variant and size classes', () => {
    render(<Button variant="secondary" size="large">Submit</Button>);
    const button = screen.getByRole('button', { name: /submit/i });
    
    expect(button).toHaveClass('btn btn--secondary btn--large');
  });
  
  test('handles click events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    fireEvent.click(screen.getByRole('button', { name: /click me/i }));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
  
  test('disables the button when disabled prop is true', () => {
    render(<Button disabled>Disabled</Button>);
    const button = screen.getByRole('button', { name: /disabled/i });
    
    expect(button).toBeDisabled();
    expect(button).toHaveClass('btn--disabled');
  });
});
```

## Build and Bundling

### Build Tools

Standardize on these build tools:

- **Vite**: For new React/Vue projects
- **Next.js**: For React applications requiring SSR/SSG
- **Angular CLI**: For Angular applications
- **Webpack**: For complex custom configurations

### Build Configuration

Implement these build optimizations:

1. **Environment-Specific Builds**: Configure for dev, staging, production
2. **Minification**: Minify JavaScript, CSS, and HTML
3. **Source Maps**: Generate source maps for debugging
4. **Asset Optimization**: Optimize and compress assets
5. **Chunking Strategy**: Optimize chunk sizes and loading
6. **Cache Busting**: Implement filename hashing
7. **Build Analysis**: Analyze build output regularly

### Example Vite Configuration

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { visualizer } from 'rollup-plugin-visualizer';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'robots.txt', 'apple-touch-icon.png'],
      manifest: {
        name: 'Bayat Application',
        short_name: 'BayatApp',
        theme_color: '#ffffff',
        icons: [
          // Icons configuration
        ]
      }
    }),
    visualizer({
      open: false,
      gzipSize: true,
      brotliSize: true,
    })
  ],
  build: {
    target: 'es2015',
    outDir: 'dist',
    assetsDir: 'assets',
    cssCodeSplit: true,
    reportCompressedSize: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          // Additional chunk definitions
        },
      },
    },
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
});
```

## Styling Architecture

### CSS Methodologies

Choose the appropriate CSS methodology based on project needs:

| Methodology | Best For | Key Benefits |
|-------------|----------|-------------|
| **CSS Modules** | Component-based apps | Local scope, composition |
| **Styled Components** | React applications | Dynamic styling, theme support |
| **Tailwind CSS** | Rapid development | Utility-first, consistency |
| **SCSS with BEM** | Large applications | Structure, readability |

### Design System Integration

Implement a consistent design system:

1. **Design Tokens**: Use design tokens for colors, spacing, typography
2. **Component Library**: Build on a shared component library
3. **Theme Support**: Implement light/dark and brand theming
4. **Responsive Design**: Use a consistent approach to responsiveness
5. **Documentation**: Maintain living documentation of the design system

### Example Tailwind Configuration

```javascript
// tailwind.config.js
const colors = require('tailwindcss/colors');

module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          // ... other shades
          900: '#0c4a6e',
        },
        secondary: {
          // Secondary color palette
        },
        // Other brand colors
      },
      fontFamily: {
        sans: ['Inter var', 'sans-serif'],
        display: ['Lexend', 'sans-serif'],
      },
      spacing: {
        // Custom spacing values
      },
      borderRadius: {
        // Custom border radius values
      },
      // Other theme extensions
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
};
```

## Routing Standards

### Routing Patterns

Implement consistent routing patterns:

1. **Declarative Routes**: Define routes declaratively
2. **Nested Routes**: Use nested routes for related content
3. **Route Parameters**: Use consistent parameter patterns
4. **Query Parameters**: Use for filtering and sorting
5. **Route Guards**: Implement authentication and authorization checks
6. **Code Splitting**: Split code by route
7. **Route Transitions**: Add smooth transitions between routes

### URL Structure

Follow these URL structure guidelines:

- Use kebab-case for URL paths
- Use descriptive, resource-focused paths
- Follow RESTful patterns where appropriate
- Keep URLs reasonably short but descriptive
- Include language in URL for multilingual sites
- Use query parameters for filtering, not URL paths

Examples:
```
/products                      # Product listing
/products/category/electronics # Category filtering
/products/123-smartphone-x     # Product detail with slug
/users/profile                 # User profile
/checkout/shipping             # Multi-step process
```

### Example React Router Configuration

```tsx
// routes.tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { lazy, Suspense } from 'react';
import MainLayout from './layouts/MainLayout';
import LoadingPage from './components/LoadingPage';
import ErrorBoundary from './components/ErrorBoundary';
import ProtectedRoute from './components/ProtectedRoute';

// Lazy-loaded route components
const Home = lazy(() => import('./pages/Home'));
const ProductList = lazy(() => import('./pages/ProductList'));
const ProductDetail = lazy(() => import('./pages/ProductDetail'));
const UserProfile = lazy(() => import('./pages/UserProfile'));
const Checkout = lazy(() => import('./pages/Checkout'));
const NotFound = lazy(() => import('./pages/NotFound'));

const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    errorElement: <ErrorBoundary />,
    children: [
      { index: true, element: <Home /> },
      { 
        path: 'products',
        children: [
          { index: true, element: <ProductList /> },
          { path: ':productId', element: <ProductDetail /> }
        ]
      },
      { 
        path: 'profile',
        element: (
          <ProtectedRoute>
            <UserProfile />
          </ProtectedRoute>
        )
      },
      { 
        path: 'checkout',
        element: (
          <ProtectedRoute>
            <Checkout />
          </ProtectedRoute>
        )
      },
      { path: '*', element: <NotFound /> }
    ]
  }
]);

const Routes = () => (
  <Suspense fallback={<LoadingPage />}>
    <RouterProvider router={router} />
  </Suspense>
);

export default Routes;
```

## API Integration

### API Client Architecture

Implement a structured API client:

1. **Base Client**: Create a configurable base API client
2. **Service Modules**: Organize by domain/resource
3. **Request/Response Types**: Define strong types
4. **Error Handling**: Implement consistent error handling
5. **Caching Strategy**: Define caching behavior
6. **Authentication**: Handle auth tokens and refreshing
7. **Interceptors**: Implement request/response interceptors
8. **Retry Logic**: Add intelligent retry for failed requests

### API Client Example

```typescript
// api/client.ts
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { getAuthToken, refreshToken } from '../auth/authService';

export class ApiClient {
  private client: AxiosInstance;
  private baseURL: string;
  
  constructor(baseURL: string) {
    this.baseURL = baseURL;
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    this.setupInterceptors();
  }
  
  private setupInterceptors(): void {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        const token = getAuthToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );
    
    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config;
        
        // Handle token refresh
        if (error.response?.status === 401 && !originalRequest.headers['X-Retry']) {
          originalRequest.headers['X-Retry'] = 'true';
          
          try {
            await refreshToken();
            return this.client(originalRequest);
          } catch (refreshError) {
            // Handle auth refresh failure
            return Promise.reject(refreshError);
          }
        }
        
        return Promise.reject(error);
      }
    );
  }
  
  // Generic request method
  public async request<T>(config: AxiosRequestConfig): Promise<T> {
    try {
      const response: AxiosResponse<T> = await this.client(config);
      return response.data;
    } catch (error) {
      this.handleError(error as AxiosError);
      throw error;
    }
  }
  
  // Convenience methods
  public async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.request<T>({ ...config, method: 'GET', url });
  }
  
  public async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return this.request<T>({ ...config, method: 'POST', url, data });
  }
  
  public async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return this.request<T>({ ...config, method: 'PUT', url, data });
  }
  
  public async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.request<T>({ ...config, method: 'DELETE', url });
  }
  
  private handleError(error: AxiosError): void {
    // Centralized error handling
    if (error.response) {
      // Server responded with non-2xx status
      console.error('API Error:', error.response.status, error.response.data);
    } else if (error.request) {
      // Request was made but no response received
      console.error('Network Error:', error.message);
    } else {
      // Error in setting up the request
      console.error('Request Error:', error.message);
    }
  }
}

// Create API instances
export const mainApi = new ApiClient(import.meta.env.VITE_API_URL);
```

### Data Fetching Patterns

Use these data fetching patterns:

1. **Custom Hooks**: Encapsulate API calls in custom hooks
2. **SWR/React Query**: Use data fetching libraries for caching
3. **Server State vs. UI State**: Separate API data from UI state
4. **Optimistic Updates**: Update UI before API responses
5. **Error Boundaries**: Handle API errors gracefully
6. **Loading States**: Show appropriate loading indicators

## Security Practices

### Frontend Security Checklist

Implement these security measures:

1. **XSS Prevention**: Sanitize data and use frameworks' protections
2. **CSRF Protection**: Implement CSRF tokens
3. **Content Security Policy**: Configure strict CSP
4. **Secure Authentication**: Use secure auth practices
5. **HTTPS Only**: Enforce HTTPS for all communication
6. **Sensitive Data**: Don't store sensitive data in localStorage/sessionStorage
7. **Input Validation**: Validate all user inputs
8. **Dependency Security**: Regularly audit and update dependencies
9. **Feature Policy**: Use feature policy headers
10. **Subresource Integrity**: Verify third-party resources

### Authentication Best Practices

1. **Token Storage**: Store tokens securely (HttpOnly cookies preferred)
2. **Token Rotation**: Implement token rotation
3. **Session Timeout**: Implement automatic session timeouts
4. **Logout Functionality**: Properly clear authentication state
5. **Auth State Management**: Centralize auth state management
6. **Multi-factor Authentication**: Support 2FA where appropriate

## Accessibility Standards

### WCAG Compliance

Ensure compliance with WCAG 2.1 AA standards:

1. **Perceivable**: Information must be presentable to users in ways they can perceive
2. **Operable**: User interface components must be operable
3. **Understandable**: Information and operation must be understandable
4. **Robust**: Content must be robust enough to be interpreted by a wide variety of user agents

### Accessibility Requirements

Implement these accessibility features:

1. **Semantic HTML**: Use proper HTML elements
2. **ARIA Attributes**: Use ARIA when HTML semantics are insufficient
3. **Keyboard Navigation**: Ensure full keyboard operability
4. **Focus Management**: Implement proper focus management
5. **Color Contrast**: Maintain sufficient color contrast
6. **Screen Reader Support**: Test with screen readers
7. **Alternative Text**: Provide alt text for images
8. **Form Labels**: Associate labels with form elements
9. **Error Identification**: Clearly identify form errors

### Accessibility Testing

Test accessibility using:

1. **Automated Tools**: Lighthouse, axe, Wave
2. **Manual Testing**: Keyboard navigation, screen readers
3. **Contrast Checkers**: WCAG contrast checkers
4. **Accessibility Review**: Regular expert review

## Internationalization

### I18n Implementation

Implement comprehensive internationalization:

1. **Translation System**: Use a robust translation system
2. **Message Format**: Support pluralization and formatting
3. **RTL Support**: Support right-to-left languages
4. **Date/Time Format**: Format dates and times by locale
5. **Number Format**: Format numbers by locale
6. **Content Expansion**: Allow for text expansion in translations
7. **Dynamic Content**: Support translating dynamic content

### Example React-i18next Configuration

```typescript
// i18n.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import Backend from 'i18next-http-backend';

i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    supportedLngs: ['en', 'fr', 'es', 'de', 'ar'],
    ns: ['common', 'auth', 'products', 'checkout'],
    defaultNS: 'common',
    interpolation: {
      escapeValue: false, // React already escapes values
    },
    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },
    detection: {
      order: ['querystring', 'cookie', 'localStorage', 'navigator'],
      lookupQuerystring: 'lang',
      lookupCookie: 'i18next',
      lookupLocalStorage: 'i18nextLng',
      caches: ['localStorage', 'cookie'],
    },
    react: {
      useSuspense: true,
    },
  });

export default i18n;
```

## Error Handling

### Error Handling Strategy

Implement a comprehensive error handling strategy:

1. **Global Error Boundary**: Catch uncaught errors
2. **API Error Handling**: Standardize API error processing
3. **User Feedback**: Provide clear error messages to users
4. **Error Logging**: Log errors for debugging
5. **Retry Mechanism**: Implement retries for transient failures
6. **Graceful Degradation**: Maintain functionality when parts fail
7. **Error Recovery**: Provide pathways to recover from errors

### Example Error Boundary

```tsx
// ErrorBoundary.tsx
import React, { Component, ErrorInfo, ReactNode } from 'react';
import { logError } from '../services/errorLoggingService';
import ErrorFallback from './ErrorFallback';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
    };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    // Log error to service
    logError(error, errorInfo);
  }

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }
      return <ErrorFallback error={this.state.error} />;
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

## Monitoring and Analytics

### Frontend Monitoring

Implement comprehensive frontend monitoring:

1. **Error Tracking**: Capture and report frontend errors
2. **Performance Monitoring**: Track page load and interaction metrics
3. **User Behavior**: Analyze user flows and interactions
4. **Session Recording**: Record user sessions for debugging
5. **Feature Usage**: Track feature adoption and usage
6. **Console Logs**: Forward console errors to monitoring system

### Analytics Implementation

Standardize analytics implementation:

1. **Event Tracking**: Define a consistent event taxonomy
2. **User Identification**: Identify users across sessions
3. **Conversion Tracking**: Track key conversion steps
4. **Custom Dimensions**: Define business-specific dimensions
5. **Data Layer**: Implement a structured data layer
6. **Privacy Compliance**: Ensure GDPR/CCPA compliance

### Example Error Monitoring Setup

```typescript
// monitoring.ts
import * as Sentry from '@sentry/react';
import { BrowserTracing } from '@sentry/tracing';
import { ErrorBoundary } from '@sentry/react';

export const initMonitoring = () => {
  if (import.meta.env.PROD) {
    Sentry.init({
      dsn: import.meta.env.VITE_SENTRY_DSN,
      integrations: [new BrowserTracing()],
      tracesSampleRate: 0.2,
      environment: import.meta.env.MODE,
      release: `${import.meta.env.VITE_APP_NAME}@${import.meta.env.VITE_APP_VERSION}`,
      beforeSend(event) {
        // Clean sensitive data if needed
        return event;
      },
    });
  }
};

export { ErrorBoundary as SentryErrorBoundary };

// Custom analytics hooks
export const useAnalytics = () => {
  const trackEvent = (category: string, action: string, label?: string, value?: number) => {
    // Implementation with your analytics provider
    if (window.gtag) {
      window.gtag('event', action, {
        event_category: category,
        event_label: label,
        value: value,
      });
    }
  };
  
  return { trackEvent };
};
```

## Documentation

### Documentation Types

Maintain these documentation types:

1. **Architecture Overview**: High-level architecture documentation
2. **Component Documentation**: Component API and usage
3. **Style Guide**: Visual style guide and design system
4. **State Management**: State structure and management patterns
5. **API Integration**: API endpoints and data models
6. **Coding Standards**: Frontend coding standards and patterns

### Documentation Tools

Use these tools for documentation:

1. **Storybook**: Component documentation and testing
2. **JSDoc/TSDoc**: Code-level documentation
3. **Markdown**: General documentation
4. **Diagrams**: Architecture and flow diagrams
5. **README Files**: Project and directory documentation

### Example Storybook Setup

```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import Button from './Button';

const meta: Meta<typeof Button> = {
  title: 'UI/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: { 
      control: { type: 'select' }, 
      options: ['primary', 'secondary', 'tertiary'] 
    },
    size: { 
      control: { type: 'select' }, 
      options: ['small', 'medium', 'large'] 
    },
    disabled: { control: 'boolean' },
    onClick: { action: 'clicked' },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Button',
    size: 'medium',
  },
};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button',
    size: 'medium',
  },
};

export const Small: Story = {
  args: {
    size: 'small',
    children: 'Small Button',
  },
};

export const Large: Story = {
  args: {
    size: 'large',
    children: 'Large Button',
  },
};

export const Disabled: Story = {
  args: {
    disabled: true,
    children: 'Disabled Button',
  },
};
``` 