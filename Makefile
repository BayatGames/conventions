.PHONY: validate check-links update-versions help

# Default target executed when no arguments are given to make.
default: help

# Help target displays all available targets.
help:
	@echo "Available targets:"
	@echo "  validate           : Run validation script to check documentation consistency"
	@echo "  check-links        : Check for broken links in documentation"
	@echo "  update-versions    : Update version headers in documentation files"
	@echo "  help               : Show this help message"

# Run the validation script to check documentation consistency
validate:
	@echo "Running documentation validation..."
	@chmod +x scripts/validate_documentation.sh
	@./scripts/validate_documentation.sh

# Check for broken links in documentation
check-links:
	@echo "Checking for broken links in documentation..."
	@find . -name "*.md" -type f -exec grep -l "\[.*\](" {} \; | xargs -I{} sh -c 'echo "Checking {}..."; grep -o "\[.*\]([^)]*)" {} | grep -v "http" | sed "s/.*(\(.*\))/\1/" | while read link; do [ -f "$${link}" ] || echo "  Broken link: $${link}"; done'

# Update version headers in documentation files
update-versions:
	@echo "Updating version headers in documentation files..."
	@find . -name "*.md" -type f -not -path "./.git/*" -exec sed -i '' -E '1,/^---$$/{s/^(Last Updated:) .*/\1 $(shell date +%Y-%m-%d)/g}' {} \;

# Run all validation checks
check-all: validate check-links
	@echo "All validation checks completed." 