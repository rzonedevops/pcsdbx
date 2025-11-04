# Data Quality Standards

This document defines the data quality standards and validation rules for the Personal Care Suppliers Database.

## Schema Version

Current schema version: **1.0**

All listings must include a `schema_version` field to ensure proper validation and future compatibility.

## Required Fields

Every listing **must** include the following fields:

- **schema_version**: Version of the schema (e.g., "1.0")
- **category_id**: Numeric identifier for the category (integer or string)
- **listing_id**: Unique identifier for the listing (integer or string)
- **category_path**: Hierarchical path of the category (e.g., "Raw_Materials/Actives")
- **url**: Full URL to the listing on personalcaresuppliers.com
- **status**: Status of the listing (must be one of: "active", "inactive", "pending", "archived")
- **date_added**: Date when added to database (YYYY-MM-DD format)

## Optional Fields

### Basic Information
- **company_name**: Name of the company/supplier
- **address**: Physical address
- **country**: Country location
- **phone**: Contact phone number
- **email**: Contact email address
- **website**: Company website URL

### Enhanced Fields
- **date_updated**: Date when last updated (YYYY-MM-DD format)
- **tags**: Array of classification tags for filtering
- **specializations**: Array of specializations or product categories
- **certifications**: Array of certifications held
- **product_highlights**: Key products or product lines
- **key_benefits**: Key benefits or selling points
- **raw_material_source**: Source of raw materials (if applicable)
- **shipping_regions**: Regions where supplier ships
- **distributor_regions**: Regions where supplier has distributors
- **notes**: Additional notes about the listing

### Service Provider Fields
- **services**: Array of services offered (for service providers)

### Corporate Information
- **parent_company**: Parent company name if applicable
- **former_names**: Array of previous company names
- **manufacturing_facilities**: Array of manufacturing facility locations

### Listing Metadata
- **metadata**: Object containing:
  - **last_validated**: Date of last validation (YYYY-MM-DD)
  - **validation_method**: How validated ("manual", "automated", or "hybrid")
  - **data_source**: Source of data ("website", "manual_entry", "api", or "scraper")
  - **quality_score**: Quality score from 0-100 (optional)

## Field Requirements by Supplier Type

### Basic Listings
- **Required**: All required fields listed above
- **Recommended**: company_name, website
- **Optional**: All other fields

### Standard Listings
- **Required**: All required fields
- **Recommended**: All basic information fields, specializations, tags
- **Optional**: Enhanced fields

### Strategic Suppliers
Strategic suppliers are identified by tags such as "oat-specialist", "major-player", etc.

- **Required**: All required fields + enhanced fields
- **Strongly Recommended**: 
  - company_name
  - specializations
  - certifications
  - product_highlights
  - tags (to identify as strategic)
  - metadata (with quality metrics)

**Strategic Supplier Categories:**
- Oat specialists (highest priority)
- Major players (Lonza, Ashland, Givaudan, etc.)
- Unique capabilities (organic, sustainable, biotechnology)

## Tagging System

Use tags to enable filtering and quick identification of supplier characteristics:

**Available Tags:**
- `oat-specialist`: Specializes in oat-derived ingredients
- `organic`: Offers organic certified products
- `sustainable`: Focus on sustainable practices
- `small-batch`: Small batch production
- `major-player`: Large, established industry player
- `biotechnology`: Uses biotechnology in production
- `natural-ingredients`: Focus on natural ingredients
- `certified`: Holds relevant certifications
- `global-distributor`: Has global distribution network
- `contract-manufacturer`: Provides contract manufacturing
- `private-label`: Offers private label services
- `full-service`: Full-service provider

## Validation Rules

### Schema Validation
1. All required fields must be present
2. Field types must match schema definition
3. Date fields must follow YYYY-MM-DD format
4. Status must be one of the allowed values
5. URLs must be valid URI format
6. Email addresses must be valid format (if present)

### Business Logic Validation
1. **File Naming**: Files must follow pattern `{category_id}_{listing_id}.json`
2. **ID Matching**: Filename category_id and listing_id must match data fields
3. **Directory Structure**: File location must match category_path
4. **Strategic Suppliers**: Those tagged as strategic should have enhanced fields

### Data Quality Metrics

**Target Quality Levels:**
- Schema compliance: **100%** (all listings must validate)
- Enhanced field coverage: **80%+** (target for scalability)
- Tags coverage: **70%+** (for effective filtering)
- Metadata tracking: **90%+** (for quality monitoring)

## Quality Scores

Listings can be assigned a quality_score (0-100) in their metadata based on:

- **Completeness** (40 points):
  - All required fields present: 10 points
  - Company name and contact info: 10 points
  - Specializations listed: 10 points
  - Product highlights included: 10 points

- **Accuracy** (30 points):
  - Verified URL works: 15 points
  - Contact information verified: 15 points

- **Richness** (30 points):
  - Certifications listed: 10 points
  - Tags applied: 10 points
  - Additional details (benefits, sources, etc.): 10 points

**Quality Levels:**
- 90-100: Excellent - Strategic supplier quality
- 70-89: Good - Standard listing quality
- 50-69: Adequate - Basic listing quality
- Below 50: Needs improvement

## Validation Tools

### validate_listings.py
Validates all listings against the schema and business rules.

**Usage:**
```bash
python3 scripts/validation/validate_listings.py
```

**Output:**
- Console report with validation status
- Detailed error messages for invalid listings
- Quality metrics summary
- Written report to `validation_report.txt`

### migrate_to_v1.py
Migrates existing listings to schema version 1.0.

**Usage:**
```bash
# Dry run (preview changes)
python3 scripts/validation/migrate_to_v1.py --dry-run

# Apply migration
python3 scripts/validation/migrate_to_v1.py
```

**What it does:**
- Adds schema_version field
- Adds date_updated field (uses date_added if not present)
- Adds metadata section with validation tracking
- Auto-generates tags based on content analysis

## Best Practices

1. **Always validate** before committing new listings
2. **Use tags consistently** to enable effective filtering
3. **Keep URLs current** - verify they still work
4. **Document sources** in metadata.data_source
5. **Update date_updated** when making changes
6. **Track quality** using metadata.quality_score
7. **Follow naming conventions** strictly for consistency
8. **Use enhanced fields** for strategic suppliers
9. **Validate after batch imports** to catch issues early
10. **Review validation reports** regularly to maintain quality

## Future Enhancements

Planned improvements to data quality:

- **Month 2**: SQLite database for advanced querying while maintaining JSON as source of truth
- **Month 3**: Automated URL verification
- **Month 3**: Automated data quality scoring
- **Month 4**: Integration with external APIs for enrichment
- **Month 4**: Duplicate detection and merging tools
