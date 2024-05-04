import pandas as pd

df = pd.read_csv("master.csv")

unique_counts = df.nunique()

unique_counts_per_column = df.groupby('sound').nunique()
print(unique_counts_per_column["video_id"])