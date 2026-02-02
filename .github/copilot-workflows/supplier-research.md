# Supplier Research Workflow
**Version:** 1.0
**Date:** February 2, 2026
**Purpose:** Systematic methodology for discovering and documenting personal care suppliers

## Overview

This workflow defines the step-by-step process for researching personal care suppliers, extracting relevant information, creating JSON listings, validating quality, and documenting findings. Following this workflow ensures consistency, quality, and efficiency in database expansion.

## Workflow Steps

### Step 1: Check Collaboration Folders & Priorities

**Purpose:** Align research with current strategic priorities and avoid duplication

**Actions:**
1. Read `/manus-2-copilot/` for priority updates from Manus AI
2. Review strategic focus areas in `copilot-instructions.md`
3. Check current targets and milestone dates
4. Note any specific supplier requests or category priorities
5. Verify no overlap with Manus's current research

**Decision Point:**
- ✅ Priorities clear → Proceed to Step 2
- ❌ Priorities unclear → Leave clarification message and wait for response

**Time Estimate:** 5-10 minutes

### Step 2: Identify Target Category & Research Strategy

**Purpose:** Define specific research scope and approach

**Actions:**
1. Select target category based on strategic priorities
2. Determine research depth (broad survey vs. deep dive)
3. Identify primary research sources
4. Set target for number of suppliers to discover
5. Define success criteria for this research session

**Strategic Priority Categories (Feb-Apr 2026):**
- ⭐⭐⭐⭐⭐ Microbiome Science (postbiotics, prebiotics, probiotics)
- ⭐⭐⭐⭐⭐ Advanced Delivery Systems (encapsulation, liposomes, nanotech)
- ⭐⭐⭐⭐⭐ Environmental Protection Actives (pollution, blue light, infrared)
- ⭐⭐⭐⭐ Longevity Science Actives (senolytics, autophagy, mitochondrial)
- ⭐⭐⭐⭐ Specialized Manufacturing Equipment (spray drying, freeze drying, etc.)

**Research Depth Options:**
- **Broad Survey:** Discover 10-20 suppliers quickly, basic information
- **Deep Dive:** Research 3-5 suppliers thoroughly, comprehensive information
- **Balanced:** Discover 5-10 suppliers with good information depth

**Time Estimate:** 5 minutes

### Step 3: Conduct Initial Research

**Purpose:** Discover suppliers and gather preliminary information

**Primary Research Sources:**

