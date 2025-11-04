#!/usr/bin/env python3
"""
Validation tool for Personal Care Suppliers Database listings.

This script validates JSON listing files against the defined schema and
performs additional business logic validation checks.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any
import re


def load_schema() -> Dict:
    """Load the JSON schema for validation."""
    schema_path = Path(__file__).parent / "listing_schema.json"
    with open(schema_path, 'r') as f:
        return json.load(f)


def load_listing(file_path: Path) -> Tuple[Dict, List[str]]:
    """
    Load a listing JSON file.
    
    Returns:
        Tuple of (data dict, list of errors)
    """
    errors = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data, errors
    except json.JSONDecodeError as e:
        errors.append(f"JSON parsing error: {e}")
        return {}, errors
    except Exception as e:
        errors.append(f"Error reading file: {e}")
        return {}, errors


def validate_schema(data: Dict, schema: Dict) -> List[str]:
    """
    Validate data against JSON schema.
    
    Note: This is a basic implementation. For production use,
    consider using the jsonschema library.
    """
    errors = []
    
    # Check required fields
    required = schema.get("required", [])
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Validate field types and patterns
    properties = schema.get("properties", {})
    for field, value in data.items():
        if field not in properties:
            if not schema.get("additionalProperties", True):
                errors.append(f"Unexpected field: {field}")
            continue
        
        field_schema = properties[field]
        
        # Type validation
        expected_type = field_schema.get("type")
        if expected_type:
            if isinstance(expected_type, list):
                valid_type = any(check_type(value, t) for t in expected_type)
            else:
                valid_type = check_type(value, expected_type)
            
            if not valid_type:
                errors.append(f"Field '{field}' has incorrect type. Expected {expected_type}, got {type(value).__name__}")
        
        # Pattern validation
        if "pattern" in field_schema and isinstance(value, str):
            pattern = field_schema["pattern"]
            if not re.match(pattern, value):
                errors.append(f"Field '{field}' does not match required pattern: {pattern}")
        
        # Enum validation
        if "enum" in field_schema:
            if value not in field_schema["enum"]:
                errors.append(f"Field '{field}' value '{value}' not in allowed values: {field_schema['enum']}")
        
        # Array items validation
        if field_schema.get("type") == "array" and "items" in field_schema:
            if isinstance(value, list):
                items_schema = field_schema["items"]
                if "enum" in items_schema:
                    for item in value:
                        if item not in items_schema["enum"]:
                            errors.append(f"Array item '{item}' in field '{field}' not in allowed values")
    
    return errors


def check_type(value: Any, expected_type: str) -> bool:
    """Check if value matches the expected JSON schema type."""
    type_map = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
        "array": list,
        "object": dict,
        "null": type(None)
    }
    expected_python_type = type_map.get(expected_type)
    if expected_python_type is None:
        return True
    return isinstance(value, expected_python_type)


def validate_business_logic(data: Dict, file_path: Path) -> List[str]:
    """
    Validate business logic rules beyond schema validation.
    
    Args:
        data: The listing data
        file_path: Path to the listing file
        
    Returns:
        List of validation errors
    """
    errors = []
    
    # Validate file naming convention
    filename = file_path.name
    expected_pattern = r"^\d+_[\w\d_]+\.json$"
    if not re.match(expected_pattern, filename):
        errors.append(f"Filename does not match pattern: {expected_pattern}")
    
    # Validate filename matches category_id and listing_id
    if "_" in filename:
        parts = filename.replace(".json", "").split("_", 1)
        if len(parts) == 2:
            file_category_id, file_listing_id = parts
            
            data_category_id = str(data.get("category_id", ""))
            data_listing_id = str(data.get("listing_id", ""))
            
            if file_category_id != data_category_id:
                errors.append(f"Filename category_id '{file_category_id}' does not match data category_id '{data_category_id}'")
            
            if file_listing_id != data_listing_id:
                errors.append(f"Filename listing_id '{file_listing_id}' does not match data listing_id '{data_listing_id}'")
    
    # Validate category_path matches directory structure
    if "category_path" in data:
        expected_dir = Path("listings") / data["category_path"]
        actual_dir = file_path.parent
        
        # Compare relative to listings directory
        repo_root = find_repo_root(file_path)
        if repo_root:
            expected_full = repo_root / expected_dir
            if actual_dir != expected_full:
                errors.append(f"File location does not match category_path. Expected: {expected_dir}, Got: {actual_dir.relative_to(repo_root)}")
    
    # Validate date formats
    for date_field in ["date_added", "date_updated"]:
        if date_field in data:
            try:
                datetime.strptime(data[date_field], "%Y-%m-%d")
            except ValueError:
                errors.append(f"Invalid date format in '{date_field}': {data[date_field]} (expected YYYY-MM-DD)")
    
    # Validate URL format
    if "url" in data:
        url = data["url"]
        if not url.startswith("http://") and not url.startswith("https://"):
            errors.append(f"URL does not start with http:// or https://: {url}")
    
    # Check for strategic suppliers requirements
    tags = data.get("tags", [])
    if "oat-specialist" in tags or "major-player" in tags:
        # Strategic suppliers should have enhanced fields
        enhanced_fields = ["company_name", "specializations", "certifications"]
        missing_enhanced = [f for f in enhanced_fields if f not in data or not data[f]]
        if missing_enhanced:
            errors.append(f"Strategic supplier missing recommended enhanced fields: {missing_enhanced}")
    
    return errors


def find_repo_root(file_path: Path) -> Path:
    """Find the repository root directory."""
    current = file_path.parent
    while current != current.parent:
        if (current / "listings").exists():
            return current
        current = current.parent
    return None


def validate_listing(file_path: Path, schema: Dict) -> Tuple[bool, List[str]]:
    """
    Validate a single listing file.
    
    Returns:
        Tuple of (is_valid, list of errors)
    """
    all_errors = []
    
    # Load the file
    data, load_errors = load_listing(file_path)
    all_errors.extend(load_errors)
    
    if load_errors:
        return False, all_errors
    
    # Schema validation
    schema_errors = validate_schema(data, schema)
    all_errors.extend(schema_errors)
    
    # Business logic validation
    business_errors = validate_business_logic(data, file_path)
    all_errors.extend(business_errors)
    
    return len(all_errors) == 0, all_errors


def find_all_listings(root_dir: Path) -> List[Path]:
    """Find all listing JSON files in the repository."""
    listings_dir = root_dir / "listings"
    if not listings_dir.exists():
        return []
    
    return list(listings_dir.rglob("*.json"))


def generate_report(results: Dict[Path, Tuple[bool, List[str]]]) -> str:
    """Generate a validation report."""
    total = len(results)
    valid = sum(1 for is_valid, _ in results.values() if is_valid)
    invalid = total - valid
    
    report = []
    report.append("=" * 80)
    report.append("PERSONAL CARE SUPPLIERS DATABASE - VALIDATION REPORT")
    report.append("=" * 80)
    report.append("")
    report.append(f"Total listings validated: {total}")
    report.append(f"Valid listings: {valid} ({valid/total*100:.1f}%)" if total > 0 else "Valid listings: 0")
    report.append(f"Invalid listings: {invalid} ({invalid/total*100:.1f}%)" if total > 0 else "Invalid listings: 0")
    report.append("")
    
    if invalid > 0:
        report.append("=" * 80)
        report.append("VALIDATION ERRORS")
        report.append("=" * 80)
        report.append("")
        
        for file_path, (is_valid, errors) in results.items():
            if not is_valid:
                report.append(f"File: {file_path}")
                for error in errors:
                    report.append(f"  ❌ {error}")
                report.append("")
    
    # Quality metrics
    report.append("=" * 80)
    report.append("QUALITY METRICS")
    report.append("=" * 80)
    report.append("")
    
    # Count listings with enhanced fields
    enhanced_count = 0
    schema_version_count = 0
    tags_count = 0
    metadata_count = 0
    
    for file_path, (is_valid, _) in results.items():
        if is_valid:
            data, _ = load_listing(file_path)
            if data.get("company_name"):
                enhanced_count += 1
            if data.get("schema_version"):
                schema_version_count += 1
            if data.get("tags"):
                tags_count += 1
            if data.get("metadata"):
                metadata_count += 1
    
    report.append(f"Listings with schema_version: {schema_version_count}/{total} ({schema_version_count/total*100:.1f}%)" if total > 0 else "Listings with schema_version: 0")
    report.append(f"Listings with enhanced fields: {enhanced_count}/{total} ({enhanced_count/total*100:.1f}%)" if total > 0 else "Listings with enhanced fields: 0")
    report.append(f"Listings with tags: {tags_count}/{total} ({tags_count/total*100:.1f}%)" if total > 0 else "Listings with tags: 0")
    report.append(f"Listings with metadata: {metadata_count}/{total} ({metadata_count/total*100:.1f}%)" if total > 0 else "Listings with metadata: 0")
    report.append("")
    
    report.append("=" * 80)
    
    return "\n".join(report)


def main():
    """Main entry point for the validation tool."""
    # Find repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    
    # Load schema
    print("Loading schema...")
    schema = load_schema()
    
    # Find all listings
    print("Finding listings...")
    listings = find_all_listings(repo_root)
    print(f"Found {len(listings)} listing files")
    
    if not listings:
        print("No listings found!")
        return 1
    
    # Validate each listing
    print("\nValidating listings...")
    results = {}
    for listing_path in listings:
        is_valid, errors = validate_listing(listing_path, schema)
        results[listing_path] = (is_valid, errors)
        
        # Print progress
        status = "✓" if is_valid else "✗"
        rel_path = listing_path.relative_to(repo_root)
        print(f"  {status} {rel_path}")
    
    # Generate and print report
    print("\n")
    report = generate_report(results)
    print(report)
    
    # Save report to file
    report_path = repo_root / "validation_report.txt"
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"\nReport saved to: {report_path}")
    
    # Return exit code
    invalid_count = sum(1 for is_valid, _ in results.values() if not is_valid)
    return 0 if invalid_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
