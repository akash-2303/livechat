import json
import pandas as pd

# Load both JSON files
file1_path = './wfaa_DK.json'  # Path to first file
file2_path = './WSAA_AB.json'  # Path to second file

# Load the JSON data from both files
with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
    data1 = json.load(file1)
    data2 = json.load(file2)

# Convert to DataFrames
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Merge DataFrames based on 'timestamp' and 'author' to avoid duplicates
merged_df = pd.concat([df1, df2]).drop_duplicates(subset=['timestamp', 'author'])

# Sort the DataFrame by 'timestamp' in ascending order
merged_df = merged_df.sort_values(by='timestamp', ascending=True)

# Convert the merged DataFrame back to JSON
merged_data = merged_df.to_dict(orient='records')

# Save the combined JSON to a new file
output_path = '/Users/himanshumathur/Desktop/Individual Study/livechat/Live_chat_presidential/wfaa_merged.json'
with open(output_path, 'w') as output_file:
    json.dump(merged_data, output_file, indent=4)

print(f"Combined data saved to {output_path}")
