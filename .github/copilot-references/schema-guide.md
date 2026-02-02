# JSON Schema Guide for Supplier Listings
**Version:** 1.0
**Date:** February 2, 2026
**Purpose:** Complete reference for creating schema-compliant supplier JSON listings

## Schema Overview

Every supplier listing in the pcsdbx repository must conform to a standardized JSON schema that ensures consistency, completeness, and integration-readiness across the database. The schema defines required fields, optional fields, data types, formats, and validation rules.

## Complete Schema Structure

```json
{
  "id": "string (required, unique)",
  "name": "string (required)",
  "website": "string (required, valid URL)",
  "category": "string (required, from taxonomy)",
  "subcategory": "string (required, from taxonomy)",
  "description": "string (required, 1-2 sentences)",
  "headquarters": "string (required, format: 'City, Country')",
  "products": ["array of strings (required, minimum 3 items)"],
  "certifications": ["array of strings (required, can be empty)"],
  "geographic_coverage": ["array of strings (required, minimum 1 item)"],
  "specializations": ["array of strings (required, minimum 2 items)"],
  "date_added": "string (required, format: YYYY-MM-DD)",
  "last_updated": "string (required, format: YYYY-MM-DD)",
  "pricing_tier": "string (optional, values: budget|mid-range|premium)",
  "minimum_order": "string (optional)",
  "lead_time": "string (optional)",
  "contact_email": "string (optional, valid email)",
  "phone": "string (optional)",
  "linkedin": "string (optional, valid URL)",
  "key_products": ["array of objects (optional)"]
}
```

## Required Fields

### 1. id (string, required, unique)

**Purpose:** Unique identifier for the supplier listing

**Format:** `[CATEGORY_CODE][SUBCATEGORY_CODE][SEQUENCE]`

**Rules:**
- Must be unique across entire repository
- Use consistent category and subcategory codes
- Use zero-padded sequence numbers (001, 002, etc.)
- Alphanumeric characters and underscores only

**Examples:**
- `RM_POST_001` - Raw Materials, Postbiotics, sequence 001
- `EQ_MIX_042` - Equipment, Mixing Equipment, sequence 042
- `BS_FORM_015` - Business Services, Formulation, sequence 015

**Category Codes:**
- `RM` - Raw_Materials
- `EQ` - Equipment
- `BS` - Business_Services
- `PK` - Packaging
- `LS` - Labels__Sleeves

**Validation:**
- Check uniqueness before committing
- Verify category/subcategory codes match taxonomy
- Use consistent formatting across repository

### 2. name (string, required)

**Purpose:** Official company name or trading name

**Rules:**
- Use official legal name when available
- Include legal suffixes (Ltd, Inc, GmbH, etc.) if commonly used
- Use consistent capitalization (typically Title Case)
- Avoid abbreviations unless official
- No marketing taglines or slogans

**Examples:**
- ✅ "Evonik Industries AG"
- ✅ "CLR Berlin"
- ✅ "Silab - Société Industrielle de Laboratoires"
- ❌ "Evonik - Your Partner in Innovation" (no taglines)
- ❌ "clr berlin" (incorrect capitalization)

**Validation:**
- Verify against official website
- Check company registration if available
- Use consistent naming across listings

### 3. website (string, required, valid URL)

**Purpose:** Official company website URL

