# Tauri Project Architecture

This document outlines best practices for structuring Tauri applications according to Bayat standards.

## Project Structure

### Root Directory Organization

A well-organized Tauri project should follow this structure:

```plaintext
my-tauri-app/                # Should follow Bayat naming convention (e.g., bayat-taskmanager)
├── src/                     # Rust backend code
├── src-tauri/               # Tauri configuration and bridge
├── src-frontend/            # Frontend code (React, Vue, etc.)
├── .github/                 # CI/CD workflows
├── scripts/                 # Build and utility scripts
├── .gitignore               # Git ignore patterns
├── README.md                # Project documentation
└── package.json             # Project metadata and scripts (should use io.bayat.apps.{appname})
```

### Rust Backend Structure (src/)

The Rust backend should be organized by feature:

```plaintext
src/
├── main.rs               # Entry point with Tauri builder
├── commands/             # Tauri commands
│   ├── mod.rs            # Commands module exports
│   ├── file_system.rs    # File-related commands
│   ├── database.rs       # Database-related commands
│   └── auth.rs           # Authentication commands
├── models/               # Data models and structures
│   ├── mod.rs            # Models module exports
│   ├── user.rs           # User-related models
│   └── settings.rs       # Settings models
├── services/             # Core business logic
│   ├── mod.rs            # Services module exports
│   ├── database.rs       # Database service
│   └── storage.rs        # Storage service
└── utils/                # Utility functions
    ├── mod.rs            # Utils module exports
    ├── error.rs          # Error handling utilities
    └── config.rs         # Configuration utilities
```

### Tauri Configuration (src-tauri/)

The Tauri-specific configuration should be organized as:

```plaintext
src-tauri/
├── Cargo.toml            # Rust dependencies (should use bayat-{category} crate naming)
├── tauri.conf.json       # Tauri configuration (should use io.bayat.apps.{appname} identifier)
├── build.rs              # Build script
├── icons/                # Application icons
└── Tauri.toml            # Tauri-specific metadata
```

### Frontend Structure (src-frontend/)

The frontend should follow standard practices for the chosen framework:

```plaintext
src-frontend/             # React example
├── public/               # Static assets
├── src/
│   ├── api/              # Frontend API client
│   │   ├── index.ts      # API exports
│   │   ├── user.ts       # User-related API calls
│   │   └── files.ts      # File-related API calls
│   ├── components/       # UI components
│   ├── hooks/            # Custom hooks
│   ├── pages/            # Page components
│   ├── store/            # State management
│   ├── styles/           # CSS/styling
│   ├── utils/            # Frontend utilities
│   ├── App.tsx           # Main application component
│   └── main.tsx          # Entry point
├── package.json          # Frontend dependencies
└── tsconfig.json         # TypeScript configuration
```

## Module Organization

### Rust Module Pattern

Follow these patterns for Rust modules:

- **Use a `mod.rs` file** in each directory to re-export items
- **Group related functionality** into modules
- **Maintain a clear separation** between different layers

Example `commands/mod.rs`:

```rust
mod file_system;
mod database;
mod auth;

// Re-export commands for Tauri
pub use file_system::*;
pub use database::*;
pub use auth::*;

// Register all commands
pub fn register_commands() -> Vec<Command> {
    vec![
        file_system::read_file::read_file,
        file_system::write_file::write_file,
        database::get_users::get_users,
        auth::login::login,
        // Other commands...
    ]
}
```

### Frontend Module Pattern

For frontend code, use the following patterns:

- **Create barrel files** (`index.ts`) to re-export components and hooks
- **Colocate related files** (component, styles, tests) when appropriate
- **Use feature-based organization** for larger applications

## Configuration Management

### Tauri Configuration

Organize your `tauri.conf.json` into logical sections:

```json
{
  "build": {
    "distDir": "../dist",
    "devPath": "http://localhost:3000"
  },
  "tauri": {
    "bundle": {
      "identifier": "com.bayat.myapp",
      "icon": ["icons/32x32.png", "icons/128x128.png", "icons/128x128@2x.png"]
    },
    "security": {
      "csp": "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'"
    },
    "updater": {
      "active": true,
      "endpoints": ["https://releases.myapp.com/{{target}}/{{current_version}}"],
      "dialog": true,
      "pubkey": "YOUR_PUB_KEY"
    },
    "allowlist": {
      "fs": {
        "readFile": true,
        "writeFile": true,
        "readDir": true,
        "scope": ["$APPDATA/*", "$RESOURCE/*"]
      },
      "dialog": {
        "open": true,
        "save": true
      }
    },
    "windows": [
      {
        "title": "My Tauri App",
        "width": 800,
        "height": 600,
        "center": true,
        "resizable": true
      }
    ]
  }
}
```

### Environment-Specific Configuration

- **Use environment files** (.env, .env.development, etc.) for environment-specific values
- **Implement configuration loading** in both frontend and backend
- **Keep sensitive values out of source control**

## Application Architecture

### Data Flow

Implement a clear data flow pattern:

1. **UI Layer** (React/Vue components) - Handle user interaction and display
2. **API Layer** (Frontend API clients) - Communicate with Tauri commands
3. **Command Layer** (Tauri commands) - Validate inputs and route to services
4. **Service Layer** (Rust services) - Implement business logic
5. **Data Layer** (Rust models) - Persistence and data access

### State Management

Define a clear strategy for state management:

- **Backend state** - Persistent data stored in databases or files
- **Session state** - User-specific temporary data
- **UI state** - Transient state for UI components

## Testing Structure

Organize tests to mirror your source structure:

```plaintext
src/
├── commands/
│   ├── file_system.rs
│   └── file_system_test.rs  # Unit tests for file_system commands
```

```plaintext
src-frontend/
├── src/
│   ├── components/
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx  # Component tests
│   │   │   └── Button.module.css
```

## Build and Deployment

### Build Scripts

Organize build scripts for different environments:

```plaintext
scripts/
├── build.js           # Main build script
├── build-dev.js       # Development build
├── build-prod.js      # Production build
└── pre-release.js     # Pre-release checks
```

### CI/CD Configuration

Structure CI/CD workflows by platform:

```plaintext
.github/workflows/
├── release.yml        # Release workflow
├── build-windows.yml  # Windows build
├── build-macos.yml    # macOS build
├── build-linux.yml    # Linux build
└── test.yml           # Test workflow
```

## Documentation

Organize documentation by audience and purpose:

```plaintext
docs/
├── architecture/      # Architecture documentation
├── api/               # API documentation
├── user/              # User documentation
└── developer/         # Developer documentation
```
