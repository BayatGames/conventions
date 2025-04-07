<!--
Document: API Documentation Standards
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# API Documentation Standards

This document outlines the standards and best practices for creating and maintaining API documentation across all Bayat projects. Following these guidelines ensures that APIs are well-documented, accessible, and usable by developers.

## Table of Contents

- [API Documentation Principles](#api-documentation-principles)
- [Documentation Structure](#documentation-structure)
- [API Reference Documentation](#api-reference-documentation)
- [OpenAPI/Swagger Standards](#openapiswagger-standards)
- [Code Examples](#code-examples)
- [GraphQL Schema Documentation](#graphql-schema-documentation)
- [Authentication Documentation](#authentication-documentation)
- [Error Handling Documentation](#error-handling-documentation)
- [Versioning Documentation](#versioning-documentation)
- [Internationalization (i18n)](#internationalization-i18n)
- [Documentation Tools](#documentation-tools)
- [Documentation Review Process](#documentation-review-process)
- [Keeping Documentation Updated](#keeping-documentation-updated)

## API Documentation Principles

All API documentation at Bayat should adhere to the following core principles:

1. **Comprehensive**: Cover all endpoints, parameters, and response formats
2. **Accurate**: Ensure documentation matches the actual implementation
3. **Clear**: Use plain language and avoid unnecessary jargon
4. **Consistent**: Follow the same format and style throughout
5. **Accessible**: Structure documentation to be easily navigable and searchable
6. **Example-driven**: Include practical examples for all operations
7. **User-centric**: Consider the needs of the API consumer
8. **Maintainable**: Design documentation to be easily updated alongside code changes

## Documentation Structure

Each API documentation set should include the following components:

### 1. Introduction

- Overview of the API's purpose and functionality
- Target audience and use cases
- System requirements and prerequisites
- API versioning information
- Support and feedback channels

### 2. Getting Started

- Authentication overview
- Base URL information
- Basic request/response examples
- Rate limiting details
- Quick start guide with simple working examples

### 3. Core Concepts

- Explanation of domain-specific terminology
- Resource model overview
- Relationships between resources
- Common patterns used throughout the API

### 4. API Reference

- Comprehensive documentation of all endpoints
- Request parameters, headers, and body schemas
- Response status codes, headers, and body schemas
- Example requests and responses

### 5. Guides and Tutorials

- Step-by-step tutorials for common use cases
- Integration examples with popular frameworks
- Migration guides for version upgrades
- Best practices for using the API

### 6. SDK Documentation (if applicable)

- Installation instructions
- Configuration options
- Method reference
- Example SDK usage

## API Reference Documentation

Each API endpoint must be documented with the following information:

### HTTP APIs

```
# Endpoint Name

## Description

Concise description of what the endpoint does and when to use it.

## Request

`METHOD /path/to/resource`

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| Content-Type | Yes | Must be application/json |
| Authorization | Yes | Bearer {token} |

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Unique identifier of the resource |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| limit | integer | No | 20 | Maximum number of items to return |
| offset | integer | No | 0 | Number of items to skip |

### Request Body

```json
{
  "property1": "string",
  "property2": 123,
  "property3": {
    "nested": true
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| property1 | string | Yes | Description of property1 |
| property2 | integer | No | Description of property2 |
| property3.nested | boolean | No | Description of nested property |

## Response

### Success Response (200 OK)

```json
{
  "id": "abc123",
  "property1": "string value",
  "property2": 123,
  "createdAt": "2023-01-01T12:00:00Z"
}
```

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier of the created resource |
| property1 | string | Description of property1 |
| property2 | integer | Description of property2 |
| createdAt | string | ISO 8601 timestamp of creation date |

### Error Responses

#### 400 Bad Request

```json
{
  "error": "validation_error",
  "message": "Invalid request parameters",
  "details": [
    {"field": "property1", "message": "Field is required"}
  ]
}
```

#### 401 Unauthorized

```json
{
  "error": "unauthorized",
  "message": "Authentication required"
}
```

#### 404 Not Found

```json
{
  "error": "not_found",
  "message": "Resource not found"
}
```

## Examples

### Example Request

```bash
curl -X POST \
  https://api.example.com/v1/resources \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "property1": "example",
    "property2": 42,
    "property3": {
      "nested": true
    }
  }'
```

### Example Response

```json
{
  "id": "abc123",
  "property1": "example",
  "property2": 42,
  "createdAt": "2023-01-01T12:00:00Z"
}
```

## Notes

Additional notes, edge cases, or limitations to be aware of.

```

## OpenAPI/Swagger Standards

For RESTful APIs, use OpenAPI (Swagger) specification version 3.0 or later.

### File Structure

- Use separate files for large API definitions
- Organize by resource type
- Use `$ref` to reference reusable components

### Best Practices

- Include detailed descriptions for all components
- Use standard formats for common types (dates, emails, etc.)
- Specify examples for all schemas
- Document all possible response codes
- Include security schemes

### Example OpenAPI Extract

```yaml
openapi: 3.0.3
info:
  title: Example API
  description: API for managing examples
  version: 1.0.0
  contact:
    name: Bayat API Team
    email: api@bayat.io
    url: https://docs.bayat.io
servers:
  - url: https://api.bayat.io/v1
    description: Production server
  - url: https://api.staging.bayat.io/v1
    description: Staging server
paths:
  /users:
    get:
      summary: List users
      description: Returns a paginated list of users
      parameters:
        - name: limit
          in: query
          description: Maximum number of users to return
          schema:
            type: integer
            default: 20
            minimum: 1
            maximum: 100
      responses:
        '200':
          description: Successful operation
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
          example: "123e4567-e89b-12d3-a456-426614174000"
        name:
          type: string
          example: "John Doe"
        email:
          type: string
          format: email
          example: "john.doe@example.com"
      required:
        - id
        - name
        - email
    Pagination:
      type: object
      properties:
        total:
          type: integer
          example: 100
        limit:
          type: integer
          example: 20
        offset:
          type: integer
          example: 0
        has_more:
          type: boolean
          example: true
```

## Code Examples

### Code Example Guidelines

- Include code examples in all relevant programming languages for your API
- Provide examples for common use cases and operations
- Include both basic usage and more complex scenarios
- Ensure examples are complete and can be run with minimal changes
- Keep examples up-to-date with the latest API version
- Provide examples for handling errors and edge cases

### Example Format

For each endpoint, provide examples in at least these formats:

- cURL command
- HTTP request/response
- JavaScript/TypeScript (for web APIs)
- Platform-specific examples (Swift, Kotlin, etc. for mobile APIs)
- SDK examples if applicable

### Interactive Examples

Where possible, provide interactive examples using:

- Swagger UI for REST APIs
- GraphQL Playground for GraphQL APIs
- Runnable code snippets with tools like JSFiddle or CodePen

## GraphQL Schema Documentation

For GraphQL APIs, all schemas must be thoroughly documented:

### Type Documentation

Each type must include:

- Clear description of what the type represents
- Description for each field
- Description for arguments on fields
- Examples of usage

### Example GraphQL Schema Documentation

```graphql
"""
A user in the system.
This type represents a user account with profile information.
"""
type User {
  """Unique identifier for the user"""
  id: ID!
  
  """User's full name"""
  name: String!
  
  """User's email address"""
  email: String!
  
  """
  User's profile picture URL
  If no picture is set, returns a default avatar
  """
  profilePicture(
    """Size of the image in pixels"""
    size: Int = 128
  ): String
  
  """List of posts authored by this user"""
  posts(
    """Maximum number of posts to return"""
    limit: Int = 10,
    
    """Number of posts to skip for pagination"""
    offset: Int = 0
  ): [Post!]!
  
  """When the user account was created"""
  createdAt: DateTime!
}

"""
A post created by a user.
Posts can contain text content and optional media attachments.
"""
type Post {
  """Unique identifier for the post"""
  id: ID!
  
  """The main content of the post"""
  content: String!
  
  """User who created this post"""
  author: User!
  
  """When the post was created"""
  createdAt: DateTime!
  
  """When the post was last updated"""
  updatedAt: DateTime!
}
```

## Authentication Documentation

Authentication documentation must include:

1. **Authentication Methods**:
   - Detailed explanation of all supported authentication methods
   - When to use each method
   - Security considerations for each method

2. **Token Management**:
   - How to obtain tokens
   - Token lifecycle (expiration, refresh)
   - Handling token errors
   - Revoking tokens

3. **Example Flows**:
   - Complete examples for each authentication flow
   - Diagrams for complex flows (like OAuth 2.0)

4. **Best Practices**:
   - Security recommendations
   - Token storage guidelines
   - Error handling strategies

### OAuth 2.0 Example

````markdown
# OAuth 2.0 Authentication

Our API uses OAuth 2.0 for authentication. We support the following grant types:

## Authorization Code Flow

This flow is recommended for server-side applications.

1. Direct the user to:
   ```
   https://auth.bayat.io/oauth/authorize?
     response_type=code&
     client_id=YOUR_CLIENT_ID&
     redirect_uri=YOUR_REDIRECT_URI&
     scope=read+write&
     state=RANDOM_STATE_STRING
   ```

2. After user authorization, we'll redirect to your `redirect_uri` with a code:
   ```
   https://your-app.com/callback?code=AUTHORIZATION_CODE&state=RANDOM_STATE_STRING
   ```

3. Exchange the code for an access token:
   ```bash
   curl -X POST https://auth.bayat.io/oauth/token \
     -d 'grant_type=authorization_code' \
     -d 'client_id=YOUR_CLIENT_ID' \
     -d 'client_secret=YOUR_CLIENT_SECRET' \
     -d 'code=AUTHORIZATION_CODE' \
     -d 'redirect_uri=YOUR_REDIRECT_URI'
   ```

4. The response will include your access token:
   ```json
   {
     "access_token": "ACCESS_TOKEN",
     "token_type": "Bearer",
     "expires_in": 3600,
     "refresh_token": "REFRESH_TOKEN",
     "scope": "read write"
   }
   ```

5. Use the access token in API requests:
   ```bash
   curl -H "Authorization: Bearer ACCESS_TOKEN" https://api.bayat.io/v1/users/me
   ```
````

## Error Handling Documentation

Error documentation must include:

1. **Standard Error Format**:
   - JSON schema for error responses
   - Explanation of common fields

2. **Error Types**:
   - Comprehensive list of error codes
   - Description of each error type
   - Possible causes for each error
   - Recommended actions to resolve errors

3. **HTTP Status Codes**:
   - Complete list of used status codes
   - Meaning in the context of your API

### Error Documentation Example

````markdown
# Error Handling

## Error Response Format

All API errors are returned in a consistent JSON format:

```json
{
  "error": {
    "code": "resource_not_found",
    "message": "The requested resource was not found",
    "details": {
      "resource_type": "user",
      "resource_id": "123"
    },
    "request_id": "f7a8b934-1c38-42e7-9151-a74b21efb5c7"
  }
}
```

## Error Fields

| Field | Description |
|-------|-------------|
| code | Machine-readable error code string |
| message | Human-readable error message |
| details | Additional context about the error (varies by error type) |
| request_id | Unique identifier for the request, useful for troubleshooting |

## Common Error Codes

| Code | HTTP Status | Description | Resolution |
|------|-------------|-------------|------------|
| authentication_required | 401 | No valid authentication provided | Ensure you're sending valid credentials |
| invalid_credentials | 401 | The provided credentials are invalid | Check your API key or token |
| permission_denied | 403 | User lacks permission for this action | Request additional permissions or use a different account |
| resource_not_found | 404 | The requested resource doesn't exist | Verify the ID or path is correct |
| validation_error | 400 | The request data failed validation | Check the details field for specific validation failures |
| rate_limit_exceeded | 429 | You've exceeded your rate limit | Slow down your request rate and try again later |
| internal_server_error | 500 | Something went wrong on our end | Contact support with the request_id |
````

## Versioning Documentation

API versioning documentation must include:

1. **Versioning Strategy**:
   - How versioning is implemented (URL path, header, parameter)
   - Current versions and their status (stable, beta, deprecated)
   - Sunset policy for deprecated versions

2. **Version Changelog**:
   - What changed between versions
   - Breaking vs. non-breaking changes
   - Migration guides for major changes

3. **Version Selection**:
   - How to request specific versions
   - Default version behavior

### Versioning Documentation Example

````markdown
# API Versioning

## Version Structure

Our API uses URL-based versioning, with the version as the first path segment:

```
<https://api.bayat.io/v1/resources>
<https://api.bayat.io/v2/resources>

```

## Current Versions

| Version | Status | Released | End-of-Life |
|---------|--------|----------|-------------|
| v1 | Deprecated | 2021-01-15 | 2023-01-15 |
| v2 | Stable | 2022-06-10 | - |
| v3 | Beta | 2023-03-01 | - |

## Version Lifecycle

- **Beta**: May have breaking changes between minor versions
- **Stable**: No breaking changes without a major version change
- **Deprecated**: No new features, only critical security updates
- **End-of-Life**: No longer supported, will return 410 Gone

## V1 to V2 Migration Guide

V2 includes the following breaking changes:

1. User resource changes:
   - `name` field split into `first_name` and `last_name`
   - `address` now requires a structured object instead of string

2. Authentication changes:
   - Only OAuth 2.0 is supported (Basic Auth removed)
   - Tokens expire after 24 hours (was 7 days in v1)

See our [detailed migration guide](https://docs.bayat.io/api/migration/v1-to-v2) for code examples.
````

## Internationalization (i18n)

For APIs that support internationalization:

1. **Locale Support**:
   - List of supported locales
   - Default locale behavior
   - How to request specific locales (headers, parameters)

2. **Localized Content**:
   - How to retrieve content in specific languages
   - Translation fallback behavior
   - Handling for RTL languages

3. **Date/Time/Number Formatting**:
   - Time zone handling
   - Date and time formats
   - Number and currency formats

## Documentation Tools

### Recommended Documentation Tools

Choose the appropriate tools based on your API type:

**REST APIs**:

- OpenAPI/Swagger with Swagger UI
- ReDoc
- Stoplight Studio

**GraphQL APIs**:

- GraphQL Playground
- GraphiQL
- Apollo Studio Explorer

**General Documentation**:

- Markdown for baseline documentation
- Docusaurus for documentation websites
- Postman for interactive collections
- ReadMe.io for full-featured documentation platform

### Documentation as Code

- Store documentation alongside code in version control
- Use CI/CD to validate and publish documentation
- Implement automated tests for documentation accuracy
- Set up linting for documentation files

## Documentation Review Process

To ensure high-quality documentation:

1. **Technical Review**:
   - Ensure technical accuracy
   - Verify examples work as described
   - Check all endpoints, parameters, and responses are documented

2. **Developer Experience Review**:
   - Assess clarity from a new developer's perspective
   - Ensure logical organization and flow
   - Check completeness of examples

3. **Editorial Review**:
   - Check grammar, spelling, and style consistency
   - Ensure compliance with branding guidelines
   - Apply plain language principles

4. **Regular Reviews**:
   - Schedule quarterly documentation audits
   - Collect and incorporate user feedback
   - Test documentation with new developers

## Keeping Documentation Updated

To maintain accurate documentation:

1. **Documentation-Code Linkage**:
   - Generate documentation from code where possible
   - Verify documentation in CI/CD pipelines
   - Enforce "docs or it didn't happen" policy for new features

2. **Version Control**:
   - Keep documentation in the same repository as code
   - Review documentation changes in pull requests
   - Tag documentation with applicable API versions

3. **Monitoring**:
   - Track documentation usage and feedback
   - Identify most-viewed and most-confused areas
   - Analyze support requests to identify documentation gaps

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 2025-03-20 | Initial version |
