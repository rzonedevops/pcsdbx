#!/usr/bin/env python3
"""
Tests for the validation tools.

Run with: python3 -m pytest tests/test_validation.py -v
Or simply: python3 tests/test_validation.py
"""

import json
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "validation"))

from validate_listings import (
    load_schema,
    validate_schema,
    validate_business_logic,
    load_listing,
    check_type
)


def test_load_schema():
    """Test that schema loads correctly."""
    schema = load_schema()
    assert schema is not None
    assert "required" in schema
    assert "properties" in schema
    assert "schema_version" in schema["required"]
    print("✓ Schema loads correctly")


def test_check_type():
    """Test type checking function."""
    assert check_type("test", "string") == True
    assert check_type(123, "integer") == True
    assert check_type(123.45, "number") == True
    assert check_type(True, "boolean") == True
    assert check_type([], "array") == True
    assert check_type({}, "object") == True
    assert check_type(None, "null") == True
    
    assert check_type("test", "integer") == False
    assert check_type(123, "string") == False
    print("✓ Type checking works correctly")


def test_valid_listing():
    """Test validation of a valid listing."""
    schema = load_schema()
    fixture_path = Path(__file__).parent / "fixtures" / "valid_listing.json"
    
    data, load_errors = load_listing(fixture_path)
    assert len(load_errors) == 0, "Should load without errors"
    
    schema_errors = validate_schema(data, schema)
    assert len(schema_errors) == 0, f"Should validate without schema errors, got: {schema_errors}"
    
    print("✓ Valid listing passes validation")


def test_invalid_listing_missing_schema():
    """Test validation of listing missing schema_version."""
    schema = load_schema()
    fixture_path = Path(__file__).parent / "fixtures" / "invalid_listing_missing_schema.json"
    
    data, load_errors = load_listing(fixture_path)
    assert len(load_errors) == 0, "Should load without errors"
    
    schema_errors = validate_schema(data, schema)
    assert len(schema_errors) > 0, "Should have validation errors"
    
    # Check that schema_version error is present
    has_schema_error = any("schema_version" in error for error in schema_errors)
    assert has_schema_error, "Should have error about missing schema_version"
    
    print("✓ Invalid listing (missing schema) fails validation")


def test_strategic_supplier():
    """Test validation of strategic supplier with enhanced fields."""
    schema = load_schema()
    fixture_path = Path(__file__).parent / "fixtures" / "strategic_supplier.json"
    
    data, load_errors = load_listing(fixture_path)
    assert len(load_errors) == 0, "Should load without errors"
    
    schema_errors = validate_schema(data, schema)
    assert len(schema_errors) == 0, f"Should validate without schema errors, got: {schema_errors}"
    
    # Check strategic supplier fields
    assert "tags" in data
    assert "oat-specialist" in data["tags"]
    assert "certifications" in data
    assert "metadata" in data
    assert "quality_score" in data["metadata"]
    
    print("✓ Strategic supplier with enhanced fields validates correctly")


def test_required_fields():
    """Test that all required fields are checked."""
    schema = load_schema()
    required_fields = schema["required"]
    
    # Create minimal data with only some required fields
    data = {
        "schema_version": "1.0",
        "category_id": 1828,
        "listing_id": "test"
        # Missing other required fields
    }
    
    errors = validate_schema(data, schema)
    assert len(errors) > 0, "Should have errors for missing required fields"
    
    # Check that errors mention missing fields
    for field in ["category_path", "url", "status", "date_added"]:
        has_error = any(field in error for error in errors)
        assert has_error, f"Should have error for missing {field}"
    
    print("✓ Required fields are properly validated")


def test_enum_validation():
    """Test that enum values are validated."""
    schema = load_schema()
    
    # Test with invalid status
    data = {
        "schema_version": "1.0",
        "category_id": 1828,
        "listing_id": "test",
        "category_path": "Raw_Materials/Actives",
        "url": "https://example.com",
        "status": "invalid_status",  # Not in enum
        "date_added": "2025-11-03"
    }
    
    errors = validate_schema(data, schema)
    has_status_error = any("status" in error and "not in allowed values" in error for error in errors)
    assert has_status_error, "Should have error for invalid status enum value"
    
    print("✓ Enum validation works correctly")


def test_array_validation():
    """Test that array fields are validated."""
    schema = load_schema()
    
    # Test with invalid array (should be array, not string)
    data = {
        "schema_version": "1.0",
        "category_id": 1828,
        "listing_id": "test",
        "category_path": "Raw_Materials/Actives",
        "url": "https://example.com",
        "status": "active",
        "date_added": "2025-11-03",
        "tags": "not-an-array"  # Should be array
    }
    
    errors = validate_schema(data, schema)
    has_type_error = any("tags" in error and "incorrect type" in error for error in errors)
    assert has_type_error, "Should have error for tags not being an array"
    
    print("✓ Array type validation works correctly")


def run_all_tests():
    """Run all tests."""
    print("\nRunning validation tests...\n")
    
    tests = [
        test_load_schema,
        test_check_type,
        test_valid_listing,
        test_invalid_listing_missing_schema,
        test_strategic_supplier,
        test_required_fields,
        test_enum_validation,
        test_array_validation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Tests completed: {passed} passed, {failed} failed")
    print(f"{'='*60}\n")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
