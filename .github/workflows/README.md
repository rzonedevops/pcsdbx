# Manus-Copilot Message Monitor Workflow

## Overview

This GitHub Action automates the communication flow between the Manus AI Agent and GitHub Copilot Agent by monitoring message folders and creating appropriate responses.

## How It Works

### Trigger Events

The workflow runs automatically on:
- Every push to the `main` branch
- Every push to `copilot/**` branches
- Manual dispatch via GitHub Actions UI

### Workflow Logic

```
┌─────────────────────────────────────────┐
│  Workflow Triggered on Push/Dispatch    │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  Check manus-2-copilot/ for new messages│
└───────────────┬─────────────────────────┘
                │
        ┌───────┴────────┐
        │                │
        ▼                ▼
   [Messages?]       [No messages]
        │                │
        │                ▼
        │    ┌──────────────────────────┐
        │    │ Check copilot-2-manus/   │
        │    │ for existing responses   │
        │    └───────────┬──────────────┘
        │                │
        │         ┌──────┴─────┐
        │         │            │
        │         ▼            ▼
        │   [Responses?]  [No responses]
        │         │            │
        │         │            ▼
        │         │    ┌────────────────┐
        │         │    │ Create Help    │
        │         │    │ Request PR     │
        │         │    └────────────────┘
        │         │
        │         ▼
        │   [All OK - Exit]
        │
        ▼
┌──────────────────────────┐
│ Process Latest Message   │
│ - Create new branch      │
│ - Update agent file      │
│ - Create PR              │
└──────────────────────────┘
```

## Workflow Steps

### 1. New Messages Found

When the workflow detects new markdown files in `manus-2-copilot/` (excluding README.md):

1. **Check Processing Status:** For each message, checks if a PR already exists with the message's name
2. **Identify Unprocessed Messages:** Only processes messages that haven't had a PR created yet
3. **Create Branch:** Creates a new branch `copilot/agent-update-{message-filename}` for the latest unprocessed message
4. **Update Agent File:** Adds a note to `.github/agents/personal-care-agent.md` acknowledging the message
5. **Commit Changes:** Commits the updated agent file
6. **Create PR:** Opens a pull request with:
   - Title indicating the message source
   - Body containing message preview and next steps
   - Base branch: `main`
   - Head branch: The newly created update branch

**Note:** The workflow uses exact PR title matching to track which messages have been processed, preventing duplicate PRs for the same message. The workflow now uses `jq` to filter PRs by exact title match rather than using fuzzy full-text search, which could incorrectly match PRs containing similar text in their body or comments.

### 2. No New Messages - Health Check

When no new messages are found:

1. **Count Messages:** Checks how many messages exist in `manus-2-copilot/`
2. **Count Responses:** Checks how many responses exist in `copilot-2-manus/`
3. **Evaluate Status:**
   - If messages exist but no responses → Communication stuck
   - If messages exist with responses → Healthy state
   - If no messages at all → Healthy state

### 3. Communication Stuck - Help Request

When messages exist but no responses have been created:

1. **Check for Existing Help Requests:** Verifies no help request PR or file already exists
2. **Create Help Message:** Creates a markdown file in `copilot-2-manus/` with timestamp (only if none exists)
3. **Create PR:** Opens a pull request flagging the stuck communication (only if first occurrence)

**Note:** The workflow checks both for existing help request PRs (using exact title match) and help request message files to prevent duplicate notifications. The exact title matching ensures that only PRs with the title "Help Request: Manus-Copilot Communication Stuck" are detected, not PRs that merely mention these words in their body.

## File Naming Conventions

### Messages from Manus
- Location: `manus-2-copilot/`
- Format: `YYYY-MM-DD_topic.md`
- Example: `2025-11-03_welcome.md`

### Responses from Copilot
- Location: `copilot-2-manus/`
- Format: `YYYY-MM-DD_topic.md` or `YYYY-MM-DD_help-request.md`
- Example: `2025-11-03_response.md`

