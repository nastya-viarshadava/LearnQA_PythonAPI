def test_service_availability(self):
    # First check if the API is responding
    response = requests.get('https://reqres.in/api/users/1')
    assert response.status_code == 200, "API service appears to be down"