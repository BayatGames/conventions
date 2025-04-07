<!--
Document: Bayat Naming Conventions
Version: 1.0.0
Last Updated: 2025-04-06
Last Updated By: Bayat Platform Team
Change Log:
- 2025-04-06: Initial version
-->

# Bayat Naming Conventions

This document outlines the standardized naming conventions for namespaces, package identifiers, and other naming structures across all Bayat projects.

## Namespace Conventions

### C# and Unity

For C# projects, including Unity games and libraries:

- **Games**: `Bayat.Games.{GameName}`
  - Example: `Bayat.Games.Twins`
  - Optional Game suffix: `Bayat.Games.TwinsGame`

- **Game Libraries**: `Bayat.Games.{Category}`
  - Example: `Bayat.Games.UI`, `Bayat.Games.Core`

- **Core Libraries**: `Bayat.{Category}`
  - Example: `Bayat.Core`, `Bayat.UI`, `Bayat.Tools`

- **Platform-Specific**: `Bayat.{Platform}.{Category}`
  - Example: `Bayat.Unity.UI`, `Bayat.Unreal.Core`

### JavaScript and TypeScript

For JavaScript/TypeScript projects:

- **Packages**: `@bayat/{category}`
  - Example: `@bayat/ui`, `@bayat/core`

- **Platform-Specific**: `@bayat/{platform}-{category}`
  - Example: `@bayat/react-components`, `@bayat/vue-forms`

### Rust

For Rust projects:

- **Main Libraries**: `bayat::{category}`
  - Example: `bayat::core`, `bayat::utils`

- **Applications**: `bayat::apps::{appname}`
  - Example: `bayat::apps::taskmanager`

- **Tools**: `bayat::tools::{toolname}`
  - Example: `bayat::tools::bundler`

## Package Identifier Conventions

### Unity

- **Unity Packages**: `io.bayat.unity.{category}`
  - Example: `io.bayat.unity.ui`, `io.bayat.unity.tools`

- **Game Bundles**: `io.bayat.games.{gamename}`
  - Example: `io.bayat.games.twins`

### Tauri and Electron

- **Application Bundles**: `io.bayat.apps.{appname}`
  - Example: `io.bayat.apps.taskmanager`, `io.bayat.apps.dashboard`

- **Tauri Plugins**: `io.bayat.tauri.{plugin}`
  - Example: `io.bayat.tauri.storage`

### Native Mobile

- **iOS Applications**: `io.bayat.ios.{appname}`
  - Example: `io.bayat.ios.twins`

- **Android Applications**: `io.bayat.android.{appname}`
  - Example: `io.bayat.android.twins`

### Web Applications

- **Web Applications**: `io.bayat.web.{appname}`
  - Example: `io.bayat.web.dashboard`

### npm Packages

- **npm Packages**: `@bayat/{category}`
  - Example: `@bayat/ui`, `@bayat/core`

### Rust Crates

- **Rust Crates**: `bayat-{category}`
  - Example: `bayat-core`, `bayat-utils`

## File Naming Conventions

- **C# Files**: PascalCase matching class name
  - Example: `PlayerController.cs`

- **JavaScript/TypeScript Files**: kebab-case for utilities, PascalCase for components
  - Example: `api-client.ts`, `UserProfile.tsx`

- **Rust Files**: snake_case
  - Example: `database_manager.rs`

## Directory Structure Conventions

- **Unity Projects**: PascalCase for main directories
  - Example: `Assets/Scripts/Player/`

- **Web Projects**: kebab-case for directories
  - Example: `src/components/user-profile/`

- **Rust Projects**: snake_case for directories
  - Example: `src/database/queries/`

## Implementation Guidelines

- All new projects MUST follow these naming conventions
- Existing projects should be migrated to these conventions during major updates
- Package identifiers should be consistent across all platforms for the same product
- Documentation should reference these conventions explicitly

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 2025-04-06 | Initial version |
