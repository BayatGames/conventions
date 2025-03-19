<!--
Document: GraphQL Development Standards
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# GraphQL Development Standards

This document outlines Bayat's standards and best practices for GraphQL API development.

## Table of Contents

- [Introduction](#introduction)
- [Schema Design](#schema-design)
- [Resolvers](#resolvers)
- [Authentication & Authorization](#authentication--authorization)
- [Performance](#performance)
- [Error Handling](#error-handling)
- [Versioning](#versioning)
- [Testing](#testing)
- [Security](#security)
- [Tools & Libraries](#tools--libraries)
- [Code Organization](#code-organization)
- [Documentation](#documentation)
- [Monitoring & Observability](#monitoring--observability)

## Introduction

GraphQL provides a flexible and efficient alternative to REST APIs by allowing clients to request exactly the data they need. This document establishes standards for GraphQL implementation across Bayat projects.

## Schema Design

### Naming Conventions

- Use PascalCase for type names
- Use camelCase for field names and arguments
- Use ALL_CAPS for enum values
- Use descriptive names that reflect domain concepts

```graphql
type User {
  id: ID!
  firstName: String!
  lastName: String!
  emailAddress: String!
  userRole: UserRole!
}

enum UserRole {
  ADMIN
  EDITOR
  VIEWER
}
```

### Type Definitions

- Make fields non-nullable (`!`) unless there's a specific reason they should be nullable
- Prefer object references over ID references when objects are frequently accessed together
- Use custom scalar types for specialized data (e.g., `DateTime`, `Email`, `URL`)
- Include descriptions for all types and fields

```graphql
"""
A user account in the system.
"""
type User {
  """
  Unique identifier for the user.
  """
  id: ID!
  
  """
  User's display name.
  """
  displayName: String!
  
  """
  When the user account was created.
  """
  createdAt: DateTime!
}
```

### Schema Organization

- Group related types and operations together
- Split schema into logical modules by domain
- Use interfaces and unions for polymorphic types
- Implement pagination for list responses using Relay-style connections

```graphql
interface Node {
  id: ID!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type UserEdge {
  cursor: String!
  node: User!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}
```

## Resolvers

### Resolver Structure

- Follow a consistent resolver structure across the codebase
- Implement the data loader pattern to avoid N+1 query problems
- Keep resolvers focused on data fetching, not business logic
- Move complex business logic to separate service classes

```typescript
// User resolver example
const resolvers = {
  Query: {
    user: (_, { id }, { dataSources }) => 
      dataSources.userService.getUserById(id),
      
    users: (_, { first, after }, { dataSources }) => 
      dataSources.userService.getUsers({ first, after })
  },
  
  User: {
    posts: (parent, args, { dataSources }) => 
      dataSources.postService.getPostsByUserId(parent.id, args)
  }
};
```

### Performance Considerations

- Use DataLoader for batching and caching database queries
- Implement query complexity analysis to prevent resource-intensive queries
- Consider persisted queries for production environments
- Apply appropriate field-level resolver caching

```typescript
// DataLoader implementation
const userLoader = new DataLoader(async (ids) => {
  const users = await UserModel.findAll({ where: { id: ids } });
  return ids.map(id => users.find(user => user.id === id) || null);
});

// In resolver
const user = (_, { id }, { loaders }) => loaders.users.load(id);
```

## Authentication & Authorization

- Implement authentication through context objects
- Apply authorization at both the field and resolver levels
- Use directive-based permission controls for declarative authorization
- Never expose sensitive data through GraphQL

```graphql
type Query {
  publicData: PublicData!
  sensitiveData: SensitiveData! @requiresAuth
  adminData: AdminData! @requiresRole(role: ADMIN)
}
```

```typescript
// Authorization in resolver
const resolvers = {
  Query: {
    sensitiveData: (_, __, { user }) => {
      if (!user) throw new AuthenticationError('You must be logged in');
      return getSensitiveData(user.id);
    }
  }
};
```

## Error Handling

- Use standard GraphQL error format
- Include appropriate error codes and user-friendly messages
- Avoid exposing implementation details or sensitive info in errors
- Log detailed error information for debugging

```typescript
try {
  // Operation that might fail
} catch (error) {
  console.error('Detailed internal error:', error);
  
  throw new ApolloError(
    'A problem occurred while processing your request', 
    'SERVICE_ERROR',
    { 
      publicData: error.publicContext,
      httpStatus: 500
    }
  );
}
```

## Versioning

- Prefer schema evolution over versioning
- Add new fields and types without removing old ones
- Use deprecation to mark fields scheduled for removal
- Document when deprecated fields will be removed

```graphql
type User {
  id: ID!
  name: String! @deprecated(reason: "Use firstName and lastName instead")
  firstName: String!
  lastName: String!
}
```

## Testing

- Write unit tests for resolvers and business logic
- Implement integration tests for complete GraphQL operations
- Use schema validation tests to ensure schema integrity
- Create performance tests for critical queries

```typescript
describe('User queries', () => {
  it('should return user by ID', async () => {
    const result = await graphql({
      schema,
      source: `
        query GetUser($id: ID!) {
          user(id: $id) {
            id
            firstName
            lastName
          }
        }
      `,
      variableValues: { id: 'user-1' }
    });
    
    expect(result.errors).toBeUndefined();
    expect(result.data.user).toEqual({
      id: 'user-1',
      firstName: 'John',
      lastName: 'Doe'
    });
  });
});
```

## Security

- Implement query depth limitation
- Use query complexity analysis to prevent DoS attacks
- Apply rate limiting for GraphQL operations
- Validate incoming variables and arguments
- Consider persisted queries in production

```typescript
// Apollo Server configuration
const server = new ApolloServer({
  schema,
  validationRules: [
    depthLimitRule(7),
    createComplexityLimitRule(1000),
  ],
  plugins: [
    responseCachePlugin(),
    ApolloServerPluginLandingPageGraphQLPlayground()
  ]
});
```

## Tools & Libraries

### Recommended Libraries

- **Node.js**: Apollo Server, GraphQL Yoga, Mercurius
- **TypeScript**: TypeGraphQL, GraphQL Nexus, Pothos
- **.NET**: Hot Chocolate, GraphQL .NET
- **Java/Kotlin**: DGS Framework, GraphQL Java
- **Python**: Strawberry, Ariadne, Graphene
- **Ruby**: GraphQL Ruby
- **PHP**: Lighthouse, GraphQL PHP

### Code Generation

Use code generation to ensure type safety between schema and resolvers:

```bash
# GraphQL Code Generator example
yarn graphql-codegen --config codegen.yml
```

Sample `codegen.yml`:

```yaml
schema: src/schema/**/*.graphql
documents: src/operations/**/*.graphql
generates:
  src/generated/graphql.ts:
    plugins:
      - typescript
      - typescript-resolvers
      - typescript-operations
```

## Code Organization

### Folder Structure

```plaintext
/graphql
  /schema
    schema.graphql          # Main schema file or entry point
    /types                  # GraphQL type definitions
      user.graphql
      post.graphql
    /inputs                 # Input types
    /enums                  # Enum definitions
  /resolvers
    /queries                # Query resolvers
    /mutations              # Mutation resolvers
    /subscriptions          # Subscription resolvers
    /types                  # Type resolvers
  /directives               # Custom directive implementations
  /scalars                  # Custom scalar implementations
  /dataloaders              # DataLoader implementations
  /utils                    # Utility functions for GraphQL
/services                   # Business logic services
  userService.js
  postService.js
/models                     # Data models
  user.js
  post.js
```

## Documentation

- Document schema using GraphQL's built-in description syntax
- Provide examples for complex queries and mutations
- Use tools like GraphQL Playground or GraphiQL in development
- Generate schema documentation for developer reference

## Monitoring & Observability

- Implement tracing for GraphQL operations
- Monitor resolver performance and query execution times
- Track error rates and types
- Set up alerts for problematic patterns

```typescript
// Apollo Server with tracing
const server = new ApolloServer({
  schema,
  plugins: [
    ApolloServerPluginUsageReporting({
      sendVariableValues: { all: true },
      sendHeaders: { all: true },
      generateClientInfo: ({ request }) => {
        return {
          clientName: request.http.headers.get('client-name') || 'Unknown Client',
          clientVersion: request.http.headers.get('client-version') || 'Unknown Version',
        };
      },
    }),
  ],
});
```

## Framework-Specific Standards

### Apollo Server (Node.js)

- Implement custom plugins for cross-cutting concerns
- Use Apollo's cache control capabilities
- Configure appropriate response caching
- Structure resolvers consistently

### GraphQL in React Applications

- Use Apollo Client or Relay for state management
- Implement proper caching strategies
- Structure queries by component needs
- Handle loading and error states consistently

```jsx
// React component with Apollo Client
function UserProfile({ userId }) {
  const { loading, error, data } = useQuery(GET_USER, {
    variables: { id: userId },
    fetchPolicy: 'cache-first'
  });

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorDisplay error={error} />;

  return (
    <div>
      <h1>{data.user.firstName} {data.user.lastName}</h1>
      <UserDetails user={data.user} />
    </div>
  );
}
```

### GraphQL with Mobile Clients

- Implement offline support through local caching
- Consider bandwidth usage with selective queries
- Handle network connectivity changes gracefully
- Use optimistic UI updates for mutations
