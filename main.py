from ctypes import Union
import pathlib
import json
import pathlib
from typing import List, Union
from fastapi import FastAPI, Response

from models import Track
from data.tracks import tracks_set
app=FastAPI()
data=tracks_set
@app.get("/ping")
def pong():
    return {"ping": "pong!"}

#get all the tracks on the list
@app.get("/tracks/",response_model=List[Track])
def tracks(response:Response):
    response.status_code=200
    return data

#get a specific track based on the track id
@app.get('/tracks/{track_id}',response_model=Union[Track, str])
def track(track_id:int,response:Response):
    track=None
    for t in data:
        if t['id']==track_id:
            track=t
            response.status_code=200
            break
    if track is None:
        response.status_code=404
        return "Track not found"
    response.status_code=200
    return track
    
# create tracks
@app.post('/tracks',response_model=Track,status_code=201)
def create_track(track: Track):
    track_dict=track.dict()
    track_dict['id']=max(data,key=lambda x: x['id']).get('id')+1
    data.append(track_dict)
    return track_dict
#Update track based on the track id
@app.put("/tracks/{track_id}", response_model=Union[Track, str])
def update_track(track_id: int, updated_track: Track, response: Response):

    track = next(
        (track for track in data if track["id"] == track_id), None
    )

    if track is None:
        # if a track with given ID doesn't exist, set 404 code and return string
        response.status_code = 404
        return "Track not found"
    
    # update the track data
    for key, val in updated_track.dict().items():
        if key != 'id': # don't reset the ID
            track[key] = val
            response.status_code=200
    return track

@app.delete("/tracks/{track_id}",response_model=Union[Track,str])
def delete_track(track_id:int,response:Response):
    # get the index of the track to delete
    
    delete_index=-1
    for track in data:
        delete_index+=1
        if track_id==track["id"]:
            response=track
            del data[delete_index] 
            Response(status_code=200)
            return "Deleted track successfully"

    response.status_code = 404
    return "Track not found"