# Tauri Development Conventions - MDC Files

These Multi-Document Context (MDC) files provide quick reference guidelines for Tauri application development according to Bayat standards. Place these files in the `.cursor/mdc/` directory of your project to enable context-aware development in Cursor IDE.

## Available Convention Files

- [Tauri Best Practices](tauri_best_practices.md) - Core Tauri patterns and security best practices
- [Rust Standards](rust_standards.md) - Rust coding conventions and patterns for Tauri backend
- [Frontend Integration](frontend_integration.md) - Guidelines for connecting frontend framework with Tauri
- [Project Architecture](project_architecture.md) - Project structure, organization, and file layout

## Setup Instructions

1. Create a `.cursor/mdc/` directory in your project root
2. Copy these MDC files into that directory
3. Add the corresponding `.cursorrules` file from `templates/cursorrules/tauri.json` to your project root as `.cursorrules`

## Related Guidelines

For more detailed documentation, refer to the full convention docs:

- [Rust Standards](../../../docs/languages/rust.md)
- [Tauri Standards](../../../docs/frameworks/tauri.md)
- [Desktop App Architecture](../../../docs/architecture/desktop.md)
