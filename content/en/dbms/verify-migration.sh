#!/bin/bash

# Migration Verification Script
# This script helps verify the content migration was successful

echo "========================================="
echo "MACHBASE DOCUMENTATION MIGRATION VERIFICATION"
echo "========================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Base directory
BASE_DIR="/home/sjkim/work/machbase/content/en/dbms2"

echo "1. CHECKING FILE COUNTS"
echo "----------------------------------------"
TOTAL_FILES=$(find "$BASE_DIR" -type f -name "*.md" | wc -l)
echo "Total markdown files: $TOTAL_FILES"

if [ "$TOTAL_FILES" -ge 100 ]; then
    echo -e "${GREEN}✓ File count looks good (expected ~116)${NC}"
else
    echo -e "${RED}✗ File count seems low (expected ~116)${NC}"
fi
echo ""

echo "2. CHECKING REQUIRED SECTIONS"
echo "----------------------------------------"

check_section() {
    local section=$1
    local path=$2
    if [ -d "$path" ]; then
        local count=$(find "$path" -name "*.md" | wc -l)
        echo -e "${GREEN}✓${NC} $section: $count files"
    else
        echo -e "${RED}✗${NC} $section: Directory not found!"
    fi
}

check_section "Getting Started" "$BASE_DIR/getting-started"
check_section "Common Tasks" "$BASE_DIR/common-tasks"
check_section "Core Concepts" "$BASE_DIR/core-concepts"
check_section "Tutorials" "$BASE_DIR/tutorials"
check_section "Tag Tables" "$BASE_DIR/table-types/tag-tables"
check_section "Log Tables" "$BASE_DIR/table-types/log-tables"
check_section "Volatile Tables" "$BASE_DIR/table-types/volatile-tables"
check_section "Lookup Tables" "$BASE_DIR/table-types/lookup-tables"
check_section "SQL Reference" "$BASE_DIR/sql-reference"
check_section "Tools Reference" "$BASE_DIR/tools-reference"
check_section "Configuration" "$BASE_DIR/configuration"
check_section "Advanced Features" "$BASE_DIR/advanced-features"
check_section "Installation" "$BASE_DIR/installation"
check_section "SDK Integration" "$BASE_DIR/sdk-integration"
check_section "Troubleshooting" "$BASE_DIR/troubleshooting"
echo ""

echo "3. CHECKING INDEX FILES"
echo "----------------------------------------"

check_index() {
    local path=$1
    if [ -f "$path/_index.md" ]; then
        echo -e "${GREEN}✓${NC} $path/_index.md"
    else
        echo -e "${RED}✗${NC} $path/_index.md MISSING"
    fi
}

check_index "$BASE_DIR"
check_index "$BASE_DIR/getting-started"
check_index "$BASE_DIR/common-tasks"
check_index "$BASE_DIR/core-concepts"
check_index "$BASE_DIR/tutorials"
check_index "$BASE_DIR/table-types"
check_index "$BASE_DIR/table-types/tag-tables"
check_index "$BASE_DIR/table-types/log-tables"
check_index "$BASE_DIR/table-types/volatile-tables"
check_index "$BASE_DIR/table-types/lookup-tables"
check_index "$BASE_DIR/sql-reference"
check_index "$BASE_DIR/tools-reference"
check_index "$BASE_DIR/configuration"
check_index "$BASE_DIR/advanced-features"
check_index "$BASE_DIR/sdk-integration"
check_index "$BASE_DIR/troubleshooting"
echo ""

echo "4. CHECKING KEY MIGRATED FILES"
echo "----------------------------------------"

check_file() {
    local desc=$1
    local path=$2
    if [ -f "$path" ]; then
        echo -e "${GREEN}✓${NC} $desc"
    else
        echo -e "${RED}✗${NC} $desc - NOT FOUND: $path"
    fi
}

# Tag Tables
check_file "Tag: Creating tables" "$BASE_DIR/table-types/tag-tables/creating-tag-tables.md"
check_file "Tag: Metadata" "$BASE_DIR/table-types/tag-tables/tag-metadata.md"
check_file "Tag: Inserting data" "$BASE_DIR/table-types/tag-tables/inserting-data.md"
check_file "Tag: Querying data" "$BASE_DIR/table-types/tag-tables/querying-data.md"
check_file "Tag: Rollup tables" "$BASE_DIR/table-types/tag-tables/rollup-tables.md"

# SQL Reference
check_file "SQL: Data types" "$BASE_DIR/sql-reference/datatypes.md"
check_file "SQL: DDL" "$BASE_DIR/sql-reference/ddl.md"
check_file "SQL: DML" "$BASE_DIR/sql-reference/dml.md"
check_file "SQL: Functions" "$BASE_DIR/sql-reference/functions.md"

# Tools
check_file "Tools: machsql" "$BASE_DIR/tools-reference/machsql.md"
check_file "Tools: machadmin" "$BASE_DIR/tools-reference/machadmin.md"

# Configuration
check_file "Config: Properties" "$BASE_DIR/configuration/property.md"

# Troubleshooting
check_file "Troubleshooting: Common issues" "$BASE_DIR/troubleshooting/common-issues.md"
check_file "Troubleshooting: Error codes" "$BASE_DIR/troubleshooting/error-code.md"
echo ""

echo "5. CHECKING FRONT MATTER"
echo "----------------------------------------"

# Check if files have proper front matter
MISSING_TITLE=0
for file in $(find "$BASE_DIR" -type f -name "*.md" | head -20); do
    if ! grep -q "^title:" "$file"; then
        echo -e "${YELLOW}⚠${NC} Missing 'title' in: $file"
        MISSING_TITLE=$((MISSING_TITLE + 1))
    fi
done

if [ $MISSING_TITLE -eq 0 ]; then
    echo -e "${GREEN}✓${NC} All checked files have front matter"
else
    echo -e "${YELLOW}⚠${NC} $MISSING_TITLE files might be missing proper front matter"
fi
echo ""

echo "6. CHECKING FOR BROKEN LINKS (Sample)"
echo "----------------------------------------"

# Sample check for old /dbms/ paths in new files
BROKEN_LINKS=0
for file in $(find "$BASE_DIR/table-types/tag-tables" -type f -name "*.md"); do
    if grep -q "/dbms/feature-table" "$file" 2>/dev/null; then
        echo -e "${YELLOW}⚠${NC} Possible broken link in: $(basename $file)"
        BROKEN_LINKS=$((BROKEN_LINKS + 1))
    fi
done

if [ $BROKEN_LINKS -eq 0 ]; then
    echo -e "${GREEN}✓${NC} No broken links detected in tag-tables"
else
    echo -e "${YELLOW}⚠${NC} $BROKEN_LINKS files may have broken links - manual review recommended"
fi
echo ""

echo "7. SUMMARY"
echo "========================================="
echo "Total Files: $TOTAL_FILES"
echo ""
echo "Migration appears to be: "
if [ "$TOTAL_FILES" -ge 100 ]; then
    echo -e "${GREEN}✓ SUCCESSFUL${NC}"
    echo ""
    echo "Next Steps:"
    echo "  1. Review MIGRATION-REPORT.md for details"
    echo "  2. Test Hugo build: hugo server"
    echo "  3. Check for broken internal links"
    echo "  4. Update any cross-references"
    echo "  5. Review and update image paths"
else
    echo -e "${YELLOW}⚠ INCOMPLETE - Review needed${NC}"
fi
echo ""
echo "========================================="
