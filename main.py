from textblob import TextBlob
from io import BytesIO
import pandas as pd
import streamlit as st
import json
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt
import os
import base64

st.set_page_config(
    page_title="Sentilyzer",
    page_icon="🧊"
)


def get(path: str):
    with open(path, 'r') as f:
        return json.load(f)


path = get('./ani.json')
doc_path = get('./doc.json')

st.title('Sentilyzer')

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
    if uploaded_file is not None:
        # Read the uploaded file
        df = pd.read_excel(uploaded_file)

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

# Documentation Page

open_docs = st.button("Open Documentation")

# Check if the button is clicked
if open_docs:
    st_lottie(doc_path)
    st.header("Abstract")

    st.write(
        "The Sentilyzer is a web-based application designed to provide users with a quick and effective way "
        "to analyze sentiments in both individual text entries and large sets of comments from social media platforms. "
        "Leveraging Natural Language Processing (NLP) techniques, the tool categorizes text into positive, negative, or "
        "neutral sentiments, offering valuable insights for businesses, marketers, and individuals seeking real-time sentiment "
        "feedback."
    )

    st.header("Key Features")

    st.write("### 1. User-Friendly Interface:")
    st.write("- The tool boasts an intuitive web interface, making it easy for users to input text for analysis or upload Excel files containing comments.")

    st.write("### 2. Real-Time Sentiment Analysis:")
    st.write("- For individual text entries, the tool instantly evaluates the sentiment, providing polarity scores and emotional categorizations (Positive, Negative, Neutral).")

    st.write("### 3. Excel File Analysis:")
    st.write("- Users can upload Excel files containing comments for batch sentiment analysis. The tool calculates sentiment scores and categorizes comments by their sentiment.")

    st.write("### 4. Visual Feedback:")
    st.write("- The tool offers visual representations of sentiment trends, allowing users to easily grasp the distribution of sentiments in their data.")

    st.write("### 5. Total Sentiment Score:")
    st.write("- In Excel file analysis, the tool calculates the total sentiment score, providing an overall assessment of the sentiment in the comments.")

    st.write("### 6. Data Privacy Compliance:")
    st.write("- The tool prioritizes ethical handling of user data and ensures compliance with data privacy regulations.")

    st.header("Technical Details")

    st.write("### Dependencies:")
    st.write("  - `streamlit`, `pandas`, `textblob`, `matplotlib`")

    st.write("### Underlying Technology:")
    st.write("  - Natural Language Processing (NLP) techniques are employed for sentiment analysis, utilizing the TextBlob library.")

    st.write("### Visualization:")
    st.write("  - Visual feedback and sentiment trends are generated using the Matplotlib library, providing users with graphical representations of sentiment data.")

    st.header("Use Cases")

    st.write("- Businesses can use this tool to monitor public sentiment towards their products or services on social media, enabling them to make data-driven decisions for marketing and customer service strategies.")

    st.write("- Marketers can quickly gauge the effectiveness of their campaigns by analyzing customer feedback in real-time.")

    st.write("- Individuals can gain insights into public sentiment on various topics by analyzing social media comments and posts.")

    st.header("Conclusion")

    st.write(
        "The Sentilyzer offers a powerful and user-friendly solution for understanding and categorizing sentiment "
        "in social media content. With its ability to provide real-time feedback and process large datasets, it serves as a "
        "valuable resource for businesses and individuals seeking to stay informed about public sentiment in the digital landscape."
    )
