from consumer.app.kafka_consumer import read_news
import pandas as pd
def convert_to_df(topic, num):
    a = read_news(topic,num)
    first_message = a[0]['message']
    df = pd.DataFrame([first_message])
    return df


