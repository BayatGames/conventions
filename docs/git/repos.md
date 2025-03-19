# Git Repositories Conventions

This document outlines Bayat's repository conventions, guidelines, and standards. It provides a comprehensive framework for repository management that integrates with the \1\2) and \1\2) to ensure consistency across all project types.

## Introduction

Well-structured repositories are fundamental to efficient development workflows. This document establishes standards for:

- Repository naming and organization
- Repository configuration and setup
- Access control and collaboration workflows
- Project-specific repository considerations
- Documentation requirements

Following these guidelines ensures consistent repository management across all Bayat teams and project types.

## Repository Naming Conventions

### General Rules

All repository names should:

- Use lowercase letters
- Use hyphens (`-`) to separate words (kebab-case)
- Be descriptive but concise
- Avoid abbreviations unless universally understood
- Avoid version numbers in the repository name
- Start with the appropriate prefix for the repository type

### Repository Type Prefixes

Use the following prefixes to clearly indicate the repository type:

- **game-**: For game projects
  - Example: `game-space-adventure`

- **web-**: For web applications and sites
  - Example: `web-dashboard-app`

- **app-**: For mobile or desktop applications
  - Example: `app-inventory-manager`

- **api-**: For backend services and APIs
  - Example: `api-authentication-service`

- **lib-**: For libraries and packages
  - Example: `lib-data-structures`

- **tool-**: For development tools
  - Example: `tool-asset-optimizer`

- **prototype-**: For experimental projects
  - Example: `prototype-ar-navigation`

- **docs-**: For documentation, conventions, and guidelines
  - Example: `docs-code-conventions`, `docs-style-guide`

- **config-**: For shared configuration repositories
  - Example: `config-eslint-rules`, `config-ci-templates`

- **infra-**: For infrastructure and DevOps code
  - Example: `infra-kubernetes-setup`, `infra-aws-terraform`

- **template-**: For starter templates and boilerplates
  - Example: `template-react-app`, `template-unity-game`

- **training-**: For learning materials and tutorials
  - Example: `training-onboarding`, `training-advanced-unity`

- **data-**: For datasets and data processing projects
  - Example: `data-analytics-pipeline`, `data-game-metrics`

- **research-**: For research projects, experiments, and studies
  - Example: `research-ai-optimization`, `research-player-behavior`

- **plugin-**: For plugin and extension development
  - Example: `plugin-unity-editor`, `plugin-vscode-formatter`

- **sandbox-**: For experimental code exploration (less structured than prototypes)
  - Example: `sandbox-shader-experiments`, `sandbox-physics-testing`

- **demo-**: For demonstration and sample projects
  - Example: `demo-gameplay-mechanics`, `demo-api-usage`

- **workshop-**: For hands-on workshop and hackathon projects
  - Example: `workshop-multiplayer-development`, `workshop-shader-graph`

- **marketing-**: For marketing-related code and assets
  - Example: `marketing-company-website`, `marketing-campaign-assets`

- **mono-**: For monorepo projects containing multiple related components
  - Example: `mono-frontend-apps`, `mono-game-framework`

- **security-**: For security tools, tests, and configurations
  - Example: `security-penetration-tests`, `security-compliance-tools`

### Internal vs. Public Repositories

- **Internal repositories** should follow the standard naming convention with appropriate prefixes
- **Public repositories** intended for community use may omit prefixes and use more marketing-friendly names
  - Example: `bayat-unity-utilities` instead of `lib-unity-utilities`

## Repository Structure

### Root-Level Files

Every repository should include these files at the root level:

- **README.md**: Project overview, setup instructions, and basic documentation
- **LICENSE**: The project's license file
- **.gitignore**: Appropriate for the project type
- **.gitattributes**: For handling line endings and large files
- **CHANGELOG.md**: Document version history and changes
- **CONTRIBUTING.md**: For public or multi-team repositories

### Standard Directories

Depending on project type, repositories should include appropriate standard directories:

#### Common Directories (All Projects)

