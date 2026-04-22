from pymongo import MongoClient

def main():
    # 1. Connect to the local MongoDB Server
    # Ensure MongoDB is running locally on the default port 27017
    client = MongoClient("mongodb://localhost:27017/")
    
    # 2. Create or access a small database for the presentation demo
    db = client["fitness_users_db"]
    
    # Access a collection (which acts similar to a table in SQL)
    profiles_collection = db["fitness_profiles"]
    
    # Drop existing collection to ensure a clean slate for the demo run
    profiles_collection.drop()

    # 3. Insert documents into the NoSQL database
    print("Inserting user profiles into the MongoDB collection...")
    users = [
        {
            "username": "athlete_john",
            "age": 28,
            "goals": ["muscle gain", "stamina"],
            "active_subscription": True
        },
        {
            "username": "yoga_jane",
            "age": 34,
            "goals": ["flexibility", "mindfulness"],
            "active_subscription": True,
            "preferred_sessions": "morning" # Example of dynamic, schematic-less data
        },
        {
            "username": "casual_mike",
            "age": 41,
            "goals": ["weight loss"],
            "active_subscription": False
        }
    ]
    
    insert_result = profiles_collection.insert_many(users)
    print(f"Successfully inserted {len(insert_result.inserted_ids)} user profiles.\n")

    # 4. Run a simple database query
    print("--- QUERY RESULTS: Find Active Subscriptions ---")
    
    # Filtering query to find only users with an 'active_subscription' equal to True
    active_users = profiles_collection.find({"active_subscription": True})
    
    for user_doc in active_users:
        goals_joined = ", ".join(user_doc.get("goals", []))
        print(f"User: {user_doc['username']} | Age: {user_doc['age']} | Primary Goals: {goals_joined}")

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Failed to connect to MongoDB or run operations. Make sure the database is running.\nError Details: {error}")
