# Frontend Performance Optimization

This document provides comprehensive standards and best practices for optimizing frontend performance across Bayat projects.

## Table of Contents

- [Introduction](#introduction)
- [Performance Metrics](#performance-metrics)
- [Loading Optimization](#loading-optimization)
- [Rendering Optimization](#rendering-optimization)
- [Network Optimization](#network-optimization)
- [Asset Optimization](#asset-optimization)
- [JavaScript Optimization](#javascript-optimization)
- [CSS Optimization](#css-optimization)
- [Framework-Specific Optimizations](#framework-specific-optimizations)
- [Mobile Optimizations](#mobile-optimizations)
- [Performance Testing](#performance-testing)
- [Monitoring and Analytics](#monitoring-and-analytics)
- [Implementation Checklist](#implementation-checklist)

## Introduction

Frontend performance is a critical aspect of user experience that directly impacts engagement, conversion, and satisfaction. This document outlines standards for optimizing frontend performance across all Bayat applications.

### Impact of Performance

- **User Experience**: 53% of users abandon sites that take longer than 3 seconds to load
- **Conversion Rates**: 1-second delay can reduce conversions by 7%
- **SEO Ranking**: Page speed is a ranking factor for search engines
- **Accessibility**: Performance is an accessibility concern, especially for users with limited bandwidth

### Performance-First Approach

All Bayat projects should adopt a performance-first approach:

1. **Define Performance Budgets**: Set clear targets for key metrics
2. **Measure Early and Often**: Integrate performance testing into the development workflow
3. **Optimize Incrementally**: Implement and test optimizations one at a time
4. **Automate Monitoring**: Track performance in production environments

## Performance Metrics

### Core Web Vitals

Optimize for the following Core Web Vitals:

1. **Largest Contentful Paint (LCP)**: Measures loading performance
   - **Target**: < 2.5 seconds
   - **Measured**: Time until the largest content element is visible

2. **First Input Delay (FID)**: Measures interactivity
   - **Target**: < 100 milliseconds
   - **Measured**: Time from first user interaction to browser's response

3. **Cumulative Layout Shift (CLS)**: Measures visual stability
   - **Target**: < 0.1
   - **Measured**: Sum of all unexpected layout shifts

### Additional Metrics

4. **Time to First Byte (TTFB)**:
   - **Target**: < 600ms
   - **Measured**: Time from request to first byte received

5. **First Contentful Paint (FCP)**:
   - **Target**: < 1.8 seconds
   - **Measured**: Time until first content is rendered

6. **Total Blocking Time (TBT)**:
   - **Target**: < 200ms
   - **Measured**: Total time main thread is blocked

7. **Speed Index**:
   - **Target**: < 3.4 seconds
   - **Measured**: How quickly content is visually displayed

## Loading Optimization

### Critical Rendering Path

1. **Minimize Critical Resources**: Identify and reduce resources needed for initial render
2. **Optimize Critical Path Length**: Reduce the number of round trips required
3. **Prioritize Visible Content**: Load above-the-fold content first

### Code Splitting

1. **Route-Based Splitting**: Load code only for the current route
2. **Component-Based Splitting**: Lazy load components as needed
3. **Vendor Splitting**: Separate application code from dependencies

Example React code splitting:

```jsx
import React, { lazy, Suspense } from 'react';

// Lazy load component
const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <div>
      <Suspense fallback={<div>Loading...</div>}>
        <HeavyComponent />
      </Suspense>
    </div>
  );
}
```

### Lazy Loading

1. **Lazy Load Images**: Load images as they enter viewport
2. **Lazy Load Components**: Load components when needed
3. **Lazy Load Routes**: Load routes on demand

Example image lazy loading:

```html
<img 
  src="placeholder.jpg"
  data-src="actual-image.jpg" 
  loading="lazy" 
  alt="Description"
/>
```

### Resource Hints

Use resource hints to optimize resource loading:

1. **Preload**: `<link rel="preload">` for critical assets
2. **Prefetch**: `<link rel="prefetch">` for resources needed for next navigation
3. **Preconnect**: `<link rel="preconnect">` for early connection establishment
4. **DNS-Prefetch**: `<link rel="dns-prefetch">` for early DNS resolution

Example implementation:

```html
<!-- Preload critical fonts -->
  <link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>

        <!-- Preconnect to required origins -->
<link rel="preconnect" href="https://api.example.com">
        <link rel="dns-prefetch" href="https://analytics.example.com">

<!-- Prefetch for likely next page -->
<link rel="prefetch" href="/next-page.js">
        ```

## Rendering Optimization

### Efficient DOM Manipulation

1. **Minimize DOM Size**: Keep DOM elements under 1500 nodes
2. **Batch DOM Updates**: Group multiple DOM changes together
3. **Use Document Fragments**: Build complex DOM structures off-screen
4. **Avoid Layout Thrashing**: Separate read and write operations

Example of batching DOM updates:

        ```javascript
// Poor practice - causes multiple reflows
        elements.forEach(el => {
  el.style.width = '100px';
  el.style.height = '100px';
  el.style.marginTop = '10px';
});

// Better practice - batches updates
elements.forEach(el => {
  // Read operations
  const measurements = calculateMeasurements(el);
  
  // Write operations - batched
        requestAnimationFrame(() => {
    el.style.width = measurements.width;
    el.style.height = measurements.height;
    el.style.marginTop = measurements.margin;
        });
        });
        ```

### Layout Stability

Prevent layout shifts with these techniques:

1. **Set Size Attributes**: Always specify width and height for images and media
2. **Reserve Space**: Use placeholders for dynamic content
3. **Avoid Injecting Content**: Don't insert content above existing content
4. **Use Transform for Animations**: Prefer transform/opacity for animations

Example of setting image dimensions:

```html
<!-- Poor practice - causes layout shift -->
<img src="image.jpg" alt="Description">

<!-- Better practice - prevents layout shift -->
<img src="image.jpg" width="800" height="600" alt="Description">

<!-- Or with CSS -->
<img src="image.jpg" alt="Description" style="aspect-ratio: 4/3;">
```

### Virtualization

For long lists:

1. **Virtualize Long Lists**: Only render visible items
2. **Recycle DOM Elements**: Reuse elements as user scrolls
3. **Progressive Rendering**: Load and render in chunks

Example using React-Window:

```jsx
import { FixedSizeList } from 'react-window';

function VirtualizedList({ items }) {
  const Row = ({ index, style }) => (
    <div style={style}>
      Item {items[index].name}
    </div>
  );
        
        return (
    <FixedSizeList
      height={500}
      width={300}
      itemCount={items.length}
      itemSize={35}
    >
      {Row}
    </FixedSizeList>
        );
        }
        ```

## Network Optimization

### HTTP/2 and HTTP/3

1. **Enable HTTP/2**: Configure servers to use HTTP/2
2. **Reduce Domain Sharding**: Consolidate resources under one domain
3. **Multiplexing**: Leverage parallel requests over single connection
4. **Server Push**: Use server push for critical resources

### Caching Strategy

1. **Set Proper Cache Headers**:
   - `Cache-Control: max-age=31536000` for static assets
   - `Cache-Control: no-cache` for HTML files
   - `ETag` and `If-None-Match` for validation

2. **Service Worker Caching**:
   - Cache API for application assets
   - Stale-while-revalidate patterns
   - Custom caching strategies per resource type

Example service worker cache strategy:

        ```javascript
// Service worker cache strategy
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.open('dynamic-cache').then(cache => {
      return cache.match(event.request).then(cachedResponse => {
        const networkFetch = fetch(event.request).then(networkResponse => {
          cache.put(event.request, networkResponse.clone());
          return networkResponse;
        });
        
        // Stale-while-revalidate: return cached version immediately,
        // but update cache in background
        return cachedResponse || networkFetch;
      });
    })
  );
});
```

### Compression

1. **Enable Gzip/Brotli**: Configure servers to compress responses
2. **Compress Images**: Use modern formats and appropriate compression
3. **Text Compression**: Minify HTML, CSS, and JavaScript

### API Optimization

1. **GraphQL Queries**: Request only needed fields
2. **Batching Requests**: Combine multiple API requests
3. **Data Pagination**: Load data in chunks as needed
4. **Response Compression**: Compress API responses

Example GraphQL query with selecting only needed fields:

```graphql
query GetUserProfile($id: ID!) {
  user(id: $id) {
    id
    name
    email
    # Only request needed fields, not the entire user object
        }
        }
        ```

## Asset Optimization

### Images

1. **Format Selection**:
   - AVIF/WebP for modern browsers with PNG/JPEG fallbacks
   - SVG for icons and simple graphics
   - Use responsive images with `srcset`

2. **Optimization Techniques**:
   - Compression: Reduce file size without visible quality loss
   - Resizing: Serve appropriately sized images
   - Lazy loading: Load images only when needed

Example responsive images:

        ```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img 
    srcset="image-small.jpg 500w, image-medium.jpg 1000w, image-large.jpg 1500w"
    sizes="(max-width: 600px) 500px, (max-width: 1200px) 1000px, 1500px"
    src="image-medium.jpg"
    alt="Description"
        loading="lazy"
        width="800"
        height="600"
        >
</picture>
```

### Fonts

1. **Web Font Optimization**:
   - Use `font-display: swap` to prevent blocking
   - Subset fonts to include only needed characters
   - Self-host critical fonts
   - Use variable fonts where appropriate

2. **Font Loading Strategies**:
   - Preload critical fonts
   - Use system fonts for initial render

Example font implementation:

        ```css
/* Font loading strategy */
        @font-face {
        font-family: 'MainFont';
        src: url('/fonts/main.woff2') format('woff2');
        font-weight: 400;
        font-style: normal;
  font-display: swap;  /* Show text with system font while loading */
}

/* Font fallback system */
body {
  font-family: 'MainFont', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
}
```

### Videos

1. **Video Optimization**:
   - Use appropriate codec (H.264, VP9, AV1)
   - Compress videos to appropriate quality
   - Consider animated images for short clips
   - Lazy load videos

2. **Implementation Best Practices**:
   - Add `preload="none"` or `preload="metadata"`
   - Add `loading="lazy"` attribute
   - Use `poster` attribute

Example video implementation:

```html
<video 
  controls
  width="640" 
  height="360" 
  preload="metadata"
  poster="video-poster.jpg"
  loading="lazy">
  <source src="video.webm" type="video/webm">
  <source src="video.mp4" type="video/mp4">
</video>
```

## JavaScript Optimization

### Code Quality

1. **Tree Shaking**: Remove unused code
2. **Dead Code Elimination**: Remove unreachable code
3. **Bundle Analysis**: Identify and remove large dependencies
4. **Module Optimization**: Use ES modules for better tree shaking

Example Webpack configuration for bundle analysis:

```javascript
// webpack.config.js
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  // ...
  plugins: [
    new BundleAnalyzerPlugin()
  ]
};
```

### Execution Optimization

1. **Defer Non-Critical JavaScript**: Use `defer` or `async` attributes
2. **Break Up Long Tasks**: Split JavaScript execution into smaller chunks
3. **Use Web Workers**: Offload heavy computation to background threads
4. **Optimize Event Listeners**: Remove unnecessary event listeners

Example web worker implementation:

```javascript
// Main thread
const worker = new Worker('heavy-calculation.js');

worker.addEventListener('message', event => {
  console.log('Result:', event.data.result);
});

worker.postMessage({ data: complexData });

// heavy-calculation.js (worker)
self.addEventListener('message', event => {
  const result = performHeavyCalculation(event.data.data);
  self.postMessage({ result });
        });
        ```

### Third-Party JavaScript

1. **Audit Third-Party Scripts**: Regularly review necessity and impact
2. **Load Third-Party Scripts Asynchronously**: Prevent blocking main thread
3. **Self-Host When Possible**: Reduce external dependencies
4. **Use Resource Hints**: `dns-prefetch` and `preconnect` for third-party domains

## CSS Optimization

### CSS Delivery

1. **Critical CSS**: Inline critical styles in the HTML
2. **Non-Critical CSS**: Load with `preload` and `onload`
3. **Reduce Unused CSS**: Remove unused styles with tools like PurgeCSS

Example critical CSS implementation:

        ```html
<head>
  <!-- Inline critical CSS -->
  <style>
    /* Critical styles needed for above-the-fold content */
    body { margin: 0; font-family: sans-serif; }
    header { height: 80px; background: #f0f0f0; }
    /* ... */
  </style>
  
  <!-- Non-critical CSS loaded asynchronously -->
  <link rel="preload" href="/css/main.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="/css/main.css"></noscript>
</head>
```

### CSS Performance

1. **Minimize Specificity**: Avoid deeply nested selectors
2. **Optimize Animations**: Use `transform` and `opacity`
3. **Reduce Repaints**: Minimize style changes that cause repaints
4. **Use Efficient Selectors**: Avoid universal selectors and deep nesting

Examples of CSS optimization:

```css
/* Poor performance */
#main .article .content p span { color: red; }

/* Better performance */
.content-text { color: red; }

/* Poor performance - triggers repaints */
.animate-element {
  animation: move 2s infinite;
}
@keyframes move {
  0% { left: 0; top: 0; }
  100% { left: 100px; top: 100px; }
}

/* Better performance - uses compositor-only properties */
.animate-element {
  animation: move 2s infinite;
}
@keyframes move {
  0% { transform: translate(0, 0); }
  100% { transform: translate(100px, 100px); }
}
```

## Framework-Specific Optimizations

### React

1. **Component Optimization**:
   - Use `React.memo` for pure functional components
   - Implement `shouldComponentUpdate` or `React.PureComponent` for class components
   - Use `useCallback` and `useMemo` to memoize functions and values

2. **State Management**:
   - Keep state as local as possible
   - Consider using state management libraries only when necessary
   - Split context providers to minimize re-renders

Example React optimization:

        ```jsx
// Optimized React component
import React, { useCallback, useMemo } from 'react';

const ExpensiveComponent = React.memo(({ data, onItemClick }) => {
  // Memoize expensive calculations
        const processedData = useMemo(() => {
    return data.map(item => expensiveProcessing(item));
        }, [data]);
        
  // Memoize callback functions
  const handleClick = useCallback((id) => {
    onItemClick(id);
  }, [onItemClick]);
  
  return (
    <div>
      {processedData.map(item => (
        <div key={item.id} onClick={() => handleClick(item.id)}>
          {item.name}
        </div>
      ))}
    </div>
  );
});

export default ExpensiveComponent;
```

### Angular

1. **Change Detection**:
   - Use `OnPush` change detection strategy
   - Use pure pipes for transformations
   - Avoid function calls in templates

2. **Lazy Loading**:
   - Lazy load feature modules
   - Preload strategically based on user patterns

Example Angular optimization:

        ```typescript
// Optimized Angular component
import { Component, ChangeDetectionStrategy, Input } from '@angular/core';

        @Component({
  selector: 'app-data-list',
  template: `
    <div *ngFor="let item of items">
      {{ item.name }}
    </div>
  `,
        changeDetection: ChangeDetectionStrategy.OnPush
        })
export class DataListComponent {
  @Input() items: any[];
}
```

### Vue

1. **Reactivity Optimizations**:
   - Use `v-once` for static content
   - Implement `v-memo` for memoizing part of the template
   - Use functional components for stateless rendering

2. **Rendering Optimizations**:
   - Use `v-show` instead of `v-if` for frequent toggles
   - Use keyed `v-for` loops
   - Avoid expensive operations in computed properties

Example Vue optimization:

        ```vue
        <template>
  <!-- Static content rendered only once -->
        <header v-once>
    <h1>{{ title }}</h1>
        </header>
        
  <!-- Efficient list rendering -->
  <div>
    <div v-for="item in items" :key="item.id">
            {{ item.name }}
    </div>
  </div>
        </template>

<script>
export default {
  props: ['items', 'title'],
  
  // Cache expensive computations
  computed: {
    processedItems() {
      return this.items.filter(item => item.isActive);
    }
  }
}
</script>
```

## Mobile Optimizations

### Mobile-Specific Considerations

1. **Responsive Images**: Serve appropriately sized images
2. **Touch Optimization**: Optimize for touch interactions
3. **Network Awareness**: Adapt to varying network conditions
4. **Data Saver Mode**: Respect user preferences for reduced data usage

### Progressive Web Apps (PWA)

1. **Offline Support**: Implement service workers for offline access
2. **App Shell Architecture**: Cache the application shell
3. **Add to Home Screen**: Implement Web App Manifest
4. **Push Notifications**: Implement only when necessary and valuable

Example network-aware loading:

```javascript
// Adapt to network conditions
if ('connection' in navigator) {
  if (navigator.connection.saveData) {
    // Load lower quality images for data saver mode
    loadLowResImages();
  }
  
  if (navigator.connection.effectiveType === '4g') {
    // Load high-quality assets
    prefetchNextPage();
  } else {
    // Reduce quality for slower connections
    adjustContentForSlowNetwork();
  }
}
```

## Performance Testing

### Testing Methodologies

1. **Lighthouse**: Run Lighthouse in CI/CD pipeline
2. **Web Vitals Monitoring**: Track Core Web Vitals
3. **Synthetic Testing**: Regular tests on simulated environments
4. **Real User Monitoring (RUM)**: Gather performance data from real users

### Testing Tools

1. **Developer Tools**:
   - Chrome DevTools Performance panel
   - Firefox Performance Tools
   - Safari Web Inspector

2. **Dedicated Tools**:
   - WebPageTest for comprehensive analysis
   - Lighthouse for audit scores
   - Bundle analyzers for JavaScript size analysis

3. **CI/CD Integration**:
   - Lighthouse CI
   - Automated performance testing
   - Performance budgets enforcement

Example Lighthouse CI configuration:

```javascript
// lighthouserc.js
module.exports = {
  ci: {
    collect: {
      numberOfRuns: 3,
      url: ['https://example.com/', 'https://example.com/product']
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'first-contentful-paint': ['warn', {maxNumericValue: 2000}],
        'interactive': ['error', {maxNumericValue: 3500}],
        'cumulative-layout-shift': ['error', {maxNumericValue: 0.1}],
        'largest-contentful-paint': ['error', {maxNumericValue: 2500}]
      }
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
```

## Monitoring and Analytics

### Real User Monitoring

1. **Core Web Vitals**: Track LCP, FID, CLS
2. **Custom Metrics**: Track application-specific metrics
3. **User-Centric Analysis**: Segment by device, connection, location
4. **Error Tracking**: Monitor JavaScript errors and API failures

Example Core Web Vitals monitoring:

```javascript
// Web Vitals monitoring
import {getLCP, getFID, getCLS} from 'web-vitals';

function sendToAnalytics({name, delta, id}) {
  // Send metrics to your analytics platform
  analytics.send({
    metric: name,
    value: delta,
    id: id
  });
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getLCP(sendToAnalytics);
```

### Performance Dashboards

1. **Executive Dashboards**: High-level performance overview
2. **Developer Dashboards**: Detailed technical metrics
3. **Alerting**: Set up alerts for performance regressions
4. **Trend Analysis**: Track performance over time

## Implementation Checklist

### Initial Development

- [ ] Set performance budgets
- [ ] Implement critical rendering path optimization
- [ ] Set up asset optimization pipeline
- [ ] Configure appropriate caching

### Pre-Launch Checklist

- [ ] Run comprehensive performance audit
- [ ] Test on various devices and connection speeds
- [ ] Verify Core Web Vitals meet targets
- [ ] Set up monitoring for production

### Regular Maintenance

- [ ] Conduct monthly performance reviews
- [ ] Update dependencies and optimize new features
- [ ] Analyze real user data for problem areas
- [ ] Implement iterative improvements
