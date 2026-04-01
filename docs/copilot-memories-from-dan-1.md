# Copilot Memories

Hey copilot it's me dan you tried to store these memories but it failed so i saved them here for you :-)

---

Perfect! Let me store some key facts about this codebase for future sessions:

Call to store_memory
Input
{
  "subject": "database schema compliance",
  "fact": "All supplier listings must be valid JSON with schema_version 1.0 and include listing_id, category_path, url, status, and date_added fields",
  "citations": "scripts/validation/listing_schema.json, listings/Labels__Sleeves/*/*.json",
  "reason": "Future sessions creating supplier listings must follow this schema to maintain database integrity. The schema_version field is required for all listings, and the validation tests check for this. This ensures consistency across all 568+ listings in the database and prevents data quality issues.",
  "category": "file_specific"
}
Failed to store memory with error: Resource not found

Call to store_memory
Input
{
  "subject": "validation and testing",
  "fact": "Run python3 tests/test_validation.py to validate supplier listing schema compliance before committing",
  "citations": "tests/test_validation.py, successful test run showing 8/8 tests passed",
  "reason": "This validation ensures all listings maintain 100% schema compliance, which is a critical project requirement. The test suite validates JSON structure, required fields, type checking, and business logic. Running this before commits prevents introducing invalid data into the database.",
  "category": "bootstrap_and_build"
}
Failed to store memory with error: Resource not found

Call to store_memory
Input
{
  "subject": "collaboration protocol",
  "fact": "Check manus-2-copilot folder for messages from Manus and leave responses in copilot-2-manus folder after each session",
  "citations": "manus-2-copilot/collaboration_update_2025-11-21.md, copilot-2-manus/2025-11-23_LABELS_SLEEVES_CRITICAL_GAP_CLOSED.md",
  "reason": "This collaboration protocol ensures effective communication between AI agents working on the project. Manus provides strategic direction and research, while GitHub Copilot implements the listings. Following this protocol ensures continuity across sessions and prevents duplicated work.",
  "category": "general"
}
Failed to store memory with error: Resource not found

Now let me create a final comprehensive summary and complete the task
