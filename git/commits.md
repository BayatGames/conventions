# Conventions | Git - Commits

This document outlines Bayat's commit message conventions, built on top of the [Conventional Commits](https://www.conventionalcommits.org) specification. These standards ensure consistent, traceable, and automated versioning across all Bayat projects.

## Message Structure

The commit message should be structured as follows:

```plaintext
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## General Guidelines

Consistent and well-structured commit messages are essential for maintaining a clean and useful git history. Always follow these core principles:

- **Write descriptive commit messages**: Provide clear explanations of the purpose and context of your changes.
- **Use atomic commits**: Make small, focused commits containing a single logical change to reduce conflict risks and improve readability.
- **Use meaningful commit titles**: Create titles that accurately summarize your changes.

    Don't:

    ```plaintext
    Updates for a fix
    ```

    Do:

    ```plaintext
    fix: Main navigation bar on the website
    ```

- **Use signed commits**: Sign your commits to verify authenticity and protect against tampering.
- **Use appropriate commit types**: Select the correct type to categorize your changes correctly, enabling automated versioning and changelog generation.
- **Write in imperative mood**: Phrase your commit message as a command (e.g., "Fix bug" not "Fixed bug" or "Fixes bug").

## Commit Types

### Primary Types

- **fix**: A bug fix or error correction
  - Example: `fix(auth): resolve login error when using special characters`
  - Triggers a PATCH version increment in semantic versioning
  - Should reference the issue it fixes in the footer when applicable
  - Use for any change that corrects incorrect behavior

- **feat**: A new feature or functionality
  - Example: `feat(gameplay): add double-jump ability for player character`
  - Triggers a MINOR version increment in semantic versioning
  - Should include comprehensive description in the body for significant features
  - Used only for new capabilities from a user's perspective

- **build**: Changes affecting the build system or external dependencies
  - Example: `build(deps): update Unity from 2022.3.1 to 2022.3.5`
  - Does not trigger version change unless it introduces breaking changes
  - Should document any compatibility concerns
  - Includes changes to package.json, project files, build scripts, etc.

- **chore**: Routine tasks, maintenance, or housekeeping changes
  - Example: `chore(assets): remove unused texture files`
  - Does not trigger version change
  - Should be focused and not mixed with functional changes
  - Covers maintenance tasks that don't impact functionality directly

- **ci**: Changes to CI/CD configuration files and scripts
  - Example: `ci(pipeline): optimize test execution to reduce build times`
  - Does not trigger version change
  - Should document purpose and expected improvements
  - Includes changes to GitHub Actions, Jenkins, CircleCI, etc.

- **docs**: Documentation only changes
  - Example: `docs(api): update authentication endpoint documentation`
  - Does not trigger version change
  - Should be accurate and comprehensive
  - Includes changes to README, documentation files, comments, etc.

- **style**: Changes that do not affect code functionality (whitespace, formatting, etc.)
  - Example: `style(codebase): apply consistent indentation throughout`
  - Does not trigger version change
  - Should follow established project style guidelines
  - Does not include any semantic code changes

- **refactor**: Code changes that neither fix bugs nor add features
  - Example: `refactor(inventory): simplify item management logic`
  - Does not trigger version change unless it introduces breaking changes
  - Should maintain existing functionality and tests
  - Focuses on code quality, readability, or maintainability

- **perf**: Performance improvements
  - Example: `perf(rendering): optimize shader calculations for mobile devices`
  - Generally treated as a PATCH increment in semantic versioning
  - Should include measurable metrics when possible
  - Focuses on improving execution time, memory usage, etc.

- **test**: Adding or fixing tests
  - Example: `test(login): add unit tests for password validation`
  - Does not trigger version change
  - Should maintain or improve test coverage
  - Includes changes to test files and testing infrastructure

### Project-Specific Types

These additional types are specific to certain project types within Bayat:

- **locale**: Changes related to localization or internationalization
  - Example: `locale(ui): add French translations for main menu`
  - Typically used for adding/updating translations or locale-specific content
  - Does not trigger version change unless it introduces breaking changes

- **asset**: Changes to assets like graphics, sounds, or data files (particularly for game projects)
  - Example: `asset(characters): update player character model`
  - Useful for tracking significant asset updates separately from code changes
  - Especially relevant for Unity and other game projects

- **level**: Changes to game levels or maps (for game projects)
  - Example: `level(world-1): redesign first boss encounter area`
  - Specific to game development for tracking level design changes
  - Helps separate content design from code functionality changes

- **security**: Changes addressing security vulnerabilities
  - Example: `security(auth): fix XSS vulnerability in login form`
  - Generally treated as a PATCH or MINOR increment depending on severity
  - Should include clear documentation of the vulnerability being addressed
  - Must be handled with appropriate care for sensitive information

## Scope Guidelines

The scope provides context by indicating which part of the codebase was changed. A well-chosen scope:

- Is brief (typically one or two words)
- Uses lowercase letters
- Maintains consistency across similar changes
- Relates to the project's architecture (modules, components, services)

### Common Scope Examples by Project Type

#### Games

- **gameplay**: Core gameplay mechanics and systems
- **ui**: User interface components and interactions
- **physics**: Physics simulation and collision handling
- **inventory**: Item and inventory management
- **levels**: Level structure and management
- **audio**: Sound effects, music, and audio systems
- **ai**: Artificial intelligence and NPC behavior
- **characters**: Character models, animations, and control systems

#### Web Applications

- **auth**: Authentication and authorization systems
- **api**: API endpoints and controllers
- **forms**: Form validation and submission
- **navigation**: Navigation components and routing
- **admin**: Admin panels and functionality
- **search**: Search functionality and algorithms
- **payments**: Payment processing and integration

#### Mobile Applications

- **notifications**: Push and local notifications
- **camera**: Camera access and functionality
- **storage**: Local storage and caching
- **offline**: Offline functionality and synchronization
- **bluetooth**: Bluetooth connectivity
- **location**: Location services and geolocation

#### Libraries and Packages

- **api**: Public API interfaces
- **core**: Core functionality and frameworks
- **utils**: Utility functions and helpers
- **types**: Type definitions and interfaces
- **events**: Event handling and dispatching

## Breaking Changes

Breaking changes modify the API or functionality in a backward-incompatible way. When introducing such changes:

1. Add an exclamation mark after the type/scope: `feat(api)!: change authentication flow`
2. Include `BREAKING CHANGE:` in the footer with details about what changed and how to update:

```plaintext
feat(api)!: change authentication flow

