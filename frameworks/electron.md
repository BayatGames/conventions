# Electron.js Development Guidelines

This document outlines the standards and best practices for developing desktop applications using Electron.js at Bayat.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Application Architecture](#application-architecture)
3. [Security Best Practices](#security-best-practices)
4. [Performance Optimization](#performance-optimization)
5. [IPC Communication](#ipc-communication)
6. [Native Integration](#native-integration)
7. [Packaging and Distribution](#packaging-and-distribution)
8. [Testing](#testing)
9. [OS-Specific Considerations](#os-specific-considerations)
10. [Resources](#resources)

## Project Structure

### Standard Project Layout

```
project-root/
├── .github/                # GitHub workflows and templates
├── assets/                 # Application assets (icons, images)
├── build/                  # Build configuration and scripts
├── dist/                   # Distribution output
├── node_modules/           # Dependencies (git-ignored)
├── src/                    # Source code
│   ├── main/               # Main process code
│   │   ├── index.ts        # Main entry point
│   │   ├── menu.ts         # Application menu
│   │   └── preload.ts      # Preload scripts
│   ├── renderer/           # Renderer process code
│   │   ├── components/     # UI components
│   │   ├── hooks/          # Custom React hooks (if using React)
│   │   ├── pages/          # Application pages/screens
│   │   ├── store/          # State management
│   │   ├── utils/          # Utility functions
│   │   ├── App.tsx         # Main React component (if using React)
│   │   └── index.tsx       # Renderer entry point
│   └── common/             # Shared code between processes
│       ├── constants.ts    # Shared constants
│       ├── types.ts        # TypeScript types/interfaces
│       └── utils.ts        # Shared utility functions
├── .eslintrc.js            # ESLint configuration
├── .gitignore              # Git ignore file
├── electron-builder.yml    # Electron builder configuration
├── package.json            # Project manifest
├── tsconfig.json           # TypeScript configuration
└── README.md               # Project documentation
```

### Key Files

- **package.json**: Define main process entry point and dependencies
- **electron-builder.yml**: Configure builds for different platforms
- **src/main/index.ts**: Main process entry point
- **src/main/preload.ts**: Preload scripts for secure IPC
- **src/renderer/index.tsx**: Renderer process entry point

## Application Architecture

### Process Separation

- Maintain a clear separation between main and renderer processes
- Follow the principle of least privilege

### Recommended Architecture

- **Main Process**: Handle system-level operations (file I/O, native APIs)
- **Renderer Process**: Handle UI and user interactions
- **Preload Scripts**: Bridge main and renderer processes securely

### State Management

- Use Redux, MobX, or Zustand for complex state management
- Avoid global state patterns that cross process boundaries
- Prefer local state for UI components when possible

### Framework Recommendations

- Use React, Vue, or Svelte for the renderer process
- TypeScript is strongly recommended for both processes
- Consider electron-react-boilerplate or vite-electron-builder for project startup

## Security Best Practices

### Critical Security Rules

1. **Never** enable `nodeIntegration` in renderer processes
2. **Always** use a preload script with contextIsolation
3. **Never** use `allowRunningInsecureContent` or `webSecurity: false`
4. Keep Electron and Chromium up-to-date
5. Validate all inputs from users and external sources

### Secure IPC Pattern

```typescript
// Preload script (preload.ts)
import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('electronAPI', {
  saveFile: (content: string) => ipcRenderer.invoke('save-file', content),
  readFile: (path: string) => ipcRenderer.invoke('read-file', path)
})

// Main process (main.ts)
ipcMain.handle('save-file', async (event, content) => {
  // Validate content
  if (typeof content !== 'string') {
    throw new Error('Invalid content type')
  }
  
  // Process the request
  try {
    // Save file logic
    return { success: true }
  } catch (error) {
    console.error('Error saving file:', error)
    return { success: false, error: error.message }
  }
})
```

### Content Security Policy

Implement a strict Content Security Policy to prevent XSS attacks:

```typescript
session.defaultSession.webRequest.onHeadersReceived((details, callback) => {
  callback({
    responseHeaders: {
      ...details.responseHeaders,
      'Content-Security-Policy': [
        "default-src 'self'; script-src 'self'; object-src 'none'"
      ]
    }
  })
})
```

## Performance Optimization

### Main Process Optimization

- Avoid heavy computation in the main process
- Use worker threads for CPU-intensive tasks
- Implement proper error handling to prevent crashes

### Renderer Process Optimization

- Implement code-splitting for large applications
- Optimize DOM operations and React rendering cycles
- Use virtual scrolling for large lists

### Memory Management

- Watch for memory leaks, especially in event listeners
- Implement proper cleanup when windows are closed
- Use DevTools Memory profiler to identify issues

## IPC Communication

### Recommended Patterns

- Use `ipcRenderer.invoke` and `ipcMain.handle` for request/response patterns
- Use `webContents.send` and `ipcRenderer.on` for one-way notifications

### Anti-Patterns to Avoid

- Avoid using the remote module (deprecated and insecure)
- Don't use synchronous IPC methods that block UI
- Don't expose entire Node.js modules to the renderer

## Native Integration

### Node.js Integration

- Keep Node.js code in the main process whenever possible
- Use IPC to communicate between renderer and Node.js functionality
- Document all native module dependencies

### Native Modules

- Prefer pure JS/TS modules when available
- Use node-gyp compatible modules
- Test native modules across all target platforms

## Packaging and Distribution

### Build Process

- Use electron-builder for packaging
- Sign your applications for all platforms
- Implement auto-updates using electron-updater

### Configuration Example

```yaml
# electron-builder.yml
appId: com.bayat.appname
productName: AppName
directories:
  output: dist
  buildResources: build
files:
  - from: .
    filter:
      - package.json
      - app
publish:
  provider: github
  owner: bayat
  repo: appname
mac:
  category: public.app-category.developer-tools
  hardenedRuntime: true
  gatekeeperAssess: false
  entitlements: build/entitlements.mac.plist
  entitlementsInherit: build/entitlements.mac.plist
win:
  target:
    - target: nsis
      arch:
        - x64
linux:
  target:
    - target: AppImage
    - target: deb
  category: Development
```

### Auto-Updates

Implement auto-updates using electron-updater:

```typescript
import { autoUpdater } from 'electron-updater'

export function setupAutoUpdater() {
  autoUpdater.logger = log
  autoUpdater.checkForUpdatesAndNotify()
}
```

## Testing

### Testing Strategy

- **Unit Tests**: Jest for individual functions
- **Integration Tests**: Spectron for application testing
- **E2E Tests**: Playwright or Cypress

### Example Test Setup

```typescript
// Jest unit test example
import { calculateValue } from '../src/common/utils'

describe('Utils', () => {
  test('calculateValue should return correct result', () => {
    expect(calculateValue(10, 5)).toBe(15)
  })
})
```

## OS-Specific Considerations

### Windows

- Implement proper app installation/uninstallation
- Support both light and dark themes
- Use native file dialogs

### macOS

- Follow macOS UI guidelines
- Support sandboxing for Mac App Store
- Implement proper notarization for distribution

### Linux

- Package as AppImage, deb, and rpm
- Follow freedesktop.org standards
- Test on multiple distributions (Ubuntu, Fedora)

## Resources

- [Electron Documentation](https://www.electronjs.org/docs)
- [Electron Security Documentation](https://www.electronjs.org/docs/tutorial/security)
- [Electron Builder Documentation](https://www.electron.build/)
- [Secure Electron Template](https://github.com/reZach/secure-electron-template) 