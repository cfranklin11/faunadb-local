def test_user_creation(faunadb_client):
    username = "burgerbob"
    created_user = faunadb_client.create_user(
        username=username, password="password1234"
    )
    assert created_user["username"] == username

    all_users = faunadb_client.all_users()
    assert len(all_users) == 1
