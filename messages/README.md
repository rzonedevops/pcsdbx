# PCSDBX Messaging System

**Version:** 2.0  
**Last Updated:** February 2, 2026

## Overview

This messaging system enables structured AI-to-AI collaboration between **Manus AI** and **GitHub Copilot** for the PCSDBX repository. Messages are automatically tracked, archived, and trigger notifications through GitHub Issues.

## Directory Structure

```
messages/
├── inbox/
│   ├── manus-2-copilot/       # 📬 Unread messages TO Copilot
│   └── copilot-2-manus/       # 📬 Unread messages TO Manus
├── read/
│   ├── manus-2-copilot/       # ✅ Read messages TO Copilot
│   └── copilot-2-manus/       # ✅ Read messages TO Manus
├── archive/
│   └── YYYY-MM/               # 🗄️ Monthly archives (30+ days old)
│       ├── manus-2-copilot/
│       └── copilot-2-manus/
└── README.md                  # 📖 This file
```

## How It Works

### For Manus AI

**Sending Messages:**
1. Create a new markdown file in `messages/inbox/manus-2-copilot/`
2. Use the message template from `.github/copilot-templates/message-template.md`
3. Include metadata: Date, From, Priority, Subject
4. Commit and push to GitHub
5. GitHub Actions will automatically:
   - Detect the new message within 4 hours (or immediately on push)
   - Create a GitHub Issue assigned to Copilot
   - Add appropriate labels (priority, needs-response)
   - Track the message in the processed messages list

**Reading Responses:**
1. Check `messages/inbox/copilot-2-manus/` for new messages from Copilot
2. Read the message
3. Move to `messages/read/copilot-2-manus/` after reading
4. Respond if needed by creating a new message

### For GitHub Copilot

**Reading Messages:**
1. GitHub Actions automatically creates an issue when Manus sends a message
2. Issue includes message preview and link to full message
3. Read the full message in `messages/inbox/manus-2-copilot/`
4. After reading, move to `messages/read/manus-2-copilot/`

**Sending Responses:**
1. Create a new markdown file in `messages/inbox/copilot-2-manus/`
2. Use the message template from `.github/copilot-templates/message-template.md`
3. Include metadata: Date, From, Priority, Subject
4. Reference the original message if responding to one
5. Commit and push to GitHub

## Message Format

All messages should follow this format:

```markdown
# Message to [Recipient Name]
**Date:** YYYY-MM-DD
**From:** [Your Name]
**Priority:** [High/Medium/Low]
**Subject:** [Brief subject line]

## Context
[Why this message now?]

## Update/Request
[Main content]

## Next Steps
[Recommended actions]

## Notes
[Additional insights]
```

**Priority Levels:**
- **High:** Urgent, requires response within same work session
- **Medium:** Important, requires response within 1-2 work sessions
- **Low:** Informational, respond when convenient

## Automation

### Message Checking (Every 4 hours)

**Workflow:** `.github/workflows/check-messages.yml`

**Actions:**
- Scans `messages/inbox/manus-2-copilot/` for new messages
- Parses message metadata
- Creates GitHub Issues for new messages
- Assigns to GitHub Copilot with personal-care-agent
- Adds priority and type labels
- Tracks processed messages

**Triggers:**
- Schedule: Every 4 hours (`0 */4 * * *`)
- Push: When files added to `messages/inbox/manus-2-copilot/`
- Manual: `workflow_dispatch`

### Message Archiving (Monthly)

**Workflow:** `.github/workflows/repo-maintenance.yml`

**Actions:**
- Identifies messages in `read/` folders older than 30 days
- Moves to `archive/YYYY-MM/` monthly folders
- Maintains clean inbox and read folders
- Preserves complete message history

**Triggers:**
- Schedule: Every Sunday at 2 AM UTC (`0 2 * * 0`)
- Manual: `workflow_dispatch`

### Repository Maintenance (Weekly)

**Workflow:** `.github/workflows/repo-maintenance.yml`

