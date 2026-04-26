#!/usr/bin/env python3
"""
Tests for convert_research.py

Run with: python3 -m pytest tests/test_convert_research.py -v
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "conversion"))

from convert_research import (
    clean_company_name,
    create_listing_id,
    parse_supplier_section,
    parse_research_file,
    infer_category_from_filepath,
    build_json_listing,
    save_listing,
)


# ---------------------------------------------------------------------------
# clean_company_name
# ---------------------------------------------------------------------------

def test_clean_company_name_plain():
    """Plain company name is returned unchanged (stripped)."""
    assert clean_company_name("Acme Corp") == "Acme Corp"
    print("✓ clean_company_name: plain name unchanged")


def test_clean_company_name_removes_star_marker():
    """⭐ MAJOR PLAYER marker is stripped."""
    name = "⭐ MAJOR PLAYER Acme Corp"
    result = clean_company_name(name)
    assert "⭐" not in result
    assert "MAJOR PLAYER" not in result
    assert "Acme Corp" in result
    print("✓ clean_company_name: star marker removed")


def test_clean_company_name_removes_manufacturer_marker():
    """⭐ MANUFACTURER marker is stripped."""
    name = "⭐ MANUFACTURER / DISTRIBUTOR BioTech Inc."
    result = clean_company_name(name)
    assert "⭐" not in result
    assert "MANUFACTURER" not in result
    print("✓ clean_company_name: manufacturer marker removed")


def test_clean_company_name_extra_whitespace():
    """Extra whitespace is collapsed."""
    result = clean_company_name("  Acme   Corp  ")
    assert result == "Acme Corp"
    print("✓ clean_company_name: extra whitespace removed")


def test_clean_company_name_empty():
    """Empty string returns empty string."""
    assert clean_company_name("") == ""
    print("✓ clean_company_name: empty string handled")


# ---------------------------------------------------------------------------
# create_listing_id
# ---------------------------------------------------------------------------

def test_create_listing_id_simple():
    """Simple lowercase name becomes ID with underscores."""
    assert create_listing_id("Acme Corp") == "acme_corp"
    print("✓ create_listing_id: simple name")


def test_create_listing_id_special_chars():
    """Special characters become underscores."""
    assert create_listing_id("BioTech & Co.") == "biotech_co"
    print("✓ create_listing_id: special chars replaced")


def test_create_listing_id_leading_trailing_underscores():
    """Leading/trailing underscores are stripped."""
    result = create_listing_id("  Acme Corp  ")
    assert not result.startswith("_")
    assert not result.endswith("_")
    print("✓ create_listing_id: no leading/trailing underscores")


def test_create_listing_id_numbers_preserved():
    """Numbers in company name are preserved."""
    result = create_listing_id("Chem4U")
    assert "4" in result
    print("✓ create_listing_id: numbers preserved")


def test_create_listing_id_lowercase():
    """Output is always lowercase."""
    result = create_listing_id("BASF SE")
    assert result == result.lower()
    print("✓ create_listing_id: output is lowercase")


# ---------------------------------------------------------------------------
# parse_supplier_section
# ---------------------------------------------------------------------------

SUPPLIER_DETAILS = """\
**Website:** https://www.acmecorp.com
**Location:** 123 Main St, New York, United States
**Phone:** +1-555-123-4567
**Specializations:** Active Ingredients, Botanical Extracts
**Products:** Vitamin C, Retinol
**Tags:** organic, sustainable
**Notes:** A leading supplier of cosmetic actives.
**Strategic Importance:** Core supplier for premium actives.
"""


def test_parse_supplier_section_website():
    """Website is extracted."""
    result = parse_supplier_section("Acme Corp", SUPPLIER_DETAILS)
    assert result is not None
    assert result.get("website") == "https://www.acmecorp.com"
    print("✓ parse_supplier_section: website extracted")


def test_parse_supplier_section_address():
    """Address is extracted."""
    result = parse_supplier_section("Acme Corp", SUPPLIER_DETAILS)
    assert "123 Main St" in result.get("address", "")
    print("✓ parse_supplier_section: address extracted")


def test_parse_supplier_section_country():
    """Country is inferred from address when 'United States' present."""
    result = parse_supplier_section("Acme Corp", SUPPLIER_DETAILS)
    assert result.get("country") == "United States"
    print("✓ parse_supplier_section: country inferred")


def test_parse_supplier_section_phone():
    """Phone number is extracted."""
    result = parse_supplier_section("Acme Corp", SUPPLIER_DETAILS)
    assert result.get("phone") == "+1-555-123-4567"
    print("✓ parse_supplier_section: phone extracted")


def test_parse_supplier_section_specializations():
    """Specializations are split by comma."""
    result = parse_supplier_section("Acme Corp", SUPPLIER_DETAILS)
    specs = result.get("specializations", [])
    assert "Active Ingredients" in specs
    assert "Botanical Extracts" in specs
    print("✓ parse_supplier_section: specializations extracted")


def test_parse_supplier_section_tags():
    """Tags are extracted from the Tags field."""
    result = parse_supplier_section("Acme Corp", SUPPLIER_DETAILS)
    tags = result.get("tags", [])
    assert "organic" in tags
    assert "sustainable" in tags
    print("✓ parse_supplier_section: tags extracted")


def test_parse_supplier_section_notes():
    """Notes are combined from Notes and Strategic Importance fields."""
    result = parse_supplier_section("Acme Corp", SUPPLIER_DETAILS)
    notes = result.get("notes", "")
    assert "leading supplier" in notes
    assert "Core supplier" in notes
    print("✓ parse_supplier_section: notes combined")


def test_parse_supplier_section_infers_major_player_tag():
    """⭐ MAJOR PLAYER in name adds major-player tag."""
    result = parse_supplier_section("⭐ MAJOR PLAYER Acme Corp", SUPPLIER_DETAILS)
    tags = result.get("tags", [])
    assert "major-player" in tags
    print("✓ parse_supplier_section: major-player tag inferred")


def test_parse_supplier_section_infers_sustainable_tag():
    """'sustainable' keyword in details adds the sustainable tag."""
    details = "**Website:** https://eco.com\nWe are a sustainable brand.\n"
    result = parse_supplier_section("Eco Co.", details)
    tags = result.get("tags", [])
    assert "sustainable" in tags
    print("✓ parse_supplier_section: sustainable tag inferred")


def test_parse_supplier_section_no_company_name():
    """Returns None when company name resolves to empty string."""
    result = parse_supplier_section("", "some details")
    assert result is None
    print("✓ parse_supplier_section: empty company name returns None")


def test_parse_supplier_section_minimal_details():
    """Works with no fields other than company name."""
    result = parse_supplier_section("Bare Minimum Co.", "No structured fields here.")
    assert result is not None
    assert result["company_name"] == "Bare Minimum Co."
    print("✓ parse_supplier_section: minimal details handled")


# ---------------------------------------------------------------------------
# parse_research_file
# ---------------------------------------------------------------------------

RESEARCH_MARKDOWN = """\
# Supplier Research

