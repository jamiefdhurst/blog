def test_index(client):
    response = client.get('/')
    assert b'Blog' in response.data
    assert b'Test 1' in response.data
    assert b'Test 2' in response.data
    assert b'placeholder.png' in response.data
    assert b'very little inside of it' in response.data

def test_view(client):
    response = client.get('/2022-01-01_test-1')
    assert b'Test 1' in response.data
    assert b'Test 2' not in response.data
    assert b'placeholder.png' in response.data
    assert b'They were just sucked into space.' in response.data
    
