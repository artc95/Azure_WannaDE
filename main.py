import pandas as pd

song_names = ["Formation", "Test Drive"]
artist_names = ["Beyonce", "Ariana Grande"]
played_at = ["2021", "2020"]

song_dict = {
    "song_name": song_names,
    "artist_name": artist_names,
    "played_at": played_at
}

song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at"])
