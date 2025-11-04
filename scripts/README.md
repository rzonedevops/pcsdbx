# Scripts Directory

This directory contains automation tools for the Personal Care Suppliers Database.

## Directory Structure

```
scripts/
├── validation/       # Data quality and validation tools
├── scraper/          # Web scraping tools (coming in Week 2)
├── import/           # Batch import utilities (planned)
└── reporting/        # Analytics and reporting (planned)
```

## Available Tools

### Validation Tools (`validation/`)

#### validate_listings.py
Validates all listing files against the schema and business rules.

**Usage:**
```bash
python3 scripts/validation/validate_listings.py
```

**Features:**
- Schema validation (required fields, types, formats)
- Business logic validation (naming, directory structure)
- Quality metrics reporting
- Generates `validation_report.txt`

**Output:**
- ✓ Valid listings
- ✗ Invalid listings with detailed errors
- Quality metrics (schema compliance, enhanced fields coverage, etc.)

#### migrate_to_v1.py
Migrates existing listings to schema version 1.0.

**Usage:**
```bash
# Preview changes (dry run)
python3 scripts/validation/migrate_to_v1.py --dry-run

# Apply migration
python3 scripts/validation/migrate_to_v1.py
```

**Features:**
- Adds `schema_version` field
- Adds `date_updated` field
- Adds `metadata` section
- Auto-generates `tags` based on content analysis
- Safe dry-run mode

#### listing_schema.json
JSON Schema definition for supplier listings.

Defines:
- Required fields
- Optional fields
- Field types and formats
- Validation rules
- Allowed values (enums)

## Coming Soon

### Scraper Tools (`scraper/`)
Web scraping tools for automated data collection. Planned for Week 2.

Features:
- Rate limiting (1.5s between requests)
- Error handling and retry logic
- Progress tracking
- Validation integration

See [docs/SCRAPER_GUIDE.md](../docs/SCRAPER_GUIDE.md) for details.

### Import Tools (`import/`)
Batch import utilities for adding multiple listings at once.

Planned features:
- CSV to JSON conversion
- Bulk validation
- Duplicate detection
- Progress reporting

### Reporting Tools (`reporting/`)
Analytics and reporting on the database.

Planned features:
- Supplier statistics by category
- Tag distribution analysis
- Quality metrics dashboard
- Growth tracking
- Export to various formats

## Requirements

Python 3.7+ required for all scripts.

No external dependencies currently needed for validation tools (pure Python).

Future tools will require:
```
requests>=2.31.0
beautifulsoup4>=4.12.0
jsonschema>=4.19.0
python-dateutil>=2.8.0
```

Install with:
```bash
pip install -r requirements.txt
```

(requirements.txt will be added when needed)

## Running Tests

Tests will be added in the `tests/` directory.

```bash
# Run all tests
python3 -m pytest tests/

# Run specific test file
python3 -m pytest tests/test_validation.py
```

## Documentation

For detailed information, see:
- [DATA_QUALITY.md](../docs/DATA_QUALITY.md) - Data quality standards
- [CONTRIBUTING.md](../docs/CONTRIBUTING.md) - How to add listings
- [SCRAPER_GUIDE.md](../docs/SCRAPER_GUIDE.md) - Scraper documentation (coming soon)
- [API_DESIGN.md](../docs/API_DESIGN.md) - Future API design

## Best Practices

1. **Always validate** before committing changes
2. **Use dry-run mode** when testing migration or import tools
3. **Check validation reports** regularly
4. **Keep scripts updated** as schema evolves
5. **Document new tools** with usage examples

## Contributing

When adding new scripts:
1. Add comprehensive docstrings
2. Include usage examples in comments
3. Update this README
4. Add relevant tests
5. Document in appropriate docs/ file

## Questions?

See the main [README.md](../README.md) or open an issue.
