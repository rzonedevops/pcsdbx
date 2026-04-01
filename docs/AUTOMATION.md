# GitHub Actions - Manus-Copilot Communication Automation

This repository now includes automated GitHub Actions workflows to facilitate communication between AI agents.

## 🤖 Automated Message Monitoring

A GitHub Action workflow automatically monitors the `manus-2-copilot/` and `copilot-2-manus/` folders to:

1. **Detect new messages** from the Manus agent
2. **Create pull requests** to update the personal-care-agent.md file
3. **Monitor communication health** and flag issues
4. **Request help** when communication appears stuck

### How It Works

```
┌─────────────────────────┐
│   Push to Repository    │
└───────────┬─────────────┘
            │
            ▼
    ┌───────────────┐
    │ Workflow Runs │
    └───────┬───────┘
            │
            ├─→ New messages? ──→ Create PR to update agent
            │
            └─→ No messages? ──→ Check health ──→ Create help request if stuck
```

### Files and Folders

- **`.github/workflows/manus-copilot-monitor.yml`** - The main workflow file
- **`.github/workflows/README.md`** - Detailed workflow documentation
- **`manus-2-copilot/`** - Messages FROM Manus TO Copilot
- **`copilot-2-manus/`** - Messages FROM Copilot TO Manus
- **`.github/agents/personal-care-agent.md`** - Agent configuration (updated by workflow)

### What Happens When Messages Arrive

1. **Automatic Detection**: When a new `.md` file appears in `manus-2-copilot/`, the workflow detects it
2. **PR Creation**: A pull request is automatically created to acknowledge the message
3. **Agent Update**: The `personal-care-agent.md` file is updated with a note about the message
4. **Smart Tracking**: The workflow remembers which messages have been processed (no duplicates!)

### What Happens When Communication is Stuck

1. **Health Check**: If messages exist but no responses are found
2. **Help Request**: A one-time help request is created in `copilot-2-manus/`
3. **PR Notification**: A pull request alerts maintainers that manual intervention may be needed

### Manual Workflow Trigger

You can manually trigger the workflow:

1. Go to **Actions** tab in GitHub
2. Select **"Manus-Copilot Message Monitor"**
3. Click **"Run workflow"**
4. Choose the branch and click **"Run workflow"**

### For More Details

See the complete documentation in [`.github/workflows/README.md`](.github/workflows/README.md)

---

## 📝 Message Format

Both agents should follow this format for messages:

**Filename:** `YYYY-MM-DD_topic.md`

**Example:** `2025-11-03_welcome.md`

**Content:**
```markdown
# Message Title

**From:** [Agent Name]  
**To:** [Agent Name]  
**Date:** [ISO Date]

## Content

[Your message here]

---

**— [Your Agent Name]**
```

---

## 🚀 Getting Started

### As Manus Agent
1. Create a new `.md` file in `manus-2-copilot/`
2. Push to repository
3. GitHub Action will automatically detect and process it
4. Watch for the PR to be created

### As Copilot Agent (or Human)
1. Review PRs created by the workflow
2. Merge the PR if appropriate
3. Create a response in `copilot-2-manus/` if needed
4. The cycle continues!

---

## 🔧 Customization

To modify the workflow behavior:

1. Edit `.github/workflows/manus-copilot-monitor.yml`
2. Test changes in a feature branch
3. Merge to main when ready

See the workflow README for customization options.

---

**Status:** ✅ Active and Monitoring  
**Last Updated:** 2025-11-03  
**Workflow Version:** 1.0
