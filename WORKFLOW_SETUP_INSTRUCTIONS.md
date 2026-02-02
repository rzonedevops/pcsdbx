# GitHub Actions Workflow Setup Instructions

**Date:** February 2, 2026  
**Status:** Manual setup required due to workflow permissions

## Issue

The GitHub App used by `gh` CLI doesn't have `workflows` permission, so workflow files cannot be pushed automatically. They need to be added manually or via a Personal Access Token (PAT) with workflow scope.

## Workflow Files to Add

The following workflow files have been created locally and need to be added to the repository:

### 1. `.github/workflows/check-messages.yml`
**Purpose:** Automatically check for new messages and create GitHub Issues  
**Schedule:** Every 4 hours + on push to `messages/inbox/manus-2-copilot/`  
**Actions:**
- Detects new messages in inbox
- Parses message metadata
- Creates GitHub Issues for Copilot notification
- Assigns with priority labels
- Tracks processed messages

### 2. `.github/workflows/repo-maintenance.yml`
**Purpose:** Weekly repository maintenance and validation  
**Schedule:** Every Sunday at 2 AM UTC  
**Actions:**
- Archives old messages (30+ days)
- Validates JSON schema compliance
- Updates repository statistics
- Creates maintenance reports

### 3. `.github/workflows/validate-data.yml`
**Purpose:** Continuous data quality validation  
**Schedule:** Daily + on every PR to `listings/`  
**Actions:**
- Validates JSON schema
- Checks for duplicate IDs
- Posts PR comments with results
- Blocks merge if critical errors

## Option 1: Manual Upload via GitHub Web Interface

1. Go to https://github.com/rzonedevops/pcsdbx
2. Navigate to `.github/workflows/` directory
3. Click "Add file" → "Upload files"
4. Upload the three workflow files from your local repository:
   - `check-messages.yml`
   - `repo-maintenance.yml`
   - `validate-data.yml`
5. Commit with message: "Add GitHub Actions workflows for automation"

## Option 2: Push with Personal Access Token (PAT)

If you have a GitHub PAT with `workflow` scope:

```bash
# Set PAT as environment variable
export GITHUB_TOKEN="your_pat_with_workflow_scope"

# Configure git to use PAT
git remote set-url origin https://${GITHUB_TOKEN}@github.com/rzonedevops/pcsdbx.git

# Add workflow files
git add .github/workflows/*.yml

# Commit
git commit -m "Add GitHub Actions workflows for automation"

# Push
git push origin main

# Restore original remote URL
git remote set-url origin https://github.com/rzonedevops/pcsdbx.git
```

## Option 3: Use GitHub API with PAT

```bash
# For each workflow file
for file in check-messages.yml repo-maintenance.yml validate-data.yml; do
  gh api \
    --method PUT \
    -H "Accept: application/vnd.github+json" \
    /repos/rzonedevops/pcsdbx/contents/.github/workflows/$file \
    -f message="Add $file workflow" \
    -f content="$(base64 < .github/workflows/$file)"
done
```

## Verification

After adding the workflows:

1. **Check Actions Tab:**
   - Go to https://github.com/rzonedevops/pcsdbx/actions
   - Verify workflows appear in the list

2. **Test Message Checker:**
   - Manually trigger "Check Messages for Copilot" workflow
   - Verify it detects existing messages in `messages/inbox/manus-2-copilot/`
   - Check if GitHub Issues are created

3. **Test Validation:**
   - Manually trigger "Validate Data Quality" workflow
   - Verify it validates all JSON files
   - Check for validation report

## Required Permissions

The workflows require the following permissions (already configured in YAML):

```yaml
permissions:
  contents: write    # To commit processed messages tracking
  issues: write      # To create GitHub Issues for notifications
```

These permissions are granted automatically to `GITHUB_TOKEN` in GitHub Actions, so no additional setup is needed once the workflows are added.

## Workflow Files Location

The workflow files are located in your local repository at:
```
/home/ubuntu/pcsdbx/.github/workflows/
├── check-messages.yml
├── repo-maintenance.yml
└── validate-data.yml
```

## Supporting Scripts

The following Python scripts are already pushed to the repository and will be used by the workflows:

```
.github/scripts/
├── check_messages.py      # Parse and track new messages
├── archive_messages.py    # Archive old messages monthly
├── validate_repo.py       # Validate JSON schema and quality
└── update_stats.py        # Update repository statistics
```

## Next Steps

1. Choose one of the three options above to add the workflow files
2. Verify workflows are active in GitHub Actions tab
3. Test each workflow manually to ensure they work correctly
4. Monitor first automated runs (check-messages runs every 4 hours)
5. Review any issues or errors in workflow logs

## Benefits Once Active

- **Automatic Notifications:** Copilot gets GitHub Issues for new messages
- **Clean Organization:** Messages archived monthly automatically
- **Quality Assurance:** Weekly validation ensures data integrity
- **Continuous Validation:** PR checks prevent schema violations
- **Statistics Tracking:** Automatic updates to repository metrics

## Troubleshooting

**If workflows don't appear:**
- Check that files are in `.github/workflows/` directory
- Verify YAML syntax is valid
- Check repository Actions settings are enabled

**If workflows fail:**
- Check workflow logs in Actions tab
- Verify Python scripts are executable
- Ensure required directories exist (`messages/`, `listings/`)

**If Issues aren't created:**
- Verify `GITHUB_TOKEN` has `issues: write` permission
- Check workflow logs for errors
- Manually trigger workflow to test

---

**Once workflows are active, the enhanced messaging system will be fully operational!** 🚀
