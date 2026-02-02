#!/usr/bin/env python3
"""Archive old read messages to monthly folders."""

import os
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path
import re

READ_DIRS = [
    "messages/read/manus-2-copilot",
    "messages/read/copilot-2-manus"
]
ARCHIVE_DIR = "messages/archive"
ARCHIVE_AFTER_DAYS = 30

def extract_date_from_filename(filename):
    """Extract date from message filename."""
    # Try to match YYYY-MM-DD pattern
    date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
    if date_match:
        try:
            return datetime(int(date_match.group(1)), 
                          int(date_match.group(2)), 
                          int(date_match.group(3)))
        except ValueError:
            pass
    
    return None

def archive_old_messages():
    """Archive messages older than ARCHIVE_AFTER_DAYS."""
    cutoff_date = datetime.now() - timedelta(days=ARCHIVE_AFTER_DAYS)
    archived_count = 0
    
    for read_dir in READ_DIRS:
        read_path = Path(read_dir)
        
        if not read_path.exists():
            continue
        
        direction = read_path.name  # 'manus-2-copilot' or 'copilot-2-manus'
        
        for filepath in read_path.glob('*.md'):
            # Extract date from filename
            msg_date = extract_date_from_filename(filepath.name)
            
            if msg_date is None:
                # If can't extract date, use file modification time
                msg_date = datetime.fromtimestamp(filepath.stat().st_mtime)
            
            # Check if old enough to archive
            if msg_date < cutoff_date:
                # Determine archive month
                archive_month = msg_date.strftime('%Y-%m')
                
                # Create archive directory
                archive_path = Path(ARCHIVE_DIR) / archive_month / direction
                archive_path.mkdir(parents=True, exist_ok=True)
                
                # Move file
                destination = archive_path / filepath.name
                
                try:
                    shutil.move(str(filepath), str(destination))
                    archived_count += 1
                    print(f"Archived: {filepath.name} -> {archive_month}/{direction}/")
                except Exception as e:
                    print(f"Error archiving {filepath.name}: {e}", file=sys.stderr)
    
    # Output for GitHub Actions
    github_output = os.getenv('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f"archived_count={archived_count}\n")
    
    print(f"\nTotal messages archived: {archived_count}")
    return archived_count

def main():
    """Main entry point."""
    try:
        archived_count = archive_old_messages()
        return 0
    except Exception as e:
        print(f"Error during archival: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
