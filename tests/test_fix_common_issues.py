#!/usr/bin/env python3
"""
Tests for fix_common_issues.py

Run with: python3 -m pytest tests/test_fix_common_issues.py -v
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "validation"))

from fix_common_issues import (
    fix_missing_schema_version,
    fix_product_highlights_type,
    fix_invalid_fields,
    fix_invalid_tags,
    process_listing,
    load_json_file,
    save_json_file,
    VALID_TAGS,
    INVALID_FIELDS,
)


# ---------------------------------------------------------------------------
# fix_missing_schema_version
# ---------------------------------------------------------------------------

def test_fix_schema_version_missing():
    """Adds schema_version when absent and returns True."""
    data = {"listing_id": "test"}
    changed = fix_missing_schema_version(data)
    assert changed is True, "Should report a change"
    assert data["schema_version"] == "1.0", "Should set schema_version to '1.0'"
    print("✓ fix_missing_schema_version: adds missing version")


def test_fix_schema_version_already_present():
    """Does not change schema_version when already present and returns False."""
    data = {"schema_version": "2.0", "listing_id": "test"}
    changed = fix_missing_schema_version(data)
    assert changed is False, "Should not report a change"
    assert data["schema_version"] == "2.0", "Should not overwrite existing version"
    print("✓ fix_missing_schema_version: leaves existing version untouched")


def test_fix_schema_version_empty_dict():
    """Works on an empty dict."""
    data = {}
    changed = fix_missing_schema_version(data)
    assert changed is True
    assert data["schema_version"] == "1.0"
    print("✓ fix_missing_schema_version: works on empty dict")


# ---------------------------------------------------------------------------
# fix_product_highlights_type
# ---------------------------------------------------------------------------

def test_fix_product_highlights_string_to_array():
    """Converts a string product_highlights to a single-item array."""
    data = {"product_highlights": "Beta-glucan oat extract"}
    changed = fix_product_highlights_type(data)
    assert changed is True, "Should report a change"
    assert isinstance(data["product_highlights"], list), "Should become a list"
    assert data["product_highlights"] == ["Beta-glucan oat extract"]
    print("✓ fix_product_highlights_type: string converted to array")


def test_fix_product_highlights_already_array():
    """Does not change product_highlights that is already a list."""
    data = {"product_highlights": ["Beta-glucan", "Colloidal oat"]}
    changed = fix_product_highlights_type(data)
    assert changed is False, "Should not report a change"
    assert data["product_highlights"] == ["Beta-glucan", "Colloidal oat"]
    print("✓ fix_product_highlights_type: array unchanged")


def test_fix_product_highlights_absent():
    """Returns False when product_highlights is not present."""
    data = {"listing_id": "test"}
    changed = fix_product_highlights_type(data)
    assert changed is False
    assert "product_highlights" not in data
    print("✓ fix_product_highlights_type: absent field ignored")


def test_fix_product_highlights_empty_string():
    """Converts an empty string to a single-item array with empty string."""
    data = {"product_highlights": ""}
    changed = fix_product_highlights_type(data)
    assert changed is True
    assert data["product_highlights"] == [""]
    print("✓ fix_product_highlights_type: empty string converted to array")


# ---------------------------------------------------------------------------
# fix_invalid_fields
# ---------------------------------------------------------------------------

def test_fix_invalid_fields_removes_city():
    """Removes the 'city' field."""
    data = {"listing_id": "test", "city": "New York"}
    changed = fix_invalid_fields(data)
    assert changed is True
    assert "city" not in data
    print("✓ fix_invalid_fields: city removed")


def test_fix_invalid_fields_removes_all_invalid():
    """Removes all known invalid fields in one pass."""
    data = {
        "listing_id": "test",
        "city": "NY",
        "state": "NY",
        "zip": "10001",
        "postal_code": "10001",
    }
    changed = fix_invalid_fields(data)
    assert changed is True
    for field in INVALID_FIELDS:
        assert field not in data, f"'{field}' should have been removed"
    assert data.get("listing_id") == "test", "Valid fields should be kept"
    print("✓ fix_invalid_fields: all invalid fields removed")


def test_fix_invalid_fields_nothing_to_remove():
    """Returns False when no invalid fields are present."""
    data = {"listing_id": "test", "company_name": "Acme"}
    changed = fix_invalid_fields(data)
    assert changed is False
    assert data == {"listing_id": "test", "company_name": "Acme"}
    print("✓ fix_invalid_fields: no-op on clean data")


# ---------------------------------------------------------------------------
# fix_invalid_tags
# ---------------------------------------------------------------------------

def test_fix_invalid_tags_removes_invalid():
    """Removes tags not in the VALID_TAGS set."""
    data = {"tags": ["organic", "totally_invalid_tag", "sustainable"]}
    changed = fix_invalid_tags(data)
    assert changed is True
    assert "totally_invalid_tag" not in data["tags"]
    assert "organic" in data["tags"]
    assert "sustainable" in data["tags"]
    print("✓ fix_invalid_tags: invalid tags removed")


def test_fix_invalid_tags_all_valid():
    """Returns False when all tags are valid."""
    data = {"tags": ["organic", "sustainable", "certified"]}
    changed = fix_invalid_tags(data)
    assert changed is False
    assert set(data["tags"]) == {"organic", "sustainable", "certified"}
    print("✓ fix_invalid_tags: all valid tags unchanged")


def test_fix_invalid_tags_empty_list():
    """Returns False for an empty tags list."""
    data = {"tags": []}
    changed = fix_invalid_tags(data)
    assert changed is False
    print("✓ fix_invalid_tags: empty list unchanged")


def test_fix_invalid_tags_no_tags_field():
    """Returns False when tags field is absent."""
    data = {"listing_id": "test"}
    changed = fix_invalid_tags(data)
    assert changed is False
    print("✓ fix_invalid_tags: absent field handled")


def test_fix_invalid_tags_not_a_list():
    """Returns False when tags is not a list (type error is silently handled)."""
    data = {"tags": "organic"}
    changed = fix_invalid_tags(data)
    assert changed is False
    print("✓ fix_invalid_tags: non-list tags ignored")


def test_fix_invalid_tags_all_invalid():
    """All tags removed when all are invalid."""
    data = {"tags": ["invalid1", "invalid2"]}
    changed = fix_invalid_tags(data)
    assert changed is True
    assert data["tags"] == []
    print("✓ fix_invalid_tags: all tags removed when all invalid")


# ---------------------------------------------------------------------------
# load_json_file / save_json_file
# ---------------------------------------------------------------------------

def test_load_json_file():
    """Loads a JSON file into a dict."""
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        json.dump({"key": "value"}, f)
        tmp_path = Path(f.name)
    data = load_json_file(tmp_path)
    assert data == {"key": "value"}
    tmp_path.unlink()
    print("✓ load_json_file: reads correctly")


def test_save_json_file():
    """Saves a dict to a JSON file with trailing newline."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        tmp_path = Path(f.name)
    data = {"schema_version": "1.0", "listing_id": "test"}
    save_json_file(tmp_path, data)
    raw = tmp_path.read_text(encoding="utf-8")
    assert raw.endswith("\n"), "File should end with newline"
    loaded = json.loads(raw)
    assert loaded == data
    tmp_path.unlink()
    print("✓ save_json_file: writes correctly with trailing newline")


