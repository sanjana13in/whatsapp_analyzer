#importing required packages

import streamlit as st #for frontend
import matplotlib.pyplot as plt #for charts
import preprocessor, helper #for preprocessing & displaying the chats
import seaborn as sns #for charts

#setting of basic frontend using streamlit
st.set_page_config(page_title='WhatsApp Chat Analyzer ',layout='wide', initial_sidebar_state='expanded')
st.sidebar.title('WhatsApp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader('Upload a WhatsApp Chat File:')

#it reads the file, decodes the bytes to a UTF-8 string, and preprocesses the data using the preprocessor module.
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist() #fetching the unique users from the preprocessed data
    #removing the "whatsapp notification" user (if present), sorts the user list, and inserts "Overall" as the first option
    for user in user_list:
        if user == 'whatsapp notification':
            user_list.remove('whatsapp notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis w.r.t:", user_list)

    # fetching statistics like total messages, total words, media shared, and links shared based on the selection
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_msgs, links = helper.fetch_stats(selected_user, df)

        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(len(words))

        with col3:
            st.header("Media Shared")
            st.title(num_media_msgs)

        with col4:
            st.header("Links Shared")
            st.title(len(links))
            
        

        # displaying the monthly timeline of messages
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # displaying the daily timeline of messages
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # displaying the most busy days and months
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Days")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Months")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # displaying the weekly activity
        st.title('Weekly Activity Map')
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # for overall selection --> finding the most active users in a group
        if selected_user == 'Overall':
            st.title("Most Active Users")
            x, new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # displaying the word cloud of the selected user's messages.
        st.title('Wordcloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # displaying the most common words used by the selected user.
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='red')
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        # analyzing and displaying the most common emojis used by the selected user
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        if emoji_df.empty is True:
            st.header("No Emojis Used")

        else:
            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)

            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
                st.pyplot(fig)
