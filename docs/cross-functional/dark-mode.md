# Dark Mode Implementation Guidelines

This document outlines Bayat's standardized approach to implementing dark mode across all platforms and products.

## Table of Contents

- [Introduction](#introduction)
- [Design Principles](#design-principles)
- [Color System](#color-system)
- [Implementation Standards](#implementation-standards)
- [User Preferences](#user-preferences)
- [Testing Guidelines](#testing-guidelines)
- [Performance Considerations](#performance-considerations)
- [Common Challenges](#common-challenges)
- [Platform-Specific Guidelines](#platform-specific-guidelines)
- [Migration Strategy](#migration-strategy)
- [Accessibility Considerations](#accessibility-considerations)

## Introduction

### Purpose

Dark mode reduces eye strain in low-light conditions, decreases power consumption on OLED/AMOLED displays, and provides users with a preference option. These guidelines ensure consistent implementation across all Bayat products.

### Benefits

- **Reduced Eye Strain**: Lower brightness and light emission in low-light environments
- **Battery Efficiency**: Up to 30% battery savings on devices with OLED/AMOLED screens
- **Accessibility**: Alternative visualization that benefits users with certain visual sensitivities
- **User Preference**: Meets diverse user expectations across platforms
- **Brand Consistency**: Ensures our brand identity is maintained across light and dark themes

## Design Principles

### Core Principles

1. **Content Hierarchy**: Maintain the same visual hierarchy in both modes
2. **Reduce Eye Strain**: Avoid pure white (#FFFFFF) on dark backgrounds
3. **Avoid Pure Black**: Use dark grays (e.g., #121212, #1E1E1E) instead of pure black (#000000)
4. **Maintain Contrast Ratios**: Ensure WCAG AA compliance (4.5:1 for normal text, 3:1 for large text)
5. **Subtle Depth**: Use subtle shadows and elevation in dark mode with lighter shadows
6. **Color Semantics**: Preserve color meaning between modes (e.g., error states remain red)
7. **Brand Identity**: Adapt brand colors appropriately while maintaining recognition

### Anti-patterns to Avoid

- Inverting colors without consideration for contrast and readability
- Using pure black backgrounds that create excessive contrast
- Applying the same shadows in dark mode as in light mode
- Using saturated colors that cause visual vibration against dark backgrounds
- Creating new UI elements solely for dark mode

## Color System

### Token-Based System

| Purpose | Light Mode | Dark Mode |
|---------|------------|-----------|
| Background (primary) | #FFFFFF | #121212 |
| Background (secondary) | #F5F5F5 | #1E1E1E |
| Surface | #FFFFFF | #242424 |
| Primary | #0056D6 | #519AFF |
| Secondary | #7B1FA2 | #BB86FC |
| Text (primary) | #212121 | #E1E1E1 |
| Text (secondary) | #757575 | #A0A0A0 |
| Divider | #DEDEDE | #323232 |
| Error | #D32F2F | #F88078 |
| Warning | #F9A825 | #FDD663 |
| Success | #2E7D32 | #7CB342 |

### Color Adaptation Rules

1. **Background Colors**: Reduce luminance by 85-90%
2. **Text Colors**: Light mode text at 87% opacity becomes 95% in dark mode
3. **Primary Brand Colors**: Adjust saturation (+5-10%) and luminance (+15-30%)
4. **Accent Colors**: Desaturate by 10-15% and increase luminance by 20-30%
5. **Alert Colors**: Maintain semantic meaning while reducing intensity
6. **Inactive States**: Use lower contrast in both modes

### Elevation and Surfaces

In dark mode, higher surfaces should be lighter to convey elevation:

| Elevation Level | Light Mode (shadows) | Dark Mode (surface color) |
|-----------------|----------------------|---------------------------|
| 0dp (baseline) | No shadow | #121212 |
| 1dp | Small shadow | #1D1D1D |
| 2dp | Medium shadow | #222222 |
| 3dp | Medium-large shadow | #252525 |
| 4dp | Large shadow | #272727 |
| 8dp | Very large shadow | #2C2C2C |
| 16dp | Extreme shadow | #2E2E2E |
| 24dp | Maximum shadow | #323232 |

## Implementation Standards

### Architecture Patterns

#### Approach 1: Theme Provider with Design Tokens

Use a theme provider that exposes design tokens:

```typescript
// Design tokens structure
interface ThemeTokens {
  colors: {
    background: {
      primary: string;
      secondary: string;
      // ...
    };
    text: {
      primary: string;
      secondary: string;
      // ...
    };
    // ...
  };
  spacing: {
    // ...
  };
  // ...
}

// Component example
function Button({ children, variant }) {
  const theme = useTheme();
  return (
    <button
      style={{
        backgroundColor: theme.colors[variant].background,
        color: theme.colors[variant].text,
        // ...
      }}
    >
      {children}
    </button>
  );
}
```

#### Approach 2: CSS Variables with Media Queries

```css
:root {
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F5F5F5;
  --color-text-primary: #212121;
  /* ... */
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg-primary: #121212;
    --color-bg-secondary: #1E1E1E;
    --color-text-primary: #E1E1E1;
    /* ... */
  }
}

.button {
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
  /* ... */
}
```

### File Structure

```plaintext
src/
├── themes/
│   ├── index.ts         # Theme exports
│   ├── tokens.ts        # Design tokens for both modes
│   ├── lightTheme.ts    # Light theme-specific values
│   ├── darkTheme.ts     # Dark theme-specific values
│   └── utils.ts         # Theme utility functions
├── components/
│   └── [component]/
│       ├── Component.tsx
│       └── styles.ts    # Component styles using theme tokens
```

### Image Assets

For images that need to be adapted:

1. **SVGs**: Use currentColor or theme-aware fills
2. **PNGs/JPGs**: Provide separate assets for each mode
3. **Icons**: Use vector formats with dynamic coloring

Example for SVG icons:

```tsx
function IconButton({ icon, color, ...props }) {
  const theme = useTheme();
  return (
    <button {...props}>
      <svg fill={theme.colors.icon[color]} ...>
        {icon}
      </svg>
    </button>
  );
}
```

## User Preferences

### Settings Defaults

Provide three options:

1. **System Default** (recommended default): Follow OS setting
2. **Light Mode**: Always use light theme
3. **Dark Mode**: Always use dark theme

### Persistence

Store user preference in a persistent storage (localStorage, app settings, etc.):

```typescript
// Example logic for web apps
function useThemePreference() {
  const [theme, setTheme] = useState(() => {
    const saved = localStorage.getItem('theme-preference');
    if (saved === 'light' || saved === 'dark') return saved;
    
    return window.matchMedia('(prefers-color-scheme: dark)').matches 
      ? 'dark' 
      : 'light';
  });

  useEffect(() => {
    localStorage.setItem('theme-preference', theme);
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  return [theme, setTheme];
}
```

### Real-time OS Updates

Listen for changes to system preference:

```typescript
useEffect(() => {
  if (userPreference === 'system') {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = (e) => {
      setTheme(e.matches ? 'dark' : 'light');
    };
    
    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }
}, [userPreference]);
```

## Testing Guidelines

### Test Matrix

| Test Case | Expected Result |
|-----------|----------------|
| Default theme on first visit | System preference is applied |
| Toggle to dark mode | UI updates immediately without page reload |
| Toggle to light mode | UI updates immediately without page reload |
| System change to dark mode | UI updates if system preference is selected |
| Saved preference persists | User preference maintained across sessions |

### Visual Regression Testing

- Capture screenshots in both modes for each component and page
- Verify color contrast meets WCAG AA standards
- Test with a device's dark mode enabled/disabled
- Test all interactive states (hover, active, focus, disabled)

### Accessibility Testing

Test both themes with screen readers and keyboard navigation to ensure:

- Focus states are clearly visible in both modes
- Contrast ratios remain WCAG compliant
- Interactive elements are identifiable in both modes
- Custom controls maintain proper accessibility attributes

## Performance Considerations

### Runtime Theme Switching

To minimize performance impact:

1. Prefer CSS variables for theme switching when possible
2. Use efficient selectors (e.g., `[data-theme="dark"]` at the root)
3. Avoid rerendering the entire application on theme change
4. Leverage code-splitting to load theme-specific assets on demand
5. For complex themes, consider server-side rendering with theme detection

### Initial Load Performance

To prevent flash of incorrect theme:

```html
<script>
  // Inline script in <head> to apply theme before content renders
  (function() {
    const saved = localStorage.getItem('theme-preference');
    if (saved === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
      return;
    }
    if (saved === 'light') {
      document.documentElement.setAttribute('data-theme', 'light');
      return;
    }
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.setAttribute('data-theme', 'dark');
    }
  })();
</script>
```

## Common Challenges

### Images and Media

Handle images with these strategies:

1. **Transparency**: Use transparent PNGs with appropriate shadows
2. **Image Filters**: Apply slight brightness/contrast reductions for photos in dark mode
3. **Image Isolation**: Use subtle elevation shadows or borders for images with white backgrounds
4. **Contextual Images**: Provide separate assets for complex images (diagrams, charts)

Example CSS for photo adjustments:

```css
@media (prefers-color-scheme: dark) {
  img:not([src*=".svg"]) {
    filter: brightness(0.8) contrast(1.2);
  }
}
```

### Third-party Components

Strategies for handling external components:

1. Select libraries with built-in dark mode support
2. Use CSS overrides for libraries without theme support
3. Create wrappers around third-party components to enforce themed styles
4. For embeds (maps, videos, etc.), use containers with themed borders

### User-generated Content

For content created by users:

1. Apply subtle background colors to user content containers
2. Ensure user text has appropriate contrast in both modes
3. Consider desaturating user-uploaded images slightly in dark mode
4. For HTML content, inject a class/attribute for theming

### Complex Visualizations

For charts, graphs, and data visualizations:

1. Define theme-aware color palettes with appropriate contrast
2. Adjust background grid opacity and contrast
3. Increase data point/line thickness slightly in dark mode
4. Consider inverting certain visualization types entirely

## Platform-Specific Guidelines

### Web

- Use CSS custom properties for theme tokens
- Use the `prefers-color-scheme` media query
- Consider generating separate bundled CSS for each theme
- Test across multiple browsers for consistent implementation

```css
/* Example media query */
@media (prefers-color-scheme: dark) {
  :root {
    --color-background: #121212;
    --color-text: #E1E1E1;
  }
}
```

### iOS

- Use semantic colors from UIKit/SwiftUI
- Use system-aware assets with light/dark variants
- Follow iOS Human Interface Guidelines for dark mode
- Adapt to Dynamic Type with all color choices

```swift
// SwiftUI example
Text("Hello World")
  .foregroundColor(Color("textPrimary"))

// UIKit example
label.textColor = UIColor(named: "textPrimary")
```

### Android

- Use Material Design night resources
- Define theme attributes in `styles.xml`
- Use theme-aware resource references
- Support both AppCompat and Material Components

```xml
<!-- res/values/colors.xml -->
<resources>
  <color name="colorPrimary">#0056D6</color>
</resources>

<!-- res/values-night/colors.xml -->
<resources>
  <color name="colorPrimary">#519AFF</color>
</resources>
```

### Desktop Applications

For Electron, Tauri, or similar:

- Follow OS-specific design guidelines
- Respect system-level dark mode settings
- Provide manual override options in settings
- Use CSS variables or theme providers based on platform API

```js
// Electron example
const { nativeTheme } = require('electron');
nativeTheme.themeSource = 'system'; // or 'light' or 'dark'
```

## Migration Strategy

### Phased Approach

For existing applications, implement dark mode in phases:

1. **Phase 1**: Define token system and infrastructure
   - Create design tokens and theme provider
   - Implement theme switching mechanism
   - Apply basic theme to shell components (navigation, layout)

2. **Phase 2**: Core UI components
   - Migrate common UI components to use theme tokens
   - Implement dark mode for forms, buttons, cards, dialogs
   - Test and validate core functionality

3. **Phase 3**: Content and specialized components
   - Migrate content areas, user-generated content
   - Implement dark mode for visualizations, media components
   - Address third-party components and integrations

4. **Phase 4**: Refinement and polish
   - Conduct thorough testing across devices
   - Optimize performance
   - Refine animations and transitions between modes

### Priority Order

When migrating incrementally, prioritize:

1. Global layout components and navigation
2. Typography and content containers
3. Interactive elements (buttons, links, forms)
4. Data display components (tables, lists)
5. Media and visualizations
6. Third-party components and embedded content

## Accessibility Considerations

### Color Contrast

Ensure proper contrast for both themes:

- Normal text: 4.5:1 contrast ratio
- Large text: 3:1 contrast ratio
- Interface components: 3:1 contrast ratio

Test all interactive states:

| Element State | Light Mode Contrast | Dark Mode Contrast |
|---------------|---------------------|---------------------|
| Default | 4.5:1 minimum | 4.5:1 minimum |
| Hover | Maintain or increase | Maintain or increase |
| Active | Maintain or increase | Maintain or increase |
| Focus | 4.5:1 minimum with indicator | 4.5:1 minimum with indicator |
| Disabled | 3:1 minimum | 3:1 minimum |

### Focus Indicators

Ensure focus indicators are visible in both modes:

```css
:focus {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}
```

### Motion Sensitivity

For theme transitions:

- Allow users to disable transitions (respect `prefers-reduced-motion`)
- Keep transitions under 300ms
- Avoid flashing or strobing effects during transitions

```css
@media (prefers-reduced-motion: no-preference) {
  .theme-transition {
    transition: background-color 200ms ease, color 200ms ease;
  }
}
```

### Other Considerations

- Test with screen readers in both modes
- Ensure proper semantic structure is maintained
- Avoid relying solely on color to convey information
- Test with high contrast mode enabled