def test_save_and_reload_roundtrip():
    """Data written by save_json_file can be read back identically."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        tmp_path = Path(f.name)
    original = {"a": 1, "b": [1, 2, 3], "c": {"nested": True}}
    save_json_file(tmp_path, original)
    reloaded = load_json_file(tmp_path)
    assert reloaded == original
    tmp_path.unlink()
    print("✓ save/load roundtrip: data preserved")


# ---------------------------------------------------------------------------
# process_listing – integration
# ---------------------------------------------------------------------------

def _make_listing_file(tmpdir: Path, name: str, data: dict) -> Path:
    filepath = tmpdir / name
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return filepath


def test_process_listing_fixes_schema_version(tmp_path):
    """process_listing adds schema_version to a file missing it."""
    filepath = _make_listing_file(
        tmp_path,
        "listing.json",
        {"listing_id": "test"},
    )
    stats = process_listing(filepath, dry_run=False)
    assert stats["schema_version"] == 1, "Should count schema_version fix"
    reloaded = load_json_file(filepath)
    assert reloaded["schema_version"] == "1.0"
    print("✓ process_listing: schema_version added")


def test_process_listing_dry_run_does_not_modify(tmp_path):
    """process_listing with dry_run=True reports changes but does not write."""
    original_data = {"listing_id": "test"}
    filepath = _make_listing_file(tmp_path, "listing.json", original_data)
    original_text = filepath.read_text(encoding="utf-8")

    stats = process_listing(filepath, dry_run=True)
    assert stats["schema_version"] == 1, "Should detect a change"
    # File must remain untouched
    assert filepath.read_text(encoding="utf-8") == original_text
    print("✓ process_listing: dry_run does not modify file")


def test_process_listing_no_changes_needed(tmp_path):
    """process_listing returns zero counts when file is already clean."""
    clean_data = {
        "schema_version": "1.0",
        "listing_id": "test",
        "product_highlights": ["Item A"],
        "tags": ["organic"],
    }
    filepath = _make_listing_file(tmp_path, "listing.json", clean_data)
    stats = process_listing(filepath, dry_run=False)
    total = sum(stats.values())
    assert total == 0, f"No fixes should be needed: {stats}"
    print("✓ process_listing: clean file has zero fixes")


def test_process_listing_multiple_fixes(tmp_path):
    """process_listing applies multiple fixes in a single pass."""
    data = {
        "listing_id": "test",
        "product_highlights": "Single string highlight",
        "city": "Paris",
        "tags": ["organic", "invalid_xyz"],
    }
    filepath = _make_listing_file(tmp_path, "listing.json", data)
    stats = process_listing(filepath, dry_run=False)

    assert stats["schema_version"] == 1
    assert stats["product_highlights"] == 1
    assert stats["invalid_fields"] == 1
    assert stats["invalid_tags"] == 1

    reloaded = load_json_file(filepath)
    assert reloaded["schema_version"] == "1.0"
    assert isinstance(reloaded["product_highlights"], list)
    assert "city" not in reloaded
    assert "invalid_xyz" not in reloaded.get("tags", [])
    print("✓ process_listing: multiple fixes applied")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_all_tests():
    print("\nRunning fix_common_issues tests...\n")

    tests = [
        test_fix_schema_version_missing,
        test_fix_schema_version_already_present,
        test_fix_schema_version_empty_dict,
        test_fix_product_highlights_string_to_array,
        test_fix_product_highlights_already_array,
        test_fix_product_highlights_absent,
        test_fix_product_highlights_empty_string,
        test_fix_invalid_fields_removes_city,
        test_fix_invalid_fields_removes_all_invalid,
        test_fix_invalid_fields_nothing_to_remove,
        test_fix_invalid_tags_removes_invalid,
        test_fix_invalid_tags_all_valid,
        test_fix_invalid_tags_empty_list,
        test_fix_invalid_tags_no_tags_field,
        test_fix_invalid_tags_not_a_list,
        test_fix_invalid_tags_all_invalid,
        test_load_json_file,
        test_save_json_file,
        test_save_and_reload_roundtrip,
    ]

    # Tests that need tmp_path via pytest fixtures are excluded from
    # the manual runner; they run correctly under pytest.
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
            print(f"✗ {test.__name__} error: {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Tests completed: {passed} passed, {failed} failed")
    print(f"{'='*60}\n")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
