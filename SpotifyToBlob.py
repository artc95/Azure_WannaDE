### DO BEFORE RUNNING CODE!!!
### in cmd, run "pip install azure-storage-blob" to install Azure Blob Storage client library for Python package
### in cmd, run "setx AZURE_STORAGE_CONNECTION_STRING "<yourconnectionstring>" to set environment variable
### (details https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python)

import datetime
import json
import requests
import pandas as pd

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

#--------SET TIMESTAMPS--------#
datetime_now = datetime.datetime.now().strftime("%d%b%Y,%H%M") # current datetime
after = datetime.datetime.now() - datetime.timedelta(days=5) # set "after" timestamp i.e. for songs played after this timestamp

#--------REQEUST RECENTLY PLAYED FROM SPOTIFY--------#
TOKEN = "BQDKVlRmqmCivi__zPeAp1PcQLsMgudcqKMTttw2aGRaLm7227xjWHa1NwYvGWjdFNEGUXY0cCp-XonRIxPskPsFrti2vowaC36F-Sx9SS6MVhTPGZ_w5NahaCCfxXUPkffwf93tHJe7Ai1KGMdqcKi9-ob_JdWMybz9L7PBx945OynDaOR_AA"

headers = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "Authorization" : "Bearer {token}".format(token = TOKEN)
    }

after_unix = int(after.timestamp()) * 1000 #convert unix in seconds to milliseconds for spotify

r = requests.get("https://api.spotify.com/v1/me/player/recently-played?&after={time}".format(time=after_unix), headers=headers)
data = r.json()

#--------CREATE SONG_DICT, SONG_DF--------#
song_names = []
artist_names = []
played_at = []

for song in data["items"]:
    song_names.append(song["track"]["name"])
    artist_names.append(song["track"]["album"]["artists"][0]["name"])
    played_at.append(song["played_at"])

song_dict = {
    "song_name": song_names,
    "artist_name": artist_names,
    "played_at": played_at
}

song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at"])

#--------SAVE SONG_DF AS RECENTPLAY.CSV--------#

# save df as csv
csv_name = "recentplay_{}.csv".format(datetime_now)
csv_file = song_df.to_csv(csv_name)

#--------STORE RECENTPLAY.CSV AS AZURE BLOB--------#

try:
	connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
	print(connect_str)

	# create BlobServiceClient object , used to create container client
	blob_service_client = BlobServiceClient.from_connection_string(connect_str)

	# create unique name for container, then create container
	# container_name = str(uuid.uuid4())
	# container_client = blob_service_client.create_container(container_name)

	# create blob client
	blob_client = blob_service_client.get_blob_client(container = "recentplay", blob = csv_name)

	print("Uploading blob " + csv_name)

	with open("./" + csv_name, "rb") as data:
		blob_client.upload_blob(data)

except Exception as ex:
	print("Exception:")
	print(ex)
