import os
import pandas as pd
import numpy as np

# Cleaning accountInformation.csv
accInfo = pd.read_csv('accounts/accInfoScraped.csv')

# Remove newline characters from all columns
accInfo = accInfo.replace('\n', ' ', regex=True)

# Making count values into ints
def str_to_int(x):
    if 'B' in str(x):
        return int(float(x[:-1]) * 1000000000)
    if 'M' in str(x):
        return int(float(x[:-1]) * 1000000)
    elif 'K' in str(x):
        return int(float(x[:-1]) * 1000)
    elif type(x) != str:
        return 0
    else:
        return int(float(x))
    
accInfo['author_followercount'] = accInfo['author_followers'].apply(str_to_int)
accInfo['author_likecounts'] = accInfo['author_likes'].apply(str_to_int)

accInfo = accInfo[["author_username","author_name","author_bio",
                   "author_followercount","author_likecounts"]]

accInfo.to_csv('accounts/accInfo.csv', index=False)

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
pyktok_len = len(pyktok)

pyktok["video_likecount"] = pyktok["video_diggcount"]

pyktok = pyktok[["sound", "year", "video_id", "video_timestamp", "video_duration", 
                "video_likecount", "video_commentcount", "video_sharecount", 
                "video_playcount", "video_description", "suggested_words", 
                 "author_username","video_stickers", 
                "video_is_ad", "video_locationcreated"]]

# Merging accInfo to pyktok
df = accInfo.merge(pyktok, on="author_username", how="outer").drop_duplicates()

# Organize and save as csv
df = df[["sound", "year", "video_id", "video_timestamp", "video_duration", 
         "video_likecount", "video_commentcount", "video_sharecount", 
         "video_playcount", "video_description", "suggested_words", 
         "author_username", "author_name", "author_bio", "author_followercount", 
         "author_likecounts", "video_stickers", "video_is_ad", "video_locationcreated"]]


# filtered_df = df[df['author_username'].isna() | (df['author_username'] == '')]
# print("NaN sound rows:")
# print(filtered_df["sound"].value_counts())

df = df[~df["author_username"].isna()]
df.dropna(subset=['sound'], inplace=True)

print("\naccounts.csv: ", len(accInfo), "=?", len(df["author_username"].drop_duplicates()))
print("master.csv: ", pyktok_len, "=?", len(df), "\n")

df.to_csv("master.csv", index=False)
