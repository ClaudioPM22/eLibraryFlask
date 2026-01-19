
"""----------Book Routes----------"""
def test_create_book_route(client, auth_headers):
  response = client.post(
    '/api/books/',
    json = {
    "title": "Test Book",
    "author": "Tester",
    "isbn": "1234567890123",
    "numpages": 300,
    },
    headers=auth_headers,
    )

  assert response.status_code == 201
  assert response.json['title'] == "Test Book"

def test_create_book_unauthorized_route(client):
  json = {
    "title": "Test Book",
    "author": "Tester",
    "isbn": "1234567890123",
    "numpages": 300,
  }
  response = client.post('/api/books/',json=json)

  assert response.status_code == 401

def test_create_book_invalid_data_route(client,auth_headers):
  json = {
    "title": "",
    "author": "",
    "isbn": "1234567890",
    "numpages": -10,
  }
  response = client.post('/api/books/',json=json,headers=auth_headers)
  errors = response.get_json()["errors"]
  assert "title" in errors
  assert "isbn" in errors
  assert "numpages" in errors

def test_get_books_route(client, sample_books):
  response = client.get('/api/books/')
  assert response.status_code == 200

  data = response.get_json()

  assert len(data) == len(sample_books)
  assert data[0]["title"] == sample_books[0].title
  assert data[0]["author"] == sample_books[0].author
  assert data[0]["isbn"] == sample_books[0].isbn
  assert data[0]["numpages"] == sample_books[0].numpages
  assert data[1]["title"] == sample_books[1].title
  assert data[1]["author"] == sample_books[1].author
  assert data[1]["isbn"] == sample_books[1].isbn
  assert data[1]["numpages"] == sample_books[1].numpages

def test_get_book_by_id_route(client, sample_books):
  response = client.get('/api/books/1')
  assert response.status_code == 200
  data = response.get_json()

  assert data["title"] == sample_books[0].title
  assert data["author"] == sample_books[0].author
  assert data["isbn"] == sample_books[0].isbn
  assert data["numpages"] == sample_books[0].numpages

def test_update_book_success_route(client, sample_books, auth_headers):
  book = sample_books[0]

  payload = {
    "title": "Nuevo Título",
    "author": "Nuevo Autor",
    "isbn": "9999999999999",
    "numpages": 777
  }

  response = client.put(
    f"/api/books/{book.id}",
    json=payload,
    headers=auth_headers,
  )

  assert response.status_code == 200

  data = response.get_json()
  assert data["title"] == payload["title"]
  assert data["author"] == payload["author"]
  assert data["isbn"] == payload["isbn"]
  assert data["numpages"] == payload["numpages"]

def test_update_book_unauthorized_route(client, sample_books, auth_headers):
  book = sample_books[0]

  payload = {
    "title": "Intento no autorizado",
    "author": "No debería actualizarse",
    "isbn": "111",
    "numpages": 123
  }

  response = client.put(
    f"/api/books/{book.id}",
    json=payload
  )

  assert response.status_code == 401

def test_update_book_invalid_data_route(client, sample_books, auth_headers):
  book = sample_books[0]

  payload = {
    "title": "",  # inválido
    "author": "X",
    "isbn": "123",
    "numpages": -10  # inválido
  }

  response = client.put(
    f"/api/books/{book.id}",
    json=payload,
    headers=auth_headers
  )

  assert response.status_code == 400
  errors = response.get_json()["errors"]
  assert "title" in errors
  assert "isbn" in errors
  assert "numpages" in errors

def test_delete_book_success_route(client, sample_books, auth_headers):
  book = sample_books[0]
  response = client.delete(f'/api/books/{book.id}', headers=auth_headers)
  message = response.get_json()["message"]
  assert response.status_code == 200
  assert message == "Libro eliminado correctamente"

def test_delete_book_unauthorized_route(client,sample_books):
  book = sample_books[0]
  response = client.delete(f'/api/books/{book.id}')
  assert response.status_code == 401

def test_delete_book_invalid_id_route(client,auth_headers):
  response = client.delete(f'/api/books/1',headers=auth_headers)
  message = response.get_json()["message"]
  assert response.status_code == 404
  assert message == "Libro no encontrado"

"""----------Loan Routes----------"""

#def test_create_loan_success_route(client,auth_headers):

  
  