Some intro text.

#### 1. Alpha Actives Inc ⭐ MAJOR PLAYER
**Website:** https://www.alphaactives.com
**Location:** 100 Science Blvd, San Francisco, United States
**Specializations:** Peptides, Growth Factors
**Tags:** premium, high-performance

#### 2. Beta Botanicals Ltd
**Website:** https://www.betabotanicals.com
**Location:** London, United Kingdom
**Specializations:** Plant Extracts, Phytochemicals
**Notes:** Specializes in organic certified botanical extracts.
"""


def test_parse_research_file():
    """parse_research_file returns all suppliers from a markdown file."""
    with tempfile.NamedTemporaryFile(
        suffix=".md", mode="w", encoding="utf-8", delete=False
    ) as f:
        f.write(RESEARCH_MARKDOWN)
        filepath = Path(f.name)

    suppliers = parse_research_file(filepath)
    filepath.unlink()

    assert len(suppliers) == 2
    names = [s["company_name"] for s in suppliers]
    assert any("Alpha Actives" in n for n in names)
    assert any("Beta Botanicals" in n for n in names)
    print("✓ parse_research_file: both suppliers found")


def test_parse_research_file_empty_file():
    """Returns empty list for a file with no supplier sections."""
    with tempfile.NamedTemporaryFile(
        suffix=".md", mode="w", encoding="utf-8", delete=False
    ) as f:
        f.write("# Introduction\nSome text with no supplier sections.\n")
        filepath = Path(f.name)

    suppliers = parse_research_file(filepath)
    filepath.unlink()

    assert suppliers == []
    print("✓ parse_research_file: empty file returns empty list")


def test_parse_research_file_supplier_fields():
    """Supplier data is correctly extracted from the markdown."""
    with tempfile.NamedTemporaryFile(
        suffix=".md", mode="w", encoding="utf-8", delete=False
    ) as f:
        f.write(RESEARCH_MARKDOWN)
        filepath = Path(f.name)

    suppliers = parse_research_file(filepath)
    filepath.unlink()

    alpha = next(s for s in suppliers if "Alpha Actives" in s["company_name"])
    assert alpha.get("website") == "https://www.alphaactives.com"
    assert alpha.get("country") == "United States"
    assert "major-player" in alpha.get("tags", [])
    print("✓ parse_research_file: supplier fields correct")


# ---------------------------------------------------------------------------
# infer_category_from_filepath
# ---------------------------------------------------------------------------

def test_infer_category_emollients():
    """Filename containing 'emollients' maps to Emollients_Moisturizers."""
    result = infer_category_from_filepath(Path("research_emollients_2025.md"))
    assert result["path"] == "Raw_Materials/Emollients_Moisturizers"
    print("✓ infer_category_from_filepath: emollients mapped")


def test_infer_category_surfactants():
    """Filename containing 'surfactants' maps to Surfactants."""
    result = infer_category_from_filepath(Path("surfactants_suppliers.md"))
    assert result["path"] == "Raw_Materials/Surfactants"
    print("✓ infer_category_from_filepath: surfactants mapped")


def test_infer_category_packaging():
    """Filename containing 'packaging' maps to Packaging/Bottles_and_Jars."""
    result = infer_category_from_filepath(Path("packaging_research.md"))
    assert result["path"] == "Packaging/Bottles_and_Jars"
    print("✓ infer_category_from_filepath: packaging mapped")


def test_infer_category_testing():
    """Filename containing 'testing' maps to Testing_and_Quality_Control."""
    result = infer_category_from_filepath(Path("testing_labs.md"))
    assert result["path"] == "Business_Services/Testing_and_Quality_Control"
    print("✓ infer_category_from_filepath: testing mapped")


def test_infer_category_unknown_defaults():
    """Unknown filename defaults to Raw_Materials/Actives."""
    result = infer_category_from_filepath(Path("completely_unknown_file.md"))
    assert result["path"] == "Raw_Materials/Actives"
    print("✓ infer_category_from_filepath: unknown defaults to Actives")


# ---------------------------------------------------------------------------
# build_json_listing
# ---------------------------------------------------------------------------

def test_build_json_listing_required_fields():
    """build_json_listing produces all required schema fields."""
    supplier = {"company_name": "Build Test Co.", "website": "https://buildtest.com"}
    category_info = {"path": "Raw_Materials/Actives", "id": "1828"}
    listing = build_json_listing(supplier, category_info, "research.md")

    required = ["schema_version", "category_id", "listing_id", "category_path",
                "url", "status", "date_added", "date_updated", "metadata"]
    for field in required:
        assert field in listing, f"Required field '{field}' missing"
    print("✓ build_json_listing: all required fields present")


def test_build_json_listing_listing_id_derived():
    """listing_id is derived from company_name."""
    supplier = {"company_name": "BioTech Inc."}
    category_info = {"path": "Raw_Materials/Biotech_Ingredients", "id": "1828"}
    listing = build_json_listing(supplier, category_info, "research.md")
    assert listing["listing_id"] == "biotech_inc"
    print("✓ build_json_listing: listing_id derived from company name")


def test_build_json_listing_optional_fields_propagated():
    """Optional supplier fields are included when present."""
    supplier = {
        "company_name": "Eco Supplier",
        "website": "https://eco.com",
        "country": "Germany",
        "specializations": ["Botanical Extracts"],
        "tags": ["organic", "sustainable"],
        "notes": "Eco-certified supplier.",
    }
    category_info = {"path": "Raw_Materials/Botanical_Extracts", "id": "1828"}
    listing = build_json_listing(supplier, category_info, "research.md")

    assert listing.get("website") == "https://eco.com"
    assert listing.get("country") == "Germany"
    assert listing.get("specializations") == ["Botanical Extracts"]
    assert "organic" in listing.get("tags", [])
    assert listing.get("notes") == "Eco-certified supplier."
    print("✓ build_json_listing: optional fields propagated")


def test_build_json_listing_metadata():
    """Metadata block includes expected fields."""
    supplier = {"company_name": "Meta Test"}
    category_info = {"path": "Raw_Materials/Actives", "id": "1828"}
    listing = build_json_listing(supplier, category_info, "my_research.md")

    meta = listing.get("metadata", {})
    assert meta.get("validation_method") == "manual"
    assert meta.get("data_source") == "my_research.md"
    assert "last_validated" in meta
    print("✓ build_json_listing: metadata block correct")


def test_build_json_listing_status_active():
    """status is always 'active' for new listings."""
    supplier = {"company_name": "Active Status Co."}
    category_info = {"path": "Raw_Materials/Actives", "id": "1828"}
    listing = build_json_listing(supplier, category_info, "research.md")
    assert listing["status"] == "active"
    print("✓ build_json_listing: status is active")


# ---------------------------------------------------------------------------
# save_listing
# ---------------------------------------------------------------------------

def test_save_listing_creates_file(tmp_path):
    """save_listing writes the listing JSON to the correct path."""
    listing = {
        "schema_version": "1.0",
        "category_path": "Raw_Materials/Actives",
        "listing_id": "test_save_co",
        "category_id": "1828",
        "status": "active",
        "date_added": "2025-11-01",
        "date_updated": "2025-11-01",
        "metadata": {},
    }
    saved_path = save_listing(listing, tmp_path, dry_run=False)
    assert saved_path.exists()
    data = json.loads(saved_path.read_text())
    assert data["listing_id"] == "test_save_co"
    print("✓ save_listing: file created")


def test_save_listing_dry_run_no_file(tmp_path):
    """save_listing with dry_run=True does not create any file."""
    listing = {
        "schema_version": "1.0",
        "category_path": "Raw_Materials/Actives",
        "listing_id": "dry_run_co",
        "category_id": "1828",
        "status": "active",
        "date_added": "2025-11-01",
        "date_updated": "2025-11-01",
        "metadata": {},
    }
    saved_path = save_listing(listing, tmp_path, dry_run=True)
    assert not saved_path.exists(), "Dry run should not create files"
    print("✓ save_listing: dry_run creates no file")


def test_save_listing_correct_filename(tmp_path):
    """save_listing uses category_id and listing_id as filename."""
    listing = {
        "schema_version": "1.0",
        "category_path": "Raw_Materials/Actives",
        "listing_id": "filename_test",
        "category_id": "1828",
        "status": "active",
        "date_added": "2025-11-01",
        "date_updated": "2025-11-01",
        "metadata": {},
    }
    saved_path = save_listing(listing, tmp_path, dry_run=False)
    assert saved_path.name == "1828_filename_test.json"
    print("✓ save_listing: filename uses category_id_listing_id pattern")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_all_tests():
    print("\nRunning convert_research tests...\n")

    tests = [
        test_clean_company_name_plain,
        test_clean_company_name_removes_star_marker,
        test_clean_company_name_removes_manufacturer_marker,
        test_clean_company_name_extra_whitespace,
        test_clean_company_name_empty,
        test_create_listing_id_simple,
        test_create_listing_id_special_chars,
        test_create_listing_id_leading_trailing_underscores,
        test_create_listing_id_numbers_preserved,
        test_create_listing_id_lowercase,
        test_parse_supplier_section_website,
        test_parse_supplier_section_address,
        test_parse_supplier_section_country,
        test_parse_supplier_section_phone,
        test_parse_supplier_section_specializations,
        test_parse_supplier_section_tags,
        test_parse_supplier_section_notes,
        test_parse_supplier_section_infers_major_player_tag,
        test_parse_supplier_section_infers_sustainable_tag,
        test_parse_supplier_section_no_company_name,
        test_parse_supplier_section_minimal_details,
        test_parse_research_file,
        test_parse_research_file_empty_file,
        test_parse_research_file_supplier_fields,
        test_infer_category_emollients,
        test_infer_category_surfactants,
        test_infer_category_packaging,
        test_infer_category_testing,
        test_infer_category_unknown_defaults,
        test_build_json_listing_required_fields,
        test_build_json_listing_listing_id_derived,
        test_build_json_listing_optional_fields_propagated,
        test_build_json_listing_metadata,
        test_build_json_listing_status_active,
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
