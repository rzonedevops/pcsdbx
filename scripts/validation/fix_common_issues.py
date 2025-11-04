#!/usr/bin/env python3
"""
Quality Enhancement Script
Automatically fixes common validation issues in supplier listings.

Usage:
  python3 scripts/validation/fix_common_issues.py [--dry-run] [--verbose]

This script fixes:
1. Missing schema_version field (adds "1.0")
2. String product_highlights (converts to array)
3. Invalid extra fields (removes city, state, zip)
4. Invalid tag values (removes non-standard tags)
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Set

# Valid tag values from schema
VALID_TAGS = {
    "oat-specialist",
    "organic",
    "sustainable",
    "small-batch",
    "major-player",
    "biotechnology",
    "natural-ingredients",
    "certified",
    "global-distributor",
    "contract-manufacturer",
    "private-label",
    "full-service"
}

# Fields that should be removed (not in schema)
INVALID_FIELDS = {"city", "state", "zip", "postal_code"}


def load_json_file(filepath: Path) -> Dict[str, Any]:
    """Load a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(filepath: Path, data: Dict[str, Any]) -> None:
    """Save data to JSON file with consistent formatting."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')  # Add trailing newline


def fix_missing_schema_version(data: Dict[str, Any]) -> bool:
    """Add schema_version if missing. Returns True if changed."""
    if 'schema_version' not in data:
        data['schema_version'] = "1.0"
        return True
    return False


def fix_product_highlights_type(data: Dict[str, Any]) -> bool:
    """Convert product_highlights from string to array. Returns True if changed."""
    if 'product_highlights' in data and isinstance(data['product_highlights'], str):
        # Convert string to single-item array
        data['product_highlights'] = [data['product_highlights']]
        return True
    return False


def fix_invalid_fields(data: Dict[str, Any]) -> bool:
    """Remove invalid fields. Returns True if changed."""
    changed = False
    for field in INVALID_FIELDS:
        if field in data:
            del data[field]
            changed = True
    return changed


def fix_invalid_tags(data: Dict[str, Any]) -> bool:
    """Remove invalid tag values. Returns True if changed."""
    if 'tags' not in data or not isinstance(data['tags'], list):
        return False
    
    original_tags = set(data['tags'])
    valid_tags = [tag for tag in data['tags'] if tag in VALID_TAGS]
    
    if len(valid_tags) != len(original_tags):
        data['tags'] = valid_tags
        return True
    return False


def process_listing(filepath: Path, dry_run: bool = False, verbose: bool = False) -> Dict[str, int]:
    """
    Process a single listing file and fix common issues.
    
    Returns dict with counts of fixes applied.
    """
    stats = {
        'schema_version': 0,
        'product_highlights': 0,
        'invalid_fields': 0,
        'invalid_tags': 0
    }
    
    try:
        data = load_json_file(filepath)
        
        # Apply fixes
        if fix_missing_schema_version(data):
            stats['schema_version'] = 1
        
        if fix_product_highlights_type(data):
            stats['product_highlights'] = 1
        
        if fix_invalid_fields(data):
            stats['invalid_fields'] = 1
        
        if fix_invalid_tags(data):
            stats['invalid_tags'] = 1
        
        # Save if any changes were made and not in dry-run mode
        total_changes = sum(stats.values())
        if total_changes > 0:
            if verbose or dry_run:
                changes = [k for k, v in stats.items() if v > 0]
                status = "[DRY RUN] " if dry_run else ""
                print(f"  {status}Fixed {filepath.name}: {', '.join(changes)}")
            
            if not dry_run:
                save_json_file(filepath, data)
        
        return stats
        
    except Exception as e:
        print(f"  ❌ Error processing {filepath.name}: {e}")
        return {k: 0 for k in stats.keys()}


def find_all_listings(base_dir: Path) -> List[Path]:
    """Find all JSON listing files."""
    listings = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.json'):
                listings.append(Path(root) / file)
    return sorted(listings)


def main():
    """Main execution function."""
    # Parse command line arguments
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv or dry_run
    
    # Setup paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    listings_dir = repo_root / 'listings'
    
    if not listings_dir.exists():
        print(f"❌ Listings directory not found: {listings_dir}")
        sys.exit(1)
    
    print("Quality Enhancement Script")
    print("=" * 80)
    if dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
        print()
    
    # Find all listings
    listing_files = find_all_listings(listings_dir)
    print(f"Found {len(listing_files)} listing files\n")
    
    # Process each listing
    total_stats = {
        'schema_version': 0,
        'product_highlights': 0,
        'invalid_fields': 0,
        'invalid_tags': 0,
        'files_processed': 0,
        'files_changed': 0
    }
    
    print("Processing listings...")
    for filepath in listing_files:
        stats = process_listing(filepath, dry_run=dry_run, verbose=verbose)
        total_stats['files_processed'] += 1
        
        if sum(stats.values()) > 0:
            total_stats['files_changed'] += 1
            for key in stats:
                total_stats[key] += stats[key]
    
    # Print summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Files processed: {total_stats['files_processed']}")
    print(f"Files changed: {total_stats['files_changed']}")
    print()
    print("Fixes applied:")
    print(f"  - Added schema_version: {total_stats['schema_version']} files")
    print(f"  - Fixed product_highlights type: {total_stats['product_highlights']} files")
    print(f"  - Removed invalid fields: {total_stats['invalid_fields']} files")
    print(f"  - Fixed invalid tags: {total_stats['invalid_tags']} files")
    
    if dry_run:
        print()
        print("🔍 This was a DRY RUN - no files were actually modified.")
        print("   Run without --dry-run to apply these fixes.")
    else:
        print()
        print("✅ Quality enhancement complete!")
        print("   Run validation script to verify fixes: python3 scripts/validation/validate_listings.py")


if __name__ == '__main__':
    main()
