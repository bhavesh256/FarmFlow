from pymongo import AsyncMongoClient
from app.core.config import settings


async def connect_to_mongodb(app):
    client = AsyncMongoClient(settings.MONGODB_URI)

    try:
        await client.admin.command("ping")
        print("MongoDB connected successfully!")

        app.state.mongodb_client = client
        app.state.db = client[settings.MONGODB_DATABASE]

    except Exception:
        await client.close()
        raise


async def close_mongodb_connection(app):
    client = getattr(app.state, "mongodb_client", None)

    if client is not None:
        await client.close()
        print("MongoDB connection closed.")
