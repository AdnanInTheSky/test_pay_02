from pymongo import MongoClient

# ⚠️ Replace with your actual URI (include DB name for safety)
MONGO_URI = "mongodb+srv://adnan:aFdbDSQzHk8G4cs6@cluster0.7fvc3no.mongodb.net/paystation_demo?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["paystation_demo"]
orders = db["orders"]

count = orders.count_documents({})
print(f"📦 Current orders in DB: {count}")

if count == 0:
    print("✅ Database is already empty.")
else:
    confirm = input("⚠️  Are you sure you want to DELETE ALL orders? (yes/no): ").strip().lower()
    if confirm == "yes":
        result = orders.delete_many({})
        print(f"✅ Successfully deleted {result.deleted_count} order(s).")
    else:
        print("❌ Operation cancelled.")