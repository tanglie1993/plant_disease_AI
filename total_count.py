import matplotlib.pyplot as plt
import pandas as pd
import re

# Define the file path
file_path = 'data.txt'

# Read the file
with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()

# Extract publication years using regex
publication_years = re.findall(r'PY (\d{4})', data)

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(publication_years, columns=['Year'])

# Count the number of publications per year
annual_counts = df['Year'].value_counts().sort_index()

# Print the annual count of publications
print("Annual Count of Publications:")
print(annual_counts)

# Plot the line graph
plt.figure(figsize=(10, 6))
plt.plot(annual_counts.index, annual_counts.values, marker='o', linestyle='-')
plt.title('Number of Publications per Year')
plt.xlabel('Year')
plt.ylabel('Number of Publications')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()