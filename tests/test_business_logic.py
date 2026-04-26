#!/usr/bin/env python3
"""
Tests for validate_business_logic() and integrated validate_listing().

Run with: python3 -m pytest tests/test_business_logic.py -v
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "validation"))

from validate_listings import (
    validate_business_logic,
    validate_listing,
    generate_report,
    find_all_listings,
    load_schema,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


MINIMAL_VALID_DATA = {
    "schema_version": "1.0",
    "category_id": 1828,
    "listing_id": "acme_corp",
    "category_path": "Raw_Materials/Actives",
    "url": "https://personalcaresuppliers.com/Listing/Index/Raw_Materials/Actives/1828/",
    "status": "active",
    "date_added": "2025-11-03",
}


# ---------------------------------------------------------------------------
# validate_business_logic – filename pattern
# ---------------------------------------------------------------------------

def test_business_logic_valid_filename():
    """A correctly named file produces no business-logic errors for filename."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "1828_acme_corp.json"
        data = dict(MINIMAL_VALID_DATA)
        _write_json(filepath, data)

        errors = validate_business_logic(data, filepath)
        filename_errors = [e for e in errors if "Filename does not match pattern" in e]
        assert len(filename_errors) == 0, f"Unexpected filename error: {filename_errors}"
    print("✓ Valid filename accepted")


def test_business_logic_invalid_filename_pattern():
    """A file without the numeric prefix fails the filename pattern check."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "acme_corp.json"
        data = dict(MINIMAL_VALID_DATA)
        _write_json(filepath, data)

        errors = validate_business_logic(data, filepath)
        has_pattern_error = any("Filename does not match pattern" in e for e in errors)
        assert has_pattern_error, "Should flag invalid filename pattern"
    print("✓ Invalid filename pattern detected")


def test_business_logic_category_id_mismatch():
    """Filename category_id that differs from data category_id is flagged."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "9999_acme_corp.json"
        data = dict(MINIMAL_VALID_DATA)  # category_id = 1828
        _write_json(filepath, data)

        errors = validate_business_logic(data, filepath)
        has_cat_error = any("category_id" in e and "does not match" in e for e in errors)
        assert has_cat_error, "Should flag category_id mismatch"
    print("✓ category_id mismatch detected")


def test_business_logic_listing_id_mismatch():
    """Filename listing_id that differs from data listing_id is flagged."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "1828_wrong_listing_id.json"
        data = dict(MINIMAL_VALID_DATA)  # listing_id = "acme_corp"
        _write_json(filepath, data)

        errors = validate_business_logic(data, filepath)
        has_lid_error = any("listing_id" in e and "does not match" in e for e in errors)
        assert has_lid_error, "Should flag listing_id mismatch"
    print("✓ listing_id mismatch detected")


# ---------------------------------------------------------------------------
# validate_business_logic – date validation
# ---------------------------------------------------------------------------

def test_business_logic_valid_dates():
    """Valid date strings produce no date errors."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "1828_acme_corp.json"
        data = {**MINIMAL_VALID_DATA, "date_updated": "2025-12-01"}
        _write_json(filepath, data)

        errors = validate_business_logic(data, filepath)
        date_errors = [e for e in errors if "date" in e.lower() and "Invalid" in e]
        assert len(date_errors) == 0, f"Unexpected date error: {date_errors}"
    print("✓ Valid dates accepted")


def test_business_logic_invalid_date_format():
    """A malformed date string is reported."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "1828_acme_corp.json"
        data = {**MINIMAL_VALID_DATA, "date_added": "03-11-2025"}  # wrong format
        _write_json(filepath, data)

        errors = validate_business_logic(data, filepath)
        has_date_error = any("Invalid date format" in e and "date_added" in e for e in errors)
        assert has_date_error, "Should flag invalid date_added format"
    print("✓ Invalid date format detected")


def test_business_logic_invalid_date_updated_format():
    """A malformed date_updated string is reported."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "1828_acme_corp.json"
        data = {**MINIMAL_VALID_DATA, "date_updated": "not-a-date"}
        _write_json(filepath, data)

        errors = validate_business_logic(data, filepath)
        has_date_error = any("Invalid date format" in e and "date_updated" in e for e in errors)
        assert has_date_error, "Should flag invalid date_updated format"
    print("✓ Invalid date_updated format detected")


