#!/bin/bash
# Validation script to ensure all markdown files are referenced in the README

REPO_ROOT=$(git rev-parse --show-toplevel)
README_PATH="$REPO_ROOT/README.md"

# Find all markdown files in the repository
echo "Finding all markdown files in the repository..."
MARKDOWN_FILES=$(find "$REPO_ROOT" -name "*.md" -not -path "*/\.*" | sort)

# Count how many files were found
TOTAL_FILES=$(echo "$MARKDOWN_FILES" | wc -l)
echo "Found $TOTAL_FILES markdown files"

# Extract all markdown links from the README
echo "Extracting markdown links from README.md..."
README_LINKS=$(grep -o -E '\[.*\]\([^)]+\.md\)' "$README_PATH" | sed -E 's/\[.*\]\(([^)]+)\)/\1/g' | sort)

# Count referenced files
REFERENCED_FILES=$(echo "$README_LINKS" | wc -l)
echo "Found $REFERENCED_FILES referenced files in README.md"

# Check each markdown file to see if it's referenced in the README
UNREFERENCED_FILES=0
MISSING_FILES=0

echo -e "\nChecking for unreferenced markdown files..."
for FILE in $MARKDOWN_FILES; do
    # Get relative path from the repository root using Python (works on macOS and Linux)
    RELATIVE_PATH=$(python3 -c "import os.path; print(os.path.relpath('$FILE', '$REPO_ROOT'))")
    
    # Skip README.md itself
    if [ "$RELATIVE_PATH" = "README.md" ] || [ "$RELATIVE_PATH" = "./README.md" ]; then
        continue
    fi
    
    if ! echo "$README_LINKS" | grep -q "$RELATIVE_PATH"; then
        echo "- $RELATIVE_PATH is not referenced in README.md"
        UNREFERENCED_FILES=$((UNREFERENCED_FILES + 1))
    fi
done

echo -e "\nChecking for broken references in README.md..."
for LINK in $README_LINKS; do
    if [ ! -f "$REPO_ROOT/$LINK" ]; then
        echo "- $LINK is referenced in README.md but file does not exist"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

echo -e "\nSummary:"
echo "- $TOTAL_FILES total markdown files"
echo "- $REFERENCED_FILES files referenced in README.md"
echo "- $UNREFERENCED_FILES files not referenced in README.md"
echo "- $MISSING_FILES broken references in README.md"

if [ $UNREFERENCED_FILES -eq 0 ] && [ $MISSING_FILES -eq 0 ]; then
    echo -e "\n✅ All checks passed! Documentation references are consistent."
    exit 0
else
    echo -e "\n❌ Validation failed. Please update README.md to fix the issues listed above."
    exit 1
fi 