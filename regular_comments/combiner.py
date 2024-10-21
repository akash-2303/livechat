import pandas as pd
import json
import os

# List of JSON files (one for each news network)
json_files = [
    './nbc_comments.json', 
    './wfaa_comments.json', 
    './wfla_comments.json', 
    './timWalz_comments.json', 
    './kamala_harris.json', 
    './faceTheNation_comments.json', 
    './cnbctv18_comments.json', 
    './associatedPress_comments.json'
]
  # Add your actual file names

# List to store data from all networks
all_comments = []

# Iterate over each file and load the comments
for file in json_files:
    with open(file, 'r') as f:
        comments_data = json.load(f)
        all_comments.extend(comments_data)  # Append comments to the list

# Convert the list of comments to a pandas DataFrame
df_all_comments = pd.DataFrame(all_comments)

# Display or check the combined data
# print(df_all_comments)
df_all_comments.to_json('VP_comments_combined.json', orient='records', indent=4)