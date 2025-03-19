<!--
Document: Scripts Documentation
Version: 1.0.0
Last Updated: 2023-03-19
Last Updated By: Bayat Platform Team
Change Log:
- 2023-03-19: Initial version
-->

# Scripts

This directory contains utility scripts to help maintain and validate the Bayat Development Conventions.

## Available Scripts

### `validate_documentation.sh`

Validates that all markdown files in the repository are properly referenced in the main README.md file and checks for broken links in the README.

**Usage:**

```bash
./validate_documentation.sh
```

**What it does:**

1. Finds all markdown files in the repository
2. Extracts all markdown links from the README.md file
3. Checks if each markdown file is referenced in the README
4. Checks if each link in the README points to an existing file
5. Provides a summary of the validation results

**Example output:**

```
Finding all markdown files in the repository...
Found 156 markdown files
Extracting markdown links from README.md...
Found 148 referenced files in README.md

Checking for unreferenced markdown files...
- process/documentation-standards.md is not referenced in README.md
- process/onboarding-journey.md is not referenced in README.md
- templates/section-organization.md is not referenced in README.md

Checking for broken references in README.md...
- architecture/example.md is referenced in README.md but file does not exist

Summary:
- 156 total markdown files
- 148 files referenced in README.md
- 3 files not referenced in README.md
- 1 broken references in README.md

❌ Validation failed. Please update README.md to fix the issues listed above.
```

## Adding New Scripts

When adding new scripts, please follow these guidelines:

1. Use descriptive names that indicate the script's purpose
2. Add proper documentation at the beginning of the script
3. Include error handling and informative error messages
4. Add the script to this README with usage instructions

## Script Conventions

1. Shell scripts should use `#!/bin/bash` as the shebang line
2. Python scripts should use `#!/usr/bin/env python3`
3. All scripts should be executable (`chmod +x script.sh`)
4. Script names should use kebab-case (e.g., `validate-links.sh`)
5. Include a `--help` option for all scripts
