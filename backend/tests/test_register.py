import pytest
from httpx import AsyncClient
from datetime import datetime

from app.main import app
from app.api import endpoints as endpoints_pkg


class FakeUsersCollection:
    def __init__(self):
        self.user = None

    async def find_one(self, query):
        # find by email
        if "email" in query:
            if self.user and self.user.get("email") == query["email"]:
                return self.user
            return None
        # find by _id
        if "_id" in query:
            if self.user and (self.user.get("id") == str(query["_id"]) or self.user.get("_id") == query["_id"]):
                return self.user
            return None

    async def insert_one(self, doc):
        # emulate insertion and return an object with inserted_id
        from bson import ObjectId

        oid = ObjectId()
        now = datetime.utcnow()
        created = {
            **doc,
            "id": str(oid),
            "_id": oid,
            "role": doc.get("role", "Buyer"),
            "is_active": True,
            "is_verified": False,
            "created_at": now,
            "updated_at": now,
        }
        self.user = created

        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id

        return InsertResult(inserted_id=oid)


@pytest.fixture
def fake_users_collection(monkeypatch):
    fake = FakeUsersCollection()
    # Patch the users_collection function used in the users endpoint module
    from app.api.endpoints import users as users_module

    monkeypatch.setattr(users_module, "users_collection", lambda: fake)
    return fake


@pytest.mark.asyncio
async def test_register_success(fake_users_collection):
    payload = {
        "email": "newuser@example.com",
        "username": "newuser",
        "first_name": "New",
        "last_name": "User",
        "company_name": "ACME",
        "password": "strongpassword",
        "role": "Buyer",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/api/users/register", json=payload)

    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]
    assert data["role"] == payload["role"]
    # response should include id and created_at
    assert "id" in data or "_id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(fake_users_collection):
    # Pre-populate fake collection with an existing user
    fake_users_collection.user = {
        "email": "existing@example.com",
        "username": "existing",
        "first_name": "Ex",
        "last_name": "Ist",
        "company_name": "ACME",
        "hashed_password": "whatever",
        "role": "Supplier",
        "id": "existing-id",
        "_id": "existing-id",
        "is_active": True,
        "is_verified": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    payload = {
        "email": "existing@example.com",
        "username": "newuser2",
        "first_name": "New2",
        "last_name": "User2",
        "company_name": "ACME",
        "password": "anotherstrongpassword",
        "role": "Buyer",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/api/users/register", json=payload)

    assert resp.status_code == 400
    assert resp.json()["detail"] == "User with this email already exists"
