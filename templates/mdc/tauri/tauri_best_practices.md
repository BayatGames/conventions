# Tauri Best Practices

This document outlines best practices for Tauri application development according to Bayat standards.

## Security Guidelines

### Content Security Policy

- **Always define a restrictive CSP** in your `tauri.conf.json`:

  ```json
  "security": {
    "csp": "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'"
  }
  ```

- **Avoid loading remote content** such as scripts from CDNs, as they introduce security vulnerabilities
- **Limit 'unsafe-inline'** usage to only what's absolutely necessary
- **Review CSP regularly** as your application evolves to maintain the principle of least privilege

### Permissions

- **Use the allowlist pattern** to explicitly enable only the APIs your app needs:

  ```json
  "tauri": {
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
    }
  }
  ```

- **Implement path scoping** to restrict filesystem access to only necessary locations
- **Avoid enabling all permissions** by default - prefer explicit allowlisting
- **Regularly audit permissions** to ensure they match your application's current needs

### Secure Communication

- **Validate all IPC inputs** on the Rust side:

  ```rust
  #[tauri::command]
  async fn save_data(data: String) -> Result<(), String> {
    // Validate data before processing
    if !is_valid_data(&data) {
      return Err("Invalid data format".into());
    }
    // Process valid data
    Ok(())
  }
  ```

- **Use type checking** for command parameters via strong typing
- **Never trust frontend data** without validation
- **Return Result types** to properly handle errors and avoid unwraps

## API Design

### Command Structure

- **Keep commands focused** - each command should do one thing well
- **Use semantic naming** to clearly communicate purpose:

  ```rust
  #[tauri::command]
  fn read_user_settings() -> Result<Settings, String> { /* ... */ }
  
  #[tauri::command]
  fn save_user_settings(settings: Settings) -> Result<(), String> { /* ... */ }
  ```

- **Group related commands** in modules by functionality
- **Use async commands** for operations that might block:

  ```rust
  #[tauri::command]
  async fn process_large_file(path: String) -> Result<Stats, String> {
    // Long-running operation
    Ok(stats)
  }
  ```

### Error Handling

- **Return Result types** to properly handle errors:

  ```rust
  #[tauri::command]
  fn read_config() -> Result<Config, String> {
    match fs::read_to_string("config.json") {
      Ok(contents) => match serde_json::from_str(&contents) {
        Ok(config) => Ok(config),
        Err(e) => Err(format!("Failed to parse config: {}", e))
      },
      Err(e) => Err(format!("Failed to read config: {}", e))
    }
  }
  ```

- **Use clear error messages** that can guide users or developers
- **Implement error typing** for different categories of errors
- **Log errors** appropriately for debugging while respecting privacy

## Performance Considerations

### Initialization

- **Minimize startup time** by deferring non-critical initialization
- **Use splashscreens** for long-loading operations
- **Load large resources asynchronously** to avoid blocking the main thread

### State Management

- **Use state pattern** for managing global application state:

  ```rust
  #[derive(Default)]
  struct AppState {
    counter: AtomicU32,
    settings: Mutex<Settings>,
  }
  
  fn main() {
    tauri::Builder::default()
      .manage(AppState::default())
      .invoke_handler(tauri::generate_handler![increment_counter])
      .run(tauri::generate_context!())
      .expect("Error while running application");
  }
  
  #[tauri::command]
  fn increment_counter(state: tauri::State<AppState>) -> u32 {
    state.counter.fetch_add(1, Ordering::SeqCst) + 1
  }
  ```

- **Use appropriate concurrency primitives** (Mutex, RwLock) for shared state
- **Consider thread safety** when designing state access patterns

### Resource Usage

- **Implement proper cleanup** for resources
- **Avoid memory leaks** by managing ownership correctly
- **Monitor resource usage** during development

## Building and Packaging

### Application Configuration

- **Maintain separate dev and prod configurations**
- **Use environment variables** for environment-specific settings
- **Version your configurations** alongside your application code

### Updates

- **Implement the updater plugin** for automatic updates:

  ```json
  "updater": {
    "active": true,
    "endpoints": ["https://releases.myapp.com/{{target}}/{{current_version}}"],
    "dialog": true,
    "pubkey": "YOUR_PUB_KEY"
  }
  ```

- **Sign your updates** with a secure key
- **Test update process** thoroughly before deployment
- **Consider incremental updates** for large applications

### Distribution

- **Sign your binaries** for all target platforms
- **Set appropriate application metadata**
- **Ensure installers follow platform conventions**
- **Test your application on all target platforms** before release
