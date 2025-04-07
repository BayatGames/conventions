<!--
Document: Frontend Testing Best Practices
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Frontend Testing Best Practices

This document outlines the standards, strategies, and best practices for frontend testing across all Bayat projects.

## Table of Contents

- [Introduction](#introduction)
- [Testing Pyramid](#testing-pyramid)
- [Types of Frontend Tests](#types-of-frontend-tests)
- [Unit Testing](#unit-testing)
- [Component Testing](#component-testing)
- [Integration Testing](#integration-testing)
- [End-to-End Testing](#end-to-end-testing)
- [Visual Regression Testing](#visual-regression-testing)
- [Accessibility Testing](#accessibility-testing)
- [Performance Testing](#performance-testing)
- [Test-Driven Development](#test-driven-development)
- [Testing Frameworks and Tools](#testing-frameworks-and-tools)
- [Mocking and Stubbing](#mocking-and-stubbing)
- [Test Environment Management](#test-environment-management)
- [Continuous Integration](#continuous-integration)
- [Test Coverage](#test-coverage)
- [Testing Legacy Code](#testing-legacy-code)
- [Mobile-Specific Considerations](#mobile-specific-considerations)
- [Common Anti-Patterns](#common-anti-patterns)
- [Framework-Specific Guidelines](#framework-specific-guidelines)

## Introduction

Effective frontend testing is crucial for delivering reliable, maintainable, and high-quality user interfaces. This document provides comprehensive guidance on frontend testing approaches, tools, and best practices to ensure consistent quality across Bayat projects.

### Objectives of Frontend Testing

- **Prevent Regressions**: Ensure new changes don't break existing functionality
- **Verify Requirements**: Confirm implementation meets specified requirements
- **Improve Code Quality**: Encourage better design and implementation patterns
- **Document Behavior**: Tests serve as executable documentation
- **Support Refactoring**: Enable safe code changes and improvements
- **Increase Confidence**: Provide confidence in the codebase for developers

## Testing Pyramid

The testing pyramid provides a framework for balancing different types of tests:

```
    /\
   /  \
  /E2E \
 /------\
/  Integ  \
/----------\
/ Component  \
/--------------\
/     Unit      \
------------------
```

### Distribution Guidelines

Aim for this approximate distribution of tests:

- **Unit Tests**: 70% (fastest, most numerous)
- **Component Tests**: 20% (isolated component verification)
- **Integration Tests**: 8% (verify interactions between components)
- **End-to-End Tests**: 2% (validate complete user flows)

This distribution balances coverage, maintenance overhead, and execution speed.

## Types of Frontend Tests

### Overview of Test Types

| Test Type | Scope | Speed | Brittleness | Confidence | Purpose |
|-----------|-------|-------|-------------|------------|---------|
| Unit | Single function/class | Very fast | Low | Lower | Verify logic in isolation |
| Component | Individual UI components | Fast | Low-Medium | Medium | Verify component behavior |
| Integration | Multiple components | Medium | Medium | Medium-High | Verify component interactions |
| E2E | Complete flows | Slow | High | High | Verify user journeys |
| Visual | UI appearance | Medium | Medium-High | Medium | Detect UI changes |
| Accessibility | Compliance | Medium | Low | Medium | Verify accessibility |
| Performance | Speed/resource usage | Varies | Medium | Medium | Verify performance metrics |

Each type serves a specific purpose and all are necessary for comprehensive testing.

## Unit Testing

Unit tests verify that individual functions, methods, or classes work as expected in isolation.

### What to Unit Test

- Pure functions
- Business logic
- Utility functions
- State management (reducers, selectors)
- Complex algorithms
- Edge cases and error handling

### Unit Testing Best Practices

1. **Test in Isolation**: Mock dependencies to isolate the code under test
2. **Test Behavior, Not Implementation**: Focus on inputs and outputs, not how it works
3. **Small, Focused Tests**: Each test should verify one specific aspect
4. **Descriptive Test Names**: Name tests to describe what they verify
5. **Arrange, Act, Assert**: Structure tests with clear setup, execution, and verification
6. **Cover Edge Cases**: Test boundary conditions and error scenarios

### Example Unit Test (JavaScript with Jest)

```javascript
// Function to test
export function calculateTotal(items, discountCode) {
  let total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  
  if (discountCode === 'SAVE10') {
    total = total * 0.9;
  }
  
  return total;
}

// Unit test
describe('calculateTotal', () => {
  it('should calculate total price of all items', () => {
    // Arrange
    const items = [
      { name: 'Item 1', price: 10, quantity: 2 },
      { name: 'Item 2', price: 15, quantity: 1 }
    ];
    
    // Act
    const result = calculateTotal(items);
    
    // Assert
    expect(result).toBe(35);
  });
  
  it('should apply 10% discount with SAVE10 code', () => {
    // Arrange
    const items = [
      { name: 'Item 1', price: 10, quantity: 2 },
      { name: 'Item 2', price: 15, quantity: 1 }
    ];
    
    // Act
    const result = calculateTotal(items, 'SAVE10');
    
    // Assert
    expect(result).toBe(31.5);
  });
  
  it('should handle empty item list', () => {
    // Arrange
    const items = [];
    
    // Act
    const result = calculateTotal(items);
    
    // Assert
    expect(result).toBe(0);
  });
});
```

## Component Testing

Component tests verify that UI components render correctly and behave as expected.

### What to Test in Components

- **Rendering**: Component renders correctly with default/various props
- **User Interactions**: Component responds correctly to user actions
- **State Changes**: Component updates correctly when state changes
- **Props**: Component handles different prop values appropriately
- **Conditional Rendering**: Features appear/disappear based on conditions
- **Error States**: Component handles errors gracefully

### Component Testing Best Practices

1. **Isolate the Component**: Test the component in isolation, mocking dependencies
2. **Test Rendering**: Verify the component renders correctly with different props
3. **Test User Interactions**: Simulate user events and verify expected behavior
4. **Snapshot Testing**: Use sparingly for stable components only
5. **Accessibility Tests**: Include accessibility checks in component tests
6. **Mock External Dependencies**: Use mocks for API calls, stores, etc.

### Example Component Test (React with React Testing Library)

```javascript
// Component to test
function Counter({ initialCount = 0 }) {
  const [count, setCount] = useState(initialCount);
  
  return (
    <div>
      <p data-testid="count-display">Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setCount(count - 1)}>Decrement</button>
    </div>
  );
}

// Component test
describe('Counter', () => {
  it('should render with initial count', () => {
    // Arrange & Act
    const { getByTestId } = render(<Counter initialCount={5} />);
    
    // Assert
    expect(getByTestId('count-display')).toHaveTextContent('Count: 5');
  });
  
  it('should increment count when increment button is clicked', () => {
    // Arrange
    const { getByTestId, getByText } = render(<Counter initialCount={5} />);
    
    // Act
    fireEvent.click(getByText('Increment'));
    
    // Assert
    expect(getByTestId('count-display')).toHaveTextContent('Count: 6');
  });
  
  it('should decrement count when decrement button is clicked', () => {
    // Arrange
    const { getByTestId, getByText } = render(<Counter initialCount={5} />);
    
    // Act
    fireEvent.click(getByText('Decrement'));
    
    // Assert
    expect(getByTestId('count-display')).toHaveTextContent('Count: 4');
  });
});
```

## Integration Testing

Integration tests verify that multiple components work together correctly.

### What to Test in Integration Tests

- **Component Composition**: Multiple components working together
- **Data Flow**: Data passing correctly between components
- **State Management**: Components interact correctly with shared state
- **Routing**: Navigation and URL-based functionality
- **Form Submissions**: Complete form flows
- **Error Handling**: Cross-component error cases

### Integration Testing Best Practices

1. **Focus on Component Interfaces**: Test how components interact with each other
2. **Test User Workflows**: Verify complete user scenarios
3. **Minimize Mocks**: Use real implementations where practical
4. **Setup Test Environment**: Provide realistic context like routing or state providers
5. **Test Boundary Cases**: Verify error handling between components

### Example Integration Test (React with React Testing Library)

```javascript
// Components to test
function SearchForm({ onSearch }) {
  const [query, setQuery] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input 
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
        data-testid="search-input"
      />
      <button type="submit">Search</button>
    </form>
  );
}

function SearchResults({ results }) {
  if (results.length === 0) {
    return <p>No results found</p>;
  }
  
  return (
    <ul data-testid="results-list">
      {results.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}

function SearchPage() {
  const [results, setResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  
  const handleSearch = async (query) => {
    setIsSearching(true);
    try {
      const data = await searchApi(query);
      setResults(data);
    } catch (error) {
      console.error(error);
      setResults([]);
    } finally {
      setIsSearching(false);
    }
  };
  
  return (
    <div>
      <SearchForm onSearch={handleSearch} />
      {isSearching ? (
        <p>Loading...</p>
      ) : (
        <SearchResults results={results} />
      )}
    </div>
  );
}

// Integration test
describe('SearchPage', () => {
  it('should display search results when search is performed', async () => {
    // Mock API
    jest.spyOn(global, 'searchApi').mockResolvedValue([
      { id: 1, name: 'Result 1' },
      { id: 2, name: 'Result 2' }
    ]);
    
    // Arrange
    const { getByPlaceholderText, getByText, getByTestId } = render(<SearchPage />);
    
    // Act - Enter search query
    const input = getByPlaceholderText('Search...');
    fireEvent.change(input, { target: { value: 'test query' } });
    
    // Act - Submit form
    fireEvent.click(getByText('Search'));
    
    // Assert - Loading state
    expect(getByText('Loading...')).toBeInTheDocument();
    
    // Wait for results
    await waitForElementToBeRemoved(() => getByText('Loading...'));
    
    // Assert - Results displayed
    const resultsList = getByTestId('results-list');
    expect(resultsList).toBeInTheDocument();
    expect(getByText('Result 1')).toBeInTheDocument();
    expect(getByText('Result 2')).toBeInTheDocument();
  });
  
  it('should display "No results found" when search returns empty', async () => {
    // Mock API
    jest.spyOn(global, 'searchApi').mockResolvedValue([]);
    
    // Arrange
    const { getByPlaceholderText, getByText } = render(<SearchPage />);
    
    // Act - Enter search query and submit
    const input = getByPlaceholderText('Search...');
    fireEvent.change(input, { target: { value: 'no results' } });
    fireEvent.click(getByText('Search'));
    
    // Wait for loading to finish
    await waitForElementToBeRemoved(() => getByText('Loading...'));
    
    // Assert
    expect(getByText('No results found')).toBeInTheDocument();
  });
});
```

## End-to-End Testing

End-to-End (E2E) tests verify complete user journeys by simulating real user interactions with the application.

### What to Test with E2E

- **Critical User Flows**: Key paths users take through the application
- **Happy Paths**: Verify standard successful scenarios
- **Authentication Flows**: Login, logout, registration
- **Payment Processes**: Complete checkout processes
- **Multi-page Workflows**: Processes spanning multiple pages

### E2E Testing Best Practices

1. **Focus on Critical Paths**: Test the most important user journeys
2. **Minimize E2E Tests**: Keep the number of E2E tests manageable
3. **Test in Production-like Environment**: Use environments that mirror production
4. **Handle Asynchronous Operations**: Account for loading times, animations, etc.
5. **Use Stable Selectors**: Use data-testid or other stable attributes for selectors
6. **Manage Test Data**: Create, use, and clean up test data appropriately
7. **Include Cross-browser Testing**: Test on key browser/device combinations

### Example E2E Test (using Cypress)

```javascript
// E2E test for user authentication and dashboard access
describe('User Authentication', () => {
  beforeEach(() => {
    // Clear cookies and localStorage before each test
    cy.clearCookies();
    cy.clearLocalStorage();
  });

  it('should allow user to log in and access dashboard', () => {
    // Visit the login page
    cy.visit('/login');
    
    // Verify login form is displayed
    cy.get('[data-testid="login-form"]').should('be.visible');
    
    // Enter credentials
    cy.get('[data-testid="email-input"]').type('test@example.com');
    cy.get('[data-testid="password-input"]').type('password123');
    
    // Submit form
    cy.get('[data-testid="login-button"]').click();
    
    // Verify redirect to dashboard
    cy.url().should('include', '/dashboard');
    
    // Verify dashboard elements
    cy.get('[data-testid="user-greeting"]').should('contain', 'Welcome, Test User');
    cy.get('[data-testid="dashboard-stats"]').should('be.visible');
    
    // Test logout functionality
    cy.get('[data-testid="logout-button"]').click();
    
    // Verify redirect to login page
    cy.url().should('include', '/login');
  });
  
  it('should show error message with invalid credentials', () => {
    // Visit the login page
    cy.visit('/login');
    
    // Enter invalid credentials
    cy.get('[data-testid="email-input"]').type('test@example.com');
    cy.get('[data-testid="password-input"]').type('wrongpassword');
    
    // Submit form
    cy.get('[data-testid="login-button"]').click();
    
    // Verify error message
    cy.get('[data-testid="login-error"]')
      .should('be.visible')
      .and('contain', 'Invalid email or password');
    
    // Verify still on login page
    cy.url().should('include', '/login');
  });
});
```

## Visual Regression Testing

Visual regression tests detect unintended changes to the UI appearance by comparing screenshots.

### What to Test with Visual Regression

- **Key UI Components**: Core UI elements that should remain consistent
- **Responsive Layouts**: UI appearance across different screen sizes
- **Theme Variations**: Light/dark mode and other theme options
- **Dynamic Content Areas**: Areas that change based on data
- **State Variations**: Different states of components (loading, error, empty, etc.)

### Visual Regression Testing Best Practices

1. **Baseline Management**: Carefully manage baseline images
2. **Component Focus**: Test individual components when possible
3. **Handle Dynamic Content**: Mask or mock dynamic areas
4. **Test Responsive Breakpoints**: Capture key screen sizes
5. **Manage Test Environment**: Ensure consistent rendering environment
6. **Control Animation**: Disable animations during testing
7. **Review Changes**: Have a clear process for reviewing visual changes

### Example Visual Regression Test (using Storybook and Chromatic)

For component-based testing with Storybook:

```javascript
// Button component story for visual testing
import { Button } from './Button';

export default {
  title: 'Components/Button',
  component: Button,
  argTypes: {
    variant: {
      control: { type: 'select', options: ['primary', 'secondary', 'danger'] }
    },
    size: {
      control: { type: 'select', options: ['small', 'medium', 'large'] }
    },
    disabled: {
      control: 'boolean'
    }
  }
};

// Template for all button stories
const Template = (args) => <Button {...args} />;

// Primary button story
export const Primary = Template.bind({});
Primary.args = {
  variant: 'primary',
  children: 'Primary Button',
  size: 'medium'
};

// Secondary button story
export const Secondary = Template.bind({});
Secondary.args = {
  variant: 'secondary',
  children: 'Secondary Button',
  size: 'medium'
};

// Disabled button story
export const Disabled = Template.bind({});
Disabled.args = {
  variant: 'primary',
  children: 'Disabled Button',
  disabled: true,
  size: 'medium'
};

// Size variations
export const Small = Template.bind({});
Small.args = {
  variant: 'primary',
  children: 'Small Button',
  size: 'small'
};

export const Large = Template.bind({});
Large.args = {
  variant: 'primary',
  children: 'Large Button',
  size: 'large'
};
```

These stories can be used with Chromatic, Percy, or other visual testing tools to catch visual regressions.

## Accessibility Testing

Accessibility tests verify that the application is usable by people with disabilities. See the [Accessibility Standards](docs/cross-functional/accessibility.md) document for in-depth guidance.

### What to Test for Accessibility

- **Keyboard Navigation**: All functionality is accessible with keyboard only
- **Screen Reader Compatibility**: Content is properly announced by screen readers
- **Color Contrast**: Text has sufficient contrast with background
- **Text Alternatives**: Images have alt text, videos have captions
- **Focus Management**: Focus is visible and managed appropriately
- **Semantic HTML**: Elements use correct semantic markup
- **ARIA Attributes**: ARIA is used correctly where needed

### Accessibility Testing Best Practices

1. **Automated Tests**: Use tools like axe-core, pa11y, or Lighthouse
2. **Manual Testing**: Supplement automated tests with manual checks
3. **Test with Real Assistive Technology**: Test with screen readers and other tools
4. **Include in CI**: Run accessibility tests in continuous integration
5. **Test Interaction Patterns**: Verify complex interactions are accessible

### Example Accessibility Test (using Jest-Axe)

```javascript
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

import Form from './Form';

describe('Form Accessibility', () => {
  it('should not have accessibility violations', async () => {
    // Arrange
    const { container } = render(<Form />);
    
    // Act & Assert
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
  
  it('should maintain accessibility when validation errors are shown', async () => {
    // Arrange
    const { container, getByText } = render(<Form />);
    
    // Act - trigger validation errors
    fireEvent.click(getByText('Submit'));
    
    // Assert
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

## Performance Testing

Performance tests verify that the frontend meets performance requirements and identifies bottlenecks.

### What to Test for Performance

- **Load Time**: Time to first byte, First Contentful Paint, Largest Contentful Paint
- **Interactivity**: First Input Delay, Time to Interactive
- **Layout Stability**: Cumulative Layout Shift
- **Resource Size**: Bundle size, image size, total payload
- **Runtime Performance**: Frame rate, long tasks, memory usage
- **Server Response Time**: API response times
- **Rendering Performance**: Component render times

### Performance Testing Best Practices

1. **Establish Baselines**: Define performance budgets and baseline metrics
2. **Automate Performance Tests**: Include in CI pipeline
3. **Test on Representative Devices**: Include low-end devices
4. **Measure Real User Metrics**: Collect field data from actual users
5. **Focus on User-Centric Metrics**: Prioritize metrics that affect user experience
6. **Profile Critical User Journeys**: Test performance of key user flows

### Example Performance Test (using Lighthouse CI)

```javascript
// lighthouse-config.js
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/', 'http://localhost:3000/products'],
      numberOfRuns: 3,
      settings: {
        preset: 'desktop'
      }
    },
    assert: {
      assertions: {
        'first-contentful-paint': ['warn', { maxNumericValue: 1800 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['error', { maxNumericValue: 200 }],
        'interactive': ['error', { maxNumericValue: 3000 }],
        'max-potential-fid': ['warn', { maxNumericValue: 100 }]
      }
    },
    upload: {
      target: 'temporary-public-storage'
    }
  }
};
```

## Test-Driven Development

Test-Driven Development (TDD) is an approach where tests are written before implementation code.

### TDD Process

1. **Write a Test**: Create a test that defines a function or improvement
2. **Run the Test**: Verify the test fails (red)
3. **Write Implementation**: Write the minimum code to make the test pass
4. **Run the Test Again**: Verify the test passes (green)
5. **Refactor**: Clean up the code while ensuring tests still pass
6. **Repeat**: Continue the cycle for additional features

### Benefits of TDD

- **Clearer Requirements**: Tests clarify what code should do
- **Better Design**: Code is naturally more modular and testable
- **Regression Protection**: Tests catch regressions immediately
- **Documentation**: Tests serve as documentation of behavior
- **Confidence**: Changes can be made with confidence

### When to Use TDD

TDD works particularly well for:

- Complex business logic
- Algorithmic code
- Code with clear inputs and outputs
- Bug fixes (write a test that reproduces the bug first)

TDD may be less useful for:

- Exploratory UI development
- Integration with poorly documented APIs
- Legacy code without existing tests

## Testing Frameworks and Tools

### Recommended Testing Stack by Framework

#### React

- **Unit/Component Testing**: Jest + React Testing Library
- **Component Development**: Storybook
- **Visual Testing**: Chromatic or Percy
- **E2E Testing**: Cypress or Playwright
- **Accessibility Testing**: jest-axe, Lighthouse
- **Performance Testing**: Lighthouse CI, web-vitals

#### Angular

- **Unit Testing**: Karma + Jasmine
- **Component Testing**: Spectator or Angular Testing Library
- **E2E Testing**: Protractor, Cypress, or Playwright
- **Visual Testing**: Chromatic or Percy
- **Accessibility Testing**: codelyzer, Angular ESLint

#### Vue

- **Unit/Component Testing**: Jest + Vue Test Utils
- **Component Development**: Storybook
- **E2E Testing**: Cypress or Playwright
- **Visual Testing**: Percy or Chromatic
- **Accessibility Testing**: vue-axe, Lighthouse

#### General Purpose Tools

- **Mocking**: MSW (Mock Service Worker), json-server
- **Coverage**: Istanbul, nyc
- **CI Integration**: GitHub Actions, Jenkins, CircleCI
- **Performance**: WebPageTest, Lighthouse, web-vitals
- **Visual Regression**: BackstopJS, reg-suit

## Mocking and Stubbing

Effective mocking is crucial for isolating components and focusing tests.

### What to Mock

- **API Calls**: Network requests to backend services
- **Browser APIs**: localStorage, fetch, geolocation, etc.
- **Time**: Date, setTimeout, animation frames
- **External Services**: Third-party services, analytics
- **Complex Dependencies**: Components or services with complex setup

### Mocking Best Practices

1. **Mock at the Boundary**: Mock the interface, not the implementation details
2. **Realistic Mocks**: Make mocks behave like the real dependency
3. **Centralize Mocks**: Create reusable mock implementations
4. **Verify Mock Interactions**: Ensure mocks are used as expected
5. **Clear Mock State**: Reset mocks between tests

### Example Using Mock Service Worker (MSW)

```javascript
// src/mocks/handlers.js
import { rest } from 'msw';

export const handlers = [
  // Mock a GET request to fetch user data
  rest.get('/api/user', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        id: '123',
        name: 'John Doe',
        email: 'john@example.com'
      })
    );
  }),
  
  // Mock a POST request for login
  rest.post('/api/login', (req, res, ctx) => {
    const { username, password } = req.body;
    
    if (username === 'admin' && password === 'password') {
      return res(
        ctx.status(200),
        ctx.json({
          token: 'fake-auth-token',
          user: { id: '123', name: 'Admin User' }
        })
      );
    }
    
    return res(
      ctx.status(401),
      ctx.json({ message: 'Invalid credentials' })
    );
  })
];

// src/mocks/server.js
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

// Setup mock server
export const server = setupServer(...handlers);

// src/setupTests.js
import { server } from './mocks/server';

// Start server before all tests
beforeAll(() => server.listen());

// Reset handlers after each test
afterEach(() => server.resetHandlers());

// Close server after all tests
afterAll(() => server.close());
```

## Test Environment Management

Properly configuring the test environment ensures consistent and reliable tests.

### Environment Setup Best Practices

1. **Consistent Environments**: Ensure all developers use the same test setup
2. **Isolated Tests**: Each test should run in isolation without affecting others
3. **Fast Feedback**: Optimize for fast test execution
4. **Realistic Data**: Use realistic test data
5. **Clean Up**: Reset state between tests

### Test Environment Configuration

```javascript
// jest.config.js example
module.exports = {
  // Test environment
  testEnvironment: 'jsdom',
  
  // Setup and teardown
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
  
  // Coverage configuration
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.{js,jsx,ts,tsx}',
    '!src/serviceWorker.js',
    '!src/**/*.stories.{js,jsx,ts,tsx}'
  ],
  
  // Coverage thresholds
  coverageThreshold: {
    global: {
      statements: 80,
      branches: 80,
      functions: 80,
      lines: 80
    }
  },
  
  // Transform files
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': ['babel-jest', { configFile: './babel.config.test.js' }],
    '^.+\\.css$': '<rootDir>/config/jest/cssTransform.js',
    '^(?!.*\\.(js|jsx|ts|tsx|css|json)$)': '<rootDir>/config/jest/fileTransform.js'
  },
  
  // Module name mapping
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy'
  }
};
```

## Continuous Integration

Integrating tests into CI pipelines ensures code quality is maintained.

### CI Best Practices

1. **Run All Tests**: Run unit, component, integration, and E2E tests
2. **Fail Fast**: Run faster tests first to provide quick feedback
3. **Parallel Execution**: Run tests in parallel to speed up CI
4. **Artifacts**: Save test reports and screenshots
5. **Selective Testing**: Run only affected tests when possible
6. **Notifications**: Notify team of test failures

### Example GitHub Actions Workflow

```yaml
# .github/workflows/frontend-tests.yml
name: Frontend Tests

on:
  push:
    branches: [ main ]
    paths:
      - 'src/**'
      - 'package.json'
      - 'package-lock.json'
      - '.github/workflows/frontend-tests.yml'
  pull_request:
    branches: [ main ]
    paths:
      - 'src/**'
      - 'package.json'
      - 'package-lock.json'
      - '.github/workflows/frontend-tests.yml'

jobs:
  unit-and-integration:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '16'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Lint
      run: npm run lint
    
    - name: Unit & Component Tests
      run: npm run test:unit
    
    - name: Integration Tests
      run: npm run test:integration
    
    - name: Upload Coverage
      uses: codecov/codecov-action@v3
      with:
        token: ${{ secrets.CODECOV_TOKEN }}
        fail_ci_if_error: false
  
  e2e:
    needs: unit-and-integration
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '16'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Build
      run: npm run build
    
    - name: E2E Tests
      uses: cypress-io/github-action@v4
      with:
        start: npm run serve
        wait-on: 'http://localhost:3000'
    
    - name: Upload E2E Screenshots
      uses: actions/upload-artifact@v3
      if: failure()
      with:
        name: cypress-screenshots
        path: cypress/screenshots
  
  visual:
    needs: unit-and-integration
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '16'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Publish to Chromatic
      uses: chromaui/action@v1
      with:
        projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
        exitZeroOnChanges: true
```

## Test Coverage

Test coverage measures how much of your code is exercised by tests.

### Coverage Metrics

1. **Statement Coverage**: Percentage of statements executed
2. **Branch Coverage**: Percentage of branches (if/else, switch) executed
3. **Function Coverage**: Percentage of functions called
4. **Line Coverage**: Percentage of code lines executed

### Coverage Best Practices

1. **Set Realistic Goals**: Start with achievable targets and increase them over time
2. **Focus on Quality, Not Just Quantity**: High coverage with poor assertions isn't valuable
3. **Identify Critical Areas**: Ensure high coverage for critical business logic
4. **Address Coverage Gaps**: Regularly review and address uncovered code
5. **Don't Chase 100%**: Some code may not need testing (e.g., generated code)

### Recommended Coverage Targets

| Type of Code | Target Coverage |
|--------------|----------------|
| Business Logic | 95-100% |
| UI Components | 80-90% |
| Utilities | 90-100% |
| Generated Code | Optional |
| Third-party Integrations | 70-90% |

## Testing Legacy Code

Testing existing code without tests presents unique challenges.

### Approaches for Legacy Code

1. **Characterization Tests**: Write tests that document current behavior
2. **Seam Creation**: Identify and create seams for testability
3. **Refactoring**: Gradually improve testability through careful refactoring
4. **Strangler Pattern**: Incrementally replace legacy code with tested code
5. **Critical Path Testing**: Focus on the most important user flows first

### Legacy Code Testing Strategies

1. **Start with E2E Tests**: Secure critical paths before internal changes
2. **Add Integration Tests**: Add tests at component boundaries
3. **Refactor for Testability**: Carefully improve code structure
4. **Introduce Unit Tests**: Add unit tests as code is refactored
5. **Use Approval Tests**: Capture current output for verification

## Mobile-Specific Considerations

Testing for mobile web adds additional considerations.

### Mobile Testing Focus Areas

1. **Responsive Design**: Test across various screen sizes and orientations
2. **Touch Interactions**: Test touch events, gestures, and mobile-specific interactions
3. **Performance**: Test on real mobile devices and slow networks
4. **Offline Capabilities**: Test offline and poor connectivity scenarios
5. **Mobile Features**: Test integration with device capabilities
6. **Platform Differences**: Test across iOS, Android, and other platforms

### Mobile Testing Best Practices

1. **Real Device Testing**: Test on actual devices, not just emulators
2. **Network Simulation**: Test with throttled and intermittent connections
3. **Battery Impact**: Test for battery usage on long-running features
4. **Gesture Testing**: Test complex touch interactions
5. **Native Browser Features**: Test integration with mobile browser features

## Common Anti-Patterns

Avoid these common testing mistakes.

### Anti-Patterns to Avoid

1. **Brittle Tests**: Tests that break with minor changes
2. **Testing Implementation Details**: Focusing on how instead of what
3. **Overlapping Tests**: Multiple tests verifying the same behavior
4. **Slow Tests**: Tests that take too long to run
5. **Flaky Tests**: Tests that fail intermittently
6. **Mock Everything**: Overusing mocks instead of realistic scenarios
7. **No Test Structure**: Tests without clear arrange-act-assert phases
8. **Testing the Framework**: Testing built-in framework behavior
9. **Excessive Snapshots**: Overusing snapshot testing
10. **Hardcoded Test Data**: Using hardcoded values without clear explanation

### Solutions to Anti-Patterns

1. **Focus on Behavior**: Test what components do, not how they do it
2. **Use Stable Selectors**: Prefer data-testid over CSS selectors
3. **Clear Test Structure**: Use arrange-act-assert pattern
4. **Isolate Tests**: Ensure tests don't affect each other
5. **Fast Feedback**: Keep tests fast and reliable
6. **Prefer Realistic Testing**: Use the actual components when practical

## Framework-Specific Guidelines

### React Testing Best Practices

1. **Use React Testing Library**: Focus on user-centric testing
2. **Avoid Enzyme for New Code**: Prefer testing library approaches
3. **Test Hooks Separately**: Create custom hook tests with renderHook
4. **Mock Context Providers**: Provide test versions of contexts
5. **Test Custom Events**: Test custom event handlers
6. **Utilize act()**: Wrap state updates in act() when needed
7. **Test Error Boundaries**: Verify error handling

### Angular Testing Best Practices

1. **TestBed Setup**: Configure TestBed with minimal dependencies
2. **Component Harnesses**: Use component test harnesses
3. **Isolated Tests**: Use isolated tests for pipes and services
4. **Shallow vs. Deep Testing**: Choose the right level of integration
5. **Test Directives**: Test custom directives thoroughly
6. **Test Forms**: Verify reactive forms behavior
7. **Test HTTP Requests**: Use HttpClientTestingModule

### Vue Testing Best Practices

1. **Component Testing**: Use Vue Test Utils
2. **Composition API**: Test composables separately
3. **Vuex Testing**: Test store, actions, and mutations separately
4. **Vue Router**: Mock router when testing routed components
5. **Test Props Interface**: Verify component props behavior
6. **Test Events**: Verify custom events are emitted correctly
7. **Snapshot Testing**: Use sparingly for stable components

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 2025-03-20 | Initial version |
