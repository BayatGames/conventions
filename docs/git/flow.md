<!--
Document: Bayat Git Flow
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Bayat Git Flow

## Introduction

Bayat Git Flow is a comprehensive branching strategy designed to accommodate a wide variety of project types within Bayat, from game development (Unity-based and cross-platform) to web applications, mobile apps, desktop applications, and libraries/packages. This document outlines the complete workflow, conventions, and best practices to be followed across all Bayat teams.

## Core Principles

1. **Consistency** - Maintain uniform practices across different project types
2. **Flexibility** - Adapt to specific project needs without compromising the core workflow
3. **Traceability** - Ensure all changes can be tracked and understood
4. **Stability** - Protect production/release branches while enabling rapid development
5. **Efficiency** - Minimize merge conflicts and enable parallel development

## Branch Structure

### Core Branches

Every repository must maintain these primary branches:

- `main` - Production-ready code; always deployable
- `develop` - Integration branch for features; represents the next release
- `release/*` - Preparation branches for upcoming releases
- `hotfix/*` - Emergency fixes for production issues

### Support Branches

These branches are created as needed:

- `feature/*` - New features or enhancements
- `bugfix/*` - Non-critical bug fixes targeted for the next release
- `refactor/*` - Code improvements without changing functionality
- `docs/*` - Documentation updates only
- `experiment/*` - Experimental features (may never be merged)
- `platform/*` - Platform-specific implementations (for cross-platform projects)

## Branch Naming Conventions

All branch names must follow these conventions:

- Use lowercase for all branch names
- Use hyphens to separate words
- Include ticket/issue numbers when applicable
- Be descriptive but concise

Examples:

```plaintext
feature/user-authentication
feature/JIRA-123-inventory-system
bugfix/login-validation-error
hotfix/2.1.1-payment-gateway-crash
release/3.0.0
platform/ios-native-controls
```

## Workflow Details

### Feature Development

1. **Branch Creation**:
   - Always branch from `develop`
   - Command: `git checkout develop && git pull && git checkout -b feature/feature-name`

2. **During Development**:
   - Commit frequently with descriptive messages
   - Keep feature branches synchronized with `develop` by regularly rebasing or merging from `develop`
   - Command: `git checkout develop && git pull && git checkout feature/feature-name && git rebase develop`

3. **Completion**:
   - Ensure all tests pass locally
   - Submit a Pull Request (PR) to `develop`
   - Address all code review comments
   - Once approved, merge using the squash and merge strategy

### Release Process

1. **Branch Creation**:
   - Create a release branch from `develop` when ready to prepare a release
   - Use semantic versioning for branch naming
   - Command: `git checkout develop && git pull && git checkout -b release/x.y.z`

2. **Release Preparation**:
   - Only bug fixes, documentation, and release-oriented changes are permitted
   - No new features should be added to release branches
   - Version numbers and build configurations should be updated
   - Comprehensive testing should be performed

3. **Completion**:
   - Merge the release branch into `main` with a regular merge (no squash)
   - Tag the merge commit in `main` with the version number
   - Merge the release branch back into `develop`
   - Command sequence:

     ```bash
     git checkout main && git pull
     git merge --no-ff release/x.y.z
     git tag -a vx.y.z -m "Version x.y.z"
     git push origin main --tags
     git checkout develop && git pull
     git merge --no-ff release/x.y.z
     git push origin develop
     ```

### Hotfix Process

1. **Branch Creation**:
   - Create hotfix branches directly from `main`
   - Command: `git checkout main && git pull && git checkout -b hotfix/x.y.z-issue-description`

2. **During Hotfix**:
   - Keep changes minimal and focused on fixing the critical issue
   - Ensure thorough testing even with the expedited timeline

3. **Completion**:
   - Merge into `main` with a regular merge (no squash)
   - Tag the merge commit with the incremented version number
   - Merge back into `develop`
   - Command sequence (similar to release completion)

