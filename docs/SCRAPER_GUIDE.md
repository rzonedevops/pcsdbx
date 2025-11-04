# Scraper Guide

**Status**: 🚧 Coming Soon - Planned for Week 2

This guide will document how to use the web scraping tools for automated data collection from personalcaresuppliers.com.

## Planned Features

### Core Functionality
- Respectful scraping with configurable rate limiting (1.5 seconds between requests)
- Modular design for fetching, parsing, and storing data
- Robust error handling and retry logic
- Progress tracking and resume capability
- Dry-run mode for testing

### Configuration
- **Rate Limiting**: 1.5 seconds between requests (approved by Manus)
- **User Agent**: Proper identification
- **Retry Logic**: Exponential backoff
- **Logging**: Detailed logging for debugging

### Usage (Planned)

```bash
# Dry run to test scraping
python3 scripts/scraper/scrape_listings.py --category 1828 --dry-run

# Scrape specific category
python3 scripts/scraper/scrape_listings.py --category 1828 --limit 10

# Scrape all categories
python3 scripts/scraper/scrape_listings.py --all

# Resume from last run
python3 scripts/scraper/scrape_listings.py --resume
```

### Validation Integration

The scraper will automatically validate scraped data before saving using the same validation tools documented in [DATA_QUALITY.md](DATA_QUALITY.md).

## Implementation Timeline

- **Week 2**: Build scraper foundation
- **Week 3**: Test on small dataset (5-10 suppliers)
- **Week 4**: Scale to priority categories (Actives, Contract Manufacturing)
- **Month 2**: Full automation with scheduling

## Technical Stack

Planned dependencies:
- `requests` or `httpx` - HTTP requests with rate limiting
- `beautifulsoup4` - HTML parsing
- `json` - Data serialization
- Optional: `scrapy` for advanced features

## Data Flow

1. **Fetch**: Retrieve page content with rate limiting
2. **Parse**: Extract supplier information
3. **Validate**: Check against schema
4. **Store**: Save to appropriate directory
5. **Log**: Record progress and errors

## Best Practices

- Always respect robots.txt
- Use appropriate rate limiting (1.5s minimum)
- Implement proper error handling
- Log all activities
- Validate before storing
- Enable resume capability
- Test with dry-run first

## Coming Soon

Full documentation will be added when the scraper is implemented in Week 2.

For questions about the planned scraper, please see:
- [DATA_QUALITY.md](DATA_QUALITY.md) for validation requirements
- [CONTRIBUTING.md](CONTRIBUTING.md) for manual listing guidelines
- Issue tracker for feature requests
