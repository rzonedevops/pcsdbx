# Personal Care Suppliers Database (pcsdbx)

This repository contains a structured database of listings from [Personal Care Suppliers](https://personalcaresuppliers.com/).

## Repository Structure

The repository organizes listings by category path in a hierarchical directory structure:

```
listings/
├── Raw_Materials/
│   └── Actives/
│       └── 1828_1102292.json
├── Business_Services/
│   └── Auditing/
│       └── 1790_1102249.json
├── Equipment/
│   └── Tanks/
│       └── 1801_1102102.json
└── Labels__Sleeves/
    └── Stretch_Sleeve/
        └── 1800_1101991.json
```

## Data Format

Each listing is stored as a JSON file with the following schema:

```json
{
  "category_id": 1828,
  "listing_id": 1102292,
  "category_path": "Raw_Materials/Actives",
  "url": "https://personalcaresuppliers.com/Listing/Index/Raw_Materials/Actives/1828/1102292//100/1",
  "page_number": 100,
  "status": "active",
  "date_added": "2025-11-03"
}
```

### Fields

- `category_id`: The numeric identifier for the category
- `listing_id`: The unique identifier for the listing
- `category_path`: The hierarchical path of the category (using underscores for spaces)
- `url`: The full URL to the listing on personalcaresuppliers.com
- `page_number`: (Optional) Page number if applicable
- `status`: Status of the listing (e.g., "active", "inactive")
- `date_added`: Date when the listing was added to this database (YYYY-MM-DD format)

## File Naming Convention

Listing files are named using the pattern: `{category_id}_{listing_id}.json`

For example: `1828_1102292.json`

## Current Listings

The database currently contains listings in the following categories:

1. **Raw Materials → Actives** (Category ID: 1828)
2. **Business Services → Auditing** (Category ID: 1790)
3. **Equipment → Tanks** (Category ID: 1801)
4. **Labels & Sleeves → Stretch Sleeve** (Category ID: 1800)

## Contributing

To add new listings:

1. Create the appropriate category directory structure under `listings/` if it doesn't exist
2. Create a new JSON file following the naming convention and schema
3. Ensure all required fields are populated
4. Submit a pull request with your additions

## License

See [LICENSE](LICENSE) file for details.