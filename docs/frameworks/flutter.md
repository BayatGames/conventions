# Flutter Development Conventions

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Naming Conventions](#naming-conventions)
4. [Widget Architecture](#widget-architecture)
5. [State Management](#state-management)
6. [Navigation](#navigation)
7. [Styling and Theming](#styling-and-theming)
8. [Asset Management](#asset-management)
9. [Internationalization](#internationalization)
10. [Performance Optimization](#performance-optimization)
11. [Testing](#testing)
12. [Error Handling](#error-handling)
13. [Dependency Management](#dependency-management)
14. [Platform-Specific Code](#platform-specific-code)
15. [Accessibility](#accessibility)
16. [Security Best Practices](#security-best-practices)
17. [CI/CD and Deployment](#cicd-and-deployment)
18. [Documentation](#documentation)

## Introduction

This document outlines the standard conventions and best practices for Flutter application development at Bayat. These guidelines aim to ensure consistency, maintainability, and scalability across all Flutter projects.

## Project Structure

### Folder Organization

```
lib/
├── app/                  # App-level configurations
│   ├── app.dart          # App entry point
│   ├── routes.dart       # Route definitions
│   └── theme.dart        # App theme configuration
├── core/                 # Core functionality
│   ├── constants/        # App constants
│   ├── errors/           # Error handling
│   ├── network/          # Network services
│   └── utils/            # Utility functions
├── data/                 # Data layer
│   ├── models/           # Data models
│   ├── repositories/     # Repository implementations
│   ├── providers/        # Data providers
│   └── datasources/      # Data sources (local, remote)
├── domain/               # Domain layer (for clean architecture)
│   ├── entities/         # Business entities
│   ├── repositories/     # Repository interfaces
│   └── usecases/         # Business logic use cases
├── presentation/         # UI layer
│   ├── screens/          # Full screens
│   ├── widgets/          # Reusable widgets
│   │   ├── common/       # Common widgets
│   │   └── feature/      # Feature-specific widgets
│   ├── blocs/            # BLoC state management
│   └── pages/            # Page widgets
├── l10n/                 # Localization resources
└── main.dart             # Entry point
```

### Configuration Files

- `pubspec.yaml`: Package dependencies and app metadata
- `analysis_options.yaml`: Linting and static analysis rules
- `build.yaml`: Build configuration
- `.gitignore`: Git ignore rules
- `README.md`: Project documentation

## Naming Conventions

### Files and Directories

- Use snake_case for file and directory names
  - Example: `user_profile_screen.dart`, `auth_repository.dart`
- Group related files in feature-specific directories
- Suffix files based on their purpose:
  - Screens/Pages: `_screen.dart`, `_page.dart`
  - Widgets: `_widget.dart`
  - Models: `_model.dart`
  - BLoCs: `_bloc.dart`, `_event.dart`, `_state.dart`
  - Repositories: `_repository.dart`
  - Providers: `_provider.dart`

### Dart Naming

- Use UpperCamelCase for classes, enums, typedefs, and extensions
  - Example: `UserProfileScreen`, `AuthenticationState`
- Use lowerCamelCase for variables, methods, and functions
  - Example: `getUserData()`, `isLoggedIn`
- Use SCREAMING_CAPS for constants
  - Example: `MAX_LOGIN_ATTEMPTS`, `API_BASE_URL`
- Prefix private members with underscore
  - Example: `_userRepository`, `_handleLogin()`

## Widget Architecture

### Widget Types

1. **Stateless Widgets**: For UI components that don't manage state
2. **Stateful Widgets**: For components that need to manage internal state
3. **Inherited Widgets**: For propagating data down the widget tree
4. **Presentation Widgets**: For UI rendering only
5. **Container Widgets**: For managing state and business logic

### Widget Guidelines

- Keep widgets focused on a single responsibility
- Extract reusable widgets into separate classes
- Limit widget nesting to avoid deep widget trees
- Use const constructors when possible
- Implement `==` and `hashCode` for custom widgets that are frequently rebuilt

```dart
// Good example of a reusable widget
class PrimaryButton extends StatelessWidget {
  const PrimaryButton({
    Key? key,
    required this.label,
    required this.onPressed,
    this.isLoading = false,
  }) : super(key: key);

  final String label;
  final VoidCallback onPressed;
  final bool isLoading;

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: isLoading ? null : onPressed,
      style: ElevatedButton.styleFrom(
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 24),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
      child: isLoading
          ? const SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(strokeWidth: 2),
            )
          : Text(label),
    );
  }
}
```

### Composition Over Inheritance

- Prefer composition over inheritance for widget reuse
- Use mixins sparingly and only for well-defined behaviors
- Create widget factories for complex widget creation

## State Management

### Recommended Approaches

1. **BLoC/Cubit**: For complex applications with significant business logic
2. **Provider**: For simpler state management needs
3. **Riverpod**: For more advanced dependency injection and state management
4. **GetX**: For rapid development when appropriate
5. **setState**: Only for simple, localized state

### BLoC Pattern Guidelines

- Separate events, states, and business logic
- Keep BLoCs focused on specific features
- Use repositories to abstract data sources
- Handle loading, success, and error states explicitly

```dart
// Example BLoC implementation
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final AuthRepository authRepository;

  AuthBloc({required this.authRepository}) : super(AuthInitial()) {
    on<LoginRequested>(_onLoginRequested);
    on<LogoutRequested>(_onLogoutRequested);
  }

  Future<void> _onLoginRequested(
    LoginRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());
    try {
      final user = await authRepository.login(
        email: event.email,
        password: event.password,
      );
      emit(AuthAuthenticated(user));
    } catch (e) {
      emit(AuthError(e.toString()));
    }
  }

  Future<void> _onLogoutRequested(
    LogoutRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());
    try {
      await authRepository.logout();
      emit(AuthUnauthenticated());
    } catch (e) {
      emit(AuthError(e.toString()));
    }
  }
}
```

### State Management Best Practices

- Keep UI and business logic separate
- Avoid storing complex objects in state
- Use immutable state objects
- Implement proper error handling
- Consider using freezed for immutable state classes

## Navigation

### Routing Approach

- Use named routes for main navigation flows
- Implement route generation for dynamic routes
- Use the Navigator 2.0 API for complex navigation requirements
- Consider using auto_route or go_router for route management

```dart
// Example route configuration
class AppRouter {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case Routes.home:
        return MaterialPageRoute(builder: (_) => const HomeScreen());
      case Routes.profile:
        final args = settings.arguments as ProfileArguments;
        return MaterialPageRoute(
          builder: (_) => ProfileScreen(userId: args.userId),
        );
      case Routes.settings:
        return MaterialPageRoute(builder: (_) => const SettingsScreen());
      default:
        return MaterialPageRoute(
          builder: (_) => const NotFoundScreen(),
        );
    }
  }
}

// Usage
Navigator.pushNamed(
  context,
  Routes.profile,
  arguments: ProfileArguments(userId: '123'),
);
```

### Deep Linking

- Support deep linking for key app features
- Define a clear URI scheme for your app
- Handle deep links in a centralized location
- Test deep links across platforms

## Styling and Theming

### Theme Configuration

- Define a consistent theme using ThemeData
- Create a theme extension for custom theme properties
- Support both light and dark themes
- Use semantic color names in the theme

```dart
// Theme configuration
ThemeData lightTheme = ThemeData(
  primaryColor: AppColors.primary,
  colorScheme: const ColorScheme.light(
    primary: AppColors.primary,
    secondary: AppColors.secondary,
    surface: AppColors.surface,
    background: AppColors.background,
    error: AppColors.error,
  ),
  textTheme: TextTheme(
    headlineLarge: TextStyle(
      fontSize: 28,
      fontWeight: FontWeight.bold,
      color: AppColors.textPrimary,
    ),
    // Define other text styles
  ),
  // Other theme properties
);
```

### Widget Styling

- Use theme properties instead of hardcoded values
- Create reusable style components
- Implement responsive designs using MediaQuery or LayoutBuilder
- Use proper text scaling for accessibility

### Design System

- Implement a consistent design system
- Create a UI kit of standard components
- Document component usage and variations
- Ensure consistent spacing and sizing

## Asset Management

### Asset Organization

- Organize assets by type (images, icons, fonts, etc.)
- Use appropriate formats for different asset types
- Implement resolution-specific assets
- Optimize assets for size and performance

```yaml
# pubspec.yaml asset configuration
flutter:
  assets:
    - assets/images/
    - assets/icons/
    - assets/animations/
  fonts:
    - family: Roboto
      fonts:
        - asset: assets/fonts/Roboto-Regular.ttf
        - asset: assets/fonts/Roboto-Bold.ttf
          weight: 700
```

### Asset Usage

- Use const constructors for asset references
- Create helper classes for asset paths
- Implement proper error handling for asset loading
- Consider using SVGs for icons and simple illustrations

## Internationalization

- Use Flutter's intl package for localization
- Externalize all user-facing strings
- Support right-to-left languages
- Format dates, numbers, and currencies according to locale
- Test UI with different languages and text lengths

```dart
// Localization example
class AppLocalizations {
  static AppLocalizations of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations)!;
  }

  String get appTitle => Intl.message(
        'My Flutter App',
        name: 'appTitle',
        desc: 'The title of the application',
      );

  String welcomeMessage(String name) => Intl.message(
        'Welcome, $name!',
        name: 'welcomeMessage',
        desc: 'Welcome message with user name',
        args: [name],
      );
}

// Usage
Text(AppLocalizations.of(context).welcomeMessage(user.name))
```

## Performance Optimization

### Rendering Optimization

- Use const constructors for static widgets
- Implement ListView.builder for long lists
- Use RepaintBoundary to isolate repaints
- Avoid unnecessary rebuilds with proper state management
- Use cached_network_image for image caching

### Memory Management

- Dispose controllers and subscriptions
- Avoid memory leaks in stateful widgets
- Use weak references for callbacks when appropriate
- Implement pagination for large data sets

### Performance Monitoring

- Use the Flutter DevTools for performance analysis
- Monitor frame rates and jank
- Implement performance tracking in production
- Set performance budgets for key metrics

## Testing

### Test Types

1. **Unit Tests**: For business logic, models, and utilities
2. **Widget Tests**: For UI components
3. **Integration Tests**: For feature workflows
4. **Golden Tests**: For UI appearance verification

### Testing Guidelines

- Aim for high test coverage of business logic
- Mock dependencies for unit tests
- Use test fixtures for consistent test data
- Implement CI/CD pipeline for automated testing

```dart
// Example widget test
testWidgets('LoginScreen shows validation errors', (WidgetTester tester) async {
  // Build the widget
  await tester.pumpWidget(MaterialApp(home: LoginScreen()));

  // Tap the login button without entering credentials
  await tester.tap(find.byType(ElevatedButton));
  await tester.pump();

  // Verify error messages are displayed
  expect(find.text('Email is required'), findsOneWidget);
  expect(find.text('Password is required'), findsOneWidget);
});
```

## Error Handling

- Implement a centralized error handling system
- Use try-catch blocks for error-prone operations
- Display user-friendly error messages
- Log errors for debugging and monitoring
- Implement crash reporting with tools like Sentry or Firebase Crashlytics

```dart
// Error handling example
Future<void> fetchData() async {
  try {
    final result = await apiClient.getData();
    // Process result
  } catch (e) {
    if (e is NetworkException) {
      // Handle network error
      showErrorDialog('Network error. Please check your connection.');
    } else if (e is AuthenticationException) {
      // Handle auth error
      navigateToLogin();
    } else {
      // Handle generic error
      showErrorDialog('An unexpected error occurred.');
    }
    
    // Log the error
    logger.error('Error fetching data', e);
  }
}
```

## Dependency Management

### Package Selection Criteria

- Prefer packages with high pub scores
- Evaluate package maintenance and community support
- Check compatibility with your Flutter version
- Consider license implications
- Assess impact on app size

### Version Management

- Specify version constraints in pubspec.yaml
- Use semantic versioning constraints
- Regularly update dependencies
- Document major dependency changes
- Test thoroughly after dependency updates

```yaml
# Good dependency specification
dependencies:
  flutter:
    sdk: flutter
  http: ^0.13.4
  provider: ^6.0.2
  shared_preferences: ^2.0.13
```

## Platform-Specific Code

### Platform Detection

- Use `Platform` class for platform detection
- Create platform-specific implementations when needed
- Use conditional imports for platform-specific code
- Implement graceful fallbacks for unsupported platforms

```dart
// Platform-specific implementation
Widget getPlatformSpecificWidget() {
  if (Platform.isIOS) {
    return CupertinoButton(
      child: const Text('Click me'),
      onPressed: () {},
    );
  } else {
    return ElevatedButton(
      child: const Text('Click me'),
      onPressed: () {},
    );
  }
}
```

### Native Integration

- Use method channels for native functionality
- Create platform-specific plugins when needed
- Document platform-specific behaviors
- Test on all supported platforms

## Accessibility

- Support screen readers with semantic labels
- Implement proper focus navigation
- Ensure sufficient color contrast
- Support text scaling
- Test with accessibility tools

```dart
// Accessibility example
Semantics(
  label: 'Submit form button',
  hint: 'Double tap to submit the form',
  child: ElevatedButton(
    onPressed: submitForm,
    child: const Text('Submit'),
  ),
)
```

## Security Best Practices

- Secure local storage with encrypted storage solutions
- Implement proper authentication and authorization
- Use HTTPS for all network requests
- Sanitize user input
- Implement certificate pinning for sensitive applications
- Follow platform-specific security guidelines

## CI/CD and Deployment

### CI/CD Pipeline

- Implement automated builds
- Run tests on each pull request
- Perform static code analysis
- Generate build artifacts for testing
- Automate deployment to test environments

### App Distribution

- Configure proper app signing
- Implement versioning strategy
- Create automated release notes
- Set up beta testing channels
- Prepare store listings and screenshots

## Documentation

### Code Documentation

- Document public APIs with dartdoc comments
- Explain complex logic and algorithms
- Create example usage for reusable components
- Document known limitations and edge cases

```dart
/// A button that follows the application's primary style guidelines.
///
/// This button adapts to the current theme and supports loading states.
///
/// Example usage:
/// ```dart
/// PrimaryButton(
///   label: 'Sign In',
///   onPressed: () => _handleSignIn(),
///   isLoading: _isLoading,
/// )
/// ```
class PrimaryButton extends StatelessWidget {
  // Implementation
}
```

### Project Documentation

- Maintain a comprehensive README
- Document setup and installation steps
- Create architecture diagrams
- Document state management approach
- Include troubleshooting guides 