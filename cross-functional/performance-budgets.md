# Performance Budgets

This document outlines Bayat's performance budget standards for different application types, providing specific metrics, targets, and measurement approaches to ensure optimal performance across all projects.

## Table of Contents

- [Introduction to Performance Budgets](#introduction-to-performance-budgets)
- [Web Application Performance Budgets](#web-application-performance-budgets)
- [Mobile Application Performance Budgets](#mobile-application-performance-budgets)
- [Desktop Application Performance Budgets](#desktop-application-performance-budgets)
- [Game Performance Budgets](#game-performance-budgets)
- [API and Backend Performance Budgets](#api-and-backend-performance-budgets)
- [Monitoring and Enforcement](#monitoring-and-enforcement)
- [Remediation Strategies](#remediation-strategies)
- [Budget Exceptions](#budget-exceptions)
- [Performance Testing Standards](#performance-testing-standards)

## Introduction to Performance Budgets

### Definition and Purpose

Performance budgets are quantifiable limits set on performance metrics that teams must not exceed. They serve to:

- Establish clear performance expectations
- Provide objective measures for performance quality
- Help catch performance regressions before release
- Ensure consistent user experience across devices
- Align teams on performance priorities

### Types of Performance Metrics

1. **Quantity-based metrics**:
   - File size (total, per file type, per module)
   - Number of HTTP requests
   - Number of DOM elements

2. **Timing-based metrics**:
   - Load time (Time to Interactive, First Contentful Paint, etc.)
   - Response time
   - Animation frames per second
   - Time to first API response

3. **Rule-based metrics**:
   - Lighthouse scores
   - PageSpeed Insights
   - Custom heuristic evaluations

4. **User-centric metrics**:
   - Core Web Vitals (LCP, FID, CLS)
   - Custom user experience measurements

### Implementation Approach

- Define budgets early in the development lifecycle
- Integrate into CI/CD pipelines
- Make budgets visible in dashboards
- Set alerts for approaching limits
- Schedule regular review of budget effectiveness

## Web Application Performance Budgets

### Core Web Vitals Budgets

| Metric | Target (Good) | Warning Threshold | Fail Threshold |
|--------|--------------|------------------|---------------|
| Largest Contentful Paint (LCP) | < 2.5s | 2.5s - 4s | > 4s |
| First Input Delay (FID) | < 100ms | 100ms - 300ms | > 300ms |
| Cumulative Layout Shift (CLS) | < 0.1 | 0.1 - 0.25 | > 0.25 |
| First Contentful Paint (FCP) | < 1.8s | 1.8s - 3s | > 3s |
| Time to Interactive (TTI) | < 3.8s | 3.8s - 7.3s | > 7.3s |
| Total Blocking Time (TBT) | < 200ms | 200ms - 600ms | > 600ms |

### Resource Size Budgets

| Resource Type | Target (Desktop) | Target (Mobile) |
|---------------|-----------------|-----------------|
| Total Page Size | < 1.5 MB | < 1 MB |
| HTML | < 100 KB | < 80 KB |
| CSS | < 120 KB | < 80 KB |
| JavaScript (compressed) | < 300 KB | < 200 KB |
| JavaScript (parsed) | < 1 MB | < 700 KB |
| Images | < 800 KB | < 500 KB |
| Fonts | < 150 KB | < 120 KB |
| Third-party scripts | < 200 KB | < 150 KB |

### Request Budgets

| Metric | Target (Desktop) | Target (Mobile) |
|--------|-----------------|-----------------|
| Total Requests | < 60 | < 50 |
| JavaScript Requests | < 15 | < 12 |
| CSS Requests | < 5 | < 4 |
| Image Requests | < 25 | < 20 |
| Font Requests | < 5 | < 4 |
| Third-party Requests | < 10 | < 8 |

### Application-Specific Budgets

#### Marketing Websites

- Lighthouse Performance Score: ≥ 90
- Time to Interactive: < 3s (Desktop), < 5s (Mobile)
- Critical rendering path resources: < 190 KB

#### E-commerce Applications

- Time to First Byte: < 300ms
- LCP: < 2s
- Add to Cart response time: < 500ms
- Checkout page load time: < 3s
- Payment processing page: < 2s

#### Web Applications (SaaS)

- Application shell load time: < 2s
- Time to meaningful content: < 3s
- API response integration time: < 500ms
- State transition time: < 300ms

## Mobile Application Performance Budgets

### Startup Performance

| Metric | Android Target | iOS Target |
|--------|---------------|------------|
| Cold Start Time | < 2s | < 1.8s |
| Warm Start Time | < 1.2s | < 1s |
| Hot Start Time | < 400ms | < 350ms |
| Time to Interactive | < 3s | < 2.8s |

### Runtime Performance

| Metric | Android Target | iOS Target |
|--------|---------------|------------|
| Stable Frames Per Second | 60 fps (90%+ of time) | 60 fps (95%+ of time) |
| Animation Jank | < 5% dropped frames | < 3% dropped frames |
| Input Latency | < 100ms | < 80ms |
| Scrolling Performance | 60 fps (95%+ of time) | 60 fps (98%+ of time) |

### Resource Usage

| Metric | Android Target | iOS Target |
|--------|---------------|------------|
| Installation Size | < 25 MB | < 30 MB |
| Memory Usage (Average) | < 150 MB | < 150 MB |
| Memory Usage (Peak) | < 250 MB | < 280 MB |
| Battery Impact (% per hour active) | < 3% | < 3% |
| Battery Impact (% per hour background) | < 0.5% | < 0.3% |
| CPU Usage (Average) | < 15% | < 15% |
| CPU Usage (Peak) | < 40% for < 500ms | < 40% for < 500ms |

### Network Performance

| Metric | Target |
|--------|--------|
| Initial Load Data | < 1 MB |
| Subsequent Screen Data | < 200 KB |
| API Response Processing Time | < 250ms |
| Image Loading Time | < 500ms |
| Background Sync Data | < 50 KB per sync |

## Desktop Application Performance Budgets

### Startup Performance

| Metric | Target (Standard) | Target (Complex Apps) |
|--------|-----------------|----------------------|
| Application Launch Time | < 3s | < 5s |
| Time to Interactive | < 5s | < 8s |
| Initialization Data Load | < 2s | < 3s |

### Runtime Performance

| Metric | Target |
|--------|--------|
| UI Thread Responsiveness | < 50ms response to user input |
| UI Animation | 60 fps minimum |
| Background Processing Impact on UI | No visible impact |
| Context Menu Display | < 100ms |
| Dialog Opening Time | < 300ms |

### Resource Usage

| Metric | Target (Standard) | Target (Complex Apps) |
|--------|-----------------|----------------------|
| Installation Size | < 100 MB | < 300 MB |
| Memory Usage (Idle) | < 200 MB | < 400 MB |
| Memory Usage (Active) | < 500 MB | < 1 GB |
| CPU Usage (Idle) | < 1% | < 2% |
| CPU Usage (Active) | < 30% | < 50% |
| Disk I/O (Sustained) | < 10 MB/s | < 20 MB/s |
| GPU Usage | < 30% | < 60% |

## Game Performance Budgets

### Frame Rate Targets

| Platform | Target FPS | Minimum Acceptable |
|----------|-----------|-------------------|
| Mobile (Low-end) | 30 fps | 28 fps (95% of time) |
| Mobile (High-end) | 60 fps | 55 fps (95% of time) |
| PC (Minimum Spec) | 30 fps | 30 fps (97% of time) |
| PC (Recommended Spec) | 60 fps | 60 fps (97% of time) |
| Console | 60 fps | 58 fps (99% of time) |
| VR | 90 fps | 90 fps (99% of time) |

### Resource Budgets

| Resource | Mobile Budget | PC/Console Budget |
|----------|--------------|------------------|
| Draw Calls per Frame | < 50 (low-end), < 100 (high-end) | < 2000 |
| Triangles per Frame | < 100K (low-end), < 300K (high-end) | < 3M |
| Texture Memory | < 300 MB (low-end), < 800 MB (high-end) | < 4 GB |
| Total Install Size | < 150 MB (casual), < 1 GB (AAA) | < 20 GB |
| RAM Usage | < 500 MB (low-end), < 1.5 GB (high-end) | < 8 GB |
| Level Loading Time | < 10s (low-end), < 5s (high-end) | < 20s |

### Platform-Specific Metrics

#### Mobile Games

- Battery drain: < 10% per hour of gameplay
- Device temperature: No thermal throttling during 30-minute sessions
- Background memory: < 50 MB when suspended

#### PC Games

- CPU core utilization: < 80% on any core
- Streaming asset loading: No visible hitches
- Shader compilation: < 30s on first run, no runtime stutter

#### Console Games

- Memory fragmentation: < 10% after 2 hours of play
- Suspend/resume time: < 3s
- Input latency: < 50ms (standard), < 20ms (competitive)

## API and Backend Performance Budgets

### Response Time Budgets

| API Type | 50th Percentile | 95th Percentile | 99th Percentile |
|----------|----------------|----------------|----------------|
| Critical Path GET | < 100ms | < 300ms | < 500ms |
| Standard GET | < 200ms | < 500ms | < 1s |
| Search/Filter | < 300ms | < 800ms | < 1.5s |
| POST/PUT (Simple) | < 300ms | < 800ms | < 1.5s |
| POST/PUT (Complex) | < 500ms | < 1.2s | < 2s |
| Batch Operations | < 1s | < 3s | < 5s |
| Report Generation | < 2s | < 5s | < 10s |

### Resource Usage Budgets

| Metric | Target (Per Request) |
|--------|---------------------|
| CPU Time | < 50ms |
| Memory Allocation | < 20 MB |
| Database Queries | < 5 |
| Database Query Time | < 100ms total |
| External API Calls | < 2 |
| External API Time | < 300ms total |

### Scalability Budgets

| Metric | Target |
|--------|--------|
| Requests Per Second (Single Instance) | > 100 RPS |
| Max Concurrent Connections (Single Instance) | > 200 |
| Auto-scaling Response Time | < 30s |
| Initialization Time (New Instance) | < 60s |
| Cache Hit Ratio | > 80% |

## Monitoring and Enforcement

### Production Monitoring

- Set up real-user monitoring (RUM) for web applications
- Implement application performance monitoring (APM) for all services
- Gather performance data across geographic regions
- Collect device and browser-specific metrics
- Monitor 50th, 95th, and 99th percentiles for key metrics
- Create performance dashboards with budget indicators

### CI/CD Integration

- Set up automated performance testing in CI pipeline
- Implement budget threshold checks as part of the build process
- Block deployments that exceed critical budget thresholds
- Generate warnings for approaching thresholds
- Track trends across builds and releases
- Notify relevant teams of budget violations

### Tools and Services

| Application Type | Recommended Tools |
|------------------|-------------------|
| Web | Lighthouse CI, WebPageTest API, SpeedCurve, sitespeed.io |
| Mobile | Firebase Performance Monitoring, New Relic Mobile, AppDynamics |
| Desktop | Custom telemetry, ETW (Windows), DTrace (macOS) |
| Games | Unity Profiler, Unreal Insights, platform-specific tools |
| APIs | New Relic, Datadog, AppDynamics, custom middleware metrics |

## Remediation Strategies

### Web Performance Improvements

1. **JavaScript Optimization**:
   - Implement code splitting and lazy loading
   - Use tree shaking to eliminate dead code
   - Optimize third-party script loading
   - Convert to modern formats (ES modules)

2. **Asset Optimization**:
   - Implement responsive images with srcset
   - Use modern image formats (WebP, AVIF)
   - Optimize SVGs and minimize animation complexity
   - Implement font subsetting and font-display strategies

3. **Delivery Optimization**:
   - Implement effective caching strategies
   - Use content delivery networks (CDNs)
   - Implement HTTP/2 or HTTP/3 transfer
   - Optimize critical rendering path

### Mobile Application Improvements

1. **Startup Optimization**:
   - Implement app startup tracing
   - Optimize initialization processes
   - Use lazy initialization for non-critical components
   - Reduce application size with Android App Bundles or iOS App Thinning

2. **UI Performance**:
   - Flatten view hierarchies
   - Reduce overdraw
   - Optimize list views with recycling
   - Use hardware acceleration appropriately

3. **Resource Management**:
   - Implement memory usage tracking
   - Optimize bitmap handling
   - Manage background processes efficiently
   - Implement efficient data structures

### API and Backend Improvements

1. **Database Optimization**:
   - Optimize queries and add necessary indexes
   - Implement query caching
   - Use database connection pooling
   - Consider read replicas for heavy read operations

2. **Caching Strategies**:
   - Implement multiple cache layers
   - Use distributed caching for scaled deployments
   - Implement data precomputation for expensive operations
   - Set appropriate TTL values based on data volatility

3. **Code Optimization**:
   - Profile and optimize CPU-intensive operations
   - Implement asynchronous processing for appropriate tasks
   - Optimize serialization/deserialization
   - Use efficient algorithms and data structures

## Budget Exceptions

### Exception Process

1. Document the business requirement necessitating the exception
2. Provide technical justification for why the budget cannot be met
3. Outline the user impact and mitigation strategies
4. Get approval from performance architect and product owner
5. Set an expiration date for the exception
6. Create a remediation plan to bring performance back within budget

### Common Valid Exceptions

- Third-party integration requirements with performance implications
- Legacy system integration with inherent performance limitations
- Regulatory compliance requirements adding unavoidable overhead
- Short-term marketing campaigns with temporary performance impact
- Special feature deployments with planned performance improvements

### Exception Documentation Template

```plaintext
# Performance Budget Exception Request

## Basic Information
- Feature/Component: [Name]
- Requested by: [Name/Team]
- Date: [Date]
- Duration: [Timeframe for exception]

## Performance Impact
- Affected Metrics: [List of metrics exceeding budget]
- Current Values: [Current measurements]
- Budget Targets: [Budget requirements]

## Justification
[Detailed explanation of why the exception is necessary]

## Business Impact
[Description of business requirements and value]

## User Impact Analysis
[Analysis of how users will be affected]

## Mitigation Strategies
[Steps being taken to minimize impact]

## Remediation Plan
[Plan to bring performance back within budget]

## Approvals
- Performance Architect: [Name, Date]
- Product Owner: [Name, Date]
- Engineering Lead: [Name, Date]
```

## Performance Testing Standards

### Test Environments

- Configure test environments to closely match production
- Include representative networking conditions
- Test across multiple device profiles and specifications
- Include geographic distribution for global services

### Testing Methodologies

1. **Synthetic Testing**:
   - Run performance tests against key user journeys
   - Test from multiple geographic locations
   - Simulate various device and connection types
   - Test both first-visit and return-visit scenarios

2. **Load Testing**:
   - Establish baseline performance at normal load
   - Test gradual scaling to peak expected load
   - Test sudden traffic spikes
   - Measure recovery time after high load

3. **Endurance Testing**:
   - Test performance stability over extended periods
   - Monitor for memory leaks and resource degradation
   - Verify consistent performance after system has been running for days

### Testing Frequency

| Environment | Frequency | Scope |
|-------------|-----------|-------|
| Development | On significant changes | Focused component testing |
| Integration | Daily | Key user journeys |
| Staging | Before each release | Full application testing |
| Production | Weekly | Synthetic monitoring of critical paths |

### Reporting and Analysis

- Generate detailed performance reports after each test
- Compare results against established budgets
- Identify trends and degradations over time
- Prioritize improvements based on user impact
- Document specific recommendations for optimization
