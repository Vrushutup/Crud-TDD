import json
from tkinter.tix import INTEGER
from urllib import response
from starlette.testclient import TestClient
from main import app
from _pytest.monkeypatch import MonkeyPatch
client = TestClient(app)

def test_ping():
    response=client.get("/ping")
    assert response.status_code == 200
    print(response)
    print(response.json())
    assert response.json()=={"ping":"pong!"}

def test_get_track():
    ans=client.get("/tracks/10")    #id exists
    ans2=client.get("/tracks/200")  #wrong id
    dump_data={"id":8,"title":"Imagine","artist":"John Lennon","duration":212.0}
    ans_data=ans.json()
    assert len(ans_data)==len(dump_data)
    for i in ans_data:
        assert type(ans_data[i])==type(dump_data[i])
    assert ans.status_code==200
    assert ans2.status_code==404
def test_get_all():
    response=client.get("/tracks/")
    response_data=response.json()
    dump_data={"id":8,"title":"Imagine","artist":"John Lennon","duration":212.0}
    for song in response_data:
        assert len(song)==len(dump_data)
        for property in song:
            assert type(dump_data[property]) == type(song[property])

def test_post_track():
    test_request_payload =  {"title":"Namo Namo"  ,"artist":"Amit Trivedi","duration":240.0}      #input track without id
    test_response_payloads={"id":12,"title":"Namo Namo","artist":"Amit Trivedi","duration":240.0} #expected output
    response =client.post('/tracks',data=json.dumps(test_request_payload),)      
    assert response.status_code==201
    assert response.json()==test_response_payloads  #checks if expected output and real output are same

def test_delete_track():
    response=client.delete("/tracks/10") #correct id
    assert response.status_code==200   
    response_not_found=client.delete("/tracks/100") #wrong id
    assert response_not_found.status_code==404

def test_update_track():
    test_up_request = {"title": "Bohemian Rhapsody (Live-Wembly)", "artist": "Freddie Mercury", "duration": 240.0}
    test_up_response_correct={"id":7,"title": "Bohemian Rhapsody (Live-Wembly)", "artist": "Freddie Mercury", "duration": 240.0}
    response_actual=client.put("/tracks/7",data=json.dumps(test_up_request),)
    response_w=client.put("/tracks/17",data=json.dumps(test_up_request))
    assert test_up_response_correct==response_actual.json()
    assert response_w.status_code==404
