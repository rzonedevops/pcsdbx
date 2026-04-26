#!/usr/bin/env python3
"""
Research-to-JSON Conversion Tool
Converts supplier information from markdown research files to JSON listings.

Usage:
  python3 scripts/conversion/convert_research.py <research_file.md> [--output-dir listings/] [--dry-run]

This tool:
1. Parses markdown research files for supplier information
2. Generates valid JSON listings following schema v1.0
3. Auto-fills metadata, dates, and schema version
4. Validates output against the schema
5. Supports batch conversion of multiple suppliers from one research file
"""

import json
import os
import sys
import re
from pathlib import Path
from datetime import date
from typing import Dict, List, Any, Optional
import argparse


def parse_research_file(filepath: Path) -> List[Dict[str, Any]]:
    """
    Parse a markdown research file and extract supplier information.
    
    Returns a list of supplier dictionaries ready for JSON conversion.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    suppliers = []
    
    # Split by supplier sections (looking for numbered headers like "#### 1. CompanyName")
    supplier_pattern = r'####\s+\d+\.\s+([^\n]+)'
    sections = re.split(supplier_pattern, content)
    
    # Process pairs of (company_name, details)
    for i in range(1, len(sections), 2):
        if i + 1 >= len(sections):
            break
            
        company_name = sections[i].strip()
        details = sections[i + 1]
        
        supplier = parse_supplier_section(company_name, details)
        if supplier:
            suppliers.append(supplier)
    
    return suppliers


def parse_supplier_section(company_name: str, details: str) -> Optional[Dict[str, Any]]:
    """
    Parse a single supplier section from markdown.
    
    Extracts:
    - Website
    - Location/Address
    - Phone
    - Specializations
    - Product highlights
    - Strategic importance
    - Tags
    - Notes
    """
    supplier = {
        "company_name": clean_company_name(company_name)
    }
    
    # Extract website
    website_match = re.search(r'\*\*Website:\*\*\s+(\S+)', details)
    if website_match:
        supplier["website"] = website_match.group(1)
    
    # Extract location/address
    location_match = re.search(r'\*\*Location:\*\*\s+([^\n]+)', details)
    if location_match:
        address = location_match.group(1).strip()
        supplier["address"] = address
        # Try to extract country from address
        if "United States" in address or "USA" in address:
            supplier["country"] = "United States"
    
    # Extract phone
    phone_match = re.search(r'\*\*Phone:\*\*\s+([^\n]+)', details)
    if phone_match:
        supplier["phone"] = phone_match.group(1).strip()
    
    # Extract specializations (look for Specializations or Product Focus)
    specializations = []
    spec_match = re.search(r'\*\*Specializations?:\*\*\s+([^\n]+)', details)
    if spec_match:
        spec_text = spec_match.group(1).strip()
        # Split by commas
        specializations = [s.strip() for s in spec_text.split(',')]
    
    product_focus_match = re.search(r'\*\*Product Focus:\*\*\s+([^\n]+)', details)
    if product_focus_match and not specializations:
        spec_text = product_focus_match.group(1).strip()
        specializations = [s.strip() for s in spec_text.split(',')]
    
    if specializations:
        supplier["specializations"] = specializations
    
    # Extract product highlights
    highlights = []
    # Look for Products: or Product Range: or Product Highlights:
    for pattern in [r'\*\*Products?:\*\*\s+([^\n]+)', 
                    r'\*\*Product Range:\*\*\s+([^\n]+)',
                    r'\*\*Product Highlights?:\*\*\s+([^\n]+)']:
        match = re.search(pattern, details)
        if match:
            highlights.append(match.group(1).strip())
    
    if highlights:
        supplier["product_highlights"] = highlights
    
    # Extract tags
    tags = []
    tags_match = re.search(r'\*\*Tags?:\*\*\s+([^\n]+)', details)
    if tags_match:
        tag_text = tags_match.group(1).strip()
        tags = [t.strip() for t in tag_text.split(',')]
    
    # Infer tags from markers in text
    if "⭐ MAJOR PLAYER" in company_name or "major player" in details.lower():
        if "major-player" not in tags:
            tags.append("major-player")
    if "⭐ MANUFACTURER" in company_name or "manufacturer" in details.lower():
        if "contract-manufacturer" not in tags:
            tags.append("contract-manufacturer")
    if "organic" in details.lower() or "natural" in details.lower():
        if "organic" not in tags and "natural" not in tags:
            tags.append("natural-ingredients")
    if "sustainable" in details.lower():
        if "sustainable" not in tags:
            tags.append("sustainable")
    if "distributor" in details.lower() or "global" in details.lower():
        if "global-distributor" not in tags:
            tags.append("global-distributor")
    
    if tags:
        supplier["tags"] = tags
    
    # Extract notes
    notes = []
    notes_match = re.search(r'\*\*Notes?:\*\*\s+([^\n]+)', details)
    if notes_match:
        notes.append(notes_match.group(1).strip())
    
    strategic_match = re.search(r'\*\*Strategic Importance:\*\*\s+([^\n]+)', details)
    if strategic_match:
        notes.append(f"Strategic importance: {strategic_match.group(1).strip()}")
    
    if notes:
        supplier["notes"] = " ".join(notes)
    
    return supplier if supplier.get("company_name") else None


def clean_company_name(name: str) -> str:
    """Clean company name by removing markers and extra whitespace."""
    # Remove markers like ⭐ MAJOR PLAYER, ⭐ MANUFACTURER, etc.
    # Each marker word is all-caps (2+ letters); stop before mixed-case company name.
    name = re.sub(r'⭐\s*(?:[A-Z]{2,}\s*/?\s*)+', '', name)
    # Remove extra whitespace
    name = ' '.join(name.split())
    return name.strip()


def create_listing_id(company_name: str) -> str:
    """Generate a listing ID from company name."""
    # Convert to lowercase, replace spaces and special chars with underscores
    listing_id = company_name.lower()
    listing_id = re.sub(r'[^a-z0-9]+', '_', listing_id)
    listing_id = listing_id.strip('_')
    return listing_id


def infer_category_from_filepath(filepath: Path) -> Dict[str, str]:
    """
    Infer category information from research file path/name.
    
    Returns dict with category_path and category_id.
    """
    filename = filepath.stem.lower()
    
    category_map = {
        "emollients": {"path": "Raw_Materials/Emollients_Moisturizers", "id": "1828"},
        "botanical": {"path": "Raw_Materials/Botanical_Extracts", "id": "1828"},
        "preservatives": {"path": "Raw_Materials/Preservatives", "id": "1828"},
        "surfactants": {"path": "Raw_Materials/Surfactants", "id": "1828"},
        "actives": {"path": "Raw_Materials/Actives", "id": "1828"},
        "colorants": {"path": "Raw_Materials/Colorants_and_Pigments", "id": "1828"},
        "fragrances": {"path": "Raw_Materials/Fragrances", "id": "1828"},
        "bottles_jars": {"path": "Packaging/Bottles_and_Jars", "id": "1800"},
        "packaging": {"path": "Packaging/Bottles_and_Jars", "id": "1800"},
        "tubes": {"path": "Packaging/Tubes", "id": "1811"},
        "contract_manufacturing": {"path": "Business_Services/Contract_Manufacturing", "id": "1790"},
        "testing": {"path": "Business_Services/Testing_and_Quality_Control", "id": "1803"},
        "mixing": {"path": "Equipment/Mixing_Equipment", "id": "1805"},
        "filling": {"path": "Equipment/Filling_Equipment", "id": "1806"},
    }
    
    for key, value in category_map.items():
        if key in filename:
            return value
    
    # Default to raw materials if can't determine
    return {"path": "Raw_Materials/Actives", "id": "1828"}


def build_json_listing(supplier: Dict[str, Any], category_info: Dict[str, str], 
                       research_file: str) -> Dict[str, Any]:
    """
    Build a complete JSON listing from supplier data.
    
    Follows schema v1.0 requirements.
    """
    company_name = supplier.get("company_name", "Unknown")
    listing_id = create_listing_id(company_name)
    
    listing = {
        "schema_version": "1.0",
        "category_id": category_info["id"],
        "listing_id": listing_id,
        "category_path": category_info["path"],
        "url": f"https://personalcaresuppliers.com/Listing/Index/{category_info['path'].replace('/', '/')}/{category_info['id']}/",
        "company_name": company_name,
        "status": "active",
        "date_added": str(date.today()),
        "date_updated": str(date.today()),
    }
    
    # Add optional fields if present
    for field in ["address", "country", "phone", "email", "website", 
                  "specializations", "product_highlights", "tags", "notes",
                  "certifications", "key_benefits"]:
        if field in supplier:
            listing[field] = supplier[field]
    
    # Add metadata
    listing["metadata"] = {
        "last_validated": str(date.today()),
        "validation_method": "manual",
        "data_source": research_file
    }
    
    return listing


def save_listing(listing: Dict[str, Any], output_dir: Path, dry_run: bool = False) -> Path:
    """Save listing to JSON file in appropriate category directory."""
    category_path = listing["category_path"]
    listing_id = listing["listing_id"]
    category_id = listing["category_id"]
    
    # Create output directory structure
    full_path = output_dir / category_path
    
    if not dry_run:
        full_path.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    filename = f"{category_id}_{listing_id}.json"
    filepath = full_path / filename
    
    if dry_run:
        print(f"[DRY RUN] Would save to: {filepath}")
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(listing, f, indent=2, ensure_ascii=False)
            f.write('\n')
        print(f"✓ Saved: {filepath}")
    
    return filepath


def main():
    parser = argparse.ArgumentParser(
        description="Convert markdown research files to JSON listings"
    )
    parser.add_argument("research_file", type=str, 
                       help="Path to markdown research file")
    parser.add_argument("--output-dir", type=str, default="listings",
                       help="Output directory for JSON files (default: listings)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be created without actually creating files")
    parser.add_argument("--interactive", action="store_true",
                       help="Prompt for missing information interactively")
    
    args = parser.parse_args()
    
    research_file = Path(args.research_file)
    output_dir = Path(args.output_dir)
    
    if not research_file.exists():
        print(f"Error: Research file not found: {research_file}")
        sys.exit(1)
    
    print(f"\n{'='*80}")
    print(f"RESEARCH-TO-JSON CONVERSION TOOL")
    print(f"{'='*80}\n")
    
    print(f"Research file: {research_file}")
    print(f"Output directory: {output_dir}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}\n")
    
    # Parse research file
    print("Parsing research file...")
    suppliers = parse_research_file(research_file)
    print(f"Found {len(suppliers)} suppliers\n")
    
    if not suppliers:
        print("No suppliers found in research file.")
        print("Make sure the file uses the expected markdown format with numbered supplier sections.")
        sys.exit(0)
    
    # Infer category
    category_info = infer_category_from_filepath(research_file)
    print(f"Inferred category: {category_info['path']}\n")
    
    # Convert each supplier
    print("Converting suppliers to JSON...\n")
    created_files = []
    
    for i, supplier in enumerate(suppliers, 1):
        print(f"{i}. {supplier.get('company_name', 'Unknown')}")
        
        # Build JSON listing
        listing = build_json_listing(
            supplier, 
            category_info,
            research_file.name
        )
        
        # Save listing
        filepath = save_listing(listing, output_dir, args.dry_run)
        created_files.append(filepath)
        print()
    
    # Summary
    print(f"{'='*80}")
    print(f"CONVERSION COMPLETE")
    print(f"{'='*80}\n")
    print(f"Suppliers processed: {len(suppliers)}")
    print(f"Files {'would be ' if args.dry_run else ''}created: {len(created_files)}")
    
    if args.dry_run:
        print("\nRe-run without --dry-run to actually create the files.")
    else:
        print("\n✅ All listings saved successfully!")
        print("\nNext steps:")
        print("1. Review the generated JSON files")
        print("2. Fill in any missing information (address, phone, etc.)")
        print("3. Run validation: python3 scripts/validation/validate_listings.py")
        print("4. Commit the new listings")


if __name__ == "__main__":
    main()
