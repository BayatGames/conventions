<!--
Document: Cross-Platform Code Sharing Strategies
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Cross-Platform Code Sharing Strategies

This document outlines the standards, patterns, and best practices for sharing code across web, mobile, and desktop platforms at Bayat.

## Table of Contents

- [Introduction](#introduction)
- [Choosing a Cross-Platform Strategy](#choosing-a-cross-platform-strategy)
- [Code Sharing Architectures](#code-sharing-architectures)
- [Shared Business Logic Approaches](#shared-business-logic-approaches)
- [UI Approaches](#ui-approaches)
- [Networking and Data Layer](#networking-and-data-layer)
- [State Management](#state-management)
- [Testing Strategies](#testing-strategies)
- [Build and CI/CD Considerations](#build-and-cicd-considerations)
- [Platform-Specific Integration](#platform-specific-integration)
- [Performance Considerations](#performance-considerations)
- [Localization and Internationalization](#localization-and-internationalization)
- [Accessibility](#accessibility)
- [Security Considerations](#security-considerations)
- [Implementation Patterns](#implementation-patterns)
- [Common Pitfalls](#common-pitfalls)
- [Case Studies](#case-studies)

## Introduction

Cross-platform code sharing allows teams to develop applications that run on multiple platforms while sharing as much code as possible, increasing development efficiency and maintaining consistency across user experiences.

### Benefits of Code Sharing

- **Development Efficiency**: Write once, deploy to multiple platforms
- **Consistency**: Ensure similar behavior across platforms
- **Maintenance**: Fix bugs once, benefit everywhere
- **Knowledge Sharing**: Allow developers to work across platforms
- **Time-to-Market**: Launch on multiple platforms simultaneously

### Challenges of Code Sharing

- **Platform-Specific Requirements**: Each platform has unique capabilities and constraints
- **Performance Overhead**: Cross-platform solutions may not be as performant as native
- **UI/UX Consistency**: Balancing platform-specific design patterns with consistent branding
- **Team Skills**: Requires developers to understand multiple platforms
- **Debugging Complexity**: Cross-platform issues can be harder to diagnose

## Choosing a Cross-Platform Strategy

### Strategy Selection Factors

Consider these factors when selecting a cross-platform approach:

1. **Project Requirements**:
   - Performance needs
   - Platform-specific feature requirements
   - Time-to-market constraints
   - Longevity of the application

2. **Team Capabilities**:
   - Existing skills in the team
   - Learning curve for new technologies
   - Available resources for development and maintenance

3. **Business Considerations**:
   - Budget constraints
   - Target platforms and their priority
   - Update frequency
   - Long-term maintenance strategy

### Spectrum of Cross-Platform Approaches

From most to least shared code:

1. **Single Codebase, Multiple Platforms**:
   - React Native, Flutter, .NET MAUI
   - Highest code sharing percentage (70-100%)
   - Single language and framework
   - Some platform-specific code required

2. **Shared Core, Native UIs**:
   - Kotlin Multiplatform, Swift for cross-platform
   - Medium-high code sharing (50-80%)
   - Business logic shared, UI platform-specific
   - Multiple languages may be required

3. **Shared Components, Native Apps**:
   - WebView components, shared libraries
   - Medium code sharing (30-60%)
   - Core functionality shared, mostly native code
   - Multiple codebases with shared modules

4. **Native Apps with Common Patterns**:
   - Similar architecture across platforms
   - Low code sharing (5-30%)
   - Multiple codebases with similar patterns
   - Highest platform optimization

### Decision Matrix

Use this matrix to guide decision-making:

| Factor                  | Single Codebase | Shared Core | Shared Components | Native with Common Patterns |
|-------------------------|-----------------|------------|-------------------|---------------------------|
| Development Speed       | ★★★★★          | ★★★★       | ★★★              | ★★                        |
| UI Performance          | ★★★            | ★★★★★      | ★★★★★            | ★★★★★                    |
| Native Feature Access   | ★★★            | ★★★★       | ★★★★★            | ★★★★★                    |
| Maintenance Efficiency  | ★★★★★          | ★★★★       | ★★★              | ★★                        |
| Learning Curve          | ★★★            | ★★         | ★★★              | ★★★★                     |
| Long-term Flexibility   | ★★★            | ★★★★       | ★★★★             | ★★★★★                    |

## Code Sharing Architectures

### Clean Architecture for Cross-Platform

Implement Clean Architecture to separate concerns:

1. **Domain Layer** (Most Shareable):
   - Business logic
   - Models and entities
   - Business rules and validation
   - Use cases/interactors

2. **Data Layer** (Partially Shareable):
   - Repositories
   - Data sources (remote, local)
   - DTOs and mappers
   - Caching strategies

3. **Presentation Layer** (Least Shareable):
   - ViewModels/Presenters
   - State management
   - UI components
   - Platform-specific adapters

```plaintext
┌───────────────────────────────────────────────────────────┐
│                                                           │
│  ┌───────────────┐    ┌───────────────┐    ┌──────────┐  │
│  │               │    │               │    │          │  │
│  │  Domain Layer │◄───┤   Data Layer  │◄───┤ UI Layer │  │
│  │               │    │               │    │          │  │
│  └───────────────┘    └───────────────┘    └──────────┘  │
│                                                           │
│  ▲                    ▲                    ▲              │
│  │                    │                    │              │
│  │                    │                    │              │
│  │                    │                    │              │
│  100%                 50-90%               0-50%          │
│  Shareable            Shareable            Shareable      │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### Module Organization

Structure modules to maximize code sharing:

1. **Common/Core Module**:
   - Shared business logic
   - Models and utilities
   - Platform-agnostic code

2. **Platform-Specific Modules**:
   - UI implementations
   - Platform service adapters
   - Native feature integration

3. **Feature Modules**:
   - Feature-specific code organized by domain
   - Shared core with platform adaptations

Example project structure:

```plaintext
/src
  /common
    /domain
      /models
      /usecases
    /data
      /repositories
      /datasources
    /utils
  /platforms
    /web
      /components
      /pages
    /ios
      /viewcontrollers
      /views
    /android
      /activities
      /fragments
    /desktop
      /windows
      /components
  /features
    /authentication
      /common
      /web
      /mobile
      /desktop
    /products
      /common
      /web
      /mobile
      /desktop
```

## Shared Business Logic Approaches

### Kotlin Multiplatform Mobile (KMM)

Share code between Android, iOS, and potentially web/desktop:

```kotlin
// Common code (shared between platforms)
expect class PlatformSpecific {
    fun platformName(): String
}

class BusinessLogic {
    private val platform = PlatformSpecific()
    
    fun process(): String {
        return "Running on ${platform.platformName()}"
    }
}

// Android-specific implementation
actual class PlatformSpecific {
    actual fun platformName(): String = "Android"
}

// iOS-specific implementation
actual class PlatformSpecific {
    actual fun platformName(): String = "iOS"
}
```

### TypeScript/JavaScript Sharing

Share code between web, React Native, and Electron:

```typescript
// core/api.ts (shared)
export async function fetchData(endpoint: string): Promise<any> {
  const response = await fetch(`https://api.example.com/${endpoint}`);
  return response.json();
}

// platform-specific entry points
// web/index.ts
import { fetchData } from '../core/api';
// Use in web context

// mobile/index.ts
import { fetchData } from '../core/api';
// Use in React Native context
```

### C# with .NET MAUI

Share code across Windows, macOS, iOS, Android:

```csharp
// Shared business logic
public class DataService
{
    public async Task<IEnumerable<Item>> GetItemsAsync()
    {
        // Implementation that works across platforms
        return await _repository.GetAllAsync();
    }
}

// Platform-specific service
public interface IFileService
{
    Task<string> ReadFileAsync(string filename);
}

// Platform implementation for Windows
#if WINDOWS
public class FileService : IFileService
{
    public async Task<string> ReadFileAsync(string filename)
    {
        // Windows-specific implementation
    }
}
#endif

// Platform implementation for iOS
#if IOS
public class FileService : IFileService
{
    public async Task<string> ReadFileAsync(string filename)
    {
        // iOS-specific implementation
    }
}
#endif
```

### React Native and React Web

Share code between web and mobile React applications:

```javascript
// shared/components/Button.js
import React from 'react';
import { Platform } from 'react-native';

// Import appropriate component based on platform
const ButtonComponent = Platform.select({
  web: () => require('./Button.web').default,
  default: () => require('./Button.native').default,
})();

export default ButtonComponent;

// Button.web.js
import React from 'react';
export default function Button(props) {
  return <button {...props}>{props.children}</button>;
}

// Button.native.js
import React from 'react';
import { TouchableOpacity, Text } from 'react-native';
export default function Button(props) {
  return (
    <TouchableOpacity {...props}>
      <Text>{props.children}</Text>
    </TouchableOpacity>
  );
}
```

## UI Approaches

### Platform-Adaptive UI

Design UI components that adapt to platform conventions:

1. **Platform Detection**:
   - Detect platform at runtime
   - Adjust behavior accordingly

2. **Conditional Rendering**:
   - Render different components based on platform
   - Maintain consistent API across platforms

3. **Style Adaptation**:
   - Use platform-specific styling
   - Maintain consistent brand identity

```jsx
// React Native example
import { Platform, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    padding: 20,
    ...Platform.select({
      ios: {
        shadowColor: 'black',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.2,
      },
      android: {
        elevation: 4,
      },
      web: {
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)',
      },
    }),
  },
});
```

### Component Abstraction

Create a shared component API with platform-specific implementations:

```typescript
// Interface shared across platforms
export interface ButtonProps {
  title: string;
  onPress: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary';
}

// Platform-specific implementations
// Each platform implements the same interface with appropriate native components
```

### Web-Based UI Approaches

Use web technologies across platforms:

1. **WebView Components**:
   - Embed web components in native apps
   - Use for complex UI that's consistent across platforms
   - Example: Charts, rich text editors, complex forms

2. **Progressive Web Apps (PWAs)**:
   - Web apps with native-like features
   - Can be installed on many platforms
   - Share the same codebase across web and mobile

3. **Hybrid Frameworks**:
   - Capacitor or Cordova for hybrid apps
   - Tauri or Electron for desktop apps
   - Same web UI code across all platforms

### Native UI with Shared Logic

Use platform-native UI components with shared logic:

1. **Kotlin Multiplatform with SwiftUI and Jetpack Compose**:
   - Share business logic in Kotlin
   - Use SwiftUI for iOS UI
   - Use Jetpack Compose for Android UI

2. **C# with .NET MAUI**:
   - XAML or Blazor UI framework
   - Native rendering on each platform

## Networking and Data Layer

### API Client Sharing

Create a platform-agnostic API client:

```typescript
// Shared API client
export class ApiClient {
  private baseUrl: string;
  
  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }
  
  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}/${endpoint}`);
    return response.json();
  }
  
  async post<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${this.baseUrl}/${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    return response.json();
  }
}

// Platform-specific network monitoring
export interface NetworkMonitor {
  isConnected(): boolean;
  onConnectivityChange(callback: (isConnected: boolean) => void): void;
}

// Implemented differently for each platform but used with same API
```

### Data Persistence Strategies

Share data storage logic across platforms:

1. **Repository Pattern**:
   - Define repository interfaces
   - Implement platform-specific storage

        ```kotlin
        // Kotlin Multiplatform example
        interface UserRepository {
            suspend fun getUsers(): List<User>
            suspend fun getUser(id: String): User?
            suspend fun saveUser(user: User)
        }

        // Shared implementation using platform-specific storage
        class UserRepositoryImpl(private val storage: PlatformStorage) : UserRepository {
            suspend fun getUsers(): List<User> {
                return storage.getAll("users")
            }
            // Other implementations
        }

        // Platform-specific storage interface
        expect class PlatformStorage {
            suspend fun getAll(collection: String): List<Map<String, Any>>
            suspend fun get(collection: String, id: String): Map<String, Any>?
            suspend fun save(collection: String, item: Map<String, Any>)
        }
        ```

2. **Data Synchronization**:
   - Shared sync logic
   - Platform-specific offline storage
   - Conflict resolution strategies

## State Management

### Shared State Management

Implement cross-platform state management:

1. **Redux/Flux Pattern**:
   - Actions, reducers, and state are shareable
   - Store implementation may be platform-specific

        ```javascript
        // Shared Redux actions and reducers
        export const ADD_TODO = 'ADD_TODO';
        export const TOGGLE_TODO = 'TOGGLE_TODO';

        export function addTodo(text) {
        return { type: ADD_TODO, text };
        }

        export function toggleTodo(id) {
        return { type: TOGGLE_TODO, id };
        }

        export function todosReducer(state = [], action) {
        switch (action.type) {
            case ADD_TODO:
            return [
                ...state,
                { id: Date.now(), text: action.text, completed: false }
            ];
            case TOGGLE_TODO:
            return state.map(todo =>
                todo.id === action.id ? { ...todo, completed: !todo.completed } : todo
            );
            default:
            return state;
        }
        }

        // Platform-specific store initialization and middleware
        ```

2. **Observable/Reactive Pattern**:
   - Share observable models and state
   - Platform-specific UI reacts to changes

        ```typescript
        // Shared observable model
        export class TodoStore {
        @observable todos: Todo[] = [];
        
        @action
        addTodo(text: string) {
            this.todos.push({
            id: Date.now(),
            text,
            completed: false
            });
        }
        
        @action
        toggleTodo(id: number) {
            const todo = this.todos.find(t => t.id === id);
            if (todo) {
            todo.completed = !todo.completed;
            }
        }
        }

        // Platform-specific UI observes and reacts to changes
        ```

3. **Unidirectional Data Flow**:
   - Share state management core
   - Platform adapters for UI integration

## Testing Strategies

### Cross-Platform Test Hierarchy

Implement a testing pyramid suitable for cross-platform projects:

1. **Shared Core Tests** (Platform-agnostic):
   - Business logic unit tests
   - Repository tests with mocked data sources
   - Use case/interactor tests

2. **Platform-Specific Unit Tests**:
   - UI component tests
   - Platform service implementation tests
   - Platform integration tests

3. **Cross-Platform Integration Tests**:
   - End-to-end tests that run on each platform
   - Focus on critical user journeys

### Shared Test Utilities

Create shared test infrastructure:

```kotlin
// Kotlin Multiplatform test utilities
expect class TestDispatcher {
    fun runTest(block: suspend () -> Unit)
}

class UserServiceTest {
    private val testDispatcher = TestDispatcher()
    private val userService = UserService()
    
    fun testUserFetch() = testDispatcher.runTest {
        val users = userService.fetchUsers()
        assertEquals(5, users.size)
    }
}

// Platform-specific test dispatcher implementation
actual class TestDispatcher {
    actual fun runTest(block: suspend () -> Unit) {
        // Platform-specific test runner implementation
    }
}
```

### Platform-Specific Testing Tools

Use appropriate testing tools for each platform:

1. **Web**:
   - Jest, Testing Library, Cypress
   - Browser-specific testing

2. **Mobile**:
   - XCTest for iOS
   - JUnit, Espresso for Android
   - Detox, Appium for cross-platform

3. **Desktop**:
   - Playwright, Spectron
   - Platform-specific UI testing

## Build and CI/CD Considerations

### Unified Build Process

Create a cohesive build process for all platforms:

1. **Monorepo Structure**:
   - Use tools like Nx, Turborepo, or Lerna
   - Share configuration and scripts
   - Optimize builds with incremental compilation

2. **Shared CI/CD Pipeline**:
   - Build all platforms from the same source
   - Run platform-agnostic tests once
   - Run platform-specific tests on appropriate environments

```yaml
# GitHub Actions example for cross-platform CI
name: Cross-Platform Build

on: [push, pull_request]

jobs:
  # Shared core tests (run once)
  core-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up environment
        run: npm install
      - name: Run core tests
        run: npm run test:core

  # Web-specific build and tests
  web-build:
    needs: core-tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up environment
        run: npm install
      - name: Build web
        run: npm run build:web
      - name: Run web tests
        run: npm run test:web

  # iOS build and tests
  ios-build:
    needs: core-tests
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up environment
        run: npm install
      - name: Build iOS
        run: npm run build:ios
      - name: Run iOS tests
        run: npm run test:ios

  # Android build and tests
  android-build:
    needs: core-tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up environment
        run: npm install
      - name: Build Android
        run: npm run build:android
      - name: Run Android tests
        run: npm run test:android
```

### Platform-Specific Builds

Configure platform-specific build optimizations:

1. **Web**:
   - Progressive bundling
   - Code splitting
   - Tree shaking

2. **Mobile**:
   - App bundle/IPA optimization
   - Asset optimization
   - Proguard/code minimization

3. **Desktop**:
   - Installer packaging
   - Auto-update mechanisms
   - Platform distribution packaging

## Platform-Specific Integration

### Native Feature Integration

Access platform-specific APIs through abstraction:

```typescript
// Interface for platform features
export interface GeolocationService {
  getCurrentPosition(): Promise<{ latitude: number; longitude: number }>;
  watchPosition(callback: (position: { latitude: number; longitude: number }) => void): number;
  clearWatch(watchId: number): void;
}

// Platform-specific implementations
// Web implementation
export class WebGeolocationService implements GeolocationService {
  getCurrentPosition(): Promise<{ latitude: number; longitude: number }> {
    return new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        (position) => resolve({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        }),
        (error) => reject(error)
      );
    });
  }
  
  // Other method implementations
}

// React Native implementation
export class NativeGeolocationService implements GeolocationService {
  getCurrentPosition(): Promise<{ latitude: number; longitude: number }> {
    // Use React Native's Geolocation API
  }
  
  // Other method implementations
}
```

### Plugin Systems

Create extensible plugin systems for platform features:

```typescript
// Core plugin system
export interface Plugin {
  name: string;
  initialize(): Promise<void>;
}

export class PluginManager {
  private plugins: Map<string, Plugin> = new Map();
  
  registerPlugin(plugin: Plugin) {
    this.plugins.set(plugin.name, plugin);
  }
  
  async initializePlugins() {
    for (const plugin of this.plugins.values()) {
      await plugin.initialize();
    }
  }
  
  getPlugin(name: string): Plugin | undefined {
    return this.plugins.get(name);
  }
}

// Platform-specific plugin implementation
export class CameraPlugin implements Plugin {
  name = 'camera';
  
  // Platform-specific implementation injected here
  constructor(private implementation: CameraImplementation) {}
  
  async initialize() {
    await this.implementation.requestPermissions();
  }
  
  takePicture() {
    return this.implementation.takePicture();
  }
}
```

### Platform-Specific UI Extensions

Extend shared UI with platform-specific features:

```kotlin
// Kotlin Multiplatform with Compose multiplatform example
@Composable
expect fun PlatformSpecificButton(
    text: String,
    onClick: () -> Unit
)

// Android implementation
@Composable
actual fun PlatformSpecificButton(
    text: String,
    onClick: () -> Unit
) {
    Button(
        onClick = onClick,
        colors = ButtonDefaults.buttonColors(
            backgroundColor = MaterialTheme.colors.primary
        )
    ) {
        Text(text)
    }
}

// iOS implementation
@Composable
actual fun PlatformSpecificButton(
    text: String,
    onClick: () -> Unit
) {
    Button(text, onClick)
        .buttonStyle(BorderedButtonStyle())
        .foregroundColor(Color.blue)
}
```

## Performance Considerations

### Performance Monitoring

Implement cross-platform performance monitoring:

1. **Shared Metrics**:
   - Response times
   - Rendering performance
   - Memory usage
   - Startup time

2. **Platform-Specific Metrics**:
   - Web: Core Web Vitals
   - Mobile: App startup time, frame rate
   - Desktop: Memory usage, resource consumption

3. **Unified Dashboard**:
   - Collect metrics from all platforms
   - Compare performance across platforms
   - Set platform-specific benchmarks

### Platform-Specific Optimizations

1. **Web Optimizations**:
   - Bundle size optimization
   - Lazy-loading components
   - Service workers for offline support

2. **Mobile Optimizations**:
   - Native modules for performance-critical code
   - Image and asset optimization
   - Background processing strategies

3. **Desktop Optimizations**:
   - Process management
   - Hardware acceleration
   - Memory management

## Localization and Internationalization

### Shared Localization Resources

Create a unified localization system:

```typescript
// Shared localization keys
export const translations = {
  en: {
    'app.welcome': 'Welcome to the App',
    'app.login': 'Log In',
    // More translations
  },
  es: {
    'app.welcome': 'Bienvenido a la Aplicación',
    'app.login': 'Iniciar Sesión',
    // More translations
  },
  // More languages
};

// Platform-agnostic translation function
export function translate(key: string, language: string, params?: Record<string, string>): string {
  const languageTranslations = translations[language] || translations['en'];
  let text = languageTranslations[key] || key;
  
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      text = text.replace(`{${key}}`, value);
    });
  }
  
  return text;
}

// Platform-specific initialization and language detection
```

### Platform-Adapted Formatting

Adapt formatting to platform conventions:

1. **Date and Time Formatting**:
   - Respect platform-specific date formats
   - Consider 12/24-hour format preferences

2. **Number Formatting**:
   - Currency symbols and positions
   - Decimal and thousands separators

3. **Text Direction**:
   - RTL layout support
   - Platform-specific RTL implementation

## Accessibility

### Cross-Platform Accessibility Standards

Implement accessibility across platforms:

1. **Shared Semantics**:
   - Consistent labeling and descriptions
   - Shared content hierarchy

2. **Platform-Specific Implementation**:
   - Web: ARIA attributes, semantic HTML
   - iOS: UIAccessibility
   - Android: AccessibilityService
   - Desktop: Platform-specific accessibility APIs

```typescript
// Shared accessibility interface
export interface AccessibleProps {
  label: string;
  hint?: string;
  role?: string;
  isEnabled?: boolean;
  traits?: string[];
}

// Platform-specific implementation
// React Native example
function applyAccessibility(element, props: AccessibleProps) {
  return React.cloneElement(element, {
    accessible: true,
    accessibilityLabel: props.label,
    accessibilityHint: props.hint,
    accessibilityRole: props.role,
    accessibilityState: {
      disabled: !props.isEnabled
    },
    accessibilityTraits: props.traits
  });
}

// Web example
function applyAccessibility(element, props: AccessibleProps) {
  return React.cloneElement(element, {
    'aria-label': props.label,
    'aria-description': props.hint,
    role: props.role,
    'aria-disabled': !props.isEnabled
  });
}
```

## Security Considerations

### Shared Security Practices

Implement consistent security across platforms:

1. **Authentication**:
   - Shared token management
   - Biometric authentication abstraction
   - Secure storage interface

2. **Data Protection**:
   - Encryption utilities
   - Secure data handling
   - Privacy controls

3. **Secure Communication**:
   - Certificate pinning
   - Secure API communication
   - Environment-specific security

        ```typescript
        // Shared secure storage interface
        export interface SecureStorage {
        save(key: string, value: string): Promise<void>;
        retrieve(key: string): Promise<string | null>;
        delete(key: string): Promise<void>;
        }

        // Platform-specific implementations
        // iOS implementation using Keychain
        class iOSSecureStorage implements SecureStorage {
        async save(key: string, value: string): Promise<void> {
            // Use iOS Keychain API
        }
        // Other methods
        }

        // Android implementation using EncryptedSharedPreferences
        class AndroidSecureStorage implements SecureStorage {
        async save(key: string, value: string): Promise<void> {
            // Use Android EncryptedSharedPreferences
        }
        // Other methods
        }

        // Web implementation using secure cookies or localStorage with encryption
        class WebSecureStorage implements SecureStorage {
        async save(key: string, value: string): Promise<void> {
            // Encrypt and store in localStorage or secure cookie
        }
        // Other methods
        }
        ```

## Implementation Patterns

### Feature Module Pattern

Organize related functionality in cross-platform feature modules:

```
/features
  /authentication
    /common
      /domain
        auth-service.ts      # Shared business logic
        user-model.ts        # Shared data model
      /data
        auth-repository.ts   # Repository interface
    /web
      auth-repository-impl.ts # Web implementation
      login-page.tsx         # Web UI
    /ios
      AuthRepositoryImpl.swift # iOS implementation
      LoginViewController.swift # iOS UI
    /android
      AuthRepositoryImpl.kt  # Android implementation
      LoginActivity.kt       # Android UI
```

### Adapter Pattern

Implement platform specifics through adapters:

```typescript
// Shared interface
export interface FileSystem {
  readFile(path: string): Promise<string>;
  writeFile(path: string, content: string): Promise<void>;
  deleteFile(path: string): Promise<void>;
  fileExists(path: string): Promise<boolean>;
}

// Platform-specific implementations
// Each platform implements the same interface differently
// The rest of the app uses the interface without knowing implementation details
```

### Dependency Injection

Use dependency injection to manage platform-specific implementations:

```typescript
// Service container
class ServiceContainer {
  private services = new Map<string, any>();
  
  register<T>(key: string, implementation: T): void {
    this.services.set(key, implementation);
  }
  
  resolve<T>(key: string): T {
    const service = this.services.get(key);
    if (!service) {
      throw new Error(`Service not registered: ${key}`);
    }
    return service as T;
  }
}

// Platform-specific initialization
const container = new ServiceContainer();

// On Web
container.register('filesystem', new WebFileSystem());
container.register('network', new WebNetworkService());

// On iOS
container.register('filesystem', new IOSFileSystem());
container.register('network', new IOSNetworkService());

// Usage in shared code
const fileSystem = container.resolve<FileSystem>('filesystem');
await fileSystem.readFile('config.json');
```

## Common Pitfalls

### Antipatterns to Avoid

1. **Over-Abstraction**:
   - Creating excessive abstractions for platform features
   - Trying to abstract platform-specific UX that should remain distinct

2. **Platform Leakage**:
   - Allowing platform-specific code to creep into shared modules
   - Using platform APIs directly in shared code

3. **Lowest Common Denominator**:
   - Only implementing features available on all platforms
   - Ignoring platform-specific optimizations

4. **Excessive Indirection**:
   - Too many layers making debugging difficult
   - Overly complex architecture for simple apps

5. **Neglecting Platform Conventions**:
   - Forcing the same UI across platforms with different conventions
   - Ignoring platform guidelines for interactions

### Practical Challenges and Solutions

1. **Challenge**: Different UI paradigms across platforms
   - **Solution**: Use atomic design to share the smallest components possible and compose them differently on each platform

2. **Challenge**: Platform-specific performance bottlenecks
   - **Solution**: Use performance monitoring to identify issues and implement platform-specific optimizations

3. **Challenge**: Third-party library compatibility
   - **Solution**: Create abstractions around third-party functionality and implement with platform-appropriate libraries

4. **Challenge**: Growing complexity with shared code
   - **Solution**: Regular refactoring, clear boundaries, and comprehensive testing

## Case Studies

### Case Study 1: Banking App with Shared Core

**Context**: A banking application with web, iOS, and Android platforms requiring high security and native performance.

**Approach**:

- Used Kotlin Multiplatform for shared business logic
- Native UI with SwiftUI for iOS and Jetpack Compose for Android
- Web frontend with React
- Shared all security and business logic across platforms
- Platform-specific UI following each platform's conventions

**Results**:

- 75% shared code for business logic and data layers
- 100% native UI performance with platform-specific design
- Reduced development time by 40% for new features
- Single source of truth for business logic

### Case Study 2: E-Commerce App with React Native

**Context**: E-commerce platform needing rapid deployment across web and mobile platforms with consistent UI.

**Approach**:

- React Native for mobile platforms
- React for web platform
- Shared component library with platform-specific adaptations
- Shared state management with Redux
- Shared API client and business logic

**Results**:

- 90% shared code across all platforms
- Consistent brand experience with platform-specific UX refinements
- Rapid deployment of new features
- Single team capable of maintaining all platforms

### Case Study 3: Enterprise Dashboard with .NET MAUI

**Context**: Internal enterprise dashboard requiring deployment on Windows, macOS, and mobile platforms.

**Approach**:

- .NET MAUI for all platforms
- Shared C# business logic
- MVVM architecture
- Platform-specific optimizations for critical features
- Shared data access layer

**Results**:

- 95% code sharing across all platforms
- Leveraged existing .NET expertise in the team
- Consistent enterprise data security across platforms
- Simplified maintenance and updates