**Format:** Full URL with protocol (https:// or http://)

**Rules:**
- Must be accessible and current
- Use primary corporate website (not product microsites)
- Include protocol (https:// preferred)
- No trailing slashes unless required
- No URL shorteners or redirects

**Examples:**
- ✅ "https://www.evonik.com"
- ✅ "https://www.clr-berlin.com"
- ✅ "https://www.silab.fr"
- ❌ "www.evonik.com" (missing protocol)
- ❌ "https://bit.ly/evonik" (URL shortener)

**Validation:**
- Verify website is accessible
- Check for HTTPS (preferred for security)
- Confirm website is current (not outdated or abandoned)

### 4. category (string, required, from taxonomy)

**Purpose:** Main category classification

**Valid Values:**
- `Raw_Materials`
- `Equipment`
- `Business_Services`
- `Packaging`
- `Labels__Sleeves`

**Rules:**
- Must match exactly (case-sensitive)
- Must correspond to directory structure
- Cannot be custom or arbitrary value

**Examples:**
- ✅ "Raw_Materials"
- ❌ "raw_materials" (incorrect case)
- ❌ "Ingredients" (not in taxonomy)

### 5. subcategory (string, required, from taxonomy)

**Purpose:** Specific subcategory classification

**Rules:**
- Must match existing subcategory in taxonomy
- Must be child of specified category
- Use underscores for multi-word subcategories
- Case-sensitive

**Examples (Raw_Materials):**
- "Actives_Postbiotics"
- "Actives_Prebiotics"
- "Emulsifiers_Nonionic"
- "Preservatives_Traditional"

**Examples (Equipment):**
- "Mixing_Equipment"
- "Filling_Equipment"
- "Clean_Room_Equipment"

**Validation:**
- Verify subcategory exists in taxonomy
- Confirm subcategory belongs to specified category
- Check directory structure matches

### 6. description (string, required, 1-2 sentences)

**Purpose:** Concise description of what the supplier provides

**Rules:**
- 1-2 sentences maximum
- Focus on what they supply, not company history
- Include key differentiators
- Use professional, factual language
- No marketing hype or superlatives
- Start with supplier type or specialization

**Good Examples:**
```
"Global supplier of fermentation-derived postbiotic actives for skincare applications, specializing in Bifida and Lactobacillus lysates with COSMOS certification."

"French biotechnology company producing patented prebiotic ingredients through bioguided fermentation, focusing on microbiome-friendly skincare actives."

"Specialized manufacturer of high-pressure homogenizers and microfluidization equipment for cosmetic emulsion production, serving global personal care manufacturers."
```

**Poor Examples:**
```
❌ "Leading innovator revolutionizing the cosmetics industry with cutting-edge solutions." (marketing hype, vague)

❌ "Founded in 1985, the company has grown to become a trusted partner..." (company history, not what they supply)

❌ "Supplier of ingredients." (too vague, no differentiators)
```

**Validation:**
- Count sentences (1-2 only)
- Check for marketing language
- Verify factual accuracy
- Ensure key differentiators included

### 7. headquarters (string, required, format: "City, Country")

**Purpose:** Primary headquarters location

**Format:** "City, Country"

**Rules:**
- Use format: "City, Country" (comma and space)
- Use full country name (not abbreviations)
- Use English country names
- Use primary headquarters if multiple locations
- Capitalize properly

**Examples:**
- ✅ "Essen, Germany"
- ✅ "Paris, France"
- ✅ "New York, United States"
- ❌ "Essen, DE" (country abbreviation)
- ❌ "Germany" (missing city)
- ❌ "essen, germany" (incorrect capitalization)

**Validation:**
- Verify format with comma and space
- Check capitalization
- Confirm location accuracy from website

### 8. products (array of strings, required, minimum 3 items)

**Purpose:** List of product categories or key products supplied

**Rules:**
- Minimum 3 items required
- Use broad categories for general suppliers
- Use specific product names for specialized suppliers
- Maintain consistent naming conventions
- No empty strings
- Capitalize properly

**Examples (Broad Categories):**
```json
"products": [
  "Postbiotic Actives",
  "Fermentation Lysates",
  "Microbiome-Friendly Preservatives",
  "Probiotic Extracts"
]
```

**Examples (Specific Products):**
```json
"products": [
  "BeautiFerm® Lift",
  "BeautiFerm® Healerine",
  "Yeast Ferment Extract",
  "Reishi Mushroom Ferment"
]
```

**Validation:**
- Count items (minimum 3)
- Check for empty strings
- Verify naming consistency
- Confirm products match supplier specialization

### 9. certifications (array of strings, required, can be empty)

**Purpose:** List of relevant certifications and standards

**Rules:**
- Can be empty array if no certifications: `[]`
- Use standard abbreviations
- Include only verified certifications
- Capitalize properly
- No duplicates

**Common Certifications:**
- `COSMOS` - COSMOS organic/natural certification
- `IECIC` - China IECIC registration
- `ISO 22716` - GMP for cosmetics
- `NATRUE` - Natural cosmetics certification
- `ECOCERT` - Organic certification
- `Halal` - Halal certification
- `Vegan` - Vegan certification
- `Cruelty-Free` - No animal testing

**Examples:**
```json
"certifications": ["COSMOS", "IECIC", "ISO 22716"]
"certifications": ["NATRUE", "ECOCERT"]
"certifications": []
```

**Validation:**
- Verify certifications when possible
- Use standard abbreviations
- Check for duplicates
- Confirm relevance to personal care industry

### 10. geographic_coverage (array of strings, required, minimum 1 item)

**Purpose:** Regions or countries where supplier operates or distributes

**Rules:**
- Minimum 1 item required
- Use continent/region names or "Global"
- Capitalize properly
- No duplicates
- Be specific when company serves limited regions

**Standard Values:**
- `Global` - Worldwide distribution
- `Europe`
- `North America`
- `South America`
- `Asia`
- `Africa`
- `Oceania`
- `Middle East`

**Examples:**
```json
"geographic_coverage": ["Global"]
"geographic_coverage": ["Europe", "North America"]
"geographic_coverage": ["Asia", "Oceania"]
```

**Validation:**
- Check minimum 1 item
- Verify geographic accuracy from website
- Use standard region names
- Check for duplicates

### 11. specializations (array of strings, required, minimum 2 items)

**Purpose:** Unique capabilities, technologies, or focus areas

**Rules:**
- Minimum 2 items required
- Focus on unique capabilities or technologies
- Include relevant industry buzzwords
- Capitalize properly
- No duplicates

**Common Specializations:**
- Technology: "Fermentation technology", "Encapsulation systems", "Nanotechnology"
- Certifications: "COSMOS-certified actives", "IECIC-listed ingredients"
- Focus Areas: "Microbiome science", "Green chemistry", "Sustainable ingredients"
- Capabilities: "Custom formulation", "Contract manufacturing", "Regulatory support"

**Examples:**
```json
"specializations": [
  "Fermentation technology",
  "COSMOS-certified actives",
  "Microbiome science"
]
```

**Validation:**
- Count items (minimum 2)
- Verify uniqueness and relevance
- Check for duplicates
- Confirm alignment with description

### 12. date_added (string, required, format: YYYY-MM-DD)

**Purpose:** Date when listing was added to repository

**Format:** YYYY-MM-DD (ISO 8601 date format)

**Rules:**
- Use ISO 8601 format (YYYY-MM-DD)
- Use date when listing was created
- Must be valid date
- Cannot be future date

**Examples:**
- ✅ "2026-02-02"
- ✅ "2025-11-15"
- ❌ "02/02/2026" (wrong format)
- ❌ "2026-2-2" (missing zero-padding)

**Validation:**
- Verify format YYYY-MM-DD
- Check date is valid
- Confirm date is not in future

### 13. last_updated (string, required, format: YYYY-MM-DD)

**Purpose:** Date when listing was last updated

**Format:** YYYY-MM-DD (ISO 8601 date format)

**Rules:**
- Use ISO 8601 format (YYYY-MM-DD)
- Initially same as date_added
- Update when information changes
- Must be >= date_added
- Cannot be future date

**Examples:**
- ✅ "2026-02-02"
- ✅ "2026-02-15" (if updated after initial creation)
- ❌ "2025-11-01" (before date_added)

**Validation:**
- Verify format YYYY-MM-DD
- Check date is valid
- Confirm date >= date_added
- Confirm date is not in future

## Optional Fields

### 14. pricing_tier (string, optional)

**Purpose:** General pricing category

**Valid Values:**
- `budget` - Lower-cost options
- `mid-range` - Average market pricing
- `premium` - Higher-end pricing

**Rules:**
- Use lowercase
- Based on market positioning
- Subjective assessment acceptable
- Omit if uncertain

**Examples:**
```json
"pricing_tier": "premium"
"pricing_tier": "mid-range"
```

### 15. minimum_order (string, optional)

**Purpose:** Minimum order quantity or value

**Format:** Free-form string with units

**Examples:**
```json
"minimum_order": "1 kg"
"minimum_order": "$500 USD"
"minimum_order": "No minimum"
```

### 16. lead_time (string, optional)

**Purpose:** Typical delivery timeframe

**Format:** Free-form string

**Examples:**
```json
"lead_time": "2-4 weeks"
"lead_time": "Stock items: 1 week, Custom: 6-8 weeks"
```

### 17. contact_email (string, optional, valid email)

**Purpose:** Sales or general contact email

**Format:** Valid email address

**Examples:**
```json
"contact_email": "sales@example.com"
"contact_email": "info@example.com"
```

### 18. phone (string, optional)

**Purpose:** Contact phone number

**Format:** Free-form string with country code

**Examples:**
```json
"phone": "+49-201-177-01"
"phone": "+1-234-567-8900"
```

### 19. linkedin (string, optional, valid URL)

**Purpose:** LinkedIn company page URL

**Format:** Full LinkedIn URL

**Examples:**
```json
"linkedin": "https://linkedin.com/company/evonik"
```

### 20. key_products (array of objects, optional)

**Purpose:** Detailed information about specific products

**Structure:**
```json
"key_products": [
  {
    "name": "Product Name",
    "inci_name": "INCI Name",
    "category": "Category",
    "price_range": "Price information"
  }
]
```

**Example:**
```json
"key_products": [
  {
    "name": "BeautiFerm® Lift",
    "inci_name": "Pichia Ferment Lysate",
    "category": "Postbiotic Active",
    "price_range": "Premium"
  }
]
```

## Complete Example

```json
{
  "id": "RM_POST_001",
  "name": "Evonik Industries AG",
  "website": "https://www.evonik.com",
  "category": "Raw_Materials",
  "subcategory": "Actives_Postbiotics",
  "description": "Global supplier of fermentation-derived postbiotic actives for skincare applications, specializing in yeast and mushroom ferments with COSMOS certification and 40+ years of biotechnology expertise.",
  "headquarters": "Essen, Germany",
  "products": [
    "BeautiFerm® Lift (Yeast Ferment)",
    "BeautiFerm® Healerine (Reishi Mushroom Ferment)",
    "Fermentation-Derived Actives",
    "Microbiome-Friendly Ingredients"
  ],
  "certifications": ["COSMOS", "IECIC"],
  "geographic_coverage": ["Global"],
  "specializations": [
    "Fermentation technology",
    "COSMOS-certified actives",
    "Microbiome science",
    "Sustainable biotechnology"
  ],
  "date_added": "2026-02-02",
  "last_updated": "2026-02-02",
  "pricing_tier": "premium",
  "contact_email": "personal-care@evonik.com",
  "linkedin": "https://linkedin.com/company/evonik",
  "key_products": [
    {
      "name": "BeautiFerm® Lift",
      "inci_name": "Pichia Ferment Lysate",
      "category": "Postbiotic Active",
      "price_range": "Premium"
    },
    {
      "name": "BeautiFerm® Healerine",
      "inci_name": "Ganoderma Lucidum (Mushroom) Extract",
      "category": "Postbiotic Active",
      "price_range": "Premium"
    }
  ]
}
```

## Validation Checklist

### Pre-Commit Validation

**Required Fields:**
- ✅ `id` present, unique, correct format
- ✅ `name` present, non-empty, proper capitalization
- ✅ `website` present, valid URL, accessible
- ✅ `category` present, matches taxonomy
- ✅ `subcategory` present, matches taxonomy
- ✅ `description` present, 1-2 sentences, factual
- ✅ `headquarters` present, format "City, Country"
- ✅ `products` array present, minimum 3 items
- ✅ `certifications` array present (can be empty)
- ✅ `geographic_coverage` array present, minimum 1 item
- ✅ `specializations` array present, minimum 2 items
- ✅ `date_added` present, format YYYY-MM-DD
- ✅ `last_updated` present, format YYYY-MM-DD

**Data Quality:**
- ✅ No placeholder text ("TBD", "Unknown", "N/A")
- ✅ No empty strings in arrays
- ✅ Consistent capitalization and formatting
- ✅ Factually accurate information
- ✅ Professional language (no marketing hype)

**JSON Validity:**
- ✅ Valid JSON syntax (no trailing commas)
- ✅ Proper quotes (double quotes for strings)
- ✅ Proper array and object structure
- ✅ Consistent indentation (2 or 4 spaces)
- ✅ UTF-8 encoding for special characters

## Common Errors and Solutions

### Error 1: Missing Required Field

**Error:** Listing missing `specializations` field

**Solution:**
```json
"specializations": [
  "Relevant specialization 1",
  "Relevant specialization 2"
]
```

### Error 2: Invalid Date Format

**Error:** `"date_added": "02/02/2026"`

**Solution:**
```json
"date_added": "2026-02-02"
```

### Error 3: Insufficient Array Items

**Error:** `"products": ["Product 1", "Product 2"]` (only 2 items)

**Solution:**
```json
"products": [
  "Product 1",
  "Product 2",
  "Product 3"
]
```

### Error 4: Invalid Category

**Error:** `"category": "Ingredients"`

**Solution:**
```json
"category": "Raw_Materials"
```

### Error 5: Marketing Language in Description

**Error:** `"description": "Leading innovator revolutionizing skincare with cutting-edge solutions."`

**Solution:**
```json
"description": "Supplier of fermentation-derived postbiotic actives for skincare applications, specializing in Bifida and Lactobacillus lysates with COSMOS certification."
```

## Conclusion

Following this schema guide ensures all supplier listings maintain 100% compliance, enabling seamless integration with SKIN-TWIN, PIFDocMagician, and other ecosystem components. Consistent, high-quality data is the foundation of the integrated cosmetic science platform.

**Key Principles:**
1. ✅ All required fields must be present and valid
2. ✅ Use exact formats and values specified
3. ✅ Maintain factual, professional language
4. ✅ Verify information accuracy
5. ✅ Validate before committing

**Quality is non-negotiable. Schema compliance is mandatory.** ✨
