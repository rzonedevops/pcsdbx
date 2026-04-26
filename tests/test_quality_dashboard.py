#!/usr/bin/env python3
"""
Tests for quality_dashboard.py

Run with: python3 -m pytest tests/test_quality_dashboard.py -v
"""

import json
import sys
import tempfile
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "quality"))

from quality_dashboard import (
    analyze_listing,
    generate_dashboard,
    save_trend_data,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_listing(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


FULL_LISTING = {
    "schema_version": "1.0",
    "category_id": 1828,
    "listing_id": "test_co",
    "category_path": "Raw_Materials/Actives",
    "url": "https://example.com/",
    "company_name": "Test Co.",
    "address": "123 Main St, City",
    "country": "United States",
    "phone": "+1-555-000-0000",
    "website": "https://testco.com",
    "specializations": ["Active ingredients"],
    "email": "info@testco.com",
    "tags": ["organic", "sustainable"],
    "certifications": ["COSMOS"],
    "product_highlights": ["Vitamin C", "Retinol"],
    "key_benefits": ["High efficacy"],
    "notes": "A top-quality active ingredient supplier.",
    "status": "active",
    "date_added": "2025-11-01",
    "date_updated": "2025-11-01",
    "metadata": {
        "last_validated": "2025-11-01",
        "validation_method": "manual",
        "data_source": "manual_entry",
        "quality_score": 90,
    },
}

MINIMAL_LISTING = {
    "schema_version": "1.0",
    "category_id": 1828,
    "listing_id": "minimal_co",
    "category_path": "Raw_Materials/Actives",
    "url": "https://example.com/",
    "status": "active",
    "date_added": "2025-10-01",
}


# ---------------------------------------------------------------------------
# analyze_listing
# ---------------------------------------------------------------------------

def test_analyze_listing_full():
    """Full listing yields high completeness and correct flags."""
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        path = Path(f.name)
        json.dump(FULL_LISTING, f)

    result = analyze_listing(path)
    path.unlink()

    assert result["has_schema_version"] is True
    assert result["has_required_fields"] is True
    assert result["has_tags"] is True
    assert result["has_specializations"] is True
    assert result["has_certifications"] is True
    assert result["has_metadata"] is True
    assert result["tag_count"] == 2
    assert result["specialization_count"] == 1
    assert result["completeness_score"] > 80, "Full listing should score > 80"
    print(f"✓ analyze_listing: full listing score = {result['completeness_score']:.1f}")


def test_analyze_listing_minimal():
    """Minimal listing (only required fields) has low completeness."""
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        path = Path(f.name)
        json.dump(MINIMAL_LISTING, f)

    result = analyze_listing(path)
    path.unlink()

    assert result["has_schema_version"] is True
    assert result["has_required_fields"] is True
    assert result["has_tags"] is False
    assert result["has_specializations"] is False
    assert result["has_certifications"] is False
    assert result["tag_count"] == 0
    assert result["completeness_score"] < 60, "Minimal listing should score < 60"
    print(f"✓ analyze_listing: minimal listing score = {result['completeness_score']:.1f}")


def test_analyze_listing_no_schema_version():
    """Listing without schema_version is detected."""
    data = dict(MINIMAL_LISTING)
    del data["schema_version"]
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        path = Path(f.name)
        json.dump(data, f)

    result = analyze_listing(path)
    path.unlink()

    assert result["has_schema_version"] is False
    print("✓ analyze_listing: missing schema_version flagged")


def test_analyze_listing_category_path():
    """category_path is extracted into result."""
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        path = Path(f.name)
        json.dump(FULL_LISTING, f)

    result = analyze_listing(path)
    path.unlink()

    assert result["category_path"] == "Raw_Materials/Actives"
    assert result["company_name"] == "Test Co."
    print("✓ analyze_listing: category_path and company_name extracted")


def test_analyze_listing_date_added():
    """date_added is preserved in result."""
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        path = Path(f.name)
        json.dump(MINIMAL_LISTING, f)

    result = analyze_listing(path)
    path.unlink()

    assert result["date_added"] == "2025-10-01"
    print("✓ analyze_listing: date_added preserved")


# ---------------------------------------------------------------------------
# generate_dashboard
# ---------------------------------------------------------------------------

def _make_analysis(
    *,
    completeness: float = 75.0,
    has_tags: bool = True,
    tag_count: int = 2,
    has_specializations: bool = True,
    specialization_count: int = 1,
    has_schema: bool = True,
    has_metadata: bool = True,
    has_certifications: bool = True,
    category: str = "Raw_Materials/Actives",
    date_added: str = "2025-11-01",
) -> dict:
    enhanced_total = 7
    strategic_total = 5
    return {
        "file": Path("dummy.json"),
        "category_path": category,
        "company_name": "Dummy Co.",
        "has_schema_version": has_schema,
        "has_required_fields": True,
        "enhanced_field_count": 4 if has_tags else 2,
        "enhanced_field_total": enhanced_total,
        "strategic_field_count": 3 if has_tags else 1,
        "strategic_field_total": strategic_total,
        "completeness_score": completeness,
        "has_tags": has_tags,
        "tag_count": tag_count,
        "has_specializations": has_specializations,
        "specialization_count": specialization_count,
        "has_metadata": has_metadata,
        "has_certifications": has_certifications,
        "date_added": date_added,
    }


def test_generate_dashboard_empty():
    """generate_dashboard returns error dict for empty input."""
    result = generate_dashboard([])
    assert "error" in result
    print("✓ generate_dashboard: empty list handled")


def test_generate_dashboard_single_listing():
    """Dashboard for a single listing computes metrics correctly."""
    listing = _make_analysis(completeness=80.0, has_tags=True, tag_count=3)
    result = generate_dashboard([listing])

    assert result["total_listings"] == 1
    assert result["overall"]["tags_pct"] == 100.0
    assert result["overall"]["schema_version_pct"] == 100.0
    assert result["quality_tiers"]["excellent"]["count"] == 1
    assert result["quality_tiers"]["good"]["count"] == 0
    print("✓ generate_dashboard: single listing metrics correct")


def test_generate_dashboard_quality_tiers():
    """Quality tiers are assigned based on completeness score thresholds."""
    listings = [
        _make_analysis(completeness=90.0),  # excellent
        _make_analysis(completeness=70.0),  # good
        _make_analysis(completeness=50.0),  # fair
        _make_analysis(completeness=30.0),  # poor
    ]
    result = generate_dashboard(listings)

    tiers = result["quality_tiers"]
    assert tiers["excellent"]["count"] == 1
    assert tiers["good"]["count"] == 1
    assert tiers["fair"]["count"] == 1
    assert tiers["poor"]["count"] == 1
    assert tiers["excellent"]["pct"] == 25.0
    print("✓ generate_dashboard: quality tiers correct")


def test_generate_dashboard_no_tags():
    """Dashboard correctly counts listings without tags."""
    listings = [
        _make_analysis(has_tags=False, tag_count=0),
        _make_analysis(has_tags=True, tag_count=2),
    ]
    result = generate_dashboard(listings)
    assert result["overall"]["tags_pct"] == 50.0
    print("✓ generate_dashboard: tags_pct calculated")


def test_generate_dashboard_category_breakdown():
    """Category breakdown is computed per category_path."""
    listings = [
        _make_analysis(category="Raw_Materials/Actives", completeness=80.0),
        _make_analysis(category="Raw_Materials/Actives", completeness=60.0),
        _make_analysis(category="Packaging/Bottles_and_Jars", completeness=50.0),
    ]
    result = generate_dashboard(listings)
    cats = result["categories"]
    assert "Raw_Materials/Actives" in cats
    assert cats["Raw_Materials/Actives"]["count"] == 2
    assert abs(cats["Raw_Materials/Actives"]["avg_completeness"] - 70.0) < 0.1
    assert "Packaging/Bottles_and_Jars" in cats
    assert cats["Packaging/Bottles_and_Jars"]["count"] == 1
    print("✓ generate_dashboard: category breakdown correct")


def test_generate_dashboard_recent_additions():
    """Recent additions are the 10 most recently added listings."""
    listings = [
        _make_analysis(date_added=f"2025-{m:02d}-01")
        for m in range(1, 13)
    ]
    result = generate_dashboard(listings)
    recent = result["recent_additions"]
    assert len(recent) == 10
    # Most recent should be first (sorted descending)
    assert recent[0]["date"] == "2025-12-01"
    print("✓ generate_dashboard: recent_additions ordered correctly")


def test_generate_dashboard_avg_tags_and_specs():
    """Average tags and specializations are calculated correctly."""
    listings = [
        _make_analysis(tag_count=4, specialization_count=2),
        _make_analysis(tag_count=0, specialization_count=0),
    ]
    result = generate_dashboard(listings)
    assert result["overall"]["avg_tags"] == 2.0
    assert result["overall"]["avg_specializations"] == 1.0
    print("✓ generate_dashboard: avg_tags and avg_specializations correct")


# ---------------------------------------------------------------------------
# save_trend_data
# ---------------------------------------------------------------------------

def test_save_trend_data_creates_file():
    """save_trend_data creates a new trend file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        trend_file = Path(tmpdir) / "trends.json"
        dashboard = {
            "total_listings": 100,
            "overall": {
                "avg_completeness": 75.5,
                "enhanced_coverage_pct": 60.0,
                "strategic_coverage_pct": 50.0,
                "tags_pct": 80.0,
            },
        }
        save_trend_data(dashboard, trend_file)

        assert trend_file.exists()
        trends = json.loads(trend_file.read_text())
        assert isinstance(trends, list)
        assert len(trends) == 1
        entry = trends[0]
        assert entry["total_listings"] == 100
        assert entry["avg_completeness"] == 75.5
        assert entry["date"] == str(date.today())
    print("✓ save_trend_data: creates new file")


def test_save_trend_data_appends():
    """save_trend_data appends to an existing file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        trend_file = Path(tmpdir) / "trends.json"
        dashboard = {
            "total_listings": 50,
            "overall": {
                "avg_completeness": 65.0,
                "enhanced_coverage_pct": 55.0,
                "strategic_coverage_pct": 45.0,
                "tags_pct": 70.0,
            },
        }
        # First write
        save_trend_data(dashboard, trend_file)
        # Second write
        dashboard["total_listings"] = 75
        save_trend_data(dashboard, trend_file)

        trends = json.loads(trend_file.read_text())
        assert len(trends) == 2
        assert trends[1]["total_listings"] == 75
    print("✓ save_trend_data: appends to existing file")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_all_tests():
    print("\nRunning quality_dashboard tests...\n")

    tests = [
        test_analyze_listing_full,
        test_analyze_listing_minimal,
        test_analyze_listing_no_schema_version,
        test_analyze_listing_category_path,
        test_analyze_listing_date_added,
        test_generate_dashboard_empty,
        test_generate_dashboard_single_listing,
        test_generate_dashboard_quality_tiers,
        test_generate_dashboard_no_tags,
        test_generate_dashboard_category_breakdown,
        test_generate_dashboard_recent_additions,
        test_generate_dashboard_avg_tags_and_specs,
        test_save_trend_data_creates_file,
        test_save_trend_data_appends,
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
