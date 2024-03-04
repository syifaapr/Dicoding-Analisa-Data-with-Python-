#import library
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set(style='dark')

#dashboard
st.title('Bike Sharing Dataset')


#import dataset
dataframe = pd.read_csv("data_sepeda.csv")
dataframe.head()

#menampilkan dataset
show_data = st.checkbox("Menampilkan dataset", False)
if show_data:
    st.dataframe(dataframe)

#rental
def create_rental_dataframe(dataframe):
    if 'cnt_day' in dataframe.columns:
        rental_dataframe = dataframe.groupby(by='dteday').agg({
            'cnt_day': 'sum'
        }).reset_index()
        return rental_dataframe
    else:
        st.warning("The 'count' column does not exist in the DataFrame.")
        return pd.DataFrame()


def create_weather_dataframe(dataframe):
    if 'cnt_day' in dataframe.columns:
        weather_dataframe = dataframe.groupby(by='dteday').agg({
            'cnt_day': 'sum'
        }).reset_index()
        return weather_dataframe
    else:
        st.warning("The 'count' column does not exist in the DataFrame.")
        return pd.DataFrame()


#sidebar
min_date = pd.to_datetime(dataframe['dteday']).dt.date.min()
max_date = pd.to_datetime(dataframe['dteday']).dt.date.max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label = 'Time',
        min_value = min_date,
        max_value = max_date,
        value = [min_date, max_date]
    )

main_dataframe = dataframe[(dataframe['dteday'] >= str(start_date))&
                           (dataframe['dteday'] <= str(end_date))]

rental_dataframe = create_rental_dataframe(main_dataframe)
weather_dataframe = create_weather_dataframe(main_dataframe)


#visualisasi data
st.subheader("Histogram Jumlah Sewa per Jam")
plt.figure(figsize=(12,10))
plt.hist(dataframe['hr'], bins=24, edgecolor='purple')
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()

st.subheader("Diagram Batang Jumlah Sewa Tertinggi")
daily_count = dataframe.groupby('weekday_day')['cnt_day'].sum()
plt.figure(figsize=(12,10))
daily_count.sort_values(ascending=False).plot(kind='bar', edgecolor='red')
st.pyplot()


st.subheader('Sewa')
fig, ax = plt.subplots(figsize=(12,10))
ax.plot(
    rental_dataframe.index,
    rental_dataframe['cnt_day'],
    marker = 'o',
    linewidth = 2,
    color = 'tab:green'
)
for index, row in enumerate(rental_dataframe['cnt_day']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot()

st.subheader('Sewa per Cuaca')
fig, ax = plt.subplots(figsize=(10, 12))

colors=["tab:blue", "tab:orange", "tab:green"]

sns.barplot(
    x=weather_dataframe.index,
    y=weather_dataframe['cnt_day'],
    palette=colors,
    ax=ax
)

for index, row in enumerate(weather_dataframe['cnt_day']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

st.subheader("Rerata Sewa per Jam")
rental_hour = dataframe.groupby('hr')['cnt_hour'].mean()
fig, ax = plt.subplots(figsize=(10, 12))
ax.bar(rental_hour.index, rental_hour.values, color='#556B2F')
plt.title('Rerata Sewa per Jam')
plt.xlabel('Jam')
plt.ylabel('Rerata Sewa')
st.pyplot(fig)


st.subheader("Rerata Sewa Berdasarkan Kondisi Cuaca")
average_weather = dataframe.groupby('weather_label')['cnt_day'].mean().reset_index().sort_values("cnt_day")
fig, ax = plt.subplots(figsize=(12, 10))
sns.barplot(x='cnt_day', y='weather_label', data=average_weather, palette='mako')
sns.color_palette("rocket_r", as_cmap=True)

plt.title('Average rental bicycle based weather conditions')
plt.xlabel('Average rental')
plt.ylabel('Weather conditions')

st.pyplot(fig)

st.write('The weather conditions and the average number of rentals are closely related, as shown in the graph above. on average, the most rental occur during "jernih" weather and the fewest during "Hujan ringan".')

st.subheader("Conclusion")

st.write('1. On average, most bike rentals are made in the morning and evening. 08.00 oclock is the time when people generally start work, and at this time many people use bicycles as a means of transportation to get to work or school. The increase in bicycle rentals at this time reflects the need for morning transportation.')

st.write('2. Sunny weather tends to create more comfort conditions for outdoor activities such as cycling. People are more likely to ride on sunny days because rain or bad weather does not prevent them from continuing their activities. Cycling is often associated with hobby and recreation, and interest in cycling increases when the weather is sunny.')

st.caption('Copyright (c) Syifa Apriyani 2024')
