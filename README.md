# Personal Care Suppliers Database (pcsdbx)

This repository contains a structured database of listings from [Personal Care Suppliers](https://personalcaresuppliers.com/).

## 🤖 Automated Agent Communication

This repository includes **automated GitHub Actions** that monitor and facilitate communication between AI agents working on the project. Messages between agents are automatically detected and processed.

👉 **See [AUTOMATION.md](AUTOMATION.md) for details on how the automated message monitoring works.**

## Repository Structure

The repository organizes listings by category path in a hierarchical directory structure:

```
├── source_pages.json          # Master list of source pages to track
├── listings/                  # Supplier listing JSON files
│   ├── Raw_Materials/
│   │   └── Actives/
│   │       └── 1828_*.json
│   ├── Business_Services/
│   │   ├── Auditing/
│   │   │   └── 1790_*.json
│   │   └── Contract_Manufacturing/
│   │       └── 1790_*.json
│   ├── Equipment/
│   │   └── Tanks/
│   │       └── 1801_*.json
│   └── Labels__Sleeves/
│       └── Stretch_Sleeve/
│           └── 1800_*.json
├── scripts/                   # Automation tools
│   ├── validation/            # Data quality and validation tools
│   ├── scraper/               # Web scraping tools (planned)
│   ├── import/                # Batch import utilities (planned)
│   └── reporting/             # Analytics and reporting (planned)
├── tests/                     # Test suite
│   ├── fixtures/              # Sample data for testing
│   └── test_validation.py     # Validation tool tests
└── docs/                      # Documentation
    ├── DATA_QUALITY.md        # Data quality standards
    ├── CONTRIBUTING.md        # Contribution guidelines
    ├── SCRAPER_GUIDE.md       # Scraper documentation (planned)
    └── API_DESIGN.md          # Future API design
```

### Source Pages

The `source_pages.json` file contains a comprehensive list of 313 source pages from personalcaresuppliers.com that should be tracked. This includes:

- **Informational pages**: Homepage, guides (CUI, Help), and media kit
- **Category listing pages**: 309 category-specific listing pages across all major product and service categories

This file serves as a reference for scraping, crawling, or monitoring activities.

## Data Format

Each listing is stored as a JSON file following schema version 1.0:

```json
{
  "schema_version": "1.0",
  "category_id": 1828,
  "listing_id": "company_name",
  "category_path": "Raw_Materials/Actives",
  "url": "https://personalcaresuppliers.com/Listing/Index/Raw_Materials/Actives/1828/",
  "company_name": "Example Company Inc.",
  "status": "active",
  "date_added": "2025-11-03",
  "date_updated": "2025-11-03",
  "tags": ["organic", "sustainable"],
  "metadata": {
    "last_validated": "2025-11-03",
    "validation_method": "manual",
    "data_source": "manual_entry"
  }
}
```

### Required Fields

- `schema_version`: Version of the schema being used (currently "1.0")
- `category_id`: The numeric identifier for the category
- `listing_id`: The unique identifier for the listing
- `category_path`: The hierarchical path of the category (using underscores for spaces)
- `url`: The full URL to the listing on personalcaresuppliers.com
- `status`: Status of the listing (e.g., "active", "inactive", "pending", "archived")
- `date_added`: Date when the listing was added to this database (YYYY-MM-DD format)

### Optional Fields

- `date_updated`: Date when last updated (YYYY-MM-DD)
- `company_name`: Name of the company/supplier
- `address`, `country`, `phone`, `email`, `website`: Contact information
- `specializations`: Array of specializations or product categories
- `certifications`: Array of certifications held
- `product_highlights`: Key products or product lines
- `tags`: Array of classification tags for filtering (e.g., "oat-specialist", "organic", "major-player")
- `metadata`: Tracking information (last_validated, validation_method, data_source, quality_score)
- `notes`: Additional notes about the listing

See [docs/DATA_QUALITY.md](docs/DATA_QUALITY.md) for complete field documentation.

## File Naming Convention

Listing files are named using the pattern: `{category_id}_{listing_id}.json`

For example: `1828_1102292.json`

## Current Listings

The database currently contains **15 listings** across the following categories:

1. **Raw Materials → Actives** (8 listings) - Category ID: 1828
2. **Business Services → Contract Manufacturing** (4 listings) - Category ID: 1790
3. **Business Services → Auditing** (1 listing) - Category ID: 1790
4. **Equipment → Tanks** (1 listing) - Category ID: 1801
5. **Labels & Sleeves → Stretch Sleeve** (1 listing) - Category ID: 1800

See [LISTINGS_INDEX.md](LISTINGS_INDEX.md) for a complete index.

## Tools & Automation

### Validation Tools

Validate all listings against schema and quality standards:

```bash
python3 scripts/validation/validate_listings.py
```

See [scripts/README.md](scripts/README.md) for all available tools.

### Running Tests

```bash
python3 tests/test_validation.py
```

See [tests/README.md](tests/README.md) for test documentation.

## Documentation

- **[docs/DATA_QUALITY.md](docs/DATA_QUALITY.md)** - Data quality standards and validation rules
- **[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)** - Guidelines for adding new listings
- **[docs/SCRAPER_GUIDE.md](docs/SCRAPER_GUIDE.md)** - Web scraping documentation (coming Week 2)
- **[docs/API_DESIGN.md](docs/API_DESIGN.md)** - Future API specifications

## Contributing

### Adding New Listings

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

**Quick steps:**

1. Create the appropriate category directory structure under `listings/` if it doesn't exist
2. Create a new JSON file following the naming convention: `{category_id}_{listing_id}.json`
3. Use schema version 1.0 and include all required fields
4. Add enhanced fields for better quality (especially for strategic suppliers)
5. Validate your listing: `python3 scripts/validation/validate_listings.py`
6. Submit a pull request with your additions

**Example listing:**

```json
{
  "schema_version": "1.0",
  "category_id": 1828,
  "listing_id": "example_company",
  "category_path": "Raw_Materials/Actives",
  "url": "https://personalcaresuppliers.com/Listing/Index/Raw_Materials/Actives/1828/",
  "company_name": "Example Company",
  "status": "active",
  "date_added": "2025-11-03",
  "date_updated": "2025-11-03",
  "metadata": {
    "last_validated": "2025-11-03",
    "validation_method": "manual",
    "data_source": "manual_entry"
  }
}
```

## License

See [LICENSE](LICENSE) file for details.