## Commit Message Standards

All commit messages must follow this format:

```plaintext
<type>(<scope>): <subject>

<body>

<footer>
```

Where:

- **Type**: feat (feature), fix (bugfix), docs (documentation), style (formatting), refactor, test, chore
- **Scope**: Optional component/module name affected
- **Subject**: Brief description in imperative mood, not capitalized, no period at end
- **Body**: Detailed explanation of changes (optional)
- **Footer**: Reference issues, PRs, breaking changes (optional)

Examples:

```plaintext
feat(auth): add two-factor authentication option

Implement TOTP-based two-factor authentication with QR code setup
and recovery codes generation.

Resolves: #123
```

```plaintext
fix(ui): correct button alignment on checkout page
```

For comprehensive guidelines on commit messages, including detailed descriptions of each commit type, scope conventions, and project-specific examples, refer to the [Git Commits Conventions](docs/git/commits.md).

## Pull Request Guidelines

### PR Creation

1. **Title**: Clear and descriptive, including ticket reference
2. **Description**:
   - What changes were made
   - Why these changes were necessary
   - How the changes address the issue
   - Any testing considerations
   - Screenshots/videos for UI changes
3. **Size**: Keep PRs small and focused on a single issue/feature

### PR Review Process

1. **Required Reviewers**: At least one senior developer must approve
2. **Review Criteria**:
   - Code quality and style compliance
   - Adequate test coverage
   - Performance considerations
   - Security implications
   - Documentation updates
3. **Merge Requirements**:
   - All discussions resolved
   - CI tests passing
   - Required approvals received

## Project Type-Specific Guidelines

### Game Development (Unity/Cross-platform)

1. **Asset Management**:
   - Use Git LFS for binary assets
   - Consider `.gitattributes` for platform-specific line endings
   - Exclude auto-generated files from Unity

2. **Scene Management**:
   - Prefer prefabs over direct scene modifications
   - Consider using Unity's ScriptableObjects for shared data

3. **Platform-Specific Code**:
   - Use `platform/*` branches for platform-specific implementations
   - Merge platform branches into feature branches before PR to develop

### Web Applications

1. **Database Migrations**:
   - Include migrations in the same PR as related code changes
   - Test migrations in both directions (up and down)

2. **API Versioning**:
   - Use explicit API versioning in routes
   - Document breaking changes in commit messages and PR descriptions

### Mobile Applications

1. **Feature Flags**:
   - Use feature flags for features that might need to be toggled after release
   - Consider remote configuration for dynamically enabling/disabling features

2. **App Store Requirements**:
   - Tag releases with both semantic version and build/store version

### Libraries and Packages

1. **Public API Changes**:
   - Document all public API changes thoroughly
   - Use deprecation notices before removing functionality
   - Follow semantic versioning strictly

2. **Dependency Management**:
   - Avoid introducing breaking changes in minor or patch versions
   - Document all new dependencies in PR descriptions

## CI/CD Integration

### CI Pipeline Structure

1. **Feature Branches**:
   - Run unit tests, linting, static analysis
   - Generate test coverage reports
   - Build but don't deploy

2. **Develop Branch**:
   - All feature branch checks
   - Integration tests
   - Deploy to development/staging environment

3. **Release Branches**:
   - Full test suite including performance tests
   - Deploy to pre-production/QA environment

4. **Main Branch**:
   - Minimal verification tests
   - Deploy to production with approval step

### Automated Checks

1. **Required for All Projects**:
   - Linting
   - Unit tests
   - Build verification

2. **Project-Specific Checks**:
   - Unity: Asset validation, build for target platforms
   - Web: Accessibility tests, browser compatibility tests
   - Mobile: Platform-specific validations

## Versioning Standards

### Semantic Versioning

All projects should follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking/incompatible API changes
- **MINOR**: Backward-compatible functionality additions
- **PATCH**: Backward-compatible bug fixes