# ---------------------------------------------------------------------------
# validate_business_logic – URL validation
# ---------------------------------------------------------------------------

def test_business_logic_valid_url():
    """A valid https URL produces no URL error."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "1828_acme_corp.json"
        data = dict(MINIMAL_VALID_DATA)
        _write_json(filepath, data)

        errors = validate_business_logic(data, filepath)
        url_errors = [e for e in errors if "URL does not start" in e]
        assert len(url_errors) == 0, f"Unexpected URL error: {url_errors}"
    print("✓ Valid HTTPS URL accepted")


def test_business_logic_invalid_url_no_scheme():
    """A URL missing the http(s) scheme is flagged."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "1828_acme_corp.json"
        data = {**MINIMAL_VALID_DATA, "url": "personalcaresuppliers.com/Listing/"}
        _write_json(filepath, data)

        errors = validate_business_logic(data, filepath)
        has_url_error = any("URL does not start with" in e for e in errors)
        assert has_url_error, "Should flag URL missing http/https"
    print("✓ Invalid URL scheme detected")


def test_business_logic_http_url_accepted():
    """An http:// URL is allowed (not just https)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "1828_acme_corp.json"
        data = {**MINIMAL_VALID_DATA, "url": "http://personalcaresuppliers.com/Listing/"}
        _write_json(filepath, data)

        errors = validate_business_logic(data, filepath)
        url_errors = [e for e in errors if "URL does not start" in e]
        assert len(url_errors) == 0, f"http:// URL should be accepted: {url_errors}"
    print("✓ HTTP URL accepted")


# ---------------------------------------------------------------------------
# validate_business_logic – strategic supplier checks
# ---------------------------------------------------------------------------

def test_business_logic_strategic_supplier_complete():
    """A strategic supplier with all required enhanced fields passes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "1828_oat_co.json"
        data = {
            **MINIMAL_VALID_DATA,
            "listing_id": "oat_co",
            "tags": ["oat-specialist", "organic"],
            "company_name": "Oat Co.",
            "specializations": ["Beta-glucan"],
            "certifications": ["ECOCERT"],
        }
        _write_json(filepath, data)

        errors = validate_business_logic(data, filepath)
        strategic_errors = [e for e in errors if "Strategic supplier missing" in e]
        assert len(strategic_errors) == 0, f"Complete strategic supplier should not have errors: {strategic_errors}"
    print("✓ Complete strategic supplier accepted")


def test_business_logic_strategic_supplier_missing_enhanced():
    """A strategic supplier missing enhanced fields is flagged."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "1828_oat_co.json"
        data = {
            **MINIMAL_VALID_DATA,
            "listing_id": "oat_co",
            "tags": ["major-player"],
            # company_name, specializations, certifications missing
        }
        _write_json(filepath, data)

        errors = validate_business_logic(data, filepath)
        has_strategic_error = any("Strategic supplier missing" in e for e in errors)
        assert has_strategic_error, "Should flag missing enhanced fields for strategic supplier"
    print("✓ Strategic supplier missing enhanced fields detected")


def test_business_logic_non_strategic_no_enhanced_required():
    """A non-strategic supplier is not required to have enhanced fields."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "1828_acme_corp.json"
        data = dict(MINIMAL_VALID_DATA)
        _write_json(filepath, data)

        errors = validate_business_logic(data, filepath)
        strategic_errors = [e for e in errors if "Strategic supplier missing" in e]
        assert len(strategic_errors) == 0, "Non-strategic supplier should not need enhanced fields"
    print("✓ Non-strategic supplier without enhanced fields accepted")


# ---------------------------------------------------------------------------
# validate_listing – integrated function
# ---------------------------------------------------------------------------

def test_validate_listing_valid_file():
    """A fully valid listing file passes integrated validation."""
    schema = load_schema()
    fixture_path = Path(__file__).parent / "fixtures" / "valid_listing.json"
    # The fixture filename doesn't match the naming convention,
    # so we copy it to a temp file with a correct name.
    data = json.loads(fixture_path.read_text())
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "1828_test_supplier_valid.json"
        _write_json(filepath, data)
        is_valid, errors = validate_listing(filepath, schema)
    assert is_valid, f"Valid listing should pass: {errors}"
    print("✓ validate_listing: valid file passes")


