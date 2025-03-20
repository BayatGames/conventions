# Git Conventions

## Branch Structure

- `main` - Production-ready code
- `develop` - Latest development changes
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Critical production fixes
- `release/*` - Release preparation

## Commit Messages

Follow the Conventional Commits standard:

```plaintext
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect code meaning
- `refactor`: Code changes that neither fix a bug nor add a feature
- `test`: Adding or fixing tests
- `chore`: Changes to build process or auxiliary tools
- `perf`: Performance improvements
- `ci`: CI configuration changes
- `build`: Build system changes
- `revert`: Revert a previous commit

### Examples

```
feat(auth): add social login support
fix(api): resolve null reference in user controller
docs(readme): update installation instructions
```

## Related Files

- [Git Flow](docs/git/flow.md)
- [Commit Conventions](docs/git/commits.md)
- [Repository Structure](docs/git/repos.md)
