# Contributing to Personal Care Suppliers Database

Thank you for your interest in contributing to the Personal Care Suppliers Database! This guide will help you add new listings while maintaining our quality standards.

## Table of Contents

- [Quick Start](#quick-start)
- [Adding a New Listing](#adding-a-new-listing)
- [File Naming Convention](#file-naming-convention)
- [Directory Structure](#directory-structure)
- [Required vs Optional Fields](#required-vs-optional-fields)
- [Validation](#validation)
- [Best Practices](#best-practices)
- [Getting Help](#getting-help)

## Quick Start

1. **Choose the right category** for your listing
2. **Create a JSON file** following the naming convention
3. **Fill in required fields** at minimum
4. **Add enhanced fields** for better quality (especially for strategic suppliers)
5. **Validate your listing** using the validation tool
6. **Submit a pull request**

## Adding a New Listing

### Step 1: Determine Category Path

Find the appropriate category for your listing. Examples:
- `Raw_Materials/Actives`
- `Business_Services/Contract_Manufacturing`
- `Equipment/Tanks`
- `Labels__Sleeves/Stretch_Sleeve`

**Note**: Use underscores for spaces in category names.

### Step 2: Create the JSON File

Create a new file in the appropriate directory:

```
listings/{Category_Path}/{category_id}_{listing_id}.json
```

### Step 3: Use the Template

Start with this template for a basic listing:

```json
{
  "schema_version": "1.0",
  "category_id": 1828,
  "listing_id": "company_name",
  "category_path": "Raw_Materials/Actives",
  "url": "https://personalcaresuppliers.com/Listing/Index/...",
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

### Step 4: Add Enhanced Fields

For better quality listings (especially strategic suppliers), add:

```json
{
  "schema_version": "1.0",
  "category_id": 1828,
  "listing_id": "company_name",
  "category_path": "Raw_Materials/Actives",
  "url": "https://personalcaresuppliers.com/Listing/Index/...",
  "company_name": "Company Name Inc.",
  "address": "123 Main St, City, State 12345",
  "country": "United States",
  "phone": "555-123-4567",
  "email": "info@company.com",
  "website": "https://www.company.com",
  "specializations": [
    "Product Category 1",
    "Product Category 2"
  ],
  "certifications": [
    "Organic Certification",
    "ISO 9001"
  ],
  "tags": [
    "organic",
    "sustainable"
  ],
  "status": "active",
  "date_added": "2025-11-03",
  "date_updated": "2025-11-03",
  "metadata": {
    "last_validated": "2025-11-03",
    "validation_method": "manual",
    "data_source": "manual_entry"
  },
  "notes": "Additional information about the supplier"
}
```

## File Naming Convention

**Pattern**: `{category_id}_{listing_id}.json`

**Rules**:
- Use the numeric category_id (e.g., 1828 for Raw Materials/Actives)
- Use a descriptive, lowercase listing_id with underscores
- The listing_id should match the company name or numeric ID from the website
- File must have .json extension

**Examples**:
- `1828_oat_cosmetics.json` ✅
- `1828_givaudan_active_beauty.json` ✅
- `1790_kbl_cosmetics.json` ✅
- `1828_1102292.json` ✅ (numeric ID from website)
- `1828_OatCosmetics.json` ❌ (use lowercase)
- `oat_cosmetics.json` ❌ (missing category_id)

## Directory Structure

Place your JSON file in the correct directory matching the category_path:

```
listings/
├── Raw_Materials/
│   └── Actives/
│       └── 1828_your_listing.json
├── Business_Services/
│   ├── Contract_Manufacturing/
│   │   └── 1790_your_listing.json
│   └── Auditing/
│       └── 1790_your_listing.json
├── Equipment/
│   └── Tanks/
│       └── 1801_your_listing.json
└── Labels__Sleeves/
    └── Stretch_Sleeve/
        └── 1800_your_listing.json
```

**Note**: Create new directories if needed for new categories.

## Required vs Optional Fields

### Always Required ⚠️

These fields **must** be present in every listing:

- `schema_version`: Always "1.0" for current schema
- `category_id`: Numeric or string identifier
- `listing_id`: Unique identifier (must match filename)
- `category_path`: Must match directory structure
- `url`: Valid URL to the listing
- `status`: One of: "active", "inactive", "pending", "archived"
- `date_added`: Date in YYYY-MM-DD format

### Recommended for Quality ⭐

Include these for better listings:

- `company_name`: Name of the company
- `website`: Company website
- `specializations`: What they specialize in
- `tags`: For filtering and categorization
- `date_updated`: Last update date
- `metadata`: Tracking information

### Required for Strategic Suppliers 🌟

Strategic suppliers (tagged with "oat-specialist", "major-player", etc.) should include:

- All basic required fields
- `company_name`
- `specializations`
- `certifications`
- `product_highlights`
- `tags` (to mark as strategic)
- `metadata` with quality tracking

### Optional but Valuable

- `address`, `country`, `phone`, `email`
- `product_highlights`
- `key_benefits`
- `raw_material_source`
- `shipping_regions`
- `distributor_regions`
- `notes`

## Validation

### Before Submitting

**Always run the validation tool** before submitting:

```bash
python3 scripts/validation/validate_listings.py
```

This will:
- Check for required fields
- Validate data types
- Verify file naming
- Check directory structure
- Generate a quality report

### What the Validator Checks

1. **Schema compliance**: All required fields present
2. **Type validation**: Fields have correct data types
3. **Format validation**: Dates, URLs, emails properly formatted
4. **Naming consistency**: Filename matches listing_id and category_id
5. **Location validation**: File in correct directory for category_path
6. **Business rules**: Strategic suppliers have enhanced fields

### Fixing Validation Errors

Common errors and how to fix them:

**Error**: `Missing required field: schema_version`
- **Fix**: Add `"schema_version": "1.0"` to your JSON

**Error**: `Filename does not match listing_id`
- **Fix**: Rename file to match the listing_id in the JSON

**Error**: `File location does not match category_path`
- **Fix**: Move file to correct directory or update category_path

**Error**: `Invalid date format`
- **Fix**: Use YYYY-MM-DD format (e.g., "2025-11-03")

**Error**: `Field has incorrect type`
- **Fix**: Check schema - arrays should be `[]`, strings should be `""`

## Best Practices

### 1. Use Consistent Naming

- Lowercase for listing_id
- Underscores instead of spaces
- Descriptive names when possible

### 2. Keep URLs Updated

- Verify the URL works before adding
- Include full URL path from personalcaresuppliers.com

### 3. Tag Appropriately

Choose relevant tags from:
- `oat-specialist`, `organic`, `sustainable`
- `major-player`, `small-batch`
- `biotechnology`, `natural-ingredients`
- `certified`, `global-distributor`
- `contract-manufacturer`, `private-label`, `full-service`

### 4. Add Quality Metadata

Track the source and validation:

```json
"metadata": {
  "last_validated": "2025-11-03",
  "validation_method": "manual",
  "data_source": "website"
}
```

### 5. Include Notes for Context

Add helpful context in the notes field:

```json
"notes": "Leading supplier of oat-derived ingredients. Strategic priority for oat-focused products."
```

### 6. Use Arrays Properly

Arrays should be formatted as JSON arrays:

```json
"specializations": [
  "Item 1",
  "Item 2"
]
```

Not strings:
```json
"specializations": "Item 1, Item 2"  ❌
```

### 7. Format JSON Properly

- Use 2-space indentation
- Include trailing newline
- Ensure valid JSON syntax

You can use a JSON formatter:
```bash
python3 -m json.tool your_file.json > formatted.json
```

### 8. One Listing Per File

Each supplier listing should be in its own file.

### 9. Update date_updated

When modifying an existing listing, update:
- `date_updated` field
- `metadata.last_validated` field

### 10. Document Your Sources

In metadata, note where the data came from:
- `"data_source": "website"` - From company website
- `"data_source": "manual_entry"` - Manually researched
- `"data_source": "scraper"` - Automated collection
- `"data_source": "api"` - From an API

## Getting Help

### Documentation

- See [DATA_QUALITY.md](DATA_QUALITY.md) for detailed quality standards
- See [README.md](../README.md) for repository overview
- See schema at `scripts/validation/listing_schema.json`

### Questions?

If you're unsure about:
- Which category to use
- How to structure a field
- Validation errors you can't fix

Please open an issue or ask in the pull request comments.

## Pull Request Checklist

Before submitting your PR, ensure:

- [ ] File is in correct directory
- [ ] Filename follows naming convention
- [ ] All required fields are present
- [ ] JSON is valid and properly formatted
- [ ] Validation passes (`validate_listings.py` shows no errors)
- [ ] Enhanced fields added for strategic suppliers
- [ ] Tags applied appropriately
- [ ] URLs verified to work
- [ ] `date_added` and `date_updated` are correct
- [ ] No sensitive information included

## Example: Complete Strategic Supplier Listing

```json
{
  "schema_version": "1.0",
  "category_id": 1828,
  "listing_id": "oat_cosmetics",
  "category_path": "Raw_Materials/Actives",
  "url": "https://personalcaresuppliers.com/Listing/Index/Raw_Materials/Actives/1828/",
  "company_name": "Oat Cosmetics (Oat Services Ltd.)",
  "address": "The University of Southampton Science Park, 2 Venture Road, Chilworth, Southampton, Hampshire, SO16 7NP",
  "country": "United Kingdom",
  "phone": "+44 (0) 2380 767 228",
  "email": "info@oatcosmetics.com",
  "website": "https://oatcosmetics.com",
  "specializations": [
    "100% Oat-Derived Ingredients",
    "Beta-Glucan Actives",
    "Colloidal Oatmeal"
  ],
  "certifications": [
    "ECOCERT Natural",
    "ECOCERT Organic"
  ],
  "product_highlights": [
    "EcoPep - Novel high purity oat peptide",
    "Rejuvaveen - Enriched beta-glucan active"
  ],
  "tags": [
    "oat-specialist",
    "organic",
    "sustainable",
    "biotechnology",
    "natural-ingredients",
    "certified"
  ],
  "status": "active",
  "date_added": "2025-11-03",
  "date_updated": "2025-11-03",
  "metadata": {
    "last_validated": "2025-11-03",
    "validation_method": "manual",
    "data_source": "website"
  },
  "notes": "Leading manufacturer of 100% natural oat-derived cosmetics ingredients. Strategic priority supplier for oat-based ingredient focus."
}
```

## Thank You! 🎉

Your contributions help build a comprehensive, high-quality database of personal care suppliers. Every listing adds value to the community!
