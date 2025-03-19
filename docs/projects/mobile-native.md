# Mobile Development Guidelines: Native iOS and Android

This document outlines best practices, standards, and guidelines for native mobile development at Bayat, focusing specifically on iOS (Swift/UIKit/SwiftUI) and Android (Kotlin/Java/Jetpack).

## Table of Contents

- [Introduction](#introduction)
- [Platform Selection Guidelines](#platform-selection-guidelines)
- [iOS Development Standards](#ios-development-standards)
- [Android Development Standards](#android-development-standards)
- [Common Architecture Guidelines](#common-architecture-guidelines)
- [UI/UX Guidelines](#uiux-guidelines)
- [Performance Optimization](#performance-optimization)
- [Security Best Practices](#security-best-practices)
- [Testing Guidelines](#testing-guidelines)
- [Release Process](#release-process)
- [Tools and Resources](#tools-and-resources)

## Introduction

This document provides standards for native mobile development at Bayat, complementing our cross-platform guidelines. While we support multiple approaches to mobile development, these guidelines ensure high-quality native applications when that approach is selected.

### When to Choose Native Development

Native development is recommended when:

1. **Performance is critical**: Applications requiring maximum performance
2. **Platform-specific features**: Heavy use of platform capabilities (ARKit/ARCore, CoreML, etc.)
3. **Device hardware integration**: Deep hardware access requirements
4. **Complex UI/animations**: Sophisticated user experiences
5. **Long-term strategic products**: Core business applications with long lifespans

## Platform Selection Guidelines

### iOS vs. Android First

When resources require prioritizing one platform:

- **iOS First**:
  - Primary user base is iOS-dominant
  - Higher average revenue per user is a priority
  - App leverages specific Apple ecosystem features
  - Design-focused applications where pixel-perfect implementation is critical

- **Android First**:
  - Global or emerging market focus
  - Wide device compatibility is required
  - App requires deeper OS integration or customization
  - User base is primarily Android

### Minimum Platform Support

- **iOS**: Support the two most recent major iOS versions (currently iOS 16+)
- **Android**: Support API level 26 (Android 8.0) and above

## iOS Development Standards

### Language and Tools

- **Primary Language**: Swift (latest stable version)
- **Legacy Support**: Objective-C only for maintaining existing code
- **UI Frameworks**:
  - SwiftUI for new projects where iOS 14+ is acceptable
  - UIKit for broader compatibility or complex UI needs
  - Combine for reactive programming
- **IDE**: Xcode (latest stable version)
- **Dependency Management**: Swift Package Manager preferred, CocoaPods acceptable

### Swift Coding Standards

- **Style Guide**: Follow the [Swift API Design Guidelines](https://swift.org/documentation/api-design-guidelines/)
- **Formatting**: Use SwiftLint with Bayat's configuration
- **Swift Features**:
  - Prefer structs over classes when immutability is appropriate
  - Use optionals and proper unwrapping instead of force unwrapping
  - Leverage Swift's type system for compile-time safety
  - Use protocol-oriented programming when appropriate

### iOS Architecture

- **Preferred Patterns**:
  - MVVM for UIKit applications
  - MVVM or The Composable Architecture (TCA) for SwiftUI
  - Coordinator pattern for navigation in UIKit apps
- **State Management**:
  - Combine for UIKit applications
  - State and environment objects for SwiftUI
- **Dependencies**: Use dependency injection for testability

### iOS-Specific Best Practices

- **App Lifecycle**: Properly handle background/foreground transitions
- **Memory Management**: Avoid retain cycles, use weak references appropriately
- **Localization**: Support dynamic text sizes and full localization
- **Accessibility**: Implement VoiceOver support and dynamic type
- **App Extensions**: Follow app extension guidelines for app clips, widgets, etc.

## Android Development Standards

### Language and Tools

- **Primary Language**: Kotlin (latest stable version)
- **Legacy Support**: Java only for maintaining existing code
- **UI Frameworks**:
  - Jetpack Compose for new projects where API 21+ is acceptable
  - XML layouts for broader compatibility
  - Jetpack libraries for architecture components
- **IDE**: Android Studio (latest stable version)
- **Dependency Management**: Gradle with version catalogs

### Kotlin Coding Standards

- **Style Guide**: Follow the [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- **Formatting**: Use ktlint with Bayat's configuration
- **Kotlin Features**:
  - Use coroutines for asynchronous programming
  - Leverage extension functions for cleaner code
  - Use data classes for models
  - Prefer immutability with val over var
  - Use nullable types properly with safe calls

### Android Architecture

- **Preferred Patterns**:
  - MVVM with Android Architecture Components
  - MVI for Jetpack Compose applications
  - Clean Architecture for complex applications
- **State Management**:
  - ViewModel with LiveData or StateFlow
  - Unidirectional data flow with MVI
- **Dependencies**: Use Hilt or Koin for dependency injection

### Android-Specific Best Practices

- **Activity/Fragment Lifecycle**: Properly handle configuration changes
- **Background Processing**: Use WorkManager for background tasks
- **Permissions**: Follow runtime permission best practices
- **Adaptive Layouts**: Support multiple screen sizes and orientations
- **Material Design**: Follow Material Design guidelines consistently

## Common Architecture Guidelines

### Project Structure

- **Feature-Based Organization**: Organize code by feature rather than type
- **Core Module Separation**: Separate core functionality into modules
- **UI Layer Isolation**: Keep UI layer independent from business logic
- **Repository Pattern**: Use repositories to abstract data sources
- **Clean API Layer**: Well-defined API clients with proper error handling

### Data Management

- **Local Storage**:
  - iOS: CoreData for complex data, UserDefaults for simple preferences
  - Android: Room for complex data, SharedPreferences for simple preferences
- **Remote Data**:
  - Use Retrofit (Android) or URLSession/Alamofire (iOS)
  - Implement proper caching strategies
  - Handle offline scenarios gracefully
- **State Persistence**:
  - Save and restore UI state across lifecycle events
  - Handle process death and recreation

### Networking

- **API Communication**:
  - RESTful or GraphQL with proper error handling
  - Request timeouts and retry logic
  - Authentication token management
  - Certificate pinning for sensitive applications
- **Offline Support**:
  - Clear offline indicators
  - Queue operations for sync when connection is restored
  - Conflict resolution strategy

## UI/UX Guidelines

### Platform-Specific Design

- **iOS**:
  - Follow Apple's Human Interface Guidelines
  - Support Dark Mode
  - Implement proper safe area handling
  - Use SF Symbols for iconography
  - Follow iOS navigation patterns (tabs, navigation stack)

- **Android**:
  - Follow Material Design guidelines
  - Support theme switching (light/dark)
  - Use material components for UI elements
  - Implement proper edge-to-edge handling
  - Follow Android navigation patterns (bottom nav, drawer, etc.)

### Common Design Requirements

- **Responsive Layouts**: Support all device sizes in the target range
- **Accessibility**:
  - Support screen readers (VoiceOver/TalkBack)
  - Meet minimum contrast requirements
  - Support dynamic text sizes
  - Implement proper focus navigation
- **Animation**:
  - Purposeful, not gratuitous
  - Support reduced motion settings
  - Consistent timing and easing

### Input Handling

- **Touch Targets**: Minimum 44×44pt (iOS) or 48×48dp (Android)
- **Gestures**: Follow platform conventions for common gestures
- **Keyboard**: Proper keyboard type for input fields
- **Form Validation**: Clear error feedback and recovery

## Performance Optimization

### Memory Management

- **Image Handling**:
  - Resize images appropriately before display
  - Use memory-efficient image formats
  - Implement proper caching
- **Collection Views**:
  - Reuse cells/view holders
  - Implement pagination for large datasets
  - Optimize cell measurement and layout

### Responsiveness

- **Main Thread**: Keep UI thread free from blocking operations
- **Background Processing**:
  - Move expensive operations off the main thread
  - Use appropriate concurrency primitives
  - Handle thread synchronization properly
- **Launch Time**: Optimize app startup time (<2 seconds goal)

### Battery Efficiency

- **Location Services**: Use appropriate accuracy and update frequency
- **Networking**: Batch requests, use efficient polling or push notifications
- **Background Processing**: Minimize background work
- **Sensors**: Turn off sensors when not actively used

### Size Optimization

- **App Size**:
  - Optimize asset sizes with appropriate compression
  - Use app thinning (iOS) or Android App Bundles
  - Remove unused resources and code
- **Dependencies**: Only include necessary libraries

## Security Best Practices

### Data Storage

- **Sensitive Data**:
  - iOS: Use Keychain for credentials and tokens
  - Android: Use EncryptedSharedPreferences or Keystore
- **Encryption**: Encrypt sensitive local data
- **Data Minimization**: Only store what's necessary

### Networking Security

- **TLS**: Enforce TLS 1.2+ for all network connections
- **Certificate Pinning**: Implement for sensitive applications
- **API Keys**: Never hardcode or store insecurely
- **Authentication**: Secure token handling with proper renewal

### Code Security

- **Input Validation**: Validate all user and server input
- **Dependencies**: Regular security audits of dependencies
- **Obfuscation**:
  - Android: Use R8/ProGuard
  - iOS: Strip debug symbols in release builds
- **Jailbreak/Root Detection**: Implement for financial or highly sensitive apps

## Testing Guidelines

### Unit Testing

- **Coverage Target**: Minimum 70% code coverage for business logic
- **Frameworks**:
  - iOS: XCTest, Quick/Nimble for BDD style
  - Android: JUnit, Mockito, Robolectric
- **Mock Dependencies**: Use dependency injection to facilitate testing

### UI Testing

- **Automated UI Tests**:
  - iOS: XCUITest
  - Android: Espresso, UI Automator
- **Screenshot Testing**:
  - iOS: SnapshotTesting
  - Android: Screenshot tests with Roborazzi

### Integration and End-to-End Testing

- **API Integration**: Test actual API interactions in isolation
- **End-to-End**: Critical user flows on actual devices
- **Test Environments**: Dedicated test environments for automated tests

### Performance Testing

- **Benchmarking**: Establish baseline performance metrics
- **Memory Leaks**: Use instruments (iOS) or LeakCanary (Android)
- **UI Responsiveness**: Test scrolling performance with large datasets

## Release Process

### App Store/Play Store Preparation

- **Metadata**:
  - Compelling screenshots and app preview videos
  - Keyword-optimized descriptions
  - Complete all required metadata fields
- **Release Notes**: Clear and concise description of changes
- **Staged Rollout**: Use phased releases for major updates

### CI/CD Pipeline

- **Automated Builds**: Configure fastlane or similar tools
- **Signing**:
  - iOS: Use App Store Connect API and automated provisioning
  - Android: Use signing configs in Gradle
- **Distribution Channels**:
  - Development: Internal distribution
  - Testing: TestFlight/Firebase App Distribution
  - Production: App Store/Play Store

### Pre-Release Checklist

- **Final Testing**: Test on actual target devices
- **Accessibility Audit**: Verify accessibility compliance
- **Localization Review**: Check all supported languages
- **Performance Verification**: Test on lowest supported devices
- **Store Guidelines Compliance**: Review current platform guidelines

## Tools and Resources

### Recommended Tools

- **Analytics**: Firebase Analytics, Mixpanel
- **Crash Reporting**: Firebase Crashlytics
- **Performance Monitoring**: Firebase Performance, New Relic Mobile
- **Feature Flags**: Firebase Remote Config, LaunchDarkly
- **CI/CD**: GitHub Actions, Bitrise, fastlane

### Learning Resources

- **iOS**:
  - Apple Developer Documentation
  - Swift by Sundell, Swift with Majid, Point-Free
  - WWDC session videos
- **Android**:
  - Android Developers Documentation
  - Google Codelabs
  - Android Developer Summit videos

### Internal Resources

- **Component Libraries**:
  - iOS UI component library
  - Android UI component library
- **Code Examples**: Repository of example implementations
- **Architecture Templates**: Starter projects with architecture in place
