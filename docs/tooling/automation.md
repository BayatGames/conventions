# Tooling and Automation Standards

This document outlines the standard tools and automation practices across all Bayat projects.

## Development Tools

### Code Editors and IDEs

| Tool | Primary Use Case | Standard Configuration |
|------|-----------------|------------------------|
| Visual Studio Code | Web, JavaScript, TypeScript, Python | \1https://github.com/bayat/dev-tools/vscode-config) |
| Visual Studio | .NET, C# | \1https://github.com/bayat/dev-tools/vs-config) |
| JetBrains IDEs | Language-specific development | \1https://github.com/bayat/dev-tools/jetbrains-config) |
| Xcode | iOS, macOS | \1https://github.com/bayat/dev-tools/xcode-config) |
| Android Studio | Android | \1https://github.com/bayat/dev-tools/android-studio-config) |

### Command Line Tools

| Tool | Purpose | Installation |
|------|---------|-------------|
| Git | Version control | Standard package managers |
| Docker | Containerization | [Docker Desktop](https://www.docker.com/products/docker-desktop) |
| Node.js | JavaScript runtime | [nvm](https://github.com/nvm-sh/nvm) |
| Python | Python runtime | [pyenv](https://github.com/pyenv/pyenv) |
| .NET SDK | .NET development | [.NET Downloads](https://dotnet.microsoft.com/download) |
| AWS CLI | AWS management | `pip install awscli` |
| Azure CLI | Azure management | [Installation Guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) |
| kubectl | Kubernetes management | [Installation Guide](https://kubernetes.io/docs/tasks/tools/) |
| Terraform | Infrastructure as Code | [Installation Guide](https://learn.hashicorp.com/tutorials/terraform/install-cli) |

## Linting and Formatting Tools

### JavaScript/TypeScript

| Tool | Purpose | Configuration |
|------|---------|--------------|
| ESLint | Code linting | \1https://github.com/bayat/dev-tools/eslint-config) |
| Prettier | Code formatting | \1https://github.com/bayat/dev-tools/prettier-config) |
| TypeScript | Type checking | \1https://github.com/bayat/dev-tools/tsconfig) |

### Python

| Tool | Purpose | Configuration |
|------|---------|--------------|
| Flake8 | Code linting | \1https://github.com/bayat/dev-tools/flake8-config) |
| Black | Code formatting | \1https://github.com/bayat/dev-tools/black-config) |
| mypy | Type checking | \1https://github.com/bayat/dev-tools/mypy-config) |

### C#

| Tool | Purpose | Configuration |
|------|---------|--------------|
| StyleCop | Code analysis | \1https://github.com/bayat/dev-tools/stylecop-config) |
| .editorconfig | Code formatting | \1https://github.com/bayat/dev-tools/editorconfig) |

### Java

| Tool | Purpose | Configuration |
|------|---------|--------------|
| Checkstyle | Code style enforcement | \1https://github.com/bayat/dev-tools/checkstyle-config) |
| PMD | Code analysis | \1https://github.com/bayat/dev-tools/pmd-config) |

## Git Hooks and Automation

### Pre-commit Hooks

Standard pre-commit hooks for all projects:

- Linting check
- Formatting check
- Type checking
- Unit test execution (fast tests only)
- Secret detection
- Conventional commit message enforcement

**Configuration:** \1https://github.com/bayat/dev-tools/pre-commit-config)

### Commit Message Validation

All commit messages must follow the Conventional Commits specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- feat: A new feature
- fix: A bug fix
- docs: Documentation changes
- style: Code style changes (whitespace, formatting)
- refactor: Code refactoring without functionality changes
- perf: Performance improvements
- test: Adding or correcting tests
- build: Build system changes
- ci: CI configuration changes
- chore: Routine tasks, maintenance

**Tool:** [commitlint](https://github.com/conventional-changelog/commitlint)
**Configuration:** \1https://github.com/bayat/dev-tools/commitlint-config)

## Continuous Integration

### GitHub Actions

Standard GitHub Actions workflows for all projects:

| Workflow | Purpose | Configuration |
|----------|---------|--------------|
| CI | Build, lint, test | \1https://github.com/bayat/dev-tools/github-actions/ci.yml) |
| Dependency Review | Security check | \1https://github.com/bayat/dev-tools/github-actions/dependency-review.yml) |
| CodeQL | Code security analysis | \1https://github.com/bayat/dev-tools/github-actions/codeql.yml) |
| Release | Create releases | \1https://github.com/bayat/dev-tools/github-actions/release.yml) |

### Azure DevOps Pipelines

Standard Azure DevOps pipeline templates:

| Pipeline | Purpose | Configuration |
|----------|---------|--------------|
| CI | Build, lint, test | \1https://github.com/bayat/dev-tools/azure-pipelines/ci.yml) |
| CD | Deployment | \1https://github.com/bayat/dev-tools/azure-pipelines/cd.yml) |
| PR Validation | PR checks | \1https://github.com/bayat/dev-tools/azure-pipelines/pr.yml) |

## Testing Frameworks

### JavaScript/TypeScript

| Framework | Purpose | Configuration |
|-----------|---------|--------------|
| Jest | Unit testing | \1https://github.com/bayat/dev-tools/jest-config) |
| Cypress | E2E testing | \1https://github.com/bayat/dev-tools/cypress-config) |
| Testing Library | Component testing | \1https://github.com/bayat/dev-tools/testing-library-config) |

### Python

| Framework | Purpose | Configuration |
|-----------|---------|--------------|
| pytest | Testing | \1https://github.com/bayat/dev-tools/pytest-config) |
| Selenium | Browser testing | \1https://github.com/bayat/dev-tools/selenium-config) |

### .NET

| Framework | Purpose | Configuration |
|-----------|---------|--------------|
| xUnit | Unit testing | \1https://github.com/bayat/dev-tools/xunit-config) |
| Playwright | E2E testing | \1https://github.com/bayat/dev-tools/playwright-config) |

## Code Quality Tools

| Tool | Purpose | Integration |
|------|---------|------------|
| SonarQube | Code quality analysis | \1https://github.com/bayat/dev-tools/sonarqube-integration) |
| CodeClimate | Code quality checks | \1https://github.com/bayat/dev-tools/codeclimate-integration) |
| WhiteSource | Dependency scanning | \1https://github.com/bayat/dev-tools/whitesource-integration) |
| Snyk | Security scanning | \1https://github.com/bayat/dev-tools/snyk-integration) |

## Monitoring and Observability

| Tool | Purpose | Integration |
|------|---------|------------|
| Prometheus | Metrics collection | \1https://github.com/bayat/dev-tools/prometheus-integration) |
| Grafana | Metrics visualization | \1https://github.com/bayat/dev-tools/grafana-dashboards) |
| ELK Stack | Logging | \1https://github.com/bayat/dev-tools/elk-config) |
| Jaeger | Distributed tracing | \1https://github.com/bayat/dev-tools/jaeger-integration) |

## Documentation Generation

| Tool | Purpose | Configuration |
|------|---------|--------------|
| Swagger/OpenAPI | API documentation | \1https://github.com/bayat/dev-tools/openapi-config) |
| JSDoc | JavaScript documentation | \1https://github.com/bayat/dev-tools/jsdoc-config) |
| Sphinx | Python documentation | \1https://github.com/bayat/dev-tools/sphinx-config) |
| DocFX | .NET documentation | \1https://github.com/bayat/dev-tools/docfx-config) |

## Deployment and Infrastructure

| Tool | Purpose | Templates |
|------|---------|----------|
| Terraform | Infrastructure as Code | \1https://github.com/bayat/dev-tools/terraform-modules) |
| Helm | Kubernetes packaging | \1https://github.com/bayat/dev-tools/helm-charts) |
| Docker | Containerization | \1https://github.com/bayat/dev-tools/dockerfiles) |
| AWS CDK | AWS infrastructure | \1https://github.com/bayat/dev-tools/aws-cdk-constructs) |

## Tool Configuration Files

### .editorconfig

```ini
root = true

[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.{js,ts,jsx,tsx,css,scss,json,html}]
indent_size = 2

[*.{py,java,cs,cpp,h}]
indent_size = 4

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

### .gitignore

Standardized `.gitignore` files for different project types are available at:
\1https://github.com/bayat/dev-tools/gitignore)

### package.json Scripts

Standard npm scripts for JavaScript/TypeScript projects:

```json
{
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "lint": "eslint --ext .js,.jsx,.ts,.tsx src",
    "lint:fix": "eslint --ext .js,.jsx,.ts,.tsx src --fix",
    "format": "prettier --write \"src/**/*.{js,jsx,ts,tsx,css,scss,json}\"",
    "format:check": "prettier --check \"src/**/*.{js,jsx,ts,tsx,css,scss,json}\"",
    "typecheck": "tsc --noEmit",
    "prepare": "husky install"
  }
}
```

## Internal Tool Development

Guidelines for developing internal tools:

1. Use the same standards as product code
2. Include comprehensive documentation
3. Provide example usage
4. Include tests
5. Maintain semantic versioning
6. Publish to internal package registry
7. Track usage and gather feedback

## Tool Selection and Adoption Process

For adopting new tools:

1. **Research**: Evaluate at least three alternatives
2. **Pilot**: Test with a small project
3. **Review**: Gather feedback from the pilot
4. **Decision**: Make a formal tool selection decision
5. **Documentation**: Create integration and usage guidelines
6. **Training**: Provide training to the team
7. **Rollout**: Gradually adopt across projects

## Tool Evaluation Criteria

- Alignment with technology stack
- Active maintenance and community support
- Documentation quality
- Learning curve
- Integration capabilities
- Licensing and cost
- Performance impact
- Security considerations 