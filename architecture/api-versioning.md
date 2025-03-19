# API Versioning and Deprecation Strategy

This document outlines the formal process for API lifecycle management at Bayat, providing guidelines for versioning, maintaining, and deprecating APIs in a way that balances innovation with stability for consumers.

## Table of Contents

- [Introduction](#introduction)
- [API Versioning Strategy](#api-versioning-strategy)
- [Backwards Compatibility](#backwards-compatibility)
- [Change Management](#change-management)
- [Deprecation Process](#deprecation-process)
- [API Lifecycle Stages](#api-lifecycle-stages)
- [Documentation Requirements](#documentation-requirements)
- [Communication Strategy](#communication-strategy)
- [Consumer Migration Guidelines](#consumer-migration-guidelines)
- [Version Negotiation](#version-negotiation)
- [API Versioning Patterns](#api-versioning-patterns)
- [Implementation Case Studies](#implementation-case-studies)
- [Governance and Compliance](#governance-and-compliance)
- [Tools and Implementation](#tools-and-implementation)

## Introduction

Proper API lifecycle management ensures that we can evolve our services while maintaining the stability that API consumers require. This document establishes a consistent approach to API versioning and deprecation across all Bayat services.

### Objectives

- **Stability**: Provide a stable platform for API consumers
- **Flexibility**: Allow for evolution and improvement of APIs
- **Predictability**: Establish clear expectations around API lifecycles
- **Consistency**: Maintain a uniform approach across all services
- **Communication**: Ensure timely and clear notifications of changes

### Scope

These guidelines apply to:

- Public APIs exposed to external consumers
- Internal APIs used across different teams
- Partner APIs exposed to specific third-party collaborators
- Both REST and GraphQL APIs (with appropriate adaptations)

## API Versioning Strategy

### Versioning Scheme

All APIs should follow semantic versioning principles with a mandatory major version in the URL path:

- **REST APIs**: `/v{major}/resource`
  - Example: `/v1/users`, `/v2/users`

- **GraphQL APIs**: `/graphql/v{major}`
  - Individual types and fields are versioned through the schema

### Version Components

- **Major Version (v1, v2, etc.)**: For backwards-incompatible changes
- **Minor Versions**: For backwards-compatible feature additions (not exposed in URI)
- **Patch Versions**: For backwards-compatible bug fixes (not exposed in URI)

### Version Identification

- **URI Path**: Primary method for REST API version identification
- **Accept Header**: Optional secondary method (e.g., `Accept: application/vnd.bayat.v1+json`)
- **GraphQL**: Version included in operation names and/or directives

### Versioning Criteria

#### When to Create a New Major Version

A new major version is required when making:

1. **Breaking changes to request formats**
   - Removing or renaming required request parameters
   - Changing parameter types or validation rules

2. **Breaking changes to response formats**
   - Removing or renaming response fields
   - Changing data types of existing fields
   - Significantly altering response structure

3. **Behavioral changes**
   - Changing resource identifiers
   - Fundamentally altering the processing model
   - Changing security or authorization models

#### When Not to Create a New Version

Maintain the current version when:

1. **Adding new endpoints or operations**
2. **Adding optional request parameters**
3. **Adding new response fields**
4. **Fixing bugs that align with documented behavior**
5. **Improving performance without behavioral changes**

## Backwards Compatibility

### Compatibility Guidelines

- **Additive Changes**: Preferred approach for evolving APIs
- **Default Values**: Provide sensible defaults for new parameters
- **Field Deprecation**: Mark fields as deprecated before removal
- **Payload Formats**: Support established formats even when introducing new ones

### Compatibility Testing

- **Contract Tests**: Verify API contract conformance
- **Consumer Tests**: Run tests simulating existing clients
- **Version Comparison**: Automated comparison between versions
- **CI/CD Integration**: Include compatibility checks in pipelines

### Extension Mechanisms

- **API Extensions**: Implement using optional parameters or headers
- **Feature Flags**: Control feature availability without versioning
- **Capability Discovery**: Allow consumers to query supported features

## Change Management

### Change Classification

Classify all API changes as:

- **Breaking**: Changes that violate backwards compatibility
- **Non-Breaking Additions**: New functionality that preserves compatibility
- **Non-Breaking Modifications**: Changes that don't affect contract

### Change Review Process

1. **Proposal**: Document proposed changes and classification
2. **Impact Analysis**: Assess effect on existing consumers
3. **Technical Review**: Evaluation by API design review board
4. **Approval**: Sign-off based on change classification
   - Breaking changes require higher approval level

### Change Implementation

1. **Development**: Implement changes in isolated branch
2. **Testing**: Verify compatibility and functionality
3. **Documentation**: Update API documentation
4. **Deployment**: Release using appropriate strategy
5. **Monitoring**: Watch for unexpected consumer issues

## Deprecation Process

### Deprecation Policy

- **Minimum Lifespan**: Major API versions supported for at least 24 months
- **Overlap Period**: At least 6 months of dual support when introducing new versions
- **Extended Support**: Available for critical partners or systems
- **Emergency Exceptions**: Process for critical security or compliance issues

### Deprecation Stages

1. **Announcement**: Formal notice of intent to deprecate
2. **Deprecation Period**: Phase during which API is marked as deprecated but fully functional
3. **Sunset Period**: Phase with limited support (bug fixes only)
4. **Retirement**: Complete decommissioning of the API version

### Deprecation Notices

- **Timeline Communication**: Clear dates for each deprecation stage
- **Alternative Guidance**: Documentation of migration paths
- **Impact Assessment**: Information about what functionality is affected
- **Contact Information**: Support channels for migration assistance

### Grace Periods

- **Standard Grace Period**: 12 months from deprecation to retirement
- **Extended Support**: Process for requesting extended timelines
- **Usage-Based Extensions**: Automated extensions based on active usage

## API Lifecycle Stages

### Experimental

- **Purpose**: Testing new concepts and gathering feedback
- **Stability**: No stability guarantees
- **Availability**: Limited to selected partners
- **Support**: Minimal support, rapid iteration
- **Identification**: Clearly marked as experimental

### Beta

- **Purpose**: Validating API design with broader audience
- **Stability**: Some changes may still occur
- **Availability**: Open to registered developers
- **Support**: Standard support with understanding of beta status
- **Identification**: Clearly marked as beta

### General Availability (GA)

- **Purpose**: Production use by all consumers
- **Stability**: Full stability guarantees
- **Availability**: Open to all authorized users
- **Support**: Full production support
- **Lifecycle**: Subject to standard versioning and deprecation

### Deprecated

- **Purpose**: Indicating planned removal
- **Stability**: No new features, only critical fixes
- **Availability**: Existing consumers only
- **Support**: Limited to critical issues
- **Identification**: Clearly marked as deprecated

### Retired

- **Purpose**: End of life
- **Availability**: API endpoints return appropriate error responses
- **Support**: No support provided
- **Documentation**: Maintained for archival purposes only

## Documentation Requirements

### Version Documentation

For each API version, document:

- **Release Date**: When the version became available
- **End-of-Life Date**: When the version will be retired (if known)
- **Supported Features**: Complete list of endpoints and operations
- **Known Limitations**: Any constraints or restrictions
- **Changelog**: History of updates within the version

### Deprecation Documentation

For deprecated elements, document:

- **Deprecation Date**: When the element was marked deprecated
- **Retirement Date**: When the element will be removed
- **Replacement**: Alternative approach or new version
- **Migration Guide**: Step-by-step instructions for upgrading
- **Breaking Changes**: List of incompatibilities to address

### Documentation Formats

- **OpenAPI/Swagger**: For REST API documentation
- **GraphQL Schema**: For GraphQL API documentation
- **Developer Portal**: Central location for all API information
- **API Changelogs**: Maintained for all API versions
- **Migration Guides**: Detailed instructions for version transitions

## Communication Strategy

### Announcement Channels

- **Developer Portal**: Primary location for API announcements
- **Email Notifications**: Direct communication to registered developers
- **Release Notes**: Detailed documentation of changes
- **API Response Headers**: Runtime indications of deprecation
- **API Dashboard**: Status indicators for each API version

### Notification Timelines

- **Major Releases**: Announced at least 3 months before release
- **Minor Releases**: Announced at least 1 month before release
- **Deprecation**: Announced at least 12 months before retirement
- **Emergency Changes**: As much notice as possible given circumstances

### Communication Content

- **What**: Clear description of the change
- **When**: Timeline with specific dates
- **Why**: Rationale behind the change
- **Impact**: Who is affected and how
- **Action**: What consumers need to do
- **Support**: How to get help with the transition

## Consumer Migration Guidelines

### Migration Support

- **Migration Tools**: Utilities to assist with upgrades
- **Compatibility Libraries**: Adapters for transitional support
- **Code Examples**: Before/after examples of client implementation
- **Testing Environments**: Sandbox for testing migrations
- **Migration Office Hours**: Scheduled support sessions

### Best Practices for Consumers

- **API Version Pinning**: Explicitly specify version in clients
- **Regular Upgrades**: Plan for periodic version adoption
- **Automated Tests**: Maintain tests against the API contract
- **Deprecation Monitoring**: Track deprecation notices
- **Loose Parsing**: Implement tolerant readers where possible

### Migration Validation

- **Compatibility Checkers**: Tools to verify client compatibility
- **Request/Response Simulators**: Test against old and new versions
- **Traffic Shadowing**: Send duplicate requests to validate in production
- **Phased Rollout**: Gradual migration of client traffic

## Version Negotiation

Effective version negotiation enables seamless client-server communication across API versions.

### Content Negotiation Strategies

1. **URL Path Versioning**
   - **Implementation**:

     ```http
     GET /v1/users/123
     GET /v2/users/123
     ```

   - **Advantages**:
     - Explicit and visible
     - Cache-friendly
     - Easy debugging
   - **Disadvantages**:
     - URL pollution
     - Cannot version single resources independently
     - Tied to routing infrastructure

2. **Query Parameter Versioning**
   - **Implementation**:

     ```http
     GET /users/123?version=1
     GET /users/123?version=2
     ```

   - **Advantages**:
     - Easy to implement
     - Optional parameter
     - Can default to latest
   - **Disadvantages**:
     - Less visible in logs
     - Can be overlooked
     - Mixed caching behavior

3. **Header-Based Versioning**
   - **Implementation**:

     ```http
     GET /users/123
     Accept: application/vnd.bayat.v1+json
     
     GET /users/123
     Accept: application/vnd.bayat.v2+json
     ```

   - **Advantages**:
     - Clean URLs
     - Follows HTTP specification
     - Separates versioning from resource identification
   - **Disadvantages**:
     - Less visible
     - Harder to test
     - Requires header manipulation

4. **Content Type Versioning**
   - **Implementation**:

     ```http
     GET /users/123
     Content-Type: application/vnd.bayat.v1+json
     
     GET /users/123
     Content-Type: application/vnd.bayat.v2+json
     ```

   - **Advantages**:
     - Specifies both version and format
     - Follows media type extension pattern
   - **Disadvantages**:
     - Only applicable to request body
     - Mixed support in clients

### Server-Side Implementation

1. **Routing Layer Version Detection**

   ```javascript
   // Example Express.js middleware
   function versionMiddleware(req, res, next) {
     // Extract version from URL
     const urlVersion = req.path.match(/^\/v(\d+)\//);
     if (urlVersion) {
       req.apiVersion = parseInt(urlVersion[1], 10);
     } 
     // Or from Accept header
     else if (req.headers.accept) {
       const headerVersion = req.headers.accept.match(/application\/vnd\.bayat\.v(\d+)\+json/);
       if (headerVersion) {
         req.apiVersion = parseInt(headerVersion[1], 10);
       }
     }
     // Default version
     req.apiVersion = req.apiVersion || 1;
     next();
   }
   ```

2. **Version-Based Controller Selection**

   ```javascript
   // Example controller dispatcher
   function dispatchToVersionedController(req, res) {
     const version = req.apiVersion;
     const controller = controllers[`v${version}`] || controllers.latest;
     return controller.handleRequest(req, res);
   }
   ```

3. **Content Negotiation Response**

   ```javascript
   // Example content negotiation
   function sendVersionedResponse(req, res, data) {
     const version = req.apiVersion;
     res.setHeader('API-Version', version);
     
     // Add deprecation headers if applicable
     if (version < currentVersion) {
       res.setHeader('Deprecation', 'true');
       res.setHeader('Sunset', deprecationDates[version]);
       res.setHeader('Link', `<https://api.bayat.com/v${currentVersion}${req.path}>; rel="successor-version"`);
     }
     
     // Format response according to version
     const formatter = responseFormatters[`v${version}`];
     const formattedData = formatter ? formatter(data) : data;
     
     res.json(formattedData);
   }
   ```

### Client-Side Implementation

1. **API Client with Version Support**

   ```typescript
   // Example TypeScript API client
   class BayatApiClient {
     private baseUrl: string;
     private version: number;
     
     constructor(config: {baseUrl: string, version: number}) {
       this.baseUrl = config.baseUrl;
       this.version = config.version;
     }
     
     async getResource(id: string): Promise<any> {
       const url = `${this.baseUrl}/v${this.version}/resources/${id}`;
       const response = await fetch(url, {
         headers: {
           'Accept': `application/vnd.bayat.v${this.version}+json`
         }
       });
       
       // Check for deprecation headers
       if (response.headers.get('Deprecation')) {
         console.warn(`API version ${this.version} is deprecated. Sunset date: ${response.headers.get('Sunset')}`);
         const link = response.headers.get('Link');
         if (link) {
           console.warn(`Consider upgrading to: ${link}`);
         }
       }
       
       return response.json();
     }
   }
   ```

2. **Transparent Version Upgrade**

   ```typescript
   // Example automatic version migration
   class UpgradingApiClient extends BayatApiClient {
     private preferredVersion: number;
     
     constructor(config: {baseUrl: string, version: number, preferredVersion: number}) {
       super(config);
       this.preferredVersion = config.preferredVersion;
     }
     
     async getResource(id: string): Promise<any> {
       try {
         // Try with current version
         return await super.getResource(id);
       } catch (error) {
         if (error.status === 410 && this.version < this.preferredVersion) {
           // Version gone, try preferred version
           this.version = this.preferredVersion;
           return this.getResource(id);
         }
         throw error;
       }
     }
   }
   ```

## API Versioning Patterns

Different architectural patterns for implementing API versioning:

### Facade Pattern

The facade pattern creates a unified interface that hides different versioned implementations.

```javascript
// Facade implementation
class UserServiceFacade {
  constructor() {
    this.implementations = {
      v1: new UserServiceV1(),
      v2: new UserServiceV2()
    };
  }
  
  getUser(version, userId) {
    const implementation = this.implementations[`v${version}`] || this.implementations.v1;
    const user = implementation.getUser(userId);
    
    // Some common post-processing
    return user;
  }
}
```

**Best for**:

- Centralizing version-specific logic
- Maintaining multiple implementations cleanly
- Legacy system integrations

### Adapter Pattern

The adapter pattern converts new API responses to match older formats.

```javascript
// Response adapter implementation
class V1ResponseAdapter {
  adaptUser(v2User) {
    return {
      id: v2User.id,
      name: v2User.fullName, // v2 renamed this field
      email: v2User.email,
      // v1 didn't have phoneNumber
      // Convert new createdAt ISO date to v1 timestamp
      created: new Date(v2User.createdAt).getTime() / 1000
    };
  }
}
```

**Best for**:

- Maintaining older interfaces without duplicating logic
- Gradual refactoring
- Supporting multiple API consumers with different needs

### Router Pattern

The router pattern directs requests to different service implementations based on version.

```javascript
// Router implementation
class VersionRouter {
  constructor() {
    this.routes = {
      'v1/users': UserControllerV1,
      'v2/users': UserControllerV2,
      'v1/products': ProductControllerV1,
      'v2/products': ProductControllerV2
    };
  }
  
  route(request) {
    const version = request.version;
    const resource = request.resource;
    const key = `v${version}/${resource}`;
    
    const controller = this.routes[key] || this.getLatestController(resource);
    return controller.handleRequest(request);
  }
  
  getLatestController(resource) {
    // Find latest version for this resource
    const prefix = new RegExp(`^v\\d+/${resource}$`);
    const matchingRoutes = Object.keys(this.routes).filter(r => prefix.test(r));
    const latest = matchingRoutes.sort().pop();
    return this.routes[latest];
  }
}
```

**Best for**:

- Granular control over routing
- Independent versioning of different resources
- API gateways

### Transformation Pipeline Pattern

A pipeline that transforms requests and responses based on version-specific rules.

```javascript
// Pipeline implementation
class ApiTransformationPipeline {
  constructor() {
    this.requestTransformers = {
      v1: [stripAuthenticationTransformer, convertIdsTransformer],
      v2: [enrichRequestTransformer]
    };
    
    this.responseTransformers = {
      v1: [simplifyResponseTransformer, convertDateFormatsTransformer],
      v2: [addHATEOASLinksTransformer]
    };
  }
  
  transformRequest(request) {
    const version = request.version;
    const transformers = this.requestTransformers[`v${version}`] || [];
    
    return transformers.reduce((req, transformer) => transformer(req), request);
  }
  
  transformResponse(response, version) {
    const transformers = this.responseTransformers[`v${version}`] || [];
    
    return transformers.reduce((res, transformer) => transformer(res), response);
  }
}
```

**Best for**:

- Complex transformations between versions
- Separation of version-specific logic from core business logic
- Systems with many incremental changes between versions

### Bounded Context Pattern

Separate services handle different API versions, using domain-driven design principles.

```javascript
// Bounded context example (conceptual)
class UserServiceV1 {
  // Has its own data model, repository, and domain logic
  // Optimized for V1 API requirements
}

class UserServiceV2 {
  // Has updated data model with new concepts and relationships
  // Optimized for V2 API requirements
}

// API Gateway routes to appropriate service
apiGateway.route('/v1/users', userServiceV1);
apiGateway.route('/v2/users', userServiceV2);
```

**Best for**:

- Significantly different domain models between versions
- Microservice architectures
- Complete rewrites of subsystems

## Implementation Case Studies

Real-world examples of API versioning implementations at Bayat.

### Case Study 1: Account Management API

#### Background

The Account Management API needed to transition from a monolithic structure to a more granular microservice architecture while maintaining compatibility for hundreds of existing clients.

#### Versioning Approach

- **Strategy**: URL path versioning with route-based dispatch
- **Implementation**:
  - Created v2 API with improved resource modeling
  - Maintained v1 endpoints using adapter pattern
  - Implemented automatic documentation generation for both versions

#### Migration Strategy

1. Released v2 API in parallel with v1
2. Provided client libraries that supported both versions
3. Implemented analytics to track usage of each endpoint by version
4. Targeted high-impact clients for direct migration assistance
5. Set 18-month deprecation timeline for v1

#### Challenges and Solutions

- **Challenge**: Some v1 clients were embedded in devices with limited update capability
- **Solution**: Extended support for critical v1 endpoints beyond standard timeline

- **Challenge**: Performance degradation in v1 adapter layer
- **Solution**: Implemented caching and optimized v1-to-v2 transformations

#### Results

- 93% of clients migrated within 14 months
- 99.8% uptime maintained throughout migration
- 40% reduction in operational costs after v1 retirement

### Case Study 2: Payment Processing API

#### Background

The Payment Processing API required significant security enhancements and new regulatory compliance features.

#### Versioning Approach

- **Strategy**: Combined URL and header versioning
- **Implementation**:
  - Major behavioral changes in v2
  - Granular feature flags within versions
  - Compliance requirements enforced differently by version

#### Migration Strategy

1. Created detailed migration documentation
2. Developed migration testing tool
3. Implemented side-by-side request validation
4. Provided temporary proxying between versions

#### Challenges and Solutions

- **Challenge**: Different regional compliance requirements
- **Solution**: Version-specific compliance adapters with geographical routing

- **Challenge**: Complex transaction reconciliation between versions
- **Solution**: Introduced a reconciliation service to maintain data consistency

#### Results

- 100% of clients migrated within regulatory deadline
- Zero compliance violations during transition
- 27% reduction in transaction processing latency in v2

### Case Study 3: Content Delivery API

#### Background

The Content Delivery API evolved from a simple file-serving system to a rich content management platform.

#### Versioning Approach

- **Strategy**: Content negotiation with feature discovery
- **Implementation**:
  - Content-type based versioning
  - Capability discovery endpoint
  - Progressive enhancement pattern

#### Migration Strategy

1. Introduced new capabilities as optional enhancements
2. Maintained compatibility layers for basic functionality
3. Gradually deprecated legacy features
4. Client-controlled adoption rate

#### Challenges and Solutions

- **Challenge**: Mixed client capabilities needed simultaneous support
- **Solution**: Request-based feature negotiation and content transformation pipeline

- **Challenge**: Cache efficiency across versions
- **Solution**: Variant-aware CDN configuration and normalization of cache keys

#### Results

- Seamless addition of 15 major features over 2 years
- No mandatory client migrations required
- 99.95% cache hit rate maintained throughout evolution

## Governance and Compliance

### API Review Board

- **Membership**: Cross-functional team of API experts
- **Responsibilities**: Review breaking changes and versioning decisions
- **Process**: Regular review meetings for API changes
- **Authority**: Approval required for breaking changes

### Compliance Requirements

- **Contractual Obligations**: Adherence to partner SLAs
- **Regulatory Requirements**: Consideration of regulatory constraints
- **Security Reviews**: Mandatory for all versions
- **Performance Standards**: Baseline requirements for all APIs

### Metrics and Monitoring

- **Usage Tracking**: Monitor usage by version
- **Consumer Impact**: Assess effect of changes on consumers
- **Migration Progress**: Track adoption of new versions
- **SLA Compliance**: Measure uptime and performance by version

## Tools and Implementation

### URI Versioning Implementation

```http
// Example URL structure
https://api.bayat.com/v1/resources
https://api.bayat.com/v2/resources
```

- Route traffic based on version prefix
- Maintain separate handlers for each major version
- Share common logic through internal libraries

### HTTP Header Versioning (Alternative)

```http
// Example Header
Accept: application/vnd.bayat.v1+json
```

- Parse version from Accept header
- Default to latest version if not specified
- Include version in response headers

### GraphQL Versioning

- Use schema directives to mark deprecated fields
- Implement version-specific resolvers
- Consider type extensions for versioned fields

### Deprecation Headers

```http
// Example Response Headers
Deprecation: true
Sunset: Sat, 31 Dec 2023 23:59:59 GMT
Link: <https://api.bayat.com/v2/resource>; rel="successor-version"
```

- Include standardized headers in responses
- Provide machine-readable deprecation information
- Link to documentation and successor versions

### Implementation Patterns

- **API Gateway**: Centralized version routing and migration
- **Facade Pattern**: Compatibility layers for older versions
- **Microservice Versioning**: Independent versioning of services
- **Feature Toggles**: Dynamic control of API capabilities
- **Strangler Pattern**: Gradual replacement of API implementations