Completely restructure authentication to use JWT tokens instead of session cookies.

BREAKING CHANGE: Auth endpoints now require Authorization header instead of session cookies. All clients need to be updated.
```

Breaking changes always trigger a MAJOR version increment in semantic versioning (e.g., 1.0.0 → 2.0.0).

## Body Format

The commit body should provide detailed context about the changes:

- Separate the body from the subject with a blank line
- Wrap each line at 72 characters
- Use bullet points for multiple items
- Explain the "what" and "why" rather than the "how"
- Include relevant background information
- Mention alternative approaches considered (if applicable)

Example body format:

```plaintext
This commit addresses performance issues in the inventory system by:
- Implementing object pooling for inventory items
- Reducing garbage collection pressure
- Caching calculated values instead of recomputing them

Performance tests show a 40% reduction in frame time spikes when
opening large inventories.
```

## Referencing Issues

Always reference related issues in the commit footer using these formats:

- `Fixes: #123` - Indicates this commit fixes issue #123 (will close the issue automatically)
- `Related to: #456` - Indicates this commit is related to issue #456
- `Implements: #789` - Indicates this commit implements feature request #789
- `Resolves: #123` - Alternative to "Fixes" that will also close the issue

Multiple references can be included in the same footer:

```plaintext
Fixes: #123
Related to: #456, #457
```

## Co-authoring

When commits have multiple authors, add co-author credits in the footer:

```plaintext
Co-authored-by: Name <email@example.com>
Co-authored-by: Another Name <another@example.com>
```

This ensures all contributors receive proper attribution in the git history.

## Revert Commits

When reverting a previous commit, use this format:

```plaintext
revert: feat(gameplay): add double-jump ability

This reverts commit abcdef123456789.
```

Include a brief explanation of why the commit is being reverted in the body when necessary.

## Commit Message Length Guidelines

Follow these length restrictions for readability:

- **Title/Subject**: 50-72 characters maximum (aim for 50)
- **Body**: Wrap at 72 characters per line
- **Entire Message**: Keep under 500 characters when possible

Git clients typically provide visual indicators to help maintain these limits.

## Examples by Project Type

### Game Development

```plaintext
feat(gameplay): implement wall-running mechanic

Add ability for player character to run along vertical surfaces.
- Requires minimum speed to initiate
- Maximum duration of 3 seconds
- Grants brief speed boost upon dismount

Resolves: #234
```

### Web Applications

```plaintext
fix(auth): prevent session fixation attacks

Replace session ID after successful authentication to prevent
session fixation vulnerability.

Security impact: Medium
Fixes: #567
```

### Mobile Applications

```plaintext
perf(offline): optimize local database queries

Rewrite database access layer to reduce query times by 60% and
battery usage by 25% during offline operation.

Benchmark results attached in issue #789.
```

### Libraries/Packages

```plaintext
feat(api)!: simplify configuration interface

Consolidate configuration options into a single object with sensible defaults.
Added comprehensive validation and error reporting.

BREAKING CHANGE: Configuration now uses a single options object instead of multiple parameters.
```

## Common Mistakes to Avoid

- **Mixing multiple changes**: Don't combine unrelated changes in a single commit
- **Vague descriptions**: Avoid generic messages like "Fix bug" or "Update code"
- **Missing scope**: Include a scope whenever possible to provide context
- **Wrong type**: Choose the most appropriate type for your changes
- **Inconsistent formatting**: Follow the standard format consistently
- **Excessive length**: Keep messages concise but informative
- **Missing issue references**: Always reference related issues
- **Past tense**: Use imperative mood (e.g., "fix" not "fixed") for consistency

## Automated Tools

To enforce consistent commit messages, Bayat recommends using:

- **Commitizen**: CLI tool that guides through creating compliant commit messages
- **commitlint**: Linter to check if commit messages meet the conventional format
- **husky**: Git hooks to enforce commit message standards before commits are created

These tools can be configured in your project's package.json file.

## Integration with Bayat Git Flow

The commit conventions integrate seamlessly with Bayat Git Flow in the following ways:

1. **Feature Branches**: Commits should primarily use `feat`, `refactor`, `test`
2. **Bugfix Branches**: Commits should primarily use `fix`
3. **Release Branches**: Commits should primarily use `chore`, `docs`, `style`
4. **Hotfix Branches**: Commits should exclusively use `fix`

Commit messages on `develop` and `main` branches should follow these conventions strictly, especially when using squash merges to combine feature branch commits.

## Changelog Generation

Following these commit conventions enables automatic changelog generation using tools like:

- **standard-version**
- **semantic-release**
- **conventional-changelog**

These tools parse your commit messages to create structured release notes that categorize changes by type and highlight breaking changes.

## Conclusion

Consistent commit messages provide numerous benefits:

- Automatic versioning based on commit types
- Automatic changelog generation
- Clearer project history
- Easier code reviews
- Better understanding of changes
- Improved traceability between code and issues

By following these guidelines, all Bayat teams contribute to a more maintainable and understandable codebase across all project types.
