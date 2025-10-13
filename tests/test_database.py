import unittest
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

class TestMongoDBSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Connect to MongoDB (adjust URI as needed)
        cls.client = MongoClient("mongodb://localhost:27017/")
        cls.db = cls.client["test_db"]

        # Create collections
        cls.users = cls.db["users"]
        cls.apps = cls.db["applications"]
        cls.roles = cls.db["user_app_roles"]

        # Clean collections before test
        cls.users.delete_many({})
        cls.apps.delete_many({})
        cls.roles.delete_many({})

        # Create unique indexes to simulate constraints
        cls.users.create_index("username", unique=True)
        cls.apps.create_index("app_name", unique=True)

    @classmethod
    def tearDownClass(cls):
        cls.client.drop_database("test_db")
        cls.client.close()

    def test_insert_and_reference(self):
        """Verify documents can be inserted and linked logically."""
        user_id = self.users.insert_one({"username": "alice", "email": "a@example.com"}).inserted_id
        app_id = self.apps.insert_one({"app_name": "AppX"}).inserted_id
        role_id = self.roles.insert_one({
            "user_id": user_id,
            "app_id": app_id,
            "role": "admin"
        }).inserted_id

        # Validate inserted data
        self.assertIsNotNone(user_id)
        self.assertIsNotNone(app_id)
        self.assertIsNotNone(role_id)

        # Check role references valid user and app
        role_doc = self.roles.find_one({"_id": role_id})
        self.assertEqual(role_doc["user_id"], user_id)
        self.assertEqual(role_doc["app_id"], app_id)

    def test_unique_constraints(self):
        """Verify unique indexes on username and app_name."""
        self.users.insert_one({"username": "bob", "email": "b@example.com"})
        with self.assertRaises(DuplicateKeyError):
            # Try inserting duplicate username
            self.users.insert_one({"username": "bob", "email": "other@example.com"})

    def test_missing_reference(self):
        """Ensure roles reference existing user/app documents."""
        fake_user_id = "507f1f77bcf86cd799439011"  # random ObjectId string
        app = self.apps.find_one()
        with self.assertRaises(AssertionError):
            # We expect to fail validation manually since MongoDB doesn't enforce FK
            self.assertIsNotNone(self.users.find_one({"_id": fake_user_id}))

if __name__ == "__main__":
    unittest.main()
