<!--
Document: Versioning Standards
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Versioning Standards

This document outlines the versioning standards for all Bayat projects, including how the conventions themselves are versioned.

## Semantic Versioning for Software Projects

All Bayat software projects must follow [Semantic Versioning 2.0.0](https://semver.org/) (SemVer) principles:

### Version Format

Version numbers are structured as `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`:

- **MAJOR**: Incremented for incompatible API changes
- **MINOR**: Incremented for backward-compatible functionality additions
- **PATCH**: Incremented for backward-compatible bug fixes
- **PRERELEASE**: Optional identifier for pre-release versions (e.g., alpha, beta)
- **BUILD**: Optional build metadata

### Examples

- `1.0.0`: Initial stable release
- `1.1.0`: New features added, backward compatible
- `1.1.1`: Bug fixes for version 1.1.0
- `2.0.0`: Breaking changes from version 1.x
- `1.0.0-alpha.1`: Pre-release alpha version
- `1.0.0-beta.2`: Pre-release beta version
- `1.0.0-rc.1`: Release candidate
- `1.0.0+20231115`: Build metadata

### Version Zero

For projects in initial development:

- Start with `0.1.0`
- Increment MINOR version for new features
- Increment PATCH version for bug fixes
- Move to `1.0.0` when the API is considered stable

### Pre-release Identifiers

Pre-release identifiers are used for versions that are not yet stable:

1. **alpha**: Early testing, unstable, likely to change
2. **beta**: Feature complete, but may contain bugs
3. **rc**: Release candidate, potential for final release

Pre-release versions have lower precedence than normal versions:
`1.0.0-alpha < 1.0.0-beta < 1.0.0-rc < 1.0.0`

## Convention Versioning

The Bayat Development Conventions themselves follow these versioning principles:

### Version Format

Convention versions follow the format `YEAR.QUARTER.UPDATE`:

- **YEAR**: 4-digit year (e.g., 2025)
- **QUARTER**: Quarter of the year (1-4)
- **UPDATE**: Sequential update within the quarter, starting at 0

### Examples

- `2025.1.0`: First release in Q1 2025
- `2025.1.1`: First update in Q1 2025
- `2025.2.0`: First release in Q2 2025

### Compatibility

Each new convention version should clearly document:

- Breaking changes from previous versions
- Migration paths for existing projects
- Timeline for adoption
- Justification for significant changes

## Version Control Practices

### Git Tags

All releases must be tagged in the repository:

- Pre-release: `v1.0.0-beta.1`
- Release: `v1.0.0`

Tags must be annotated with release notes:
```bash
git tag -a v1.0.0 -m "Release v1.0.0: Summary of changes"
```

### Branches

Standard branch naming for releases:

- Release branches: `release/1.0.0`
- Hotfix branches: `hotfix/1.0.1`

## Version Bumping Guidelines

### When to Bump MAJOR Version

- Incompatible API changes
- Removal of deprecated functionality
- Significant changes to core behavior
- Breaking changes to public interfaces

### When to Bump MINOR Version

- New backward-compatible functionality
- Deprecation of existing functionality
- Significant internal implementation changes
- New non-essential features

### When to Bump PATCH Version

- Backward-compatible bug fixes
- Security updates
- Very minor changes
- Performance improvements that don't change behavior

## Version Display

### User-Facing Version Display

For user-facing version displays:

- Marketing versions: May use simplified formats like "Version 2"
- About screens: Show full version including build information
- Release notes: Include full semantic version

### Internal Version Representation

For internal representation:

- Always use full semantic version in code
- Use version parsing libraries rather than string operations
- Include build number for debugging

## Versioning in Different Contexts

### API Versioning

APIs must be explicitly versioned:

- REST APIs: Include version in URL path (`/api/v1/resource`)
- GraphQL: Use schema versioning
- Library APIs: Follow semantic versioning

### Database Schema Versioning

Database schemas must be versioned through:

- Migration scripts with sequential version numbers
- Timestamp-based migration identifiers
- Changes documented in version control

### Configuration Versioning

Configuration formats must include version information:

```json
{
  "configVersion": "1.0.0",
  "settings": {
    // ...
  }
}
```

### Documentation Versioning

Documentation must be versioned to match software releases:

- Keep documentation for previous major versions
- Clearly mark documentation with applicable version range
- Provide upgrade guides between versions

## Version Workflow

### Version Bump Process

1. Determine type of version change (MAJOR/MINOR/PATCH)
2. Update version in all required files
3. Update CHANGELOG.md
4. Create release branch if needed
5. Create tagged commit
6. Merge to appropriate branches

### Required Version File Updates

Ensure these files are updated with each version change:

- package.json (JavaScript/Node.js)
- .csproj (C#/.NET)
- setup.py/pyproject.toml (Python)
- pom.xml (Java)
- build.gradle (Android)
- Info.plist (iOS)
- CHANGELOG.md (all projects)
- README.md (if version-specific)

### Automation

Version bumping should be automated using tools like:

- [standard-version](https://github.com/conventional-changelog/standard-version) for JavaScript
- [bump2version](https://github.com/c4urself/bump2version) for Python
- Custom scripts for other ecosystems

## Long-Term Support (LTS) Versions

### LTS Designation Criteria

Versions may be designated as LTS when they:

- Are stable and well-tested
- Represent significant infrastructure or platform releases
- Are used by multiple critical projects

### LTS Support Policy

- LTS versions receive security updates for at least 18 months
- LTS versions receive critical bug fixes for at least 12 months
- No new features are added to LTS versions
- Clear EOL (End of Life) dates are published

## Communication

### Version Announcements

Version releases must be communicated through:

- Internal announcements (email/Slack)
- Release notes in repository
- Documentation updates
- Breaking change notifications at least 3 months in advance

### Deprecation Process

1. Mark features as deprecated in code and documentation
2. Provide migration path in documentation
3. Keep deprecated features for at least one MAJOR version
4. Remove features only after proper notice (minimum 6 months)

## Glossary

- **SemVer**: Semantic Versioning, a versioning scheme
- **API**: Application Programming Interface
- **LTS**: Long-Term Support
- **EOL**: End of Life
- **Deprecation**: Process of marking features as obsolete before removal 