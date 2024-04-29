import os
import pandas as pd

# Cleaning accountInformation.csv
accInfo = pd.read_csv('accountInformation.csv')

# Remove newline characters from all columns
accInfo = accInfo.replace('\n', ' ', regex=True)

# Making count values into ints
def str_to_int(x):
    if 'B' in x:
        return int(float(x[:-1]) * 1000000000)
    if 'M' in x:
        return int(float(x[:-1]) * 1000000)
    elif 'K' in x:
        return int(float(x[:-1]) * 1000)
    else:
        return int(float(x))
    
accInfo['author_followercount'] = accInfo['author_followers'].apply(str_to_int)
accInfo['author_likecounts'] = accInfo['author_likes'].apply(str_to_int)

# accInfo.to_csv('accInfo.csv', index=False)

# Merging PykTok files together
directory = "pyktok/results"
pyktok = pd.DataFrame()

# Loop through subfolders and files
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            # Read CSV file
            filepath = os.path.join(root, file)
            sound = pd.read_csv(filepath)

            # Adding in year column
            sound["year"] = root.split('/')[2]
            sound["sound"] = file.split('_')[0]
            
            pyktok = pd.concat([pyktok, sound], ignore_index=True)

# Remove duplicates and organize
pyktok.drop_duplicates(inplace=True)

pyktok = pyktok[["sound", "year", "video_id", "video_timestamp", "video_duration", 
                "video_diggcount", "video_commentcount", "video_sharecount", 
                "video_playcount", "video_description", "suggested_words", 
                 "author_username","video_stickers", 
                "video_is_ad", "video_locationcreated"]]

# Merging accInfo to pyktok
df = accInfo.merge(pyktok, on="author_username", how="outer").drop_duplicates()

# Organize and save as csv
df = df[["sound", "year", "video_id", "video_timestamp", "video_duration", 
         "video_diggcount", "video_commentcount", "video_sharecount", 
         "video_playcount", "video_description", "suggested_words", 
         "author_username", "author_name", "author_bio", "author_followercount", 
         "author_likecounts", "video_stickers", "video_is_ad", "video_locationcreated"]]

print(len(pyktok), "=?", len(df))

df.to_csv("master.csv", index=False)