## Permissions

The workflow requires these GitHub permissions:
- `contents: write` - To create branches and commit files
- `pull-requests: write` - To create pull requests
- `issues: write` - For potential future issue creation

## Manual Trigger

You can manually trigger the workflow:

1. Go to the repository's Actions tab
2. Select "Manus-Copilot Message Monitor"
3. Click "Run workflow"
4. Select the branch
5. Click "Run workflow" button

## Expected Behavior

### First Run After Setup
- Detects `2025-11-03_welcome.md` from Manus
- Searches for existing PR with "Message from Manus (2025-11-03_welcome)"
- If no PR exists, creates one to update `personal-care-agent.md`
- If PR already exists, skips (already processed)

### Subsequent Runs (No New Messages)
- Checks communication health
- If messages exist but no responses exist:
  - Checks for existing help request PRs or files
  - Creates help request only if none exists
- If responses exist or no messages exist:
  - Reports healthy state and exits

### New Message Added
- Detects new message file
- Checks if this specific message already has a PR
- Creates PR only for unprocessed messages
- Older messages with existing PRs are skipped

## Customization

To modify the workflow behavior, edit `.github/workflows/manus-copilot-monitor.yml`:

- **Change trigger events:** Modify the `on:` section
- **Adjust message processing:** Edit the "Process new message and create PR" step
- **Customize PR content:** Modify the PR title and body templates
- **Add notifications:** Include additional steps for Slack/email alerts

## Troubleshooting

### Workflow Not Triggering
- Check that pushes are being made to `main` or `copilot/**` branches
- Verify workflow file is in `.github/workflows/` directory
- Check GitHub Actions are enabled for the repository

### PRs Not Being Created
- Verify `GH_TOKEN` has sufficient permissions
- Check workflow logs in Actions tab
- Ensure branch protection rules allow automated PRs

### False Help Requests
- Review logic in "Check for missing response" step
- May need to adjust message/response counting logic
- Check for `.gitkeep` and other non-message files being counted

### Messages Incorrectly Detected as Processed
- **Issue:** Workflow skips processing new messages even though no PR exists for them
- **Cause:** The `gh pr list --search` command performs fuzzy full-text search, matching PRs that contain the search terms anywhere (title, body, comments)
- **Fix (Applied):** Changed to use exact title matching with `jq` filter: `gh pr list --state all --json title --jq --arg title "..." '[.[] | select(.title == $title)] | length'`
- **Impact:** Ensures only PRs with the exact title are matched, preventing false positives

## Integration with Agent Workflow

This automation complements the manual agent workflow:

1. **Manus** creates messages manually or via automation
2. **GitHub Action** detects and processes messages
3. **PR Created** for review and merging
4. **Copilot/Human** reviews PR and creates appropriate responses
5. **Response** placed in `copilot-2-manus/` folder
6. **Cycle continues** with bidirectional communication

## Future Enhancements

Potential improvements to consider:

- [ ] Parse message content to automatically update specific agent sections
- [ ] Integrate with LLM to generate intelligent responses
- [ ] Add Slack/Discord notifications when messages arrive
- [ ] Create summary reports of communication history
- [ ] Implement message threading/conversation tracking
- [ ] Add automated testing of message processing logic
- [ ] Support for message prioritization (urgent, normal, low)
- [ ] Archive old messages after processing

## Files Created/Modified by Workflow

### Created
- Branch: `copilot/agent-update-{message-filename}`
- PR: Link to pull request with updates
- Message: `copilot-2-manus/YYYY-MM-DD_help-request.md` (if stuck)

### Modified
- `.github/agents/personal-care-agent.md` (message acknowledgment added)

## Security Considerations

- Workflow uses repository's `GITHUB_TOKEN` (automatic, scoped to repo)
- No external secrets required
- All changes go through PR review process
- Branch protection can be applied for additional security

---

**Last Updated:** 2025-11-03  
**Workflow Version:** 1.0  
**Maintained By:** GitHub Copilot Agent
