import matplotlib.pyplot as plt
import pandas as pd
import re
from collections import defaultdict, Counter

# Define the file path
file_path = 'data.txt'

# Read the file
with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()

# Split the records
records = data.strip().split('\nER\n')
records = [record + '\nER' for record in records if record.strip()]

# Function to extract citation counts
def extract_citation_count(record):
    match = re.search(r'TC (\d+)', record)
    return int(match.group(1)) if match else 0

# Function to extract institutions
def extract_institutions(record):
    pattern = re.compile(r'C1 (.*?)\n[A-Z]', re.DOTALL)
    match = pattern.search(record + '\nA')  # Adding '\nA' to capture the last C1 block
    if match:
        institutions = set()  # Use a set to avoid counting duplicates in the same record
        lines = match.group(1).split('\n')
        for line in lines:
            if ']' in line:
                parts = line.split(']')
                for part in parts:
                    if part.find('[') < 0:
                        institution = part.split(',')[0].strip()
                        if institution:  # Ensure it's not empty
                            institutions.add(institution)
        return institutions
    return set()

# Create a dictionary to store citations for each institution
institution_citations = defaultdict(list)

# Process each record
for record in records:
    citation_count = extract_citation_count(record)
    institutions = extract_institutions(record)
    for institution in institutions:
        institution_citations[institution].append(citation_count)

# Calculate H-index for each institution
def calculate_h_index(citations):
    citations.sort(reverse=True)
    h_index = 0
    for i, citation in enumerate(citations):
        if citation >= i + 1:
            h_index = i + 1
        else:
            break
    return h_index

institution_h_indices = {institution: calculate_h_index(citations) for institution, citations in institution_citations.items()}

# Get the top 10 institutions by H-index
top_institutions = Counter(institution_h_indices).most_common(10)

# Convert to DataFrame for easier plotting
df_institutions = pd.DataFrame(top_institutions, columns=['Institution', 'H-Index'])

# Print the top 10 contributing institutions by H-Index
print("Top 10 Contributing Institutions by H-Index:")
print(df_institutions)

# Plot the bar chart
plt.figure(figsize=(12, 6))
plt.barh(df_institutions['Institution'], df_institutions['H-Index'], color='skyblue')
plt.xlabel('H-Index')
plt.title('Top 10 Contributing Institutions by H-Index')
plt.gca().invert_yaxis()  # Invert y-axis to have the highest value on top
plt.grid(axis='x')

# Show the plot
plt.tight_layout()
plt.show()
