#!/bin/bash
# Script to check for broken links in documentation files

REPO_ROOT=$(git rev-parse --show-toplevel)
BROKEN_LINKS=0

# Find all markdown files that contain links
MARKDOWN_FILES=$(find "$REPO_ROOT" -name "*.md" -type f -not -path "*/\.*")

# Process each file
for FILE in $MARKDOWN_FILES; do
    # Check if file contains any links before processing
    if grep -q "\[.*\](" "$FILE"; then
        RELATIVE_PATH=$(python3 -c "import os.path; print(os.path.relpath('$FILE', '$REPO_ROOT'))")
        echo "Checking $RELATIVE_PATH..."
        
        # Use a Python script to extract links while ignoring those in code blocks
        # This is more reliable than trying to do this with grep/sed
        LINKS=$(python3 -c '
import re
import sys

def extract_links_outside_code_blocks(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    
    # Split the content into code blocks and non-code blocks
    # First, mark code blocks with special tokens
    code_block_pattern = r"```.*?```"
    # Use DOTALL flag to make . match newlines
    marked_content = re.sub(code_block_pattern, "CODE_BLOCK_PLACEHOLDER", content, flags=re.DOTALL)
    
    # Now extract links from the content with code blocks removed
    link_pattern = r"\[.*?\]\(([^)]+)\)"
    links = re.findall(link_pattern, marked_content)
    
    # Filter out http/https and mailto links
    links = [link for link in links if not link.startswith("http") and not link.startswith("mailto:")]
    
    return links

# Print links one per line
for link in extract_links_outside_code_blocks("'"$FILE"'"):
    print(link)
' 2>/dev/null)
        
        # Check each link (avoid pipe to while which creates a subshell)
        if [ -n "$LINKS" ]; then
            # Save links to temporary file
            TEMP_LINKS=$(mktemp)
            echo "$LINKS" > "$TEMP_LINKS"
            
            while read -r LINK; do
                # If link contains a # (fragment identifier), remove it
                BASE_LINK=$(echo "$LINK" | cut -d '#' -f 1)
                
                # Skip empty links or links with only fragment identifiers
                if [ -z "$BASE_LINK" ]; then
                    continue
                fi
                
                # Skip links that contain regex-like patterns or are images (which might not exist during docs writing)
                if [[ "$BASE_LINK" == *"|"* || "$BASE_LINK" == *.png || "$BASE_LINK" == *.jpg || "$BASE_LINK" == *.jpeg || "$BASE_LINK" == *.gif ]]; then
                    continue
                fi
                
                # Skip LICENSE file references
                if [[ "$BASE_LINK" == "LICENSE" ]]; then
                    continue
                fi
                
                # Check if the link points to an existing file
                # Try relative to the current file's directory first
                FILE_DIR=$(dirname "$FILE")
                if [ -f "$FILE_DIR/$BASE_LINK" ]; then
                    continue
                elif [ -f "$REPO_ROOT/$BASE_LINK" ]; then
                    continue
                else
                    echo "  Broken link: $LINK in $RELATIVE_PATH"
                    ((BROKEN_LINKS++))
                fi
            done < "$TEMP_LINKS"
            
            # Clean up temporary file
            rm "$TEMP_LINKS"
        fi
    fi
done

echo -e "\nSummary:"
if [ $BROKEN_LINKS -eq 0 ]; then
    echo -e "✅ No broken links found!"
    exit 0
else
    echo -e "❌ Found $BROKEN_LINKS broken links."
    exit 1
fi 