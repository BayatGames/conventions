<!--
Document: Project Templates and Starter Kits
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Project Templates and Starter Kits

This document outlines the standard project templates and starter kits available for all Bayat projects.

## Purpose

Project templates and starter kits serve to:

- Accelerate project setup and onboarding
- Enforce standards and best practices
- Provide consistent structure across projects
- Include pre-configured tools and dependencies
- Reduce decision fatigue for developers

## Available Templates

### Web Frontend Templates

#### React Template

**Repository:** `github.com/bayat/templates/react-starter`

**Features:**
- React 18+ with TypeScript
- State management with Redux Toolkit
- Routing with React Router
- Component library integration (MUI/Chakra UI)
- Jest and React Testing Library
- ESLint and Prettier configuration
- Husky pre-commit hooks
- GitHub Actions CI/CD workflows
- Storybook for component documentation
- Internationalization setup
- Accessibility testing configuration

**Usage:**
```bash
npx create-bayat-app my-app --template react
```

#### Angular Template

**Repository:** `github.com/bayat/templates/angular-starter`

**Features:**
- Angular 15+ with TypeScript
- NgRx for state management
- Angular Material components
- Jasmine and Karma test setup
- ESLint and Prettier configuration
- Husky pre-commit hooks
- GitHub Actions CI/CD workflows
- Internationalization with ngx-translate
- Responsive design foundation

**Usage:**
```bash
npx create-bayat-app my-app --template angular
```

#### Vue Template

**Repository:** `github.com/bayat/templates/vue-starter`

**Features:**
- Vue 3 with Composition API
- TypeScript integration
- Pinia for state management
- Vue Router
- Vite build system
- Vitest and Testing Library
- ESLint and Prettier configuration
- Husky pre-commit hooks
- GitHub Actions CI/CD workflows
- i18n internationalization

**Usage:**
```bash
npx create-bayat-app my-app --template vue
```

### Backend Templates

#### Node.js API Template

**Repository:** `github.com/bayat/templates/nodejs-api`

**Features:**
- Express.js/NestJS framework
- TypeScript configuration
- MongoDB/PostgreSQL database setup
- Authentication with JWT
- API documentation with Swagger
- Unit and integration testing with Jest
- Docker configuration
- GitHub Actions CI/CD workflows
- Logging with Winston
- Error handling middleware
- Rate limiting and security headers

**Usage:**
```bash
npx create-bayat-app my-api --template nodejs-api
```

#### ASP.NET Core API Template

**Repository:** `github.com/bayat/templates/aspnet-api`

**Features:**
- ASP.NET Core 7+
- Entity Framework Core
- Identity for authentication
- Swagger/OpenAPI documentation
- XUnit testing
- Docker configuration
- GitHub Actions CI/CD workflows
- Logging with Serilog
- HealthChecks
- API versioning

**Usage:**
```bash
dotnet new bayat-webapi -n MyApi
```

#### Django API Template

**Repository:** `github.com/bayat/templates/django-api`

**Features:**
- Django 4+ with Django REST Framework
- PostgreSQL configuration
- JWT authentication
- API documentation with drf-spectacular
- Testing with pytest
- Docker configuration
- GitHub Actions CI/CD workflows
- Celery for async tasks
- Django Debug Toolbar
- Logging configuration

**Usage:**
```bash
pipx run bayat-cli create-project --template django-api my_project
```

### Mobile Templates

#### React Native Template

**Repository:** `github.com/bayat/templates/react-native`

**Features:**
- React Native with TypeScript
- Navigation with React Navigation
- State management with Redux Toolkit
- Styled components
- Testing with Jest
- ESLint and Prettier configuration
- Husky pre-commit hooks
- Fastlane for deployment
- Internationalization
- Dark mode support

**Usage:**
```bash
npx react-native init MyApp --template bayat-react-native-template
```

#### Flutter Template

**Repository:** `github.com/bayat/templates/flutter`

**Features:**
- Flutter 3+ with Dart
- State management with Provider/Bloc
- Navigation 2.0
- Material Design 3/Cupertino components
- Unit and widget testing
- Firebase integration
- Internationalization
- Dark mode support
- CI/CD with GitHub Actions

**Usage:**
```bash
flutter create --template=bayat_flutter my_app
```

### Full-Stack Templates

#### MERN Stack Template

**Repository:** `github.com/bayat/templates/mern-stack`

**Features:**
- MongoDB, Express.js, React, Node.js
- TypeScript throughout
- Authentication system
- Form validation
- API integration
- Testing for both frontend and backend
- Docker Compose configuration
- GitHub Actions CI/CD workflows

**Usage:**
```bash
npx create-bayat-app my-app --template mern
```

#### .NET + Angular Template

**Repository:** `github.com/bayat/templates/dotnet-angular`

**Features:**
- ASP.NET Core backend
- Angular frontend
- SQL Server database
- Authentication with Identity
- Entity Framework Core
- API documentation
- Testing for both frontend and backend
- Docker Compose configuration

**Usage:**
```bash
dotnet new bayat-fullstack -n MyApp
```

### Game Development Templates

#### Unity Template

**Repository:** `github.com/bayat/templates/unity-starter`

**Features:**
- Unity project structure
- Common utility scripts
- CI/CD setup
- Testing framework
- Input system configuration
- Scene management
- Asset pipeline setup

**Usage:**
Downloadable from internal package registry

#### Unreal Template

**Repository:** `github.com/bayat/templates/unreal-starter`

**Features:**
- Unreal Engine project structure
- Blueprint organization
- C++ code standards
- Common gameplay framework
- Testing setup
- Build configuration

**Usage:**
Downloadable from internal package registry

## Template Components

All templates include the following standard components:

### Documentation
- `README.md` with setup instructions
- `CONTRIBUTING.md` with contribution guidelines
- `CHANGELOG.md` for version history
- `LICENSE` file with appropriate license

### Configuration Files
- `.gitignore` with appropriate exclusions
- `.editorconfig` for consistent editor settings
- Language-specific linting configuration
- CI/CD configuration files

### Project Structure
- Consistent folder organization
- Clear separation of concerns
- Standard naming conventions
- Environment configuration

### Security
- Dependency vulnerability scanning
- Secure defaults
- Environment variable templates
- Authentication boilerplate where applicable

## Using Templates

### Installation

Each template has its own installation method, typically using the project's standard CLI tools.

### Customization

After generating a project from a template:

1. Update project metadata in configuration files
2. Review and adjust dependencies as needed
3. Customize environment variables
4. Review and adjust CI/CD workflows
5. Update README with project-specific information

### Template Versioning

Templates follow semantic versioning:
- **Major versions**: Breaking changes
- **Minor versions**: New features, non-breaking changes
- **Patch versions**: Bug fixes and small updates

## Contributing to Templates

To suggest improvements to templates:

1. Create an issue in the template repository
2. Discuss the proposed changes
3. Submit a pull request
4. Ensure all tests pass
5. Update documentation

## Template Maintenance

Templates are maintained by the Platform Team and are updated:
- Monthly for security patches
- Quarterly for minor updates
- Bi-annually for major updates

## Support

For help with templates:
- Check template-specific documentation
- Contact the Platform Team via Slack (#platform-support)
- Submit issues to the appropriate template repository 