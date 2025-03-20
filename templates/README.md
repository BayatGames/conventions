# Bayat Development Conventions - Cursor Integration Templates

This directory contains templates for integrating Bayat Development Conventions with Cursor IDE using Multi-Document Context (MDC) files and Cursor Rules.

## Available Templates

### Project Type Templates

- [React/TypeScript Frontend](mdc/react-typescript/) - MDC files for React and TypeScript frontend projects
- [Node.js Backend](mdc/nodejs-backend/) - MDC files for Node.js backend projects
- [Full-Stack Application](mdc/fullstack/) - MDC files for full-stack web applications
- [Unity](mdc/unity/) - MDC files for Unity game development projects
- [Tauri](mdc/tauri/) - MDC files for Tauri desktop applications

### Cursor Rules Templates

- [React/TypeScript Rules](cursorrules/react-typescript.json) - Cursor Rules for React/TypeScript projects
- [Node.js Backend Rules](cursorrules/nodejs-backend.json) - Cursor Rules for Node.js backends
- [Full-Stack Rules](cursorrules/fullstack.json) - Cursor Rules for full-stack applications
- [Unity Rules](cursorrules/unity.json) - Cursor Rules for Unity game development
- [Tauri Rules](cursorrules/tauri.json) - Cursor Rules for Tauri desktop applications

## How to Use These Templates

1. Select the template that matches your project type
2. Create a `.cursor/mdc/` directory in your project root
3. Copy the relevant MDC files into this directory
4. Copy the corresponding `.cursorrules` file to your project root as `.cursorrules`

## Benefits of MDC and Cursor Rules

- **Context-Aware Development**: Cursor IDE will provide context-specific suggestions based on the file type and location
- **Consistent Standards**: Enforce project conventions consistently across your team
- **Documentation at Your Fingertips**: Access relevant documentation without leaving your editor
- **Reduced Decision Fatigue**: Clear guidelines for file organization, naming, and code structure

## Customizing Templates

These templates are starting points based on Bayat Development Conventions. You can customize them to fit your project's specific needs by:

1. Modifying the MDC files to include project-specific guidelines
2. Adjusting the Cursor Rules to match your project structure
3. Adding additional MDC files for custom conventions

## Related Resources

- [Cursor IDE Documentation](https://cursor.sh/docs)
- [Bayat Development Conventions](../docs/)
