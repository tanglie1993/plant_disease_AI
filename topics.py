import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download the stopwords corpus
nltk.download('punkt')
nltk.download('stopwords')

# Define the file path
file_path = 'data.txt'

# Read the file
with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()

# Split data into individual records
records = data.split('ER\n')

# Extract relevant fields from each record
def extract_field(pattern, record):
    match = re.search(pattern, record)
    return match.group(1).strip() if match else None

records_data = []
for record in records:
    title = extract_field(r'TI (.+)', record)
    abstract = extract_field(r'AB (.+)', record)
    keywords = extract_field(r'DE (.+)', record)
    year = extract_field(r'PY (\d{4})', record)
    if title and abstract and keywords and year:
        combined_text = title + ' ' + abstract + ' ' + keywords
        records_data.append([combined_text, year])

# Create a DataFrame
df = pd.DataFrame(records_data, columns=['Text', 'Year'])

# Preprocess text data
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = re.sub(r'\b\w{1,2}\b', '', text)  # Remove short words
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = text.lower()  # Convert to lowercase
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalnum()]  # Remove non-alphanumeric tokens
    tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords
    text = ' '.join(tokens)
    return text

df['Text'] = df['Text'].apply(preprocess_text)

# Vectorize text data using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.95, min_df=2, ngram_range=(1, 3))
text_matrix = vectorizer.fit_transform(df['Text'])

# Apply LDA
num_topics = 5  # Adjusted number of topics
lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
lda.fit(text_matrix)

# Display the top words for each topic
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print(f"Topic {topic_idx}:")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))

no_top_words = 10
display_topics(lda, vectorizer.get_feature_names_out(), no_top_words)

# Assign topics to documents
df['Topic'] = lda.transform(text_matrix).argmax(axis=1)

# Analyze topic trends over time
topic_trends = df.groupby(['Year', 'Topic']).size().unstack().fillna(0)
topic_trends.plot(kind='line', figsize=(12, 8))
plt.title('Topic Trends Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Publications')
plt.legend(title='Topic')
plt.grid(True)
plt.tight_layout()
plt.show()

# Print the annual count of publications
annual_counts = df['Year'].value_counts().sort_index()
print("Annual Count of Publications:")
print(annual_counts)
