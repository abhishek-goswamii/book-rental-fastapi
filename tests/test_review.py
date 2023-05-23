def test_add_review(authorized_client, test_add_book_fixture):
    res = authorized_client.post('/add-review/1', json={
        "Rating": 5,
        "ReviewText": "rrrrr"
    })
    assert res.json().get('BookID') == 1
    assert res.status_code == 200

def test_add_review_with_missing_field(authorized_client, test_add_book_fixture):
    res = authorized_client.post('/add-review/1', json={
        "Rating": 5,
    })
    assert res.status_code == 422

def test_add_review_with_invalid_book_id(authorized_client, test_add_book_fixture):
    res = authorized_client.post('/add-review/100', json={
        "Rating": 5,
        "ReviewText": "rrrrr"
    })
    assert res.status_code == 404

def test_add_review_with_unauthorized_user(client):
    res = client.post('/add-review/1', json={
        "Rating": 5,
        "ReviewText": "rrrrr"
    })
    assert res.status_code == 401
    assert res.json() == {'detail': 'Not authenticated'}
