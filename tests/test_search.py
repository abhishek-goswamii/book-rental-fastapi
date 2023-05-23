def test_search_book_by_genre(authorized_client, test_add_book_fixture):
    res = authorized_client.get('/search-book-by-genre/h')
    assert res.status_code == 200
    assert res.json()[0].get('Title') == 'cc'

def test_search_book_by_genre_with_invalid_genre(authorized_client, test_add_book_fixture):
    res = authorized_client.get('/search-book-by-genre/invalid')
    assert res.status_code == 200
    assert res.json() == "genre with this name not found"

def test_search_book_by_genre_with_unauthorized_user(client):
    res = client.get('/search-book-by-genre/h')
    assert res.status_code == 401
    assert res.json() == {'detail': 'Not authenticated'}

def test_search_book_by_author(authorized_client, test_add_book_fixture):
    res = authorized_client.get('/search-by-author/author3')
    assert res.status_code == 200
    assert res.json()[0].get('Title') == 'cc'

def test_search_book_by_author_with_invalid_author(authorized_client, test_add_book_fixture):
    res = authorized_client.get('/search-by-author/invalid')
    assert res.status_code == 200
    assert res.json() == "no book with this author"

def test_search_book_by_author_with_unauthorized_user(client):
    res = client.get('/search-by-author/author3')
    assert res.status_code == 401
    assert res.json() == {'detail': 'Not authenticated'}

def test_search_book_by_title(authorized_client, test_add_book_fixture):
    res = authorized_client.get('/search-by-title/cc')
    assert res.status_code == 200
    assert res.json().get('Title') == 'cc'

def test_search_book_by_title_with_invalid_title(authorized_client, test_add_book_fixture):
    res = authorized_client.get('/search-by-title/invalid')
    assert res.status_code == 200
    assert res.json() == "no book with title : invalid"

def test_search_book_by_title_with_unauthorized_user(client):
    res = client.get('/search-by-title/cc')
    assert res.status_code == 401
    assert res.json() == {'detail': 'Not authenticated'}
