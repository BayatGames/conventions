# Tauri Development Guidelines

This document outlines the standards and best practices for developing desktop applications using Tauri at Bayat.

## Table of Contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Development Environment](#development-environment)
4. [Architecture](#architecture)
5. [Security](#security)
6. [Performance](#performance)
7. [Native Integration](#native-integration)
8. [Building and Distribution](#building-and-distribution)
9. [Testing](#testing)
10. [Resources](#resources)

## Introduction

Tauri is a framework for building tiny, blazingly fast binaries for all major desktop platforms. Tauri uses a Rust-based backend and a web-based frontend, providing significantly smaller bundle sizes compared to Electron.

### When to Use Tauri

Tauri is the preferred choice for desktop applications when:
- Application size and performance are critical concerns
- The target application is relatively lightweight
- You need deep system integration with minimal overhead
- Security is a top priority

### Key Benefits

- **Performance**: Rust-based backend provides excellent performance
- **Security**: Built with a security-first approach
- **Bundle Size**: Significantly smaller than Electron applications
- **Resource Usage**: Lower memory and CPU usage
- **Multi-platform**: Support for Windows, macOS, and Linux

## Project Structure

### Recommended Project Structure

```
project-root/
├── .github/                 # GitHub workflows and templates
├── src/                     # Rust source code
│   ├── main.rs              # Main Rust entry point
│   ├── cmd.rs               # Command implementations
│   └── menu.rs              # Application menu definitions
├── src-tauri/               # Tauri configuration files
│   ├── Cargo.toml           # Rust dependencies
│   ├── tauri.conf.json      # Tauri configuration
│   ├── build.rs             # Build script
│   └── icons/               # Application icons
├── public/                  # Static assets
├── src-frontend/            # Frontend application source
│   ├── components/          # UI components
│   ├── pages/               # Application pages
│   ├── store/               # State management
│   ├── utils/               # Utility functions
│   ├── App.jsx              # Main component
│   └── main.js              # Frontend entry point
├── .gitignore               # Git ignore file
├── package.json             # Frontend dependencies
└── README.md                # Project documentation
```

### Key Configuration Files

#### tauri.conf.json

```json
{
  "build": {
    "distDir": "../dist",
    "devPath": "http://localhost:3000",
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build"
  },
  "package": {
    "productName": "AppName",
    "version": "0.1.0"
  },
  "tauri": {
    "allowlist": {
      "all": false,
      "fs": {
        "readFile": true,
        "writeFile": true,
        "scope": ["$APP/*"]
      },
      "dialog": {
        "open": true,
        "save": true
      }
    },
    "bundle": {
      "active": true,
      "category": "DeveloperTool",
      "copyright": "",
      "deb": {
        "depends": []
      },
      "icon": [
        "icons/32x32.png",
        "icons/128x128.png",
        "icons/128x128@2x.png",
        "icons/icon.icns",
        "icons/icon.ico"
      ],
      "identifier": "io.bayat.appname",
      "longDescription": "",
      "macOS": {
        "entitlements": null,
        "exceptionDomain": "",
        "frameworks": [],
        "providerShortName": null,
        "signingIdentity": null
      },
      "shortDescription": "",
      "targets": "all",
      "windows": {
        "certificateThumbprint": null,
        "digestAlgorithm": "sha256",
        "timestampUrl": ""
      }
    },
    "security": {
      "csp": "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'"
    },
    "updater": {
      "active": false
    },
    "windows": [
      {
        "fullscreen": false,
        "height": 600,
        "resizable": true,
        "title": "AppName",
        "width": 800
      }
    ]
  }
}
```

## Development Environment

### Required Tools

- Rust toolchain (latest stable)
- Node.js (LTS version)
- Platform-specific build tools:
  - **Windows**: Microsoft Visual Studio C++ Build Tools
  - **macOS**: Xcode Command Line Tools
  - **Linux**: Development packages (build-essential)

### Development Setup

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install Tauri CLI
cargo install tauri-cli

# Create a new project
npm create tauri-app@latest

# Run development server
npm run tauri dev
```

## Architecture

### Frontend

- Use React, Vue.js, or Svelte for the frontend UI
- TypeScript is strongly recommended
- Organize code using a component-based architecture

### Backend (Rust)

- Write Rust code that follows the [Rust Style Guide](https://doc.rust-lang.org/1.0.0/style/README.html)
- Implement business logic in Rust for better performance
- Use appropriate error handling patterns

### Communication

- Use Tauri's Commands API for most frontend-backend communication:

```rust
// Rust side
#[tauri::command]
fn save_data(data: String) -> Result<String, String> {
    // Implement save functionality
    Ok("Data saved successfully".into())
}

// In main.rs
fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![save_data])
        .run(tauri::generate_context!())
        .expect("Error while running tauri application");
}
```

```javascript
// Frontend side
import { invoke } from '@tauri-apps/api/tauri';

// Call the command
const result = await invoke('save_data', { data: 'Hello, World!' });
console.log(result); // "Data saved successfully"
```

## Security

### Best Practices

1. Use the principle of least privilege through the allowlist
2. Define a strict Content Security Policy
3. Validate all user inputs on both frontend and backend
4. Limit the filesystem scope to only what's necessary
5. Keep dependencies up to date

### Allowlist Configuration

The allowlist in `tauri.conf.json` should only include the APIs that your application absolutely needs:

```json
"allowlist": {
  "all": false,
  "fs": {
    "readFile": true,
    "writeFile": true,
    "scope": ["$APP/*"]
  },
  "dialog": {
    "open": true,
    "save": true
  }
}
```

## Performance

### Rust-Side Optimizations

- Move computationally intensive tasks to the Rust backend
- Use async/await for I/O-bound operations
- Implement proper error handling to avoid panics

### Frontend Optimizations

- Use production builds for deployment
- Implement code-splitting for larger applications
- Optimize asset loading and rendering

## Native Integration

### File System Access

Use Tauri's filesystem API for secure file operations:

```rust
#[tauri::command]
fn read_file_content(path: String) -> Result<String, String> {
    match std::fs::read_to_string(path) {
        Ok(content) => Ok(content),
        Err(e) => Err(e.to_string())
    }
}
```

### Shell Commands

When you need to execute shell commands:

```rust
#[tauri::command]
async fn execute_command(command: String) -> Result<String, String> {
    let output = tauri::api::process::Command::new("cmd")
        .args(&["/C", &command])
        .output()
        .await
        .map_err(|e| e.to_string())?;
    
    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    } else {
        Err(String::from_utf8_lossy(&output.stderr).to_string())
    }
}
```

## Building and Distribution

### Building for Production

```bash
# Build for production
npm run tauri build
```

The built applications will be in the `src-tauri/target/release/bundle` directory.

### Code Signing

- **Windows**: Use a code signing certificate from a trusted CA
- **macOS**: Use an Apple Developer certificate for notarization
- **Linux**: Consider using Flatpak or AppImage for distribution

### Auto-Updates

Enable and configure the updater in `tauri.conf.json`:

```json
"updater": {
  "active": true,
  "endpoints": [
    "https://releases.myapp.com/{{target}}/{{current_version}}"
  ],
  "dialog": true,
  "pubkey": "YOUR_PUBLIC_KEY"
}
```

## Testing

### Frontend Testing

- Use Jest, Vitest, or Testing Library for component testing
- Implement E2E tests with Cypress or Playwright

### Rust Testing

- Write unit tests for Rust functions

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_process_data() {
        let result = process_data("test");
        assert_eq!(result, "processed: test");
    }
}
```

## Resources

- [Tauri Official Documentation](https://tauri.app/docs/intro/)
- [Rust Book](https://doc.rust-lang.org/book/)
- [Tauri API Documentation](https://tauri.app/docs/api/js/)
- [Awesome Tauri](https://github.com/tauri-apps/awesome-tauri) 