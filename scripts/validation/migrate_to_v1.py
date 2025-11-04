#!/usr/bin/env python3
"""
Migration tool to update existing listings to schema version 1.0.

This script adds required fields to existing listings:
- schema_version: "1.0"
- date_updated: (same as date_added if not present)
- metadata: {last_validated, validation_method}
- tags: [] (for strategic suppliers)
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Set


def migrate_listing(file_path: Path, dry_run: bool = False) -> bool:
    """
    Migrate a single listing to schema version 1.0.
    
    Args:
        file_path: Path to the listing file
        dry_run: If True, don't write changes
        
    Returns:
        True if changes were made
    """
    # Load the file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    changes_made = False
    
    # Add schema_version if missing
    if "schema_version" not in data:
        data["schema_version"] = "1.0"
        changes_made = True
    
    # Add date_updated if missing
    if "date_updated" not in data:
        # Use date_added if available, otherwise use today
        data["date_updated"] = data.get("date_added", datetime.now().strftime("%Y-%m-%d"))
        changes_made = True
    
    # Add metadata if missing
    if "metadata" not in data:
        data["metadata"] = {
            "last_validated": datetime.now().strftime("%Y-%m-%d"),
            "validation_method": "manual",
            "data_source": "manual_entry"
        }
        changes_made = True
    
    # Determine if this is a strategic supplier and add tags
    if "tags" not in data:
        tags = []
        
        # Check for oat specialist
        company_name = data.get("company_name", "").lower()
        specializations = [s.lower() for s in data.get("specializations", [])]
        notes = data.get("notes", "").lower()
        
        if "oat" in company_name or any("oat" in s for s in specializations):
            tags.append("oat-specialist")
        
        # Check for major players
        major_players = ["ashland", "lonza", "givaudan", "lucas meyer", "solabia"]
        if any(player in company_name for player in major_players):
            tags.append("major-player")
        
        # Check for organic/sustainable
        certifications = [c.lower() for c in data.get("certifications", [])]
        if any("organic" in c for c in certifications):
            tags.append("organic")
        if any("sustainable" in c for c in certifications) or "sustainable" in notes:
            tags.append("sustainable")
        
        # Check for biotechnology
        if "biotechnology" in notes or any("biotech" in s for s in specializations):
            tags.append("biotechnology")
        
        # Check for natural ingredients
        if any("natural" in s for s in specializations) or any("natural" in c for c in certifications):
            tags.append("natural-ingredients")
        
        # Check for certifications
        if certifications:
            tags.append("certified")
        
        # Check for contract manufacturing
        category_path = data.get("category_path", "")
        if "Contract_Manufacturing" in category_path:
            tags.append("contract-manufacturer")
        
        # Only add tags if we found any
        if tags:
            data["tags"] = tags
            changes_made = True
    
    # Write back if changes were made and not dry run
    if changes_made and not dry_run:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')  # Add trailing newline
    
    return changes_made


def find_all_listings(root_dir: Path) -> list:
    """Find all listing JSON files in the repository."""
    listings_dir = root_dir / "listings"
    if not listings_dir.exists():
        return []
    
    return list(listings_dir.rglob("*.json"))


def main():
    """Main entry point for the migration tool."""
    # Parse arguments
    dry_run = "--dry-run" in sys.argv
    
    # Find repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    
    # Find all listings
    print("Finding listings...")
    listings = find_all_listings(repo_root)
    print(f"Found {len(listings)} listing files")
    
    if not listings:
        print("No listings found!")
        return 1
    
    if dry_run:
        print("\n🔍 DRY RUN MODE - No files will be modified\n")
    
    # Migrate each listing
    print("\nMigrating listings to schema version 1.0...")
    migrated_count = 0
    
    for listing_path in listings:
        rel_path = listing_path.relative_to(repo_root)
        changed = migrate_listing(listing_path, dry_run=dry_run)
        
        if changed:
            migrated_count += 1
            status = "🔄" if dry_run else "✓"
            print(f"  {status} {rel_path}")
        else:
            print(f"  ⊝ {rel_path} (already migrated)")
    
    print(f"\n{'Would migrate' if dry_run else 'Migrated'} {migrated_count} out of {len(listings)} listings")
    
    if dry_run:
        print("\nRun without --dry-run flag to apply changes")
    else:
        print("\n✅ Migration complete!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
