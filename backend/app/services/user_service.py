from datetime import datetime, timezone
from bson import ObjectId
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def serialize_user(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "emailOrPhone": user["emailOrPhone"],
        "role": user["role"],
        "createdAt": user["createdAt"],
    }


async def create_user(db, data):
    existing = await db.users.find_one(
        {"emailOrPhone": data.emailOrPhone}
    )

    if existing:
        return None

    user = {
        "name": data.name,
        "emailOrPhone": data.emailOrPhone,
        "passwordHash": password_hash.hash(data.password),
        "role": data.role,
        "createdAt": datetime.now(timezone.utc),
    }

    result = await db.users.insert_one(user)
    user["_id"] = result.inserted_id

    return serialize_user(user)


async def get_users(db):
    users = await db.users.find().to_list(length=100)
    return [serialize_user(user) for user in users]


async def get_user(db, user_id: str):
    if not ObjectId.is_valid(user_id):
        return None

    user = await db.users.find_one({"_id": ObjectId(user_id)})
    return serialize_user(user) if user else None


async def update_user(db, user_id: str, changes: dict):
    if not ObjectId.is_valid(user_id):
        return None

    changes = {
        key: value
        for key, value in changes.items()
        if value is not None
    }

    if not changes:
        return None

    if "emailOrPhone" in changes:
        existing = await db.users.find_one({
            "emailOrPhone": changes["emailOrPhone"],
            "_id": {"$ne": ObjectId(user_id)},
        })
        if existing:
            return None

    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": changes},
    )

    if result.matched_count == 0:
        return None

    return await get_user(db, user_id)


async def delete_user(db, user_id: str):
    if not ObjectId.is_valid(user_id):
        return False

    result = await db.users.delete_one(
        {"_id": ObjectId(user_id)}
    )

    return result.deleted_count == 1
