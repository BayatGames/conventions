# Rust Coding Standards for Tauri

This document outlines the Rust coding standards for Tauri development according to Bayat standards.

## Naming Conventions

### General Rules

- Use **snake_case** for:
  - Functions and methods (e.g., `process_data()`)
  - Variables (e.g., `user_input`)
  - Modules (e.g., `file_handling`)
  - Crates (e.g., `tauri_utils`)

- Use **CamelCase** for:
  - Types (e.g., `UserProfile`)
  - Traits (e.g., `DataProcessor`)
  - Enums (e.g., `FileState`)
  - Type parameters (e.g., `T` in `Vec<T>`)

- Use **SCREAMING_SNAKE_CASE** for:
  - Constants (e.g., `MAX_CONNECTIONS`)
  - Static variables (e.g., `GLOBAL_STATE`)

- **Prefer descriptive names** over abbreviations
- **Keep names concise** while maintaining clarity

### Tauri-Specific

- **Command functions** should be named with a verb that describes their action:
  - `get_user_data` not `user_data`
  - `save_settings` not `write_settings_to_disk`

- **Events** should use noun phrases with past tense verbs:
  - `file_saved`
  - `profile_updated`
  - `connection_established`

## Code Structure

### Module Organization

- **Group related functionality** in modules (e.g., `auth`, `database`, `fs`)
- **Export public items** through the module's `mod.rs` or `lib.rs`
- **Hide implementation details** using private functions and structures

```rust
// src/database/mod.rs
mod connection;
mod queries;

pub use connection::Connection;
pub use queries::fetch_user;
```

### Function Design

- **Keep functions small and focused** on a single responsibility
- **Limit function parameters** (consider using structs for multiple parameters)
- **Return `Result` types** for operations that can fail
- **Use documentation comments** to explain function purpose and parameters

```rust
/// Retrieves user data from the database
///
/// # Arguments
///
/// * `user_id` - The unique identifier of the user
///
/// # Returns
///
/// A Result containing either the user data or an error message
#[tauri::command]
pub async fn get_user_data(user_id: String) -> Result<User, String> {
    // Implementation
}
```

## Error Handling

### Error Types

- **Define custom error types** for your application:

  ```rust
  #[derive(Debug, thiserror::Error)]
  pub enum AppError {
      #[error("Database connection failed: {0}")]
      DatabaseConnection(String),
      
      #[error("User not found: {0}")]
      UserNotFound(String),
      
      #[error("Invalid input: {0}")]
      InvalidInput(String)
  }
  ```

- **Use the `thiserror` crate** for custom errors
- **Implement `From` traits** for error conversion

### Error Propagation

- **Use the `?` operator** for error propagation
- **Avoid `.unwrap()` and `.expect()`** in production code
- **Transform errors** into appropriate types when crossing API boundaries
- **Provide context** when converting errors:

  ```rust
  fn read_config() -> Result<Config, AppError> {
      let config_str = std::fs::read_to_string("config.json")
          .map_err(|e| AppError::FileOperation(format!("Failed to read config: {}", e)))?;
      
      serde_json::from_str(&config_str)
          .map_err(|e| AppError::ParseError(format!("Invalid config format: {}", e)))
  }
  ```

## Performance and Safety

### Memory Management

- **Minimize use of `Clone`** for large data structures
- **Consider using references** instead of ownership when appropriate
- **Use appropriate lifetime parameters** to ensure memory safety
- **Prefer stack allocation** over heap when possible

### Concurrency

- **Use message passing** over shared state when possible
- **Prefer `Arc` and `Mutex`** for thread-safe shared state
- **Avoid deadlocks** by keeping lock scopes small
- **Consider using channels** for communication between threads
- **Use the `tokio` runtime** for async operations in Tauri

```rust
use std::sync::{Arc, Mutex};

#[derive(Default)]
struct AppState {
    counter: Mutex<i32>,
}

#[tauri::command]
fn increment_counter(state: tauri::State<Arc<AppState>>) -> i32 {
    let mut counter = state.counter.lock().unwrap();
    *counter += 1;
    *counter
}
```

## Documentation

### Code Documentation

- **Document all public items** with doc comments (`///`)
- **Include examples** where appropriate
- **Explain panics and errors** that may occur
- **Document performance considerations** for critical code
- **Keep documentation up-to-date** with code changes

```rust
/// Processes a file and extracts metadata.
///
/// # Arguments
///
/// * `path` - A path to the file to process
///
/// # Returns
///
/// A Result containing the file metadata or an error
///
/// # Examples
///
/// ```
/// let metadata = process_file("config.json")?;
/// println!("File size: {}", metadata.size);
/// ```
///
/// # Errors
///
/// Returns an error if:
/// * The file does not exist
/// * The file cannot be read
/// * The file format is invalid
pub fn process_file(path: &str) -> Result<FileMetadata, AppError> {
    // Implementation
}
```

### Inline Comments

- **Comment complex algorithms** or non-obvious code
- **Avoid obvious comments** that merely repeat the code
- **Use TODO/FIXME comments** with issue references for future work

## Dependencies

### Crate Selection

- **Prefer well-maintained crates** with good documentation
- **Check for security vulnerabilities** before adding dependencies
- **Be mindful of license compatibility**
- **Minimize dependency count** to reduce build times and attack surface

### Version Pinning

- **Pin dependency versions** in `Cargo.toml`
- **Use semantic versioning** (`^` for minor, `~` for patch-level updates)
- **Audit dependencies regularly** for updates and security patches
