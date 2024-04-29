import os
import pandas as pd

# Define the directory containing the CSV files
directory = "results"

# Initialize an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Loop through subfolders and files
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            # Read CSV file
            filepath = os.path.join(root, file)
            df = pd.read_csv(filepath)
            
            # Extract 'author_username' column
            if 'author_username' in df.columns:
                df = df[['author_username']]
                
                # Append to combined_data DataFrame
                combined_data = pd.concat([combined_data, df], ignore_index=True)

# Remove duplicates
combined_data.drop_duplicates(inplace=True)

# Write the combined data to a new CSV file
combined_data.to_csv("accounts.csv", index=False)
