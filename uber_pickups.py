import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC!')



DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


data_load_state = st.text('Loading data...') 
data = load_data(10000)
data_load_state.text('Loading data ...done!')

st.subheader('Raw data')
st.write(data)
st.subheader('Number of pickups by hour')
bins = [0,8,16,24]
labels = ['morning', 'afternoon', 'evening']

hours = data[DATE_COLUMN].dt.hour
categories = pd.cut(
    hours,
    bins = bins,
    labels=labels,
    right=False,
    include_lowest=True
)
hist_values = categories.value_counts(sort =False)
st.bar_chart(hist_values)
hour_to_filter = st.slider('hour',0,23,17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)