### Version Incrementing Rules

1. **Feature Releases**:
   - Increment MINOR version
   - Reset PATCH version to 0

2. **Bug Fix Releases**:
   - Increment PATCH version only

3. **Breaking Changes**:
   - Increment MAJOR version
   - Reset MINOR and PATCH versions to 0

## Git Command Reference

### Common Operations

#### Initial Setup

```bash
# Clone repository
git clone https://github.com/bayat/project-name.git
cd project-name

# Set up Git LFS (for projects with binary assets)
git lfs install
```

#### Feature Development

```bash
# Start a new feature
git checkout develop
git pull
git checkout -b feature/feature-name

# Regularly sync with develop
git checkout develop
git pull
git checkout feature/feature-name
git rebase develop

# Push feature branch for the first time
git push -u origin feature/feature-name

# Subsequent pushes
git push
```

#### Handling Release

```bash
# Create a release branch
git checkout develop
git pull
git checkout -b release/x.y.z
git push -u origin release/x.y.z

# Finalize release
git checkout main
git pull
git merge --no-ff release/x.y.z
git tag -a vx.y.z -m "Version x.y.z"
git push origin main --tags
git checkout develop
git pull
git merge --no-ff release/x.y.z
git push origin develop
git branch -d release/x.y.z
git push origin --delete release/x.y.z
```

## Conflict Resolution Strategy

1. **Prevention**:
   - Keep feature branches short-lived
   - Regularly sync with `develop`
   - Communicate with team about overlapping work

2. **Resolution Approach**:
   - Prefer resolving conflicts locally before pushing
   - Use visual merge tools for complex conflicts
   - Consult with original code authors when necessary

3. **After Resolution**:
   - Test thoroughly after resolving conflicts
   - Document significant conflict resolutions in PR description

## Special Scenarios

### Early Access/Preview Releases

1. Create a branch `preview/x.y.z` from the appropriate `release/*` branch
2. Apply specific preview configurations/branding
3. Deploy to preview channels only

### Long-Term Support (LTS) Versions

1. Create a `support/x.y` branch from the appropriate release tag in `main`
2. Apply only critical bug fixes and security patches
3. Tag patch releases within this branch as needed

### Emergency Production Fixes

For issues that can't wait for the standard hotfix process:

1. Create a `emergency/issue-description` branch from `main`
2. Apply minimal changes to fix the critical issue
3. Use expedited review process (document reviewers in PR)
4. Deploy immediately after merge and tagging
5. Backport to `develop` as soon as possible

## Adoption and Transition

### For New Projects

- Set up branch protection rules from the start
- Configure template repositories with the correct branch structure

### For Existing Projects

1. **Preparation**:
   - Document current state of branches
   - Identify completion point for in-progress work
   - Back up existing repository

2. **Implementation**:
   - Create `develop` branch from `main`/`master`
   - Set up branch protection rules
   - Start new work using the Bayat Git Flow

3. **Gradual Transition**:
   - Complete existing work using the previous workflow
   - Begin new work using Bayat Git Flow
   - Full transition after one release cycle

## Training and Resources

### Documentation

- This document (`flow.md`)
- Example workflows (stored in `conventions/git/examples/`)
- Quick reference cheat sheet (`conventions/git/cheatsheet.md`)

### Training

- Initial team training sessions
- Buddy system for first-time usage
- Regular refresher sessions for updates

## Maintenance and Evolution

This Bayat Git Flow document should be reviewed and updated:

- After each major release cycle
- When new project types are introduced
- When significant workflows or technology changes occur

Updates to this document should follow the standard PR process with team review.

## Conclusion

The Bayat Git Flow is designed to support all project types within the company while maintaining consistency and quality. By following these guidelines, we ensure efficient development, clear history, and stable releases across our diverse project portfolio.

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 2025-03-20 | Initial version |
