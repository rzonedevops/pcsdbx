# Tests

This directory contains tests for the Personal Care Suppliers Database tools.

## Running Tests

### Run all tests
```bash
python3 tests/test_validation.py
```

### With pytest (if installed)
```bash
# Install pytest
pip install pytest

# Run all tests with verbose output
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_validation.py -v
```

## Test Files

### test_validation.py
Tests for the validation tools in `scripts/validation/`.

**Tests:**
- Schema loading
- Type checking
- Valid listing validation
- Invalid listing detection
- Strategic supplier validation
- Required fields checking
- Enum validation
- Array type validation

**Usage:**
```bash
python3 tests/test_validation.py
```

## Test Fixtures

The `fixtures/` directory contains sample JSON files for testing:

- **valid_listing.json** - A valid minimal listing
- **invalid_listing_missing_schema.json** - Missing schema_version field
- **strategic_supplier.json** - Strategic supplier with enhanced fields

## Writing New Tests

When adding new features, add corresponding tests:

1. Create test fixtures in `fixtures/` if needed
2. Add test functions to appropriate test file
3. Use descriptive test names (e.g., `test_feature_name`)
4. Include assertions to verify expected behavior
5. Add print statements for progress tracking

Example:
```python
def test_new_feature():
    """Test description."""
    # Setup
    data = {...}
    
    # Execute
    result = some_function(data)
    
    # Verify
    assert result == expected, "Error message"
    print("✓ Test passed")
```

## Test Coverage

Current test coverage:

- ✅ Schema validation
- ✅ Type checking
- ✅ Required fields
- ✅ Enum validation
- ✅ Array validation
- ✅ Business logic (basic)
- 🔲 Migration tools (planned)
- 🔲 Scraper tools (planned)
- 🔲 Import tools (planned)

## Continuous Testing

Best practices:
1. Run tests before committing changes
2. Add tests for new features
3. Update tests when schema changes
4. Keep fixtures up to date
5. Document test expectations

## Future Tests

Planned test additions:

- **test_migration.py** - Tests for migration tools
- **test_scraper.py** - Tests for scraper (Week 2)
- **test_import.py** - Tests for import tools
- **test_reporting.py** - Tests for reporting tools
- **Integration tests** - End-to-end workflow tests

## Dependencies

Current tests use only Python standard library.

Future tests may require:
```
pytest>=7.0.0
pytest-cov>=4.0.0
```

Install with:
```bash
pip install pytest pytest-cov
```

## Questions?

See the main [README.md](../README.md) or open an issue.
