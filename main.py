from textblob import TextBlob
from io import BytesIO
import pandas as pd
import streamlit as st
import json
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="Sentiment Analysis Tool",
    page_icon="🧊"
)


def get(path: str):
    with open(path, 'r') as f:
        return json.load(f)


path = get('./ani.json')
# Set NLTK data source


os.environ['NLTK_DATA'] = 'https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/'

st.title('Sentiment Analysis Tool')

# Analyze Text Section
with st.expander('Check whether Your post is positive or negative '):
    text = st.text_input('Post here: ')
    if text:
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity

        if sentiment_score > 0.2:
            emotion = 'Positive'
        elif sentiment_score < -0.2:
            emotion = 'Negative'
        else:
            emotion = 'Neutral'
        st.write('Polarity: ', round(blob.sentiment.polarity, 2))
        st.write('Emotion:  ', emotion)
    # Analyze Excel File Section
with st.expander('Analyze Comments Excel File'):
    upl = st.file_uploader('Upload file')


    def score(x):
        blob1 = TextBlob(x)
        return blob1.sentiment.polarity


    def analyze(x):
        if x >= 0.5:
            return 'Positive'
        elif x <= -0.5:
            return 'Negative'
        else:
            return 'Neutral'


    if upl:
        df = pd.read_excel(upl)
        df['score'] = df['comments'].apply(score)
        df['analysis'] = df['score'].apply(analyze)
        st.write(df.head(100))
        total_score = df['score'].sum()
        st.write('Total Score: ', round(total_score, 2))

        if total_score < 0:
            total_sentiment = 'Negative'
        elif total_score == 0:
            total_sentiment = 'Neutral'
        else:
            total_sentiment = 'Positive'

        st.write(f'Total Sentiment: {total_sentiment}')


        @st.cache_data
        def convert_df(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
            return output.getvalue()


        xlsx = convert_df(df)

        st.download_button(
            label="Download data as Excel",
            data=xlsx,
            file_name='sentiment.xlsx',
            key='xlsx'
        )
with st.expander('Visualize your excel '):
    uploaded_file = st.file_uploader("Choose an Excel file...", type=["xlsx"])


    # Sentiment Analysis Function
    def analyze_sentiment(df):
        # Your sentiment analysis code here
        # For example, let's assume you have a 'comments' column
        df['score'] = df['comments'].apply(score)
        df['analysis'] = df['score'].apply(analyze)
        return df


    if uploaded_file is not None:
        # Read the uploaded file
        df = pd.read_excel(uploaded_file)

        # Perform Sentiment Analysis
        df = analyze_sentiment(df)

        # Display Sentiment Analysis Results
        st.write(df)

        # Visualize sentiment analysis results
        sentiment_counts = df['analysis'].value_counts()
        colors = ['blue', 'green', 'red']
        fig, ax = plt.subplots()
        ax.bar(sentiment_counts.index, sentiment_counts.values, color=colors)
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Count')
        ax.set_title('Sentiment Analysis')

        st.pyplot(fig)
st_lottie(path)