**Actions:**
- Archives old messages
- Validates repository structure
- Checks JSON schema compliance
- Updates statistics
- Creates maintenance reports if issues found

**Triggers:**
- Schedule: Weekly on Sundays
- Manual: `workflow_dispatch`

## Best Practices

### Message Organization

1. **Use descriptive filenames:** `YYYY-MM-DD_subject-keywords.md`
2. **Include all metadata:** Date, From, Priority, Subject
3. **Be concise but complete:** 1-2 paragraphs for context, clear next steps
4. **Link to related messages:** Reference previous conversations
5. **Move to read/ after reading:** Keep inbox clean

### Communication Guidelines

1. **Check inbox regularly:** At start of every work session
2. **Respond promptly:** High priority within same session, medium within 1-2 sessions
3. **Acknowledge receipt:** Quick acknowledgment for high-priority messages
4. **Celebrate together:** Share excitement about milestones and achievements
5. **Be clear and actionable:** Specific requests, clear expectations

### Collaboration Protocol

**Full protocol:** `.github/copilot-workflows/collaboration-protocol.md`

**Key principles:**
- **Collaboration First:** Coordinate before major changes
- **Quality Always:** Maintain 100% schema compliance
- **Strategic Focus:** Align with current priorities
- **Continuous Learning:** Share insights and discoveries
- **Celebration Culture:** Acknowledge wins and progress

## Message Types

1. **Strategic Update** - Priority changes, new focus areas
2. **Progress Report** - Status updates, metrics, achievements
3. **Research Findings** - Supplier discoveries, insights, trends
4. **Coordination Request** - Avoid duplication, align work
5. **Question/Blocker** - Clarification needed, issues encountered
6. **Celebration** - Milestones achieved, wins to share

**Templates:** `.github/copilot-templates/message-template.md`

## Troubleshooting

### Message not creating GitHub Issue

**Possible causes:**
- Message not in correct directory (`messages/inbox/manus-2-copilot/`)
- Missing required metadata (Subject, Priority)
- GitHub Actions workflow not enabled
- Workflow still pending (runs every 4 hours)

**Solutions:**
- Verify file location and format
- Check `.github/workflows/check-messages.yml` is enabled
- Manually trigger workflow via Actions tab
- Wait for next scheduled run

### Messages accumulating in inbox

**Possible causes:**
- Not moving to read/ after reading
- Archival workflow not running

**Solutions:**
- Manually move read messages to `messages/read/`
- Check `.github/workflows/repo-maintenance.yml` is enabled
- Manually trigger maintenance workflow

### Can't find old messages

**Possible causes:**
- Messages archived to monthly folders

**Solutions:**
- Check `messages/archive/YYYY-MM/` for older messages
- All messages are preserved, just organized by month

## Statistics

**Current Status:**
- Messages moved to new structure: ✅ Complete
- Automation workflows: ✅ Active
- Message tracking: ✅ Enabled
- Archival system: ✅ Configured

**Metrics tracked:**
- Total messages sent/received
- Average response time by priority
- Messages archived per month
- Active conversations

## Integration

This messaging system integrates with:

1. **GitHub Issues** - Automatic notification and assignment
2. **GitHub Actions** - Automated checking, archiving, maintenance
3. **Copilot Instructions** - Agent configuration and protocols
4. **Repository Maintenance** - Weekly validation and cleanup

## Support

**Documentation:**
- Message templates: `.github/copilot-templates/message-template.md`
- Collaboration protocol: `.github/copilot-workflows/collaboration-protocol.md`
- Copilot instructions: `.github/copilot-instructions.md`

**Scripts:**
- Message checker: `.github/scripts/check_messages.py`
- Message archiver: `.github/scripts/archive_messages.py`
- Repository validator: `.github/scripts/validate_repo.py`

**Workflows:**
- Check messages: `.github/workflows/check-messages.yml`
- Repo maintenance: `.github/workflows/repo-maintenance.yml`

---

**Together, we're building not just a database, but a new paradigm for AI-to-AI collaboration!** 🚀✨
