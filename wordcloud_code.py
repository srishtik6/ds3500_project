from wordcloud import WordCloud, STOPWORDS
import csv
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("poem_word_df_v3.csv")
df['category'] = df['category'].astype(str)
df['word'] = df['word'].astype(str)

genre = df.groupby(['category'], as_index = False).agg({'word': ' '.join})
count = len(genre.index)
fig = plt.figure()

for i in range(count):
    # configure figure
    ax = fig.add_subplot(5,5,i+1)
    text = genre.word[i]
    # Create and generate a word cloud image:
    cloud = WordCloud(max_words=40, stopwords = STOPWORDS, background_color="black").generate(text)
    ax.set_title(genre.category[i])
    ax.imshow(cloud)
    ax.axis('off')

plt.show()

