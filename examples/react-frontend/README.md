<!--
Document: React Frontend Example
Version: 1.0.0
Last Updated: 2023-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2023-03-20: Initial version
-->

# Bayat React Frontend

This repository serves as a reference implementation of Bayat's frontend development conventions. It provides a production-ready starting point for building React applications using TypeScript and modern frontend practices.

## Conventions Demonstrated

This example demonstrates the following Bayat conventions:

- **Component Architecture**: Atomic design principles with organized component hierarchy
- **State Management**: Centralized state with Redux Toolkit and hooks
- **Type Safety**: TypeScript implementation with proper typing
- **Testing**: Component, hook, and integration testing patterns
- **Performance**: Code splitting, memoization, and performance optimization
- **Accessibility**: WCAG compliance and screen reader support
- **Styling**: CSS-in-JS with Emotion and theming
- **Project Structure**: Scalable and maintainable directory organization

## Getting Started

```bash
# Clone the repository
git clone https://github.com/bayat/examples/react-frontend

# Install dependencies
npm install

# Run development server
npm start

# Run tests
npm test

# Build for production
npm run build
```

## Project Structure

```plaintext
.
├── public/             # Static assets
├── src/
│   ├── assets/         # Images, fonts, etc.
│   ├── components/     # Reusable UI components
│   │   ├── atoms/      # Basic building blocks
│   │   ├── molecules/  # Combinations of atoms
│   │   ├── organisms/  # Complex UI sections
│   │   ├── templates/  # Page layouts
│   │   └── pages/      # Full pages
│   ├── hooks/          # Custom React hooks
│   ├── services/       # API and external services
│   ├── store/          # Redux state management
│   ├── theme/          # Styling themes
│   ├── types/          # TypeScript type definitions
│   ├── utils/          # Utility functions
│   ├── App.tsx         # Main application component
│   └── index.tsx       # Application entry point
├── tests/              # Test files
├── .eslintrc.js        # ESLint configuration
├── .prettierrc         # Prettier configuration
├── tsconfig.json       # TypeScript configuration
├── package.json        # Dependencies and scripts
└── README.md           # Project documentation
```

## Key Features

- **Component Library**: Reusable, documented UI components
- **Form Management**: Form validation with Formik/React Hook Form
- **API Integration**: Axios setup with interceptors
- **State Management**: Redux Toolkit with proper slicing
- **Routing**: React Router with route-based code splitting
- **Testing**: Jest and React Testing Library
- **Styling**: Emotion with theming and responsive design
- **i18n**: Internationalization support
- **Error Handling**: Global error boundary and error reporting
- **Accessibility**: ARIA attributes and keyboard navigation

## Contribution Guidelines

Please refer to the main [Contribution Guidelines](../../CONTRIBUTING.md) for information on contributing to this example.
