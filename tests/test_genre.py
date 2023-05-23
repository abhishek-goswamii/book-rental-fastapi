
def test_add_genre(authorized_client):
    res = authorized_client.post('/add-genre', json={
        "GenreName": "genre1"
    })
    assert res.status_code == 200
    assert res.json().get('GenreName') == 'genre1'

def test_add_genre_with_missing_field(authorized_client):
    res = authorized_client.post('/add-genre', json={
    })
    assert res.status_code == 422

def test_add_genre_with_unauthorized_user(client):
    res = client.post('/add-genre', json={
        "GenreName": "genre1"
    })
    assert res.status_code == 401
    assert res.json() == {'detail': 'Not authenticated'}

def test_add_genre_with_admin_user(authorized_client):
    res = authorized_client.post('/add-genre', json={
        "GenreName": "genre2"
    })
    assert res.status_code == 200
    assert res.json().get('GenreName') == 'genre2'

def test_get_all_genres(authorized_client,test_add_genre_fixture):
    res = authorized_client.get('/genre-list')
    assert res.status_code == 200
    assert res.json()[0].get('GenreName') == 'genre1'

def test_get_all_genres_with_unauthorized_user(client):
    res = client.get('/genre-list')
    assert res.status_code == 401
    assert res.json() == {'detail': 'Not authenticated'}

def test_get_all_genres_with_admin_user(authorized_client,test_add_genre_fixture):
    res = authorized_client.get('/genre-list')
    assert res.status_code == 200
    assert res.json()[0].get('GenreName') == 'genre1'

def test_connect_book_genre(authorized_client,test_add_book_fixture,test_add_genre_fixture):
    res = authorized_client.post('/connect-genre-book',json={
        "GenreName": 'genre1',
        "BookName": 'cc' 
    })
    assert res.status_code == 200
    assert res.json() == 'added'

def test_connect_book_genre_with_missing_field(authorized_client,test_add_book_fixture,test_add_genre_fixture):
    res = authorized_client.post('/connect-genre-book',json={
        "GenreName": 'genre1',
    })
    assert res.status_code == 422

def test_connect_book_genre_with_invalid_genre(authorized_client,test_add_book_fixture,test_add_genre_fixture):
    res = authorized_client.post('/connect-genre-book',json={
        "GenreName": 'invalid',
        "BookName": 'cc' 
    })
    assert res.status_code == 200
    assert res.json() == 'genre with this name not found'

def test_connect_book_genre_with_invalid_book(authorized_client,test_add_book_fixture,test_add_genre_fixture):
    res = authorized_client.post('/connect-genre-book',json={
        "GenreName": 'genre1',
        "BookName": 'invalid' 
    })
    assert res.status_code == 200
    assert res.json() == 'book with this name not found'

def test_connect_book_genre_with_unauthorized_user(client):
    res = client.post('/connect-genre-book',json={
        "GenreName": 'genre1',
        "BookName": 'cc' 
    })
    assert res.status_code == 401
    assert res.json() == {'detail': 'Not authenticated'}

def test_connect_book_genre_with_admin_user(authorized_client,test_add_book_fixture,test_add_genre_fixture):
    res = authorized_client.post('/connect-genre-book',json={
        "GenreName": 'genre1',
        "BookName": 'cc' 
    })
    assert res.status_code == 200
    assert res.json() == 'added'


