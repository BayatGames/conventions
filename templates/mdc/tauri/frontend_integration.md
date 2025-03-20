# Frontend Integration with Tauri

This document outlines best practices for integrating frontend frameworks with Tauri according to Bayat standards.

## API Communication

### Invoking Tauri Commands

- **Use the `invoke` function** to call backend commands:

  ```typescript
  // JavaScript/TypeScript
  import { invoke } from '@tauri-apps/api/tauri';
  
  // Call Rust command
  const result = await invoke('get_user_data', { userId: '123' });
  ```

- **Create typed wrappers** around Tauri commands for better type safety:

  ```typescript
  // userApi.ts
  import { invoke } from '@tauri-apps/api/tauri';
  
  export interface User {
    id: string;
    name: string;
    email: string;
  }
  
  export async function getUserData(userId: string): Promise<User> {
    return invoke('get_user_data', { userId });
  }
  
  export async function saveUserData(user: User): Promise<void> {
    return invoke('save_user_data', { user });
  }
  ```

- **Handle errors consistently**:

  ```typescript
  try {
    const userData = await getUserData(userId);
    updateUserState(userData);
  } catch (error) {
    console.error('Failed to fetch user data:', error);
    showErrorNotification(`Error: ${error.message || 'Unknown error'}`);
  }
  ```

### Event Handling

- **Use the Tauri event system** for backend-to-frontend communication:

  ```typescript
  // Listen for events from Rust backend
  import { listen } from '@tauri-apps/api/event';
  
  // In your component initialization
  const unlisten = await listen('file-saved', (event) => {
    console.log('File saved:', event.payload);
    showNotification(`File saved: ${event.payload.path}`);
  });
  
  // In your component cleanup
  onUnmount(() => {
    unlisten();
  });
  ```

- **Organize events by domain**, with a consistent naming pattern:
  - `entity-action` format (e.g., `file-saved`, `user-updated`)
  - Use past tense for completed actions
  - Use kebab-case for event names

## State Management

### Frontend State

- **Keep frontend state separate** from backend state:
  - Frontend state: UI state, form inputs, visual preferences
  - Backend state: Persistent data, system state, secure information

- **Use appropriate state management** based on application complexity:
  - Small applications: React Context, Vue Composition API, local state
  - Medium applications: Zustand, Jotai, Recoil
  - Large applications: Redux, Pinia, MobX

- **Sync critical state with the backend** to ensure data consistency

### Data Persistence

- **Use Tauri's filesystem API** for local storage needs:

  ```typescript
  import { writeTextFile, readTextFile } from '@tauri-apps/api/fs';
  
  // Save state to file
  async function saveAppState(state) {
    await writeTextFile('app.json', JSON.stringify(state));
  }
  
  // Load state from file
  async function loadAppState() {
    try {
      const content = await readTextFile('app.json');
      return JSON.parse(content);
    } catch (error) {
      console.error('Failed to load state:', error);
      return defaultState;
    }
  }
  ```

- **Consider using a database** for complex data:
  - SQLite through Tauri commands
  - IndexedDB for frontend-only storage
  - Custom storage solutions via Rust backend

## UI/UX Considerations

### Native Integration

- **Use native dialogs** via Tauri's dialog API:

  ```typescript
  import { open, save } from '@tauri-apps/api/dialog';
  
  // Open file dialog
  const filePath = await open({
    multiple: false,
    filters: [{
      name: 'Images',
      extensions: ['png', 'jpg']
    }]
  });
  
  // Save file dialog
  const savePath = await save({
    filters: [{
      name: 'Text',
      extensions: ['txt']
    }]
  });
  ```

- **Implement window management** using the window API:

  ```typescript
  import { appWindow } from '@tauri-apps/api/window';
  
  // Set window title
  appWindow.setTitle('New Document - My App');
  
  // Set window size
  appWindow.setSize(new PhysicalSize(800, 600));
  ```

- **Use OS notifications** for important events:

  ```typescript
  import { isPermissionGranted, requestPermission, sendNotification } from '@tauri-apps/api/notification';
  
  async function notifyUser(title, body) {
    let permissionGranted = await isPermissionGranted();
    if (!permissionGranted) {
      const permission = await requestPermission();
      permissionGranted = permission === 'granted';
    }
    
    if (permissionGranted) {
      sendNotification({ title, body });
    }
  }
  ```

### Responsive Design

- **Design UIs that adapt to window resizing**
- **Use responsive CSS** rather than fixed dimensions
- **Test on different screen sizes** and resolutions
- **Support both light and dark themes**:

  ```typescript
  // Detect system theme
  import { invoke } from '@tauri-apps/api/tauri';
  
  async function getSystemTheme() {
    return await invoke('get_system_theme');
  }
  
  // Apply theme
  const theme = await getSystemTheme();
  document.documentElement.setAttribute('data-theme', theme);
  ```

## Security Considerations

### Sensitive Data

- **Never store sensitive data** (passwords, tokens) in frontend state
- **Use the backend for sensitive operations**
- **Validate all user inputs** both in frontend and backend

### Frontend Libraries

- **Keep dependencies updated** to avoid security vulnerabilities
- **Use dependency scanning tools** (npm audit, dependabot)
- **Consider bundle size** when adding new dependencies

## Development Workflow

### Development Environment

- **Use Tauri's development features**:

  ```json
  // tauri.conf.json
  "build": {
    "devPath": "http://localhost:3000",
    "distDir": "../dist"
  }
  ```

- **Set up hot reload** for faster development
- **Use separate dev/prod configurations**

### Testing

- **Test frontend-backend integration points**
- **Mock Tauri APIs** for unit testing frontend components:

  ```typescript
  // mock.ts
  import { vi } from 'vitest';
  
  vi.mock('@tauri-apps/api/tauri', () => ({
    invoke: vi.fn((command, args) => {
      if (command === 'get_user_data') {
        return Promise.resolve({ id: args.userId, name: 'Test User' });
      }
      return Promise.reject(new Error(`Unknown command: ${command}`));
    })
  }));
  ```

- **Implement end-to-end tests** for critical user flows