- **docs/**: Detailed documentation
- **scripts/**: Utility scripts, build scripts, etc.
- **tests/**: Test files and fixtures
- **.github/**: GitHub-specific configurations (workflows, issue templates)

#### Game Projects

##### General Game Project Structure

- **assets/**: Game assets (models, textures, sounds)
- **src/**: Source code
- **levels/**: Level data and configurations
- **config/**: Game configuration files
- **tools/**: Custom tools and utilities for development
- **third-party/**: Third-party libraries and dependencies

##### Unity Projects

- **Assets/**: Unity assets folder (Unity-specific)
  - **Scripts/**: C# scripts
  - **Prefabs/**: Prefabricated game objects
  - **Scenes/**: Unity scenes
  - **Materials/**: Material assets
  - **Models/**: 3D models
  - **Textures/**: Texture files
  - **Audio/**: Audio files
  - **Animations/**: Animation files
  - **Resources/**: Runtime-loadable resources
  - **StreamingAssets/**: Platform-specific assets
  - **Plugins/**: Native plugins and extensions
- **ProjectSettings/**: Unity project settings
- **Packages/**: Unity package manager dependencies
- **UserSettings/**: User-specific settings (typically in .gitignore)

##### Unreal Engine Projects

- **Content/**: Unreal content folder
  - **Characters/**: Character assets
  - **Environments/**: Environment assets
  - **UI/**: User interface assets
  - **Materials/**: Material assets
  - **Blueprints/**: Blueprint assets
  - **Effects/**: Visual effects
  - **Sound/**: Audio files
- **Source/**: C++ source code
  - **ProjectName/**: Main project code
  - **ProjectNameEditor/**: Editor-specific code
- **Config/**: Configuration files
- **Plugins/**: Custom and third-party plugins
- **Binaries/**: Compiled binaries (typically in .gitignore)
- **Intermediate/**: Intermediate build files (typically in .gitignore)
- **Saved/**: Auto-saved content (typically in .gitignore)

#### Web/Mobile Projects

##### General Web/Mobile Project Structure

- **src/**: Source code
- **public/**: Static assets
- **components/**: Reusable UI components
- **styles/**: CSS/styling files
- **assets/**: Images, fonts, etc.
- **config/**: Configuration files
- **utils/**: Utility functions
- **hooks/**: Custom hooks (React)
- **services/**: API services and data fetching
- **types/**: Type definitions

##### React Projects

- **src/**
  - **components/**: React components
    - **common/**: Shared components
    - **layouts/**: Layout components
    - **features/**: Feature-specific components
  - **pages/**: Page components
  - **hooks/**: Custom React hooks
  - **context/**: React context providers
  - **redux/**: Redux state management (if applicable)
    - **actions/**: Redux actions
    - **reducers/**: Redux reducers
    - **selectors/**: Redux selectors
  - **api/**: API integration
  - **utils/**: Utility functions
  - **styles/**: CSS or styling solutions
  - **assets/**: Static assets
- **public/**: Static files
- **config/**: Configuration files

##### Angular Projects

- **src/**
  - **app/**: Application code
    - **components/**: Angular components
    - **services/**: Angular services
    - **directives/**: Custom directives
    - **pipes/**: Custom pipes
    - **models/**: Data models/interfaces
    - **guards/**: Route guards
    - **interceptors/**: HTTP interceptors
  - **assets/**: Static assets
  - **environments/**: Environment configurations
- **e2e/**: End-to-end tests

##### Mobile (React Native) Projects

- **src/**
  - **components/**: React Native components
  - **screens/**: Screen components
  - **navigation/**: Navigation configuration
  - **services/**: API and other services
  - **store/**: State management
  - **utils/**: Utility functions
  - **assets/**: Assets (images, fonts)
  - **hooks/**: Custom hooks
  - **constants/**: App constants
- **android/**: Android-specific code
- **ios/**: iOS-specific code

##### Flutter Projects

- **lib/**
  - **screens/**: Screen widgets
  - **widgets/**: Reusable widgets
  - **models/**: Data models
  - **services/**: Services and API clients
  - **providers/**: State providers
  - **utils/**: Utility functions
  - **constants/**: App constants
  - **routes/**: Navigation routes
- **assets/**: Static assets
- **android/**: Android-specific code
- **ios/**: iOS-specific code
- **web/**: Web-specific code (if applicable)
- **test/**: Test files

#### Backend Projects

##### General Backend Structure

- **src/**: Source code
- **config/**: Configuration files
- **controllers/**: Request handlers
- **models/**: Data models
- **services/**: Business logic
- **middleware/**: Middleware functions
- **utils/**: Utility functions
- **routes/**: API route definitions
- **tests/**: Test files

##### Node.js/Express Projects

- **src/**
  - **controllers/**: Route controllers
  - **models/**: Data models
  - **routes/**: Express routes
  - **middleware/**: Express middleware
  - **services/**: Business logic
  - **utils/**: Utility functions
  - **config/**: Configuration
  - **db/**: Database setup and migrations
- **tests/**: Test files

##### Django Projects

- **project_name/**: Project root
  - **settings/**: Django settings
  - **urls.py**: URL routing
- **apps/**: Django apps
  - **app_name/**
    - **models.py**: Data models
    - **views.py**: View functions/classes
    - **serializers.py**: API serializers
    - **urls.py**: URL patterns
    - **admin.py**: Admin configuration
    - **tests.py**: Tests
- **static/**: Static files
- **media/**: User-uploaded files
- **templates/**: HTML templates

#### Libraries/Packages

##### General Library Structure

- **src/**: Source code
- **examples/**: Example usage
- **dist/**: Compiled outputs (in .gitignore)
- **benchmark/**: Performance tests
- **docs/**: Documentation

##### JavaScript/TypeScript Library

- **src/**: Source code
- **dist/**: Built files (in .gitignore)
- **examples/**: Example usage
- **tests/**: Test files
- **types/**: TypeScript type definitions

##### C# Library

- **src/**
  - **ProjectName/**: Main project
  - **ProjectName.Tests/**: Unit tests
- **samples/**: Sample projects
- **docs/**: Documentation

##### C++ Library

- **include/**: Public header files
- **src/**: Implementation files
- **test/**: Test files
- **examples/**: Example usage
- **cmake/**: CMake configuration files
- **build/**: Build output (in .gitignore)

## Repository Configuration

### Git Configuration

#### .gitignore

Each repository should have a tailored `.gitignore` file appropriate for its project type:

- Use standard templates as starting points ([GitHub .gitignore templates](https://github.com/github/gitignore))
- Include common exclusions for:
  - Build artifacts and compiled code
  - Dependencies and packages
  - Environment-specific files
  - Editor/IDE specific files
  - System files (DS_Store, Thumbs.db)
  - Credentials and sensitive information

Example patterns for common project types:

```plaintext
# Unity Projects
/[Ll]ibrary/
/[Tt]emp/
/[Oo]bj/
/[Bb]uild/
/[Bb]uilds/
/[Ll]ogs/
/[Uu]ser[Ss]ettings/
*.pidb
*.unityproj
*.suo
*.userprefs
*.booproj

# Web Projects
/node_modules
/dist
.env.local
.env.development.local
.env.test.local
.env.production.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# General
.DS_Store
Thumbs.db
*.log
*.bak
```

#### .gitattributes

Use `.gitattributes` to specify:

- Line ending normalization
- Git LFS file patterns for binary assets
- Merge strategies for specific files
- Language-specific settings

Example for a game project:

```plaintext
# Set default behavior to automatically normalize line endings
* text=auto

# Unity YAML files
*.unity text merge=unityyamlmerge diff
*.prefab text merge=unityyamlmerge diff

# 3D models
*.fbx filter=lfs diff=lfs merge=lfs -text
*.obj filter=lfs diff=lfs merge=lfs -text

# Images
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.tga filter=lfs diff=lfs merge=lfs -text
*.psd filter=lfs diff=lfs merge=lfs -text

# Audio
*.wav filter=lfs diff=lfs merge=lfs -text
*.mp3 filter=lfs diff=lfs merge=lfs -text
*.ogg filter=lfs diff=lfs merge=lfs -text

# Video
*.mp4 filter=lfs diff=lfs merge=lfs -text
*.mov filter=lfs diff=lfs merge=lfs -text
```

### Branch Protection

Configure branch protection rules for core branches (`main` and `develop`):

1. **Require pull request reviews**:
   - At least one approval from a code owner
   - Dismiss stale pull request approvals when new commits are pushed

2. **Require status checks to pass before merging**:
   - CI/CD pipeline completion
   - Code quality checks
   - Test coverage thresholds

3. **Require linear history**:
   - Prevents merge commits
   - Maintains a clean, readable history

4. **Do not allow bypassing the above settings**:
   - Even for repository administrators (optional but recommended)

5. **Use protected tags**:
   - Restrict who can push to version tags

## Repository Documentation

### Essential Documentation

#### README.md

Every repository must have a comprehensive README.md containing:

1. **Project Title and Description**:
   - Clear description of what the repository contains
   - The purpose and scope of the project

2. **Badges**:
   - Build status
   - Test coverage
   - Version information

3. **Installation/Setup Instructions**:
   - Prerequisites
   - Step-by-step installation guide
   - Configuration instructions

4. **Usage Examples**:
   - Basic examples of how to use the code
   - Code snippets for common tasks

5. **Architecture Overview**:
   - High-level architecture diagram (for larger projects)
   - Key components and their relationships

6. **Contributing Guidelines**:
   - Link to CONTRIBUTING.md
   - How to report issues

7. **License Information**:
   - Type of license
   - Link to LICENSE file

Example README structure:

``