def test_validate_listing_invalid_file():
    """A listing missing schema_version fails integrated validation."""
    schema = load_schema()
    fixture_path = Path(__file__).parent / "fixtures" / "invalid_listing_missing_schema.json"
    data = json.loads(fixture_path.read_text())
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "1828_test_supplier_invalid.json"
        _write_json(filepath, data)
        is_valid, errors = validate_listing(filepath, schema)
    assert not is_valid, "Invalid listing should fail"
    assert len(errors) > 0, "Should have at least one error"
    print("✓ validate_listing: invalid file fails")


def test_validate_listing_bad_json():
    """A file with malformed JSON fails at load time."""
    schema = load_schema()
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "1828_bad.json"
        filepath.write_text("{invalid json", encoding="utf-8")
        is_valid, errors = validate_listing(filepath, schema)
    assert not is_valid, "Malformed JSON should fail validation"
    assert any("JSON parsing error" in e for e in errors), "Should report JSON parse error"
    print("✓ validate_listing: malformed JSON detected")


# ---------------------------------------------------------------------------
# generate_report
# ---------------------------------------------------------------------------

def test_generate_report_all_valid():
    """Report with all valid listings shows 100% validity."""
    results = {
        Path("a.json"): (True, []),
        Path("b.json"): (True, []),
    }
    report = generate_report(results)
    assert "2" in report, "Should include total count"
    assert "VALIDATION ERRORS" not in report or "0" in report
    print("✓ generate_report: all valid")


def test_generate_report_with_errors():
    """Report with some invalid listings includes the error section."""
    results = {
        Path("good.json"): (True, []),
        Path("bad.json"): (False, ["Missing required field: schema_version"]),
    }
    report = generate_report(results)
    assert "VALIDATION ERRORS" in report, "Should include error section"
    assert "bad.json" in report, "Should mention the failing file"
    assert "Missing required field: schema_version" in report
    print("✓ generate_report: errors included")


def test_generate_report_empty():
    """Report with zero listings handles division-by-zero gracefully."""
    results = {}
    report = generate_report(results)
    assert "0" in report, "Should mention zero listings"
    print("✓ generate_report: empty results handled")


# ---------------------------------------------------------------------------
# find_all_listings
# ---------------------------------------------------------------------------

def test_find_all_listings_finds_json_files():
    """find_all_listings returns JSON files under the listings directory."""
    repo_root = Path(__file__).parent.parent
    listings = find_all_listings(repo_root)
    # The repo has real listing files
    assert isinstance(listings, list), "Should return a list"
    assert len(listings) > 0, "Should find listing files in the repo"
    assert all(p.suffix == ".json" for p in listings), "Should only return .json files"
    print(f"✓ find_all_listings: found {len(listings)} listing files")


def test_find_all_listings_empty_dir():
    """find_all_listings returns empty list when listings dir doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        listings = find_all_listings(Path(tmpdir))
    assert listings == [], "Should return empty list when listings dir is missing"
    print("✓ find_all_listings: empty dir handled")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_all_tests():
    print("\nRunning business logic & integration tests...\n")

    tests = [
        test_business_logic_valid_filename,
        test_business_logic_invalid_filename_pattern,
        test_business_logic_category_id_mismatch,
        test_business_logic_listing_id_mismatch,
        test_business_logic_valid_dates,
        test_business_logic_invalid_date_format,
        test_business_logic_invalid_date_updated_format,
        test_business_logic_valid_url,
        test_business_logic_invalid_url_no_scheme,
        test_business_logic_http_url_accepted,
        test_business_logic_strategic_supplier_complete,
        test_business_logic_strategic_supplier_missing_enhanced,
        test_business_logic_non_strategic_no_enhanced_required,
        test_validate_listing_valid_file,
        test_validate_listing_invalid_file,
        test_validate_listing_bad_json,
        test_generate_report_all_valid,
        test_generate_report_with_errors,
        test_generate_report_empty,
        test_find_all_listings_finds_json_files,
        test_find_all_listings_empty_dir,
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
            print(f"✗ {test.__name__} error: {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Tests completed: {passed} passed, {failed} failed")
    print(f"{'='*60}\n")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
