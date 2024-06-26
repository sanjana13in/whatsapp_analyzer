import re
import pandas as pd

def preprocess(data):
    # Define the pattern to split data into messages and dates
    pattern = '\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2} [ap]m - '
    messages = re.split(pattern, data)[1:]  # Splitting data into messages
    dates = re.findall(pattern, data)      # Extracting dates

    # Creating a DataFrame with messages and dates
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Converting message_date to datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%y, %I:%M %p - ")
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separating users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('whatsapp notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extracting additional time-related information
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Determining the time period of the day
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df
