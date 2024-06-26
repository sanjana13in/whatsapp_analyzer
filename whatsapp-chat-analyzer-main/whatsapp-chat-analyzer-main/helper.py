import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import emoji

import streamlit
from wordcloud import WordCloud
from urlextract import URLExtract
extract = URLExtract()

#fetching statistics
def fetch_stats(selected_user, df):

    if (selected_user != "Overall"):
        df = df[df['user'] == selected_user]

    # fetch the number of msgs
    num_messages = df.shape[0]

    # fetch the number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch the number of media msgs
    num_media_msgs = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch the number of linls shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, words, num_media_msgs, links

#finding and returning the most active users in the group
def most_active_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, df

#generating a word cloud based on the messages
def create_wordcloud(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if (selected_user != "Overall"):
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'whatsapp notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    words = pd.DataFrame(words, columns=['words'])
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(words['words'].str.cat(sep=" "))
    return df_wc

#finding and returning the most common words used
def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if (selected_user != "Overall"):
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'whatsapp notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    pure_words = []
    for message in words:
        pure_words.extend([c for c in message if c in emoji.demojize(message)])

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

#analyzing and returning the most common emojis used
def emoji_helper(selected_user, df):
    if (selected_user != "Overall"):
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c not in emoji.demojize(message)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common((len(Counter(emojis)))))
    return emoji_df

# creating a timeline of monthly message counts
def monthly_timeline(selected_user, df):
    if (selected_user != "Overall"):
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline
# creating a timeline of daily message counts
def daily_timeline(selected_user, df):
    if (selected_user != "Overall"):
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

# creating a bar chart showing the most active days of the week
def week_activity_map(selected_user, df):
    if (selected_user != "Overall"):
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

# creating a bar chart showing the most active months 
def month_activity_map(selected_user, df):
    if (selected_user != "Overall"):
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

# creating a heatmap showing the activity pattern of the selected user throughout the week
def activity_heatmap(selected_user, df):
    if (selected_user != "Overall"):
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
