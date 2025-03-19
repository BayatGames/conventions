# Community Contribution Guidelines

This document outlines the standards and best practices for external contributions to Bayat's open-source projects.

## Table of Contents

- [Introduction](#introduction)
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Contribution Workflow](#contribution-workflow)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Code Standards](#code-standards)
- [Documentation Requirements](#documentation-requirements)
- [Testing Requirements](#testing-requirements)
- [Review Process](#review-process)
- [Recognition and Attribution](#recognition-and-attribution)
- [Communication Channels](#communication-channels)
- [Legal Considerations](#legal-considerations)

## Introduction

### Purpose

These guidelines facilitate successful contributions to Bayat's open-source projects by:

- Setting clear expectations for contributors
- Streamlining the contribution process
- Ensuring high-quality contributions
- Creating a positive experience for community members
- Maintaining project quality and consistency

### Scope

These guidelines apply to all contributions to Bayat's public repositories, including:

- Code contributions
- Documentation improvements
- Bug reports
- Feature requests
- Design assets
- Translations
- Test cases

## Code of Conduct

All contributors must adhere to our [Code of Conduct](../CODE_OF_CONDUCT.md), which promotes:

- Respectful and inclusive communication
- Constructive feedback
- Collaborative problem solving
- Focus on project objectives
- A welcoming environment for all participants

Violations of the Code of Conduct should be reported to the project maintainers or [conduct@bayat.com](mailto:conduct@bayat.com).

## Getting Started

### Before Contributing

1. **Read Project Documentation**:
   - Project README and contribution guidelines
   - Architecture documentation
   - Design documents or style guides

2. **Search Existing Issues and PRs**:
   - Check if the issue has already been reported
   - Look for ongoing or rejected work on similar features
   - Review related discussions

3. **Join the Community**:
   - Introduce yourself in community channels
   - Participate in discussions
   - Ask questions if something is unclear

### First Contributions

For first-time contributors:

1. Look for issues labeled `good-first-issue` or `beginner-friendly`
2. Start with small, contained changes like:
   - Documentation improvements
   - Bug fixes with clear reproduction steps
   - Test additions
   - Small feature enhancements

### Development Environment Setup

1. Fork the repository to your GitHub account
2. Clone your fork to your local machine
3. Set up the upstream remote:

   ```bash
   git remote add upstream https://github.com/bayat/[project].git
   ```

4. Follow project-specific setup instructions in the README
5. Verify your environment with provided tests or examples

## Contribution Workflow

### Standard Workflow

1. **Issue Discussion**:
   - For features: Discuss in issues before implementation
   - For bugs: Report with complete reproduction steps
   - Get maintainer feedback on proposed approach

2. **Branch Creation**:
   - Create a feature branch from the main development branch
   - Use descriptive naming: `feature/short-description` or `fix/issue-description`
   - Keep branches focused on single issues or features

3. **Development**:
   - Follow project coding standards
   - Include tests for new functionality
   - Update documentation as needed
   - Make regular, logical commits with clear messages

4. **Preparation for Submission**:
   - Sync with upstream before submitting:

     ```bash
     git fetch upstream
     git rebase upstream/main
     ```

   - Resolve any conflicts
   - Run all tests and linters locally

5. **Pull Request Submission**:
   - Submit PR against the appropriate target branch
   - Complete the PR template with all required information
   - Link to related issues
   - Request appropriate reviewers

### Contribution Size Guidelines

| Contribution Type | Recommended Size | Review Time Expectation |
|-------------------|------------------|-------------------------|
| Typo fix | 1-5 lines | 1-2 days |
| Bug fix | < 200 lines | 2-5 days |
| Small feature | < 500 lines | 5-10 days |
| Major feature | Discuss with maintainers | 2+ weeks |

For larger changes, consider:

- Breaking the work into smaller, incremental PRs
- Creating a design document or RFC first
- Implementing a prototype for feedback before full implementation

## Pull Request Guidelines

### PR Checklist

All pull requests should:

- [ ] Address a single concern (feature, bug, documentation)
- [ ] Include tests for new functionality
- [ ] Update relevant documentation
- [ ] Pass CI/CD checks
- [ ] Follow coding standards and style guides
- [ ] Include appropriate changelog entries
- [ ] Be rebased on the latest upstream changes

### PR Template

PRs should use the project-specific template that includes:

```markdown
## Description
[Concise description of the changes]

## Related Issue
Fixes #[issue_number]

## Motivation and Context
[Why is this change needed? What problem does it solve?]

## How Has This Been Tested?
[Describe the tests you ran]

## Screenshots (if appropriate)

## Types of changes
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```plaintext
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Where `type` is one of:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code changes that neither fix bugs nor add features
- `perf`: Performance improvements
- `test`: Adding or correcting tests
- `chore`: Changes to build process, tools, etc.

Examples:

```plaintext
feat(auth): add multi-factor authentication
fix(api): prevent race condition in request handling
docs: clarify installation instructions
```

## Code Standards

### Language-Specific Standards

Follow the project's established coding standards, which typically reference Bayat's language-specific standards:

- [JavaScript](../languages/javascript.md)
- [TypeScript](../languages/typescript.md)
- [Python](../languages/python.md)
- [Go](../languages/go.md)
- [Java](../languages/java.md)
- [C++](../languages/cpp.md)
- [C#](../languages/csharp.md)

### General Principles

Regardless of language:

- **Readability**: Prioritize code readability over cleverness
- **Simplicity**: Prefer simple, straightforward solutions
- **Consistency**: Follow existing patterns and conventions
- **Modularity**: Write modular, reusable components
- **Maintainability**: Consider the long-term maintenance implications

### Code Comments

- Use comments to explain "why" not "what"
- Document non-obvious design decisions
- Include references to relevant issues or external resources
- Keep comments up-to-date with code changes
- Use language-appropriate documentation tools (JSDoc, docstrings, etc.)

## Documentation Requirements

### Types of Documentation Updates

When contributing, update the following documentation as appropriate:

1. **Code Documentation**:
   - Function/method documentation
   - Class and module documentation
   - Complex algorithm explanations

2. **Project Documentation**:
   - README updates
   - Installation/setup instructions
   - API documentation
   - Usage examples

3. **User-Facing Documentation**:
   - User guides
   - Tutorials
   - FAQ updates
   - Feature documentation

### Documentation Style

- Use clear, concise language
- Include examples for APIs and functions
- Maintain consistent terminology
- Organize content logically
- Follow Markdown standards for formatting
- Include screenshots or diagrams for complex features

### Changelog Entries

Add appropriate entries to CHANGELOG.md following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format:

```markdown
## [Unreleased]
### Added
- New feature X

### Fixed
- Bug in component Y

### Changed
- Behavior of function Z
```

## Testing Requirements

### Test Coverage Expectations

| Contribution Type | Test Coverage Expectation |
|-------------------|---------------------------|
| Bug fix | Tests that verify the fix |
| New feature | Tests for all functionality |
| Refactoring | Maintain or improve existing test coverage |
| Performance improvement | Benchmarks showing improvement |

### Testing Standards

- Write tests that are:
  - Fast
  - Independent
  - Repeatable
  - Self-validating
  - Thorough

- Test both:
  - Happy paths (expected usage)
  - Edge cases and error conditions

### Testing Tools

Use the project's established testing frameworks:

- JavaScript/TypeScript: Jest, Mocha, Cypress
- Python: pytest, unittest
- Go: testing package, testify
- Java: JUnit, TestNG
- C#: xUnit, NUnit

## Review Process

### Review Criteria

Pull requests are evaluated based on:

1. **Functionality**: Does it work as intended?
2. **Quality**: Does it meet code standards?
3. **Tests**: Is it adequately tested?
4. **Documentation**: Is it properly documented?
5. **Design**: Does it align with the project's architecture?
6. **Performance**: Does it maintain or improve performance?
7. **Security**: Does it follow security best practices?

### Review Process

1. **Initial Review**:
   - Automated checks must pass
   - Maintainer performs initial review
   - Feedback provided within timeframe based on PR size

2. **Revision Cycle**:
   - Contributor addresses feedback
   - Reviewer re-reviews changes
   - Process repeats until PR is approved or rejected

3. **Approval and Merge**:
   - Requires approval from at least one maintainer
   - Some projects may require multiple approvals
   - Maintainers handle the final merge

### Feedback Guidelines

As a reviewer:

- Be respectful and constructive
- Explain the reasoning behind suggestions
- Differentiate between required changes and preferences
- Provide examples when possible
- Acknowledge good work

As a contributor:

- Respond to all feedback
- Explain your decisions when not implementing suggestions
- Ask for clarification if feedback is unclear
- Be patient and professional

## Recognition and Attribution

### Contributor Recognition

Contributors are recognized through:

- Inclusion in CONTRIBUTORS.md file
- Mention in release notes for significant contributions
- Acknowledgment in documentation
- Potential inclusion in the core team for consistent contributors

### Attribution Requirements

- Original authors should be credited in file headers
- Major contributors to a component should be listed in component documentation
- Adapted or inspired code must credit original sources

### Path to Maintainership

Active contributors may be invited to become project maintainers based on:

- Quality and consistency of contributions
- Understanding of project goals and architecture
- Positive interaction with the community
- Commitment to the project's long-term success

## Communication Channels

### Official Channels

| Channel | Purpose | Response Time |
|---------|---------|---------------|
| GitHub Issues | Bug reports, feature requests | 1-3 business days |
| GitHub Discussions | Design discussions, Q&A | 2-5 business days |
| Discord/Slack | Real-time community discussion | Best effort |
| Dev mailing list | Major announcements, RFC discussions | Weekly digest |
| Project blog | Major features, roadmap updates | Monthly posts |

### Communication Guidelines

- Keep technical discussions in public channels
- Use issues for project-related discussions, not personal messages
- Tag relevant team members when needed
- Be patient waiting for responses
- Consider time zones when expecting replies

## Legal Considerations

### Licensing

- All contributions must comply with the project's license
- By contributing, you agree that your contributions will be licensed under the project's license
- Include license headers in new files

### Contributor License Agreement (CLA)

For some projects, contributors must sign a CLA:

- Individual CLA for personal contributions
- Corporate CLA for contributions made as part of employment
- Complete the CLA before your first contribution

### Intellectual Property

- Only contribute code you have the right to contribute
- Do not contribute code that infringes on patents or copyrights
- Disclose any potential IP concerns to maintainers

### Third-Party Dependencies

When adding dependencies:

- Only add dependencies with compatible licenses
- Document new dependencies in appropriate files
- Justify the need for new dependencies
- Consider the maintenance and security status of dependencies
