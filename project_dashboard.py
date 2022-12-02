import pandas as pd
import project_sankey as proj_sk
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import re


def read_poems():
    """
    :return: convert a csv to a dataframe and change values in the century column
             Ex. 1900 --> 19th Century
    """
    century_df = pd.read_csv("century_count.csv")

    for century in century_df['century']:
        century_df['century'] = century_df['century'].replace(century, f'{str(century)[:-2]}th Century')

    word_df = pd.read_csv("poem_word.csv")
    # substitute certain values such as \r with ' '
    word_df['author'] = word_df['author'].apply(lambda x: re.sub('\s+', ' ', x))

    return century_df, word_df


def trim_count_df(df, col='century', n=5):
    """
    :param df: a poem dataframe
    :param col: a column name
    :param n: top n words for each specified column value
    :return: in the default, will return top 5 words for every century
    """
    return df.groupby(col).head(n).reset_index()


def trim_word(df, author, word_count=5):
    """
    :param df: a dataframe
    :param author: author name
    :param word_count: top n most common words for that author
    :return: a dataframe showing the top n most common words for specified author
    """
    # Keep required columns
    trim_word_df = df[["author", "word", "count"]]

    # Keep required columns, sort by count
    trim_word_df = trim_word_df[trim_word_df["author"] == author].sort_values(by=["count"], ascending=False).reset_index(drop=True)

    # Keep top n
    trim_word_df = trim_word_df.iloc[:word_count]

    return trim_word_df


century_df, word_df = read_poems()

app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Dashboard for the Evolution of Poetry",
                    style={"font-weight": "bold", "textAlign": "center"}),
            html.P("ㅤ")
        ])
    ], justify="center"),

    dbc.Row([
        dbc.Col([
            html.H4("Top n Common Words for Each Century",
                    style={"textAlign": "center"}),
            dcc.Graph(id="sankey1")
        ]),
        dbc.Col([
            html.H4("Top n Common Words for Specified Author",
                    style={"textAlign": "center"}),
            dcc.Graph(id="sankey2")
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.P("Select the number of top most common words for each century:",
                   style={"font-family": "cursive"}),
            dcc.Slider(id="most_common", min=1, max=10, step=1, value=3)
        ]),
        dbc.Col([
            html.P("Select Author:", style={"font-family": "cursive"}),
            dcc.Dropdown(id="author_name", options=word_df['author'].unique(), value='Thomas Dunn English (1819-1902)'),
            html.P("ㅤ"),
            html.P("Select the number of top most common words for the author:",
                   style={"font-family": "cursive"}),
            dcc.Slider(id="author_wc", min=1, max=10, step=1, value=5)
        ])
    ])
], fluid=True)


@app.callback(
    Output("sankey1", "figure"),
    Output("sankey2", "figure"),
    Input("most_common", "value"),
    Input("author_name", "value"),
    Input("author_wc", "value")
)
def update_graphs(most_common, author_name, author_wc):

    # sankey diagram 1
    local1 = trim_count_df(century_df, 'century', most_common)
    fig1 = proj_sk.make_sankey(local1, 'century', 'word', 'count', pad=50, thickness=40, line_width=1, opacity=0.6)

    # sankey diagram 2
    local2 = trim_word(word_df, author_name, author_wc)
    fig2 = proj_sk.make_sankey(local2, 'word', 'author', 'count', pad=50, thickness=40, line_width=1, opacity=0.6)

    return fig1, fig2


app.run_server(debug=True)
