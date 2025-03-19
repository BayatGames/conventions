#!/bin/bash

# Script to add standard headers to markdown files that don't have them

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Adding document headers to markdown files...${NC}"

# Get today's date
TODAY=$(date +%Y-%m-%d)

# Find all markdown files
MARKDOWN_FILES=$(find ./docs -name "*.md" -type f)
COUNTER=0

for file in $MARKDOWN_FILES; do
    # Skip if file is empty
    if [ ! -s "$file" ]; then
        continue
    fi
    
    # Check if file already has a header (<!-- at the beginning)
    if grep -q "^<!--" "$file"; then
        echo -e "${YELLOW}Header already exists in ${file}${NC}"
        continue
    fi
    
    # Get the document title from the first h1 in the file
    TITLE=$(grep -m 1 "^# " "$file" | sed 's/^# //')
    
    if [ -z "$TITLE" ]; then
        # If no h1 title is found, use the filename without extension
        TITLE=$(basename "$file" .md | tr '-' ' ' | sed -e 's/\b\(.\)/\u\1/g')
    fi
    
    # Create a backup of the original file
    cp "$file" "${file}.bak"
    
    # Create the header and prepend it to the file
    {
        echo "<!--"
        echo "Document: ${TITLE}"
        echo "Version: 1.0.0"
        echo "Last Updated: ${TODAY}"
        echo "Last Updated By: Bayat Platform Team"
        echo "Change Log:"
        echo "- ${TODAY}: Initial version"
        echo "-->"
        echo ""
        cat "${file}.bak"
    } > "$file"
    
    # Remove the backup file
    rm "${file}.bak"
    
    echo -e "${GREEN}Added header to ${file}${NC}"
    COUNTER=$((COUNTER+1))
done

if [ $COUNTER -eq 0 ]; then
    echo -e "${GREEN}All files already have headers.${NC}"
else
    echo -e "${GREEN}Added headers to ${COUNTER} files.${NC}"
fi

exit 0 