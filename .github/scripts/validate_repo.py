#!/usr/bin/env python3
"""Validate repository structure and data quality."""

import json
import os
import sys
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

LISTINGS_DIR = "listings"
REQUIRED_FIELDS = [
    'id', 'name', 'website', 'category', 'subcategory',
    'description', 'headquarters', 'products', 'certifications',
    'geographic_coverage', 'specializations', 'date_added', 'last_updated'
]

def validate_json_schema(filepath):
    """Validate JSON file against schema."""
    errors = []
    warnings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f'Invalid JSON: {e}'], []
    except Exception as e:
        return [f'Error reading file: {e}'], []
    
    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f'Missing required field: {field}')
        elif not data[field] and field != 'certifications':  # certifications can be empty array
            errors.append(f'Empty required field: {field}')
    
    # Check array minimums
    if 'products' in data:
        if not isinstance(data['products'], list):
            errors.append(f'products must be an array')
        elif len(data['products']) < 3:
            errors.append(f'products array must have at least 3 items (has {len(data["products"])})')
    
    if 'specializations' in data:
        if not isinstance(data['specializations'], list):
            errors.append(f'specializations must be an array')
        elif len(data['specializations']) < 2:
            errors.append(f'specializations array must have at least 2 items (has {len(data["specializations"])})')
    
    if 'geographic_coverage' in data:
        if not isinstance(data['geographic_coverage'], list):
            errors.append(f'geographic_coverage must be an array')
        elif len(data['geographic_coverage']) < 1:
            errors.append(f'geographic_coverage array must have at least 1 item')
    
    # Check date formats
    for date_field in ['date_added', 'last_updated']:
        if date_field in data:
            if not isinstance(data[date_field], str):
                errors.append(f'{date_field} must be a string')
            elif not re.match(r'^\d{4}-\d{2}-\d{2}$', data[date_field]):
                errors.append(f'{date_field} must be in YYYY-MM-DD format (got: {data[date_field]})')
    
    # Check headquarters format
    if 'headquarters' in data:
        if not isinstance(data['headquarters'], str):
            errors.append(f'headquarters must be a string')
        elif ',' not in data['headquarters']:
            warnings.append(f'headquarters should be in "City, Country" format')
    
    # Check website format
    if 'website' in data:
        if not isinstance(data['website'], str):
            errors.append(f'website must be a string')
        elif not data['website'].startswith(('http://', 'https://')):
            warnings.append(f'website should start with http:// or https://')
    
    # Check description length
    if 'description' in data and isinstance(data['description'], str):
        sentences = data['description'].count('.') + data['description'].count('!') + data['description'].count('?')
        if sentences > 3:
            warnings.append(f'description should be 1-2 sentences (appears to have {sentences})')
    
    return errors, warnings

def validate_repository():
    """Validate entire repository."""
    report = {
        'total_files': 0,
        'valid_files': 0,
        'files_with_errors': 0,
        'files_with_warnings': 0,
        'errors': {},
        'warnings': {},
        'duplicate_ids': [],
        'category_counts': defaultdict(int),
        'subcategory_counts': defaultdict(lambda: defaultdict(int))
    }
    
    seen_ids = {}
    listings_path = Path(LISTINGS_DIR)
    
    if not listings_path.exists():
        print(f"Listings directory not found: {LISTINGS_DIR}", file=sys.stderr)
        return report
    
    for filepath in listings_path.rglob('*.json'):
        report['total_files'] += 1
        
        errors, warnings = validate_json_schema(filepath)
        
        if errors:
            report['files_with_errors'] += 1
            report['errors'][str(filepath.relative_to(listings_path))] = errors
        
        if warnings:
            report['files_with_warnings'] += 1
            report['warnings'][str(filepath.relative_to(listings_path))] = warnings
        
        if not errors:
            report['valid_files'] += 1
        
        # Check for duplicate IDs and collect stats
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if 'id' in data:
                    if data['id'] in seen_ids:
                        report['duplicate_ids'].append({
                            'id': data['id'],
                            'files': [seen_ids[data['id']], str(filepath.relative_to(listings_path))]
                        })
                    seen_ids[data['id']] = str(filepath.relative_to(listings_path))
                
                if 'category' in data:
                    report['category_counts'][data['category']] += 1
                    
                    if 'subcategory' in data:
                        report['subcategory_counts'][data['category']][data['subcategory']] += 1
        except Exception as e:
            pass  # Already caught in validation
    
    return report

def generate_report(report):
    """Generate markdown report."""
    lines = []
    
    lines.append("# Repository Validation Report")
    lines.append(f"\n**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    
    lines.append("## Summary\n")
    lines.append(f"- **Total Files:** {report['total_files']}")
    lines.append(f"- **Valid Files:** {report['valid_files']}")
    lines.append(f"- **Files with Errors:** {report['files_with_errors']}")
    lines.append(f"- **Files with Warnings:** {report['files_with_warnings']}")
    
    if report['files_with_errors'] == 0:
        lines.append("\n✅ **All files passed validation!**\n")
    else:
        lines.append(f"\n⚠️ **{report['files_with_errors']} file(s) have errors**\n")
    
    # Duplicate IDs
    if report['duplicate_ids']:
        lines.append("## ❌ Duplicate IDs\n")
        for dup in report['duplicate_ids']:
            lines.append(f"- **ID `{dup['id']}`** found in:")
            for f in dup['files']:
                lines.append(f"  - `{f}`")
        lines.append("")
    
    # Errors
    if report['errors']:
        lines.append("## ❌ Validation Errors\n")
        for filepath, errors in sorted(report['errors'].items()):
            lines.append(f"### `{filepath}`\n")
            for error in errors:
                lines.append(f"- {error}")
            lines.append("")
    
    # Warnings
    if report['warnings']:
        lines.append("## ⚠️ Warnings\n")
        for filepath, warnings in sorted(report['warnings'].items()):
            lines.append(f"### `{filepath}`\n")
            for warning in warnings:
                lines.append(f"- {warning}")
            lines.append("")
    
    # Statistics
    lines.append("## 📊 Statistics\n")
    lines.append("### Categories\n")
    for category, count in sorted(report['category_counts'].items()):
        lines.append(f"- **{category}:** {count} listings")
    
    lines.append("\n### Subcategories by Category\n")
    for category in sorted(report['subcategory_counts'].keys()):
        lines.append(f"\n**{category}:**")
        for subcategory, count in sorted(report['subcategory_counts'][category].items()):
            lines.append(f"- {subcategory}: {count}")
    
    return '\n'.join(lines)

def main():
    """Main entry point."""
    
    print("Running repository validation...")
    report = validate_repository()
    
    print(f"\nValidation Summary:")
    print(f"  Total files: {report['total_files']}")
    print(f"  Valid files: {report['valid_files']}")
    print(f"  Files with errors: {report['files_with_errors']}")
    print(f"  Files with warnings: {report['files_with_warnings']}")
    
    if report['duplicate_ids']:
        print(f"  Duplicate IDs: {len(report['duplicate_ids'])}")
    
    # Generate full report
    report_md = generate_report(report)
    
    # Save report
    report_path = Path('.github/maintenance_report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_md)
    
    print(f"\nFull report saved to: {report_path}")
    
    # Output for GitHub Actions
    github_output = os.getenv('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            issues_found = 'true' if (report['files_with_errors'] > 0 or report['duplicate_ids']) else 'false'
            f.write(f"issues_found={issues_found}\n")
            f.write(f"total_files={report['total_files']}\n")
            f.write(f"valid_files={report['valid_files']}\n")
            f.write(f"error_count={report['files_with_errors']}\n")
    
    # Exit with error if critical issues found
    if report['files_with_errors'] > 0 or report['duplicate_ids']:
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
