# import neccessary modules
from datetime import datetime
import datetime
import requests
import pandas as pd
from sqlalchemy.orm import sessionmaker
import json
from logging import exception
from pandas import DataFrame as df
import sqlite3
import sqlalchemy

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
# create in advance the function to validate data before load : 
def transform_aka_validation(df):
    # 1. if the df loaded is empty
    if df.empty: #note : this funtion defaults the dataframe loaded; no need to pass specific table param.
        raise Exception('no data loaded')

    # 2. if there are NULLs in data (there should not be because this is prod data)

    if df.isnull().values.any():
        raise Exception('detected NULL in data.')
    
    return True




if __name__ == "__main__":

    #               Extract
    # source : spotify api // target : sqlite db & view w/ dbeaver (dbms). 

        ## convert yesterday's time to put in GET request
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    ## setup auth for GET request
    TOKEN = "BQAiyrKP-RKEd9ERFeEmXuFrAmsexf66x-8AcvnnA5QOe-G0E2xrYLAcmDznBAYRG-i2DcvumLOC4gS1poFpPBxtYieTkQlnV-RvOeZ-gnBF59il7ZefPtsHtpIg39mjbgfl_3mH0Tuj2ftGiRXabfWzz7GavUj1fjFOwEWfwnfXaVFzmmuvJVjsW_w-NAbB0At_C1Fu" # manually insert token here for auth. The token can be generated at https://developer.spotify.com/console/get-recently-played/?limit=&after=&before=

    header = {
        "Accept" : "application/json",
        "Content-Type" : "application/json", "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = header)

    # raise exception if token expires
    if r.status_code != 200:
        raise Exception("something went wrong with the token - not receiving code 200.")


    # extract relevant data from json. from the json return, the attributes i'd like to have are track name, artist name, timestamps.

    data = r.json()

    track_name = []
    artist_name = []
    timestamp = [] # note : in my code timestamp should be full date e.g. 2022-10-25T05:02:45.894Z
    played_date = []

    for song in data["items"]:
        track_name.append(song["track"]["name"])
        artist_name.append(song["track"]["artists"][0]["name"])
        timestamp.append(song["played_at"])
        played_date.append(song["played_at"][0:10])
    
    
    
    
    
        
    #          transform aka validate data 
        # use panda to allow native validation (validate the data frame)
        # this section is written as a function, transform_aka_validation 



        


    #               Load 

        # create panda dataframe
        # 1. assign the parsed variables into dictionaries
    song_dict = {
            "track_name" : track_name,
            "artist_name" : artist_name,
            "timestamp" : timestamp,
            "played_date" : played_date
    }
        
        # 2. create df and assign column names to df
    song_df = pd.DataFrame(song_dict, columns = ["track_name", "artist_name", "timestamp", "played_date"])


    # 4. call the function : 
    if transform_aka_validation(song_df):
        print('validation completed with successful result.')



    # init a db on sqlite & create cursor to work with it
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect("my_played_tracks.sqlite")
    cursor = conn.cursor()
    
    
    
    # execute sql to create table
    sql_command = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        track_name VARCHAR(200),
        artist_name VARCHAR(200),
        timestamp VARCHAR(200),
        played_date VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (timestamp)
    )
    """
    cursor.execute(sql_command)
    
    # load data from pd df to the created sqlite table.
    
    try: 
        song_df.to_sql("my_played_tracks", engine, if_exists = 'append', index =  False)
    except:
        print("Data already exists in db.")
    conn.close()
    print("job done. closing sqlite connection")