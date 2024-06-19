import re
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations

# Define the file path
file_path = 'data.txt'

# Read the file
with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()

# Extract keywords using regex (assuming keywords are under 'DE' field)
keywords = re.findall(r'DE (.*)', data)
all_keywords = [kw.strip().split() for kw in keywords]
flat_keywords = [kw for sublist in all_keywords for kw in sublist]

# Standardize abbreviations and combine singular/plural forms
abbreviation_map = {
    'cnn': 'convolutional neural network',
    'rnns': 'recurrent neural network',
    'rnn': 'recurrent neural network',
    'plants': 'plant',
    'diseases': 'disease',
    # Add more mappings as needed
}

standardized_keywords = [abbreviation_map.get(kw.lower(), kw.lower()) for kw in flat_keywords]

# Recreate all_keywords with standardized keywords
all_keywords_standardized = []
for sublist in all_keywords:
    standardized_sublist = [abbreviation_map.get(kw.lower(), kw.lower()) for kw in sublist]
    all_keywords_standardized.append(standardized_sublist)

# Count keyword occurrences
keyword_counts = Counter(standardized_keywords)
top_keywords = set([kw for kw, _ in keyword_counts.most_common(50)])

# Filter co-occurrences to only include top keywords
filtered_keyword_pairs = [
    pair for sublist in all_keywords_standardized for pair in combinations(sublist, 2)
    if pair[0] in top_keywords and pair[1] in top_keywords
]
co_occurrence_counts = Counter(filtered_keyword_pairs)

# Create the network graph
G = nx.Graph()
for (kw1, kw2), count in co_occurrence_counts.items():
    G.add_edge(kw1, kw2, weight=count)

# Adjust node size based on keyword frequency with a more pronounced scaling
def scale_size(count, max_size=3000, min_size=100):
    return min_size + (max_size - min_size) * (count / max(keyword_counts.values())) ** (1/2)

node_sizes = [scale_size(keyword_counts[kw]) for kw in G.nodes()]

# Assign colors to nodes
colors = plt.cm.tab20([i % 20 for i in range(len(G.nodes()))])

# Draw the network
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, k=0.3)
weights = [G[u][v]['weight'] for u, v in G.edges()]

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=colors)

# Draw edges
nx.draw_networkx_edges(G, pos, width=[w * 0.5 for w in weights], edge_color='gray')

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')

plt.title('Keyword Co-occurrence Network')
plt.show()
