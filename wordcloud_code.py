from wordcloud import WordCloud, STOPWORDS
import csv
import pandas as pd
import matplotlib.pyplot as plt
from nrclex import NRCLex
import numpy as np
import plotly.express as px
from pyplutchik import plutchik
import io
import base64

df = pd.read_csv("poem_word_df_v3.csv")
periods_df = pd.read_csv("time_periods.csv")

def get_emotions_text(text, keys):
    # Gets emotions associated to words in the review's text
    emo = NRCLex(text).raw_emotion_scores
    # Counts emotions occurrences (default is 0)
    emo = {key: int(emo[key] > 0) * 10 if key in emo else 0 for key in keys}

    return emo

def grouped_df(df, element):
    # convert to string
    df[element] = df[element].astype(str)
    df['word'] = df['word'].astype(str)
    # group by genre
    genre = df.groupby([element], as_index = False).agg({'word': ' '.join})
    #count = len(genre.index)

    return genre

def get_emo_genre(df,genre):
    """
    get emotion scores based on genre
    """
    df = grouped_df(df, 'category')
    keys = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust']
    # we want a dict < N_stars: scores of products rated N_stars >
    emo_scores = {}
    # Get texts of reviews of products rated i-star
    rslt_df = df[df['category'] == genre]
    x = [str(x) for x in rslt_df['word']]
    # Get scores
    x = x[0].split()
    scores = [get_emotions_text(t, keys) for t in x]
    #print(scores)
    emo_scores[genre] = {key: np.mean([s[key] for s in scores]) for key in keys}

    return emo_scores
def get_overall_emo(df, emotion):
    keys = [emotion]
    df = grouped_df(df, 'date')
    df.drop(df.tail(3).index,
        inplace = True)
    df['date'] = df['date'].astype('float')
    df['date'] = df['date'].astype('int')
    years = df['date'].unique()
    # we want a dict < N_stars: scores of products rated N_stars >
    emo_scores = {}
    # Get texts of reviews of products rated i-star
    for i in range(len(years)):
        year = df.loc[i]['date']
        text = df.loc[i]['word']
        # Get scores
        words = text.split()
        scores = [get_emotions_text(word, keys) for word in words]
        emo_scores[year] = np.mean([s[emotion] for s in scores])

    return emo_scores

def make_flower(df, genre):
    output = get_emo_genre(grouped_df(df, 'category'), genre)[genre]
    #print(love[])
    buf = io.BytesIO() # in-memory files
    fig = plutchik(output, title = genre)
    plt.savefig(buf, format = "png") # save to the above file object
    plt.close()
    data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
    return "data:image/png;base64,{}".format(data)

def make_line(df, emotion):
    emo_scores = get_overall_emo(df, emotion)
    emo_scores_df = pd.DataFrame(emo_scores.items(), columns=['Year', 'Value'])
    fig = px.line(emo_scores_df, x="Year", y="Value", title= emotion.capitalize() + ' over Time')
    #plt.show()
    return fig


'''

    emotion = 'fear'
    emo_scores = get_overall_emo(df, emotion)
    emo_scores_df = pd.DataFrame(emo_scores.items(), columns=['Year', 'Value'])
    print(periods_df['Period'])
    df = [dict(
        Period='Init', Start='1300', Finish='1400'),
        dict(Period='Update ', Start='1900-01-01', Finish='1950-01-01'),
        dict(Period='Production', Start='1950-01-01', Finish='2000-01-01')
    ]
    fig = px.timeline(df, x_start='Start', x_end='Finish', y='Period')
    fig.show()
'''
'''
    love = get_emotions(grouped_df(df), "Love Poems")['Love Poems']
    war = get_emotions(grouped_df(df), "Poems on Death")['Poems on Death']
    #print(love[])
    fig = plt.figure()
    plutchik(war, title = 'Death Poems')
    plt.show()
    #plutchik(war, title = 'Poems on War', title_size = 35)
'''
'''
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
'''
