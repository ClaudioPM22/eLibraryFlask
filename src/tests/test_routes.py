def test_create_book_route(client):
  response = client.post('/api/books/',json = {
    "title": "Test Book",
    "author": "Tester",
    "isbn": "1234567890123",
    "numpages": 300,
  })

  assert response.status_code == 201
  assert response.json['title'] == "Test Book"