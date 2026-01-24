


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

"""----------User Routes----------"""
from models.user import UserRole

def test_create_user_success_route(client,auth_headers):
  payload= {
    "username":"tester001",
    "email":"tester001@test01.com",
    "role":"client",
    "password":"tester001",
  }
  response = client.post('/api/users/',json= payload,headers= auth_headers,
  )

  assert response.status_code == 201
  user = response.get_json()
  assert user["username"] == "tester001"
  assert user["email"] == "tester001@test01.com"
  assert user["role"] == "client"
  assert "password" not in user
  
  payload= {
    "username":"tester002",
    "email":"tester002@test01.com",
    "role":"admin",
    "password":"tester002",
  }
  response = client.post(
    '/api/users/',
    json= payload,
    headers= auth_headers,
  )
  user2 = response.get_json()
  assert user2["role"] == "admin"

def test_create_user_duplicate_email(client, sample_users, auth_headers):
    #Prueba error cuando el email ya existe
    payload = {
        "username": "nuevo_usuario",
        "email": "tester002@test.com", 
        "role": "client",
        "password": "password123"
    }
    response = client.post('/api/users/', json=payload, headers=auth_headers)
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "El correo electronico ya esta registrado."

def test_create_user_invalid_format(client, auth_headers):
    #Prueba error de formato (Error de Marshmallow)
    payload = {
        "username": "tu",          # Demasiado corto (min 3)
        "email": "correo-invalido", # Formato mal
        "role": "client",
        "password": "123"          # Demasiado corto (min 8)
    }
    response = client.post('/api/users/', json=payload, headers=auth_headers)
    
    assert response.status_code == 400
    data = response.get_json()
    assert "errors" in data
    errors = data["errors"]
    assert "username" in errors
    assert "email" in errors
    assert "password" in errors

def test_get_user_by_id_success_route(client,sample_users,auth_headers):
  user = sample_users[0]
  response = client.get(f'/api/users/{user.id}')
  user = response.get_json()
  assert response.status_code == 200
  assert user["username"] == sample_users[0].username
  assert user["email"] == sample_users[0].email
  assert user["role"] == "client"
  assert "password" not in user

def test_get_user_by_invalid_id_route(client,auth_headers):
  user_id = 999
  response = client.get(f'/api/users/{user_id}')
  data = response.get_json()
  assert response.status_code == 404
  assert data["message"] == "Usuario no encontrado"
  

"""----------Loan Routes----------"""
from datetime import date, timedelta
def test_create_loan_success_route(client,sample_users,sample_books,auth_headers):
  user = sample_users[0]
  book = sample_books[0]
  payload = {
    "user_id":user.id,
    "book_id":book.id,
  }
  response = client.post(
    '/api/loans/',
    json=payload,
    headers=auth_headers,
  )
  assert response.status_code == 201

def test_create_loan_unauthorized_route(client,sample_users,sample_books):
  user = sample_users[0]
  book = sample_books[0]
  payload = {
    "user_id":user.id,
    "book_id":book.id,
  }
  response = client.post(
    '/api/loans/',
    json=payload,
  )
  assert response.status_code == 401

def test_create_loan_invalid_format(client, auth_headers):
    payload = {"book_id": "esto-no-es-un-numero"}
    response = client.post(
      '/api/loans/',
      json=payload,
      headers=auth_headers)
    assert response.status_code == 400
    assert "errors" in response.get_json()


def test_create_loan_book_not_found(client, auth_headers):
    payload = {"book_id": 9999, "user_id": 1}
    response = client.post(
      '/api/loans/', 
      json=payload, 
      headers=auth_headers)
    assert response.status_code == 400
    assert "error" in response.get_json() # Aquí entra al 'except'

def test_return_book_success_route(client,sample_loans,auth_headers):
  loan = sample_loans
  response = client.put(f'/api/loans/{loan.id}/return', headers=auth_headers)

  data = response.get_json()
  assert response.status_code == 200
  assert data["message"] == "Libro devuelto exitosamente"
  assert "loan" in data

def test_return_book_non_success_route(client,sample_loans,auth_headers):
  response = client.put(
    f'/api/loans/999/return',
    headers=auth_headers)

  data = response.get_json()
  assert response.status_code == 404
  assert data["message"] == "Prestamo no encontrado o ya devuelto"

def test_check_available_book_route(client,sample_books):
  book = sample_books[0]
  response = client.get(f'/api/loans/check/{book.id}')

  data = response.get_json()
  assert response.status_code == 200
  assert data["book_id"] == book.id
  assert data["available"] == True


  
  