import os
import json
from datetime import datetime

REPO_PATH = "/home/ubuntu/pcsdbx"
LISTINGS_PATH = os.path.join(REPO_PATH, "listings")
OUTPUT_PATH = "/home/ubuntu/pcsdbx_dashboard/client/public/dashboard_data.json"

def analyze_listings():
    stats = {
        "total_listings": 0,
        "categories": {},
        "top_categories": [],
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "listings": [], # Detailed listings for Explorer
        "network": {    # Data for Network Viz
            "nodes": [],
            "links": []
        }
    }

    if not os.path.exists(LISTINGS_PATH):
        print(f"Error: Listings path not found at {LISTINGS_PATH}")
        return stats

    # Helper to track unique nodes for network
    node_ids = set()
    
    def add_node(id, group, label=None):
        if id not in node_ids:
            stats["network"]["nodes"].append({
                "id": id,
                "group": group,
                "label": label or id
            })
            node_ids.add(id)

    def add_link(source, target, value=1):
        stats["network"]["links"].append({
            "source": source,
            "target": target,
            "value": value
        })

    # Walk through the listings directory
    for root, dirs, files in os.walk(LISTINGS_PATH):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        listing_data = json.load(f)
                        
                        stats["total_listings"] += 1
                        
                        # Extract basic info
                        category_path = listing_data.get("category_path", "")
                        parts = category_path.split("/")
                        category = parts[0] if len(parts) > 0 else "Uncategorized"
                        subcategory = parts[1] if len(parts) > 1 else ""
                        
                        # Normalize category name
                        category_name = category.replace("_", " ")
                        if category_name not in stats["categories"]:
                            stats["categories"][category_name] = 0
                        stats["categories"][category_name] += 1
                        
                        # Add to detailed listings
                        listing_summary = {
                            "id": listing_data.get("listing_id", file.replace(".json", "")),
                            "name": listing_data.get("company_name", "Unknown"),
                            "category": category_name,
                            "subcategory": subcategory.replace("_", " "),
                            "country": listing_data.get("country", "Unknown"),
                            "status": listing_data.get("status", "active"),
                            "tags": listing_data.get("tags", []),
                            "specializations": listing_data.get("specializations", [])
                        }
                        stats["listings"].append(listing_summary)

                        # Build Network Data
                        # 1. Supplier Node
                        supplier_id = listing_summary["id"]
                        add_node(supplier_id, "supplier", listing_summary["name"])
                        
                        # 2. Category Node & Link
                        cat_id = f"cat_{category}"
                        add_node(cat_id, "category", category_name)
                        add_link(supplier_id, cat_id)
                        
                        # 3. Subcategory Node & Link (if exists)
                        if subcategory:
                            subcat_id = f"sub_{subcategory}"
                            add_node(subcat_id, "subcategory", subcategory.replace("_", " "))
                            add_link(cat_id, subcat_id) # Link Category -> Subcategory
                            add_link(supplier_id, subcat_id) # Link Supplier -> Subcategory

                except Exception as e:
                    print(f"Error reading {file}: {e}")

    # Format category data for charts
    category_mapping = {
        "Raw_Materials": "Raw Materials",
        "Packaging": "Packaging",
        "Equipment": "Equipment",
        "Business_Services": "Services",
        "Labels_and_Sleeves": "Labels",
        "Labels": "Labels"
    }

    chart_data = []
    colors = [
        "var(--chart-1)", "var(--chart-2)", "var(--chart-3)", 
        "var(--chart-4)", "var(--chart-5)", "var(--chart-1)", "var(--chart-2)"
    ]
    
    sorted_categories = sorted(stats["categories"].items(), key=lambda x: x[1], reverse=True)
    
    for i, (cat, count) in enumerate(sorted_categories):
        display_name = category_mapping.get(cat.replace(" ", "_"), cat)
        chart_data.append({
            "name": display_name,
            "value": count,
            "color": colors[i % len(colors)]
        })

    stats["chart_data"] = chart_data
    stats["total_categories"] = len(stats["categories"])
    
    # Velocity calculation
    start_date = datetime(2025, 11, 1)
    now = datetime.now()
    days_diff = (now - start_date).days
    velocity = stats["total_listings"] / days_diff if days_diff > 0 else stats["total_listings"]
    stats["velocity"] = f"{velocity:.1f}/day"

    return stats

def main():
    print("Analyzing repository data...")
    data = analyze_listings()
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Dashboard data generated at {OUTPUT_PATH}")
    print(f"Total Listings: {data['total_listings']}")
    print(f"Total Categories: {data['total_categories']}")
    print(f"Network Nodes: {len(data['network']['nodes'])}")
    print(f"Network Links: {len(data['network']['links'])}")

if __name__ == "__main__":
    main()
