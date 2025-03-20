# API Design Standards

## RESTful Resource Naming

- Use nouns, not verbs, for resource endpoints
- Use plural nouns for collections
- Use kebab-case for URLs
- Nest resources to indicate relationships

```http
# Good
GET /api/users
GET /api/users/123
GET /api/users/123/orders

# Avoid
GET /api/getUsers
GET /api/user/123
GET /api/getUserOrders/123
```

## HTTP Methods

- `GET`: Retrieve resource(s)
- `POST`: Create a new resource
- `PUT`: Replace a resource completely
- `PATCH`: Update a resource partially
- `DELETE`: Remove a resource

## HTTP Status Codes

- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `204 No Content`: Request succeeded, no content to return
- `400 Bad Request`: Invalid request format/parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation errors
- `500 Internal Server Error`: Server-side error

## Request & Response Format

- Use JSON for request and response bodies
- Use camelCase for property names
- Include a root-level data property for the main resource
- Include metadata properties as needed (pagination, etc.)

```json
// Response for GET /api/users?page=1
{
  "data": [
    {
      "id": "123",
      "firstName": "John",
      "lastName": "Doe",
      "email": "john.doe@example.com"
    },
    // More users...
  ],
  "meta": {
    "totalCount": 42,
    "page": 1,
    "pageSize": 10,
    "totalPages": 5
  }
}
```

## Error Response Format

- Consistent error structure
- Include error code, message, and details
- Provide actionable information

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      },
      {
        "field": "password",
        "message": "Must be at least 8 characters"
      }
    ]
  }
}
```

## Versioning

- Include version in URL path
- Support at least one previous version
- Deprecate old versions with clear notices

```http
/api/v1/users
/api/v2/users
```

## Filtering, Sorting, and Pagination

- Use query parameters for filtering
  - `GET /api/users?role=admin`
- Support multiple filters
  - `GET /api/users?role=admin&status=active`
- Use query parameters for sorting
  - `GET /api/users?sort=lastName`
  - `GET /api/users?sort=-createdAt` (descending)
- Implement pagination with limit/offset or page/pageSize
  - `GET /api/users?limit=10&offset=20`
  - `GET /api/users?page=2&pageSize=10`

## Authentication

- Use OAuth 2.0 or JWT for authentication
- Send tokens in Authorization header
- Include expiration time in tokens
- Provide refresh token mechanism
