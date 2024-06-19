import pandas as pd

# Load data from file
file_path = 'term_cooccurence_map.txt'  # Replace with the actual file path
df = pd.read_csv(file_path, delimiter='\t')

# Sort the DataFrame by the 'weight<Occurrences>' column in descending order
df_sorted = df.sort_values(by='weight<Occurrences>', ascending=False)

# Select the top 50 nodes by 'weight<Occurrences>'
top_50_nodes = df_sorted.head(50)

# Output the result
print(top_50_nodes)

# If you want to save the result to a new file
top_50_nodes.to_csv('top_50_nodes.csv', index=False)
