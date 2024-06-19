import matplotlib.pyplot as plt
import pandas as pd
import re
from collections import defaultdict

# Define the file path
file_path = 'data.txt'

# Function to extract corresponding authors and their citations
def extract_corresponding_authors(data):
    author_citation_dict = defaultdict(int)
    
    # Split the data into individual records
    records = data.split('ER\n')
    
    for record in records:
        # Extract the times cited
        times_cited_match = re.search(r'\bTC (\d+)', record)
        if times_cited_match:
            tc = int(times_cited_match.group(1))
            
            # Extract the corresponding authors
            corresponding_authors = re.findall(r'RP ([\w\s,.]*?)\s*\(通讯作者\)', record)
            for author_entry in corresponding_authors:
                author_name = author_entry  # Take only the name part before the comma
                if author_name.find('Pang') >= 0:
                    print(times_cited_match)
                author_citation_dict[author_name] += tc
    
    return author_citation_dict

# Read the file
with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()

# Extract corresponding authors and their citations
author_citation_dict = extract_corresponding_authors(data)

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(list(author_citation_dict.items()), columns=['Author', 'TimesCited'])

# Get the top 10 cited authors
top_authors = df.nlargest(10, 'TimesCited')

# Plot the bar chart
plt.figure(figsize=(12, 8))
plt.barh(top_authors['Author'], top_authors['TimesCited'], color='skyblue')
plt.xlabel('Times Cited')
plt.ylabel('Author')
plt.title('Top 10 Cited Corresponding Authors')
plt.gca().invert_yaxis()  # Invert y-axis to have the highest on top
plt.tight_layout()

# Show the plot
plt.show()
