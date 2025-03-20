<!--
Document: Full-Stack Application Example
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Bayat Full-Stack Application Example

This is a complete full-stack application example that demonstrates end-to-end architecture, deployment, and CI/CD practices following Bayat's conventions.

## Tech Stack

### Frontend

- React 18
- TypeScript
- Redux Toolkit for state management
- React Router for routing
- Material UI for components
- Jest and React Testing Library for testing

### Backend

- Node.js with Express
- TypeScript
- PostgreSQL database
- Prisma ORM
- JWT authentication
- Jest for testing

### DevOps

- Docker and Docker Compose
- GitHub Actions for CI/CD
- Terraform for infrastructure
- AWS for deployment

## Features Demonstrated

- Monorepo structure with shared types
- API contract testing
- Authentication and authorization
- Environment configuration
- Database migrations
- Deployment pipeline
- Logging and monitoring
- End-to-end testing

## Getting Started

```bash
# Clone the repository
git clone https://github.com/your-org/fullstack-example.git

# Navigate to the project directory
cd fullstack-example

# Install dependencies
npm install

# Start the development environment
npm run dev
```

## Dependency Management

This project uses npm workspaces to manage dependencies across multiple packages. We maintain current dependencies to avoid using deprecated packages. Key aspects:

- All workspaces use modern, non-deprecated package versions
- The root `package.json` includes overrides for common transitive dependencies
- E2E testing is implemented with Playwright
- A postinstall script handles deprecated packages like `rimraf`

If you encounter deprecation warnings when installing, check the root `package.json` to see if overrides need to be updated.

## Project Structure

```plaintext
full-stack/
├── client/             # Frontend React application
├── server/             # Backend Express API
├── shared/             # Shared types and utilities
├── e2e/                # End-to-end tests with Playwright
├── .github/            # GitHub Actions workflows
├── docker-compose.yml  # Development environment setup
└── README.md           # This file
```

## Conventions Demonstrated

- [API Design](../../docs/architecture/api-design.md)
- [Frontend Architecture](../../docs/architecture/frontend.md)
- [Backend Architecture](../../docs/architecture/backend.md)
- [Testing Strategy](../../docs/quality/testing.md)
- [CI/CD Pipeline](../../docs/quality/ci-cd.md)
- [Deployment](../../docs/devops/deployment.md)

## Learning from this Example

This example is designed to show how different Bayat conventions work together in a real-world application. Key areas to focus on:

1. **API Contract**: See how the frontend and backend share types and ensure API consistency
2. **Authentication Flow**: Study the implementation of secure authentication
3. **State Management**: Examine how application state is organized and managed
4. **Testing Strategy**: Look at the different types of tests and how they work together
5. **Deployment Pipeline**: Understand the CI/CD process from commit to production

## Contributing

Please see the [Contributing Guide](../../CONTRIBUTING.md) for information on how to contribute to this example.
