from pymongo import MongoClient

def main():
    # 1. Connect to Local MongoDB
    # Make sure you have MongoDB locally running on the default port or update the URI.
    client = MongoClient("mongodb://localhost:27017/")
    
    # Check server availability
    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print("Could not connect to MongoDB. Is the service running?")
        print(f"Error: {e}")
        return

    # 2. Create / Access the Database
    # MongoDB creates databases and collections lazily when data is inserted.
    db = client["game_inventory_db"]
    
    # Access a collection (equivalent to a table in SQL)
    inventory = db["player_items"]
    
    # Clear out older demo data for clean runs
    inventory.drop()

    # 3. Insert specific documents
    print("\nInserting Player Items into the Database...")
    items = [
        {"player_id": "U123", "item_name": "Health Potion", "quantity": 5, "type": "consumable", "rare": False},
        {"player_id": "U123", "item_name": "Sword of Destiny", "quantity": 1, "type": "weapon", "rare": True, "stats": {"damage": 50, "durability": 100}},
        {"player_id": "U456", "item_name": "Leather Armor", "quantity": 1, "type": "armor", "rare": False},
        {"player_id": "U789", "item_name": "Mana Potion", "quantity": 10, "type": "consumable", "rare": False}
    ]
    
    result = inventory.insert_many(items)
    print(f"Inserted {len(result.inserted_ids)} documents.")

    # 4. Query Documents
    print("\n--- QUERY RESULTS ---")
    
    # Query 1: Find all items owned by player U123
    print("\nItems for Player U123:")
    for item in inventory.find({"player_id": "U123"}):
        print(f"  - {item['quantity']}x {item['item_name']}")

    # Query 2: Find all 'rare' items using an inclusive filter
    print("\nAll Rare Items in Game:")
    for item in inventory.find({"rare": True}):
        print(f"  - {item['item_name']} (Owned by {item['player_id']})")

    # Query 3: Find consumables sorting by highest quantity
    print("\nConsumables (Highest Quantity First):")
    for item in inventory.find({"type": "consumable"}).sort("quantity", -1):
        print(f"  - {item['item_name']}: {item['quantity']}")

if __name__ == "__main__":
    main()