**Industry Databases:**
- UL Prospector (https://www.ulprospector.com/) - Comprehensive ingredient database
- SpecialChem (https://www.specialchem.com/) - Formulation and supplier intelligence
- Covalo (https://covalo.com/) - Ingredient marketplace and supplier network
- Making Cosmetics (https://www.makingcosmetics.com/) - DIY and professional ingredients
- Lotion Crafter (https://lotioncrafter.com/) - Specialty ingredients and supplies

**Search Engines:**
- Google: "[ingredient category] suppliers cosmetics"
- Google: "[technology] manufacturers personal care"
- Google: "[certification] certified suppliers skincare"

**Trade Publications:**
- Cosmetics & Toiletries (https://www.cosmeticsandtoiletries.com/)
- Personal Care Insights (https://www.personalcareinsights.com/)
- Cosmetics Business (https://cosmeticsbusiness.com/)

**Industry Events:**
- In-Cosmetics (supplier exhibitor lists)
- Suppliers' Day (attendee and exhibitor lists)
- NYSCC Suppliers' Day (supplier directory)

**Actions:**
1. Search primary databases for target category
2. Compile list of potential suppliers (names and websites)
3. Prioritize by relevance and tier (Tier 1 global > Tier 2 regional > Tier 3 local)
4. Create preliminary supplier list (10-20 candidates)
5. Document search queries and sources used

**Quality Indicators:**
- Company has professional website
- Clear product portfolio and specifications
- Certifications mentioned (COSMOS, IECIC, ISO)
- Global or regional distribution
- Established company (not startup without track record)

**Time Estimate:** 30-60 minutes

### Step 4: Visit Supplier Websites & Extract Information

**Purpose:** Gather detailed information for JSON listings

**For Each Supplier:**

**1. Navigate to Website**
- Verify website is accessible and current
- Check for English language version
- Locate "Products", "About Us", "Contact" sections

**2. Extract Required Information**
- **Company Name:** Official legal name or trading name
- **Website:** Full URL (https://www.example.com)
- **Headquarters:** City, Country (from "About Us" or "Contact")
- **Products:** List of product categories or key products (minimum 3)
- **Certifications:** COSMOS, IECIC, ISO 22716, NATRUE, etc.
- **Geographic Coverage:** Regions served (Europe, North America, Asia, etc.)
- **Specializations:** Unique capabilities or focus areas

**3. Extract Optional Information (When Available)**
- **Pricing Tier:** Budget, mid-range, premium (based on indicators)
- **Minimum Order:** Quantity or value requirements
- **Lead Time:** Typical delivery timeframe
- **Contact Information:** Sales email, phone number
- **Social Media:** LinkedIn company page
- **Key Products:** Specific products with INCI names and details

**4. Verify Information Quality**
- Cross-reference product claims with industry databases
- Verify certification claims when possible
- Check for recent updates (news, product launches)
- Assess website professionalism and completeness

**5. Document Research Notes**
- Source URLs for all information
- Confidence level in data accuracy (high/medium/low)
- Any questions or uncertainties
- Additional context or insights

**Time Estimate:** 10-15 minutes per supplier

### Step 5: Create JSON Listing

**Purpose:** Structure information in schema-compliant format

**Template Structure:**

```json
{
  "id": "unique-identifier",
  "name": "Company Name",
  "website": "https://www.example.com",
  "category": "Raw_Materials",
  "subcategory": "Actives_Postbiotics",
  "description": "Clear, concise description of what they supply (1-2 sentences)",
  "headquarters": "City, Country",
  "products": [
    "Product Category 1",
    "Product Category 2",
    "Product Category 3"
  ],
  "certifications": ["COSMOS", "IECIC", "ISO 22716"],
  "geographic_coverage": ["Europe", "North America", "Asia"],
  "specializations": [
    "Specialization 1",
    "Specialization 2"
  ],
  "date_added": "2026-02-02",
  "last_updated": "2026-02-02"
}
```

**ID Generation Rules:**
- Format: `[CATEGORY_CODE][SUBCATEGORY_CODE][SEQUENCE]`
- Example: `RM_POST_001` (Raw Materials, Postbiotics, sequence 001)
- Use consistent zero-padding for sequence numbers
- Verify ID is unique in repository

**Description Guidelines:**
- 1-2 sentences maximum
- Focus on what they supply, not company history
- Include key differentiators
- Use professional, factual language
- Example: "Global supplier of fermentation-derived postbiotic actives for skincare applications, specializing in Bifida and Lactobacillus lysates with COSMOS certification."

**Products Array:**
- Minimum 3 items required
- Use broad categories for general suppliers
- Use specific product names for specialized suppliers
- Maintain consistent naming conventions
- Example: ["Bifida Ferment Lysate", "Lactobacillus Ferment Lysate", "Yeast Ferment Extract"]

**Certifications Array:**
- Only include verified certifications
- Use standard abbreviations (COSMOS, IECIC, ISO 22716, NATRUE, ECOCERT)
- Check certification databases when possible
- Leave empty array if no certifications found: `[]`

**Geographic Coverage:**
- Use continent/region names: Europe, North America, South America, Asia, Africa, Oceania
- Use "Global" for worldwide distribution
- Be specific when company clearly serves limited regions
- Example: ["Europe", "North America"] or ["Global"]

**Specializations:**
- 2-4 items recommended
- Focus on unique capabilities or technologies
- Include relevant buzzwords (fermentation, encapsulation, microbiome-friendly, etc.)
- Example: ["Fermentation technology", "COSMOS-certified actives", "Microbiome science"]

**Time Estimate:** 5-10 minutes per listing

### Step 6: Validate Schema Compliance

**Purpose:** Ensure 100% compliance with JSON schema before committing

**Validation Checklist:**

**Required Fields:**
- ✅ `id` present and unique
- ✅ `name` present and non-empty
- ✅ `website` present, valid URL format, accessible
- ✅ `category` present and matches taxonomy
- ✅ `subcategory` present and matches taxonomy
- ✅ `description` present, 1-2 sentences, factual
- ✅ `headquarters` present, format "City, Country"
- ✅ `products` array present, minimum 3 items
- ✅ `certifications` array present (can be empty)
- ✅ `geographic_coverage` array present, minimum 1 item
- ✅ `specializations` array present, minimum 2 items
- ✅ `date_added` present, format YYYY-MM-DD
- ✅ `last_updated` present, format YYYY-MM-DD

**Data Quality:**
- ✅ No placeholder text (e.g., "TBD", "Unknown", "N/A")
- ✅ No empty strings in arrays
- ✅ Consistent capitalization and formatting
- ✅ Factually accurate information
- ✅ Professional language (no marketing hype)

**JSON Validity:**
- ✅ Valid JSON syntax (no trailing commas, proper quotes)
- ✅ Proper array and object structure
- ✅ Consistent indentation (2 or 4 spaces)
- ✅ UTF-8 encoding for special characters

**Validation Tools:**
- JSON validator (https://jsonlint.com/)
- Schema validator (if available in repository)
- Manual review against checklist

**Decision Point:**
- ✅ All checks pass → Proceed to Step 7
- ❌ Validation fails → Fix issues and re-validate

**Time Estimate:** 3-5 minutes per listing

### Step 7: Save to Repository

**Purpose:** Commit validated listing to appropriate location

**File Naming:**
- Format: `[company-name-lowercase-hyphenated].json`
- Example: `evonik-care-biotics.json`
- Use company name, not product name
- Remove special characters and spaces
- Use hyphens for multi-word names

**Directory Structure:**
```
listings/
├── Raw_Materials/
│   ├── Actives_Postbiotics/
│   │   └── evonik-care-biotics.json
│   ├── Actives_Prebiotics/
│   │   └── solabia-bioecolia.json
│   └── ...
├── Equipment/
│   ├── Mixing_Equipment/
│   └── ...
└── ...
```

**Actions:**
1. Navigate to appropriate category and subcategory directory
2. Verify directory exists (create if needed)
3. Save JSON file with proper naming
4. Verify file is readable and properly formatted
5. Update category index if maintained

**Time Estimate:** 2-3 minutes per listing

### Step 8: Document Research Findings

**Purpose:** Create audit trail and share insights

**Research Notes Template:**

```markdown
# Research Session: [Category Name]
**Date:** YYYY-MM-DD
**Researcher:** GitHub Copilot
**Duration:** X hours
**Target:** [Research objective]

## Suppliers Discovered

1. **[Company Name]** - [Brief note]
   - Website: [URL]
   - Key Products: [List]
   - Confidence: High/Medium/Low
   - Notes: [Any observations]

2. **[Company Name]** - [Brief note]
   ...

## Research Sources

- [Source 1]: [URL or description]
- [Source 2]: [URL or description]
...

## Key Insights

- [Insight 1]: [Description]
- [Insight 2]: [Description]
...

## Challenges Encountered

- [Challenge 1]: [Description and resolution]
- [Challenge 2]: [Description and resolution]
...

## Recommendations

- [Recommendation 1]: [Description]
- [Recommendation 2]: [Description]
...

## Metrics

- Suppliers researched: X
- Listings created: Y
- Time per listing: Z minutes
- Schema compliance: 100%
- Confidence level: High/Medium/Low
```

**Save Location:** `/docs/research/[category-name]-[date].md`

**Time Estimate:** 10-15 minutes per session

### Step 9: Communicate Progress

**Purpose:** Share findings with Manus AI and coordinate next steps

**Message to Manus (in `/copilot-2-manus/`):**

```markdown
# Message to Manus AI
**Date:** YYYY-MM-DD
**From:** GitHub Copilot
**Priority:** Medium
**Subject:** Research Complete - [Category Name] - [X] Suppliers Added

## Context
Completed research session on [category name] focusing on [specific focus area]. This aligns with strategic priority on [priority area].

## Update
**Suppliers Added:**
- [Company 1] - [Key differentiator]
- [Company 2] - [Key differentiator]
- [Company 3] - [Key differentiator]
...

**Key Discoveries:**
- [Discovery 1]
- [Discovery 2]
...

**Metrics:**
- Listings created: X
- Research duration: Y hours
- Schema compliance: 100%
- Average confidence: High

## Next Steps
- Continue research in [related category]
- Validate existing listings in [category]
- Expand to [new subcategory]

## Notes
[Any interesting observations, questions, or insights to share]

**Research notes saved to:** `/docs/research/[filename].md`
```

**Time Estimate:** 10 minutes

### Step 10: Self-Assessment & Optimization

**Purpose:** Reflect on research effectiveness and improve methodology

**Self-Assessment Questions:**

**Efficiency:**
- Was my research strategy effective?
- Did I use the best sources for this category?
- Could I have discovered suppliers faster?
- What slowed me down?

**Quality:**
- Did I maintain 100% schema compliance?
- Was my information accurate and complete?
- Did I verify claims adequately?
- Could I have gathered more detail?

**Strategic Alignment:**
- Did I focus on priority categories?
- Did I discover the right tier of suppliers?
- Did I align with Manus's research?
- Could I have better coordinated?

**Learning:**
- What new sources did I discover?
- What patterns did I notice?
- What should I do differently next time?
- What worked particularly well?

**Optimization Actions:**
- Update research methodology based on learnings
- Refine search strategies for better results
- Improve information extraction efficiency
- Enhance quality validation processes

**Time Estimate:** 5-10 minutes

## Research Strategies by Category

### Microbiome Science Suppliers

**Search Keywords:**
- "postbiotic suppliers cosmetics"
- "fermentation lysate manufacturers"
- "prebiotic ingredients skincare"
- "probiotic extracts personal care"
- "microbiome-friendly preservatives"

**Key Sources:**
- UL Prospector (fermentation actives)
- SpecialChem (biotechnology ingredients)
- In-Cosmetics exhibitor lists
- Academic partnerships (biotech companies)

**Quality Indicators:**
- Fermentation technology capabilities
- COSMOS/IECIC certification
- Clinical studies or efficacy data
- Microbiome science expertise

### Advanced Delivery Systems

**Search Keywords:**
- "liposome suppliers cosmetics"
- "encapsulation technology skincare"
- "nanoparticle carriers personal care"
- "penetration enhancers cosmetic"
- "controlled release systems beauty"

**Key Sources:**
- SpecialChem (delivery systems)
- Academic spin-offs and biotech companies
- Patent databases (technology leaders)
- Scientific conferences (IFSCC, SCC)

**Quality Indicators:**
- Patented technologies
- Scientific publications
- Clinical efficacy data
- Regulatory approvals

### Environmental Protection Actives

**Search Keywords:**
- "pollution protection actives skincare"
- "blue light protection cosmetics"
- "anti-pollution ingredients personal care"
- "urban defense actives beauty"
- "infrared protection skincare"

**Key Sources:**
- UL Prospector (environmental protection)
- Trade publications (trend reports)
- Supplier innovation announcements
- Conference presentations

**Quality Indicators:**
- Clinical studies on pollution/blue light
- Mechanism of action documentation
- Efficacy claims substantiation
- Innovation awards or recognition

### Specialized Manufacturing Equipment

**Search Keywords:**
- "spray dryer cosmetics"
- "freeze drying equipment skincare"
- "high pressure homogenizer cosmetics"
- "clean room equipment personal care"
- "process control systems cosmetics"

**Key Sources:**
- Equipment manufacturer websites
- Trade shows (Interpack, PACK EXPO)
- Industry directories
- Manufacturing publications

**Quality Indicators:**
- GMP compliance capabilities
- Cosmetic industry experience
- After-sales support and training
- Global service network

## Quality Assurance

### Common Errors to Avoid

**Schema Violations:**
- ❌ Missing required fields
- ❌ Empty strings or placeholder text
- ❌ Invalid date formats
- ❌ Mismatched category/subcategory
- ❌ Invalid JSON syntax

**Data Quality Issues:**
- ❌ Inaccurate or outdated information
- ❌ Unverified certification claims
- ❌ Marketing hype instead of facts
- ❌ Incomplete product lists
- ❌ Vague or generic descriptions

**Process Issues:**
- ❌ Skipping validation steps
- ❌ Not checking collaboration folders
- ❌ Failing to document research
- ❌ Not communicating progress
- ❌ Duplicating Manus's work

### Quality Improvement Strategies

**Continuous Improvement:**
- Track common errors and patterns
- Refine validation checklist
- Improve information extraction
- Enhance source verification
- Optimize research efficiency

**Peer Learning:**
- Review Manus's research methodology
- Adopt successful strategies
- Share discoveries and insights
- Coordinate on quality standards
- Celebrate quality achievements

## Success Metrics

### Efficiency Metrics
- Suppliers discovered per hour: Target 3-5
- Time per listing: Target 10-15 minutes
- Research session productivity: Target 5-10 listings

### Quality Metrics
- Schema compliance rate: Target 100%
- Information completeness: Target >90%
- Source verification rate: Target >80%
- Confidence level: Target >80% high confidence

### Strategic Metrics
- Priority category coverage: Target >70%
- Tier 1 supplier percentage: Target >30%
- Certification coverage: Target >60%
- Geographic diversity: Target all major regions

## Conclusion

Following this systematic workflow ensures consistent, high-quality supplier research that aligns with strategic priorities, maintains schema compliance, and supports effective collaboration with Manus AI. Continuous self-assessment and optimization improve efficiency and quality over time.

**Key Success Factors:**
1. ✅ Check collaboration folders first
2. ✅ Align with strategic priorities
3. ✅ Use systematic research methodology
4. ✅ Maintain 100% schema compliance
5. ✅ Document findings thoroughly
6. ✅ Communicate progress proactively
7. ✅ Continuously improve through self-assessment

**Together, we're building the most comprehensive personal care supplier database on Earth!** 🚀
