
def test_login_invalid_credentials(client):
    """Invalid login should fail"""
    response = client.post("/login", data={"username": "wrong", "password": "wrong"})
    assert b"Invalid credentials" in response.data
