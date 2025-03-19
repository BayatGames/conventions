<!--
Document: Interactive Documentation Tools
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2023-03-19: Initial version
-->

# Interactive Documentation Tools

This document provides recommendations and standards for implementing interactive documentation solutions for Bayat projects.

## Recommended Solutions

| Tool | Best For | Features | Complexity |
|------|----------|----------|------------|
| [Docusaurus](https://docusaurus.io/) | Comprehensive developer portals | React integration, versioning, search, plugins | Medium |
| [MkDocs](https://www.mkdocs.org/) | Lightweight documentation | Simple, Markdown-based, Material theme | Low |
| [VuePress](https://vuepress.vuejs.org/) | Vue.js projects | Vue integration, customizable themes | Medium |
| [GitBook](https://www.gitbook.com/) | Team documentation | Collaborative editing, clean UI | Low |
| [Sphinx](https://www.sphinx-doc.org/) | API documentation | Extensive extensions, code-doc integration | High |

## Implementation Standards

### Docusaurus Implementation

For most Bayat projects, Docusaurus is the recommended solution. Implementation should follow these standards:

#### Project Structure

```plaintext
docs/
├── intro.md            # Introduction page
├── getting-started.md  # Getting started guide
├── category/           # Category directory
│   ├── _category_.json # Category metadata
│   ├── doc1.md         # Document in category
│   └── doc2.md         # Another document in category
├── another-category/
│   └── ...
static/                 # Static assets
├── img/                # Images
└── diagrams/           # Architecture diagrams
```

#### Configuration

The `docusaurus.config.js` file should include:

```javascript
module.exports = {
  title: 'Project Name Documentation',
  tagline: 'Clear, concise, complete documentation',
  url: 'https://docs.example.com',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'bayat',
  projectName: 'project-name',
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/bayat/project-name/edit/main/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
  themeConfig: {
    navbar: {
      title: 'Project Name',
      logo: {
        alt: 'Bayat Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'doc',
          docId: 'intro',
          position: 'left',
          label: 'Documentation',
        },
        {
          href: 'https://github.com/bayat/project-name',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
            {
              label: 'Getting Started',
              to: '/docs/getting-started',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Slack',
              href: 'https://slack.bayat.com',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Bayat, Inc.`,
    },
  },
};
```

### MkDocs Implementation

For simpler project documentation, MkDocs with Material theme is recommended:

#### Project Structure

```plaintext
docs/
├── index.md            # Home page
├── getting-started.md  # Getting started guide
├── user-guide/         # User guide directory
│   ├── overview.md     # Overview document
│   └── features.md     # Features document
├── api/                # API documentation
│   └── ...
```

#### Configuration

The `mkdocs.yml` file should include:

```yaml
site_name: Project Name Documentation
site_url: https://docs.example.com
repo_url: https://github.com/bayat/project-name
edit_uri: edit/main/docs/

theme:
  name: material
  palette:
    primary: indigo
    accent: indigo
  features:
    - navigation.tabs
    - navigation.instant
    - navigation.tracking
    - navigation.top
    - search.suggest
    - search.highlight

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.tabbed
  - pymdownx.emoji
  - attr_list
  - md_in_html

plugins:
  - search
  - minify:
      minify_html: true

nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - User Guide:
    - Overview: user-guide/overview.md
    - Features: user-guide/features.md
  - API:
    - Overview: api/index.md
```

## Deployment Recommendations

### Continuous Deployment

Documentation should be deployed automatically using CI/CD pipelines:

1. For GitHub repositories, use GitHub Actions
2. For GitLab repositories, use GitLab CI/CD
3. Deploy to GitHub Pages, GitLab Pages, or Netlify

### Example GitHub Action

```yaml
name: Deploy Documentation

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'docusaurus.config.js'
      - '.github/workflows/deploy-docs.yml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 16
          cache: npm
      - name: Install dependencies
        run: npm ci
      - name: Build website
        run: npm run build
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
```

## Migration Guide

If you're considering migrating existing documentation to an interactive solution:

1. **Inventory**: Catalog all existing documentation
2. **Structure**: Plan the new information architecture  
3. **Migrate**: Convert content to Markdown format
4. **Enhance**: Add cross-references, search, and navigation
5. **Test**: Verify all links and content
6. **Deploy**: Set up CI/CD for automatic deployment
7. **Redirect**: Set up redirects from old documentation

## Conclusion

Interactive documentation significantly improves the developer experience, making it easier to find, use, and contribute to documentation. Choose the appropriate tool based on your project's needs and follow the implementation standards outlined in this document.
