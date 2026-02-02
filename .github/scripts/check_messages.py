#!/usr/bin/env python3
"""Check for new messages and extract metadata for GitHub Actions."""

import os
import json
import hashlib
import re
import sys
from datetime import datetime
from pathlib import Path

INBOX_DIR = "messages/inbox/manus-2-copilot"

def parse_message_metadata(filepath):
    """Extract metadata from message file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    metadata = {
        'subject': 'No Subject',
        'priority': 'medium',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'from': 'Manus AI',
        'to': 'GitHub Copilot'
    }
    
    # Extract from markdown headers
    subject_match = re.search(r'\*\*Subject:\*\*\s*(.+)', content)
    if subject_match:
        metadata['subject'] = subject_match.group(1).strip()
    
    # Try to extract from # Message to format
    if metadata['subject'] == 'No Subject':
        title_match = re.search(r'^#\s+Message to .+?\n\*\*Subject:\*\*\s*(.+)', content, re.MULTILINE)
        if title_match:
            metadata['subject'] = title_match.group(1).strip()
    
    priority_match = re.search(r'\*\*Priority:\*\*\s*(\w+)', content, re.IGNORECASE)
    if priority_match:
        metadata['priority'] = priority_match.group(1).lower()
    
    date_match = re.search(r'\*\*Date:\*\*\s*([\d-]+)', content)
    if date_match:
        metadata['date'] = date_match.group(1)
    
    from_match = re.search(r'\*\*From:\*\*\s*(.+)', content)
    if from_match:
        metadata['from'] = from_match.group(1).strip()
    
    return metadata, content

def check_new_messages():
    """Check for new messages in inbox."""
    inbox_path = Path(INBOX_DIR)
    
    if not inbox_path.exists():
        print("Inbox directory does not exist")
        return []
    
    # Track which messages have been processed
    processed_file = Path(".github/.processed_messages.txt")
    processed_messages = set()
    
    if processed_file.exists():
        with open(processed_file, 'r') as f:
            processed_messages = set(line.strip() for line in f)
    
    new_messages = []
    
    for filepath in sorted(inbox_path.glob('*.md')):
        filename = filepath.name
        
        # Skip if already processed
        if filename in processed_messages:
            continue
        
        # Parse message
        try:
            metadata, content = parse_message_metadata(filepath)
            
            # Create truncated body for issue (first 1000 chars)
            body_preview = content[:1000]
            if len(content) > 1000:
                body_preview += "\n\n... (message truncated, see full message in repository)"
            
            new_messages.append({
                'filename': filename,
                'subject': metadata['subject'],
                'priority': metadata['priority'],
                'date': metadata['date'],
                'from': metadata['from'],
                'body': content,
                'body_preview': body_preview,
                'filepath': str(filepath.relative_to(Path.cwd()))
            })
            
            # Mark as processed
            processed_messages.add(filename)
            
        except Exception as e:
            print(f"Error processing {filename}: {e}", file=sys.stderr)
            continue
    
    # Update processed messages file
    if new_messages:
        with open(processed_file, 'w') as f:
            for msg in sorted(processed_messages):
                f.write(msg + '\n')
    
    return new_messages

def main():
    """Main entry point."""
    messages = check_new_messages()
    
    if messages:
        # Output for GitHub Actions
        print(f"Found {len(messages)} new message(s)")
        
        # Set outputs using environment file (new GitHub Actions syntax)
        github_output = os.getenv('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"new_messages=true\n")
                f.write(f"message_count={len(messages)}\n")
                # Escape JSON for multiline output
                messages_json = json.dumps(messages)
                f.write(f"messages_json<<EOF\n{messages_json}\nEOF\n")
        
        # Also print for debugging
        print(f"Messages: {json.dumps(messages, indent=2)}")
        
        return 0
    else:
        print("No new messages")
        
        github_output = os.getenv('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"new_messages=false\n")
                f.write(f"message_count=0\n")
        
        return 0

if __name__ == '__main__':
    sys.exit(main())
