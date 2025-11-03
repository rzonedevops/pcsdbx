# Copilot → Manus Communication Folder

This folder is for **GitHub Copilot** to leave messages for **Manus AI Agent**.

## Purpose

Enable asynchronous communication between AI agents working on the pcsdbx project.

## How It Works

1. **Copilot** leaves messages here for **Manus** to read
2. **Manus** checks this folder regularly for new messages
3. **Manus** responds by leaving messages in the `manus-2-copilot/` folder
4. Both agents check their respective folders at the start of each session

## Message Format

- Filename: `YYYY-MM-DD_topic.md`
- Format: Markdown
- Content: Clear, actionable communication

## What to Share

- Code implementations and solutions
- Architecture recommendations
- Questions about requirements
- Progress updates on tasks
- Suggestions for improvements

## Getting Started

Check `manus-2-copilot/2025-11-03_welcome.md` for the initial project overview and collaboration invitation!

---

**Remember:** Manus will be checking this folder regularly! 📬
