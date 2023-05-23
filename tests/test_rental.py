

def test_rent_a_book(authorized_client, test_add_book_fixture):
    res = authorized_client.post('/rentbook', json={
        "BookName": "cc",
        "RentalPeriod": 10,
        "RentalDate": "2023-05-18",
        "ReturnDate": "2023-05-28"
    })
    assert res.status_code == 200
    assert res.json().get('message') == "Book rented successfully"

def test_rent_a_book_with_missing_field(authorized_client, test_add_book_fixture):
    res = authorized_client.post('/rentbook', json={
        "BookName": "cc",
        "RentalPeriod": 10,
        "RentalDate": "2023-05-18",
    })
    assert res.status_code == 422

def test_rent_a_book_with_invalid_book_name(authorized_client, test_add_book_fixture):
    res = authorized_client.post('/rentbook', json={
        "BookName": "invalid",
        "RentalPeriod": 10,
        "RentalDate": "2023-05-18",
        "ReturnDate": "2023-05-28"
    })
    assert res.status_code == 404
    assert res.json().get('detail') == "Book not found"

def test_rent_a_book_with_unauthorized_user(client):
    res = client.post('/rentbook', json={
        "BookName": "cc",
        "RentalPeriod": 10,
        "RentalDate": "2023-05-18",
        "ReturnDate": "2023-05-28"
    })
    assert res.status_code == 401
    assert res.json() == {'detail': 'Not authenticated'}

def test_rent_a_book_with_admin_user(authorized_client, test_add_book_fixture):
    res = authorized_client.post('/rentbook', json={
        "BookName": "cc",
        "RentalPeriod": 10,
        "RentalDate": "2023-05-18",
        "ReturnDate": "2023-05-28"
    })
    assert res.status_code == 200
    assert res.json().get('message') == "Book rented successfully"

def test_return_a_book(authorized_client, test_add_book_fixture,test_rent_book_fixture):
    res = authorized_client.post('/return/cc')
    assert res.status_code == 200
    assert res.json().get('message') == "Book returned successfully"

def test_return_a_book_with_invalid_book_name(authorized_client, test_add_book_fixture,test_rent_book_fixture):
    res = authorized_client.post('/return/invalid')
    assert res.status_code == 404
    assert res.json().get('detail') == "Book not found"

def test_return_a_book_with_unauthorized_user(client):
    res = client.post('/return/cc')
    assert res.status_code == 401
    assert res.json() == {'detail': 'Not authenticated'}

def test_get_all_rented_books_with_unauthorized_user(client):
    res = client.get('/get-rented-books')
    assert res.status_code == 401
    assert res.json() == {'detail': 'Not authenticated'}

def test_get_all_rented_books_with_admin_user(authorized_client,test_add_book_fixture,test_rent_book_fixture):
    res = authorized_client.get('/get-rented-books')
    assert res.status_code == 200

def test_get_all_rented_books_with_non_admin_user(authorized_client_non_admin):
    res = authorized_client_non_admin.get('/get-rented-books')
    assert res.status_code == 400
    assert res.json().get('detail') == "Only Admin can see all rented books"   
