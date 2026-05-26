from app import app

def test_valid_text():

    client = app.test_client() #creates a fake client/user 
    #send the post request 
    response = client.post(
        "/validate",
        json={"text": "Hello123"}
    )
    #sends data json format to validate using post 

    assert response.status_code == 200
    assert response.get_json()["status"] == "valid"


def test_invalid_text():

    client = app.test_client()
    response = client.post(
        "/validate",
        json={"text": "Hello@123"}
    )

    assert response.status_code ==400
    assert response.get_json()["status"] == "invalid"