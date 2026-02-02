#!/usr/bin/env python3
"""Update repository statistics."""

import json
import os
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

LISTINGS_DIR = "listings"
STATS_DIR = "docs/stats"

def collect_statistics():
    """Collect repository statistics."""
    stats = {
        'timestamp': datetime.now().isoformat(),
        'total_listings': 0,
        'categories': {},
        'subcategories': defaultdict(lambda: defaultdict(int)),
        'certifications': defaultdict(int),
        'geographic_coverage': defaultdict(int),
        'recent_additions': []
    }
    
    listings_path = Path(LISTINGS_DIR)
    
    if not listings_path.exists():
        return stats
    
    all_listings = []
    
    for filepath in listings_path.rglob('*.json'):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            stats['total_listings'] += 1
            
            # Category counts
            category = data.get('category', 'Unknown')
            if category not in stats['categories']:
                stats['categories'][category] = 0
            stats['categories'][category] += 1
            
            # Subcategory counts
            subcategory = data.get('subcategory', 'Unknown')
            stats['subcategories'][category][subcategory] += 1
            
            # Certification counts
            for cert in data.get('certifications', []):
                stats['certifications'][cert] += 1
            
            # Geographic coverage
            for region in data.get('geographic_coverage', []):
                stats['geographic_coverage'][region] += 1
            
            # Track for recent additions
            all_listings.append({
                'name': data.get('name', 'Unknown'),
                'category': category,
                'subcategory': subcategory,
                'date_added': data.get('date_added', '1970-01-01'),
                'file': str(filepath.relative_to(listings_path))
            })
            
        except Exception as e:
            print(f"Error processing {filepath}: {e}", file=sys.stderr)
            continue
    
    # Get 10 most recent additions
    all_listings.sort(key=lambda x: x['date_added'], reverse=True)
    stats['recent_additions'] = all_listings[:10]
    
    # Convert defaultdicts to regular dicts for JSON serialization
    stats['subcategories'] = {k: dict(v) for k, v in stats['subcategories'].items()}
    stats['certifications'] = dict(stats['certifications'])
    stats['geographic_coverage'] = dict(stats['geographic_coverage'])
    
    return stats

def generate_stats_markdown(stats):
    """Generate markdown statistics report."""
    lines = []
    
    lines.append("# PCSDBX Repository Statistics")
    lines.append(f"\n**Last Updated:** {datetime.fromisoformat(stats['timestamp']).strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    
    lines.append("## Overview\n")
    lines.append(f"- **Total Listings:** {stats['total_listings']}")
    lines.append(f"- **Categories:** {len(stats['categories'])}")
    
    total_subcategories = sum(len(subs) for subs in stats['subcategories'].values())
    lines.append(f"- **Subcategories:** {total_subcategories}")
    
    lines.append("\n## Listings by Category\n")
    for category, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / stats['total_listings'] * 100) if stats['total_listings'] > 0 else 0
        lines.append(f"- **{category}:** {count} ({percentage:.1f}%)")
    
    lines.append("\n## Subcategories by Category\n")
    for category in sorted(stats['subcategories'].keys()):
        lines.append(f"\n### {category}\n")
        for subcategory, count in sorted(stats['subcategories'][category].items(), key=lambda x: x[1], reverse=True):
            lines.append(f"- {subcategory}: {count}")
    
    if stats['certifications']:
        lines.append("\n## Top Certifications\n")
        top_certs = sorted(stats['certifications'].items(), key=lambda x: x[1], reverse=True)[:10]
        for cert, count in top_certs:
            lines.append(f"- **{cert}:** {count} suppliers")
    
    if stats['geographic_coverage']:
        lines.append("\n## Geographic Coverage\n")
        for region, count in sorted(stats['geographic_coverage'].items(), key=lambda x: x[1], reverse=True):
            lines.append(f"- **{region}:** {count} suppliers")
    
    if stats['recent_additions']:
        lines.append("\n## Recent Additions (Last 10)\n")
        for listing in stats['recent_additions']:
            lines.append(f"- **{listing['name']}** ({listing['category']} / {listing['subcategory']}) - {listing['date_added']}")
    
    return '\n'.join(lines)

def main():
    """Main entry point."""
    print("Collecting repository statistics...")
    stats = collect_statistics()
    
    print(f"Total listings: {stats['total_listings']}")
    print(f"Categories: {len(stats['categories'])}")
    
    # Create stats directory
    stats_path = Path(STATS_DIR)
    stats_path.mkdir(parents=True, exist_ok=True)
    
    # Save JSON stats
    json_path = stats_path / 'repository_stats.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)
    
    print(f"JSON stats saved to: {json_path}")
    
    # Save markdown report
    md_report = generate_stats_markdown(stats)
    md_path = stats_path / 'repository_stats.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_report)
    
    print(f"Markdown report saved to: {md_path}")
    
    # Output for GitHub Actions
    github_output = os.getenv('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f"total_listings={stats['total_listings']}\n")
            f.write(f"category_count={len(stats['categories'])}\n")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
