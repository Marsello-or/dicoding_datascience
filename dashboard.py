import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_style(style='dark')

def create_daily_rent_df(df):
    daily_rent_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    daily_rent_df = daily_rent_df.reset_index()
    daily_rent_df.rename(columns={
        "instant": "order_count",
        "cnt": "total_rent"
    }, inplace=True)
    
    return daily_rent_df

def create_weathersit_cnt_df(df):
    weathersit_cnt_df = df.groupby('weathersit')['cnt'].sum().reset_index()
    weathersit_cnt_df.columns = ['weathersit', 'total_cnt']

    return weathersit_cnt_df


def create_weekday_weekend_df(df):
    weekday_weekend_df = all_df.groupby('workingday')['cnt'].sum().reset_index()
    weekday_weekend_df.columns = ['workingday', 'total_cnt']
    
    return weekday_weekend_df

def create_holiday_df(df):
    holiday_df = all_df.groupby('holiday')['cnt'].sum().reset_index()
    holiday_df.columns = ['holiday', 'total_cnt']

    return holiday_df

def create_temp_cnt_df(df):
    temp_cnt_df = all_df[['temp','cnt','dteday']]
    filtered_df = temp_cnt_df[temp_cnt_df['dteday'] == '2011-01-01']
    temp_cnt_df = filtered_df.iloc[:30]

    return temp_cnt_df

def create_atemp_cnt_df(df):
    atemp_cnt_df = all_df[['atemp','cnt','dteday']]
    filtered_df = atemp_cnt_df[atemp_cnt_df['dteday'] == '2011-01-01']
    atemp_cnt_df = filtered_df.iloc[:30]
    
    return atemp_cnt_df

def create_season_df(df):
    season_df = all_df.groupby('season', as_index=False)['cnt'].sum()

    return season_df

all_df = pd.read_csv("main_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    st.image("https://cdn.pixabay.com/photo/2017/01/31/23/42/animal-2028258_640.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

daily_rent_df = create_daily_rent_df(main_df)
weathersit_cnt_df = create_weathersit_cnt_df(main_df)
weekday_weekend_df = create_weekday_weekend_df(main_df)
holiday_df = create_holiday_df(main_df)
temp_cnt_df = create_temp_cnt_df(main_df)
atemp_cnt_df = create_atemp_cnt_df(main_df)
season_df = create_season_df(main_df)

st.header('Bike Sharing Dashboard :smile:')

total_rent = daily_rent_df.total_rent.sum()
st.metric("Timeline Rental Count", value=total_rent)

weather_mapping = {1: 'clear', 2: 'cloudy', 3: 'raining', 4: 'storm'}
weathersit_cnt_df['weathersit'] = weathersit_cnt_df['weathersit'].map(weather_mapping)

st.subheader('Banyaknya jumlah penyewaan berdasarkan cuaca')
plt.figure(figsize=(20, 6))
barplot = sns.barplot(x='total_cnt', y='weathersit', data=weathersit_cnt_df, orient='h')

for index, value in enumerate(weathersit_cnt_df['total_cnt']):
    barplot.text(value, index, f'{value}', va='center')

plt.xlabel('Total Count')
plt.ylabel('Weather Situation')
plt.title('Total Count by Weather Situation')
st.pyplot(plt)

st.subheader('Perbandingan Total Rental antara Weekdays dan Weekends')
weekday_weekend_df = all_df.groupby('workingday')['cnt'].sum().reset_index()
weekday_weekend_df.columns = ['workingday', 'total_cnt']

week_mapping = {1: 'Weekdays', 0: 'Weekends'}
weekday_weekend_df['workingday'] = weekday_weekend_df['workingday'].map(week_mapping)

plt.figure(figsize=(2, 2))
plt.pie(weekday_weekend_df['total_cnt'], labels=weekday_weekend_df['workingday'], autopct='%1.1f%%', startangle=140)
plt.axis('equal')
st.pyplot(plt)

holiday_df = all_df.groupby('holiday')['cnt'].sum().reset_index()
holiday_df.columns = ['holiday', 'total_cnt']
holiday_df.head()

st.subheader('Total Rental Berdasarkan Hari Libur')
holiday_mapping = {1: 'Holiday', 0: 'Not Holiday'}
holiday_df['holiday'] = holiday_df['holiday'].map(holiday_mapping)

fig, ax = plt.subplots(figsize=(6, 4))  

wedges, texts, autotexts = ax.pie(
    holiday_df['total_cnt'], 
    labels=holiday_df['holiday'], 
    autopct='%1.1f%%', 
    startangle=140, 
    textprops={'fontsize': 11}  
)

for text in texts:
    text.set_fontsize(11) 

for autotext in autotexts:
    autotext.set_fontsize(11) 

ax.axis('equal')  
st.pyplot(fig)
plt.clf()

st.subheader('Dampak dari Temperatur terhadap Jumlah Rental pada Bulan Januari')
col1, col2 = st.columns(2)
 
with col1:
    plt.figure(figsize=(8, 6))
    sns.regplot(x='temp', y='cnt', data=temp_cnt_df)
    plt.title('Dampak dari temperatur terhadap jumlah penyewa saat Januari')
    st.pyplot(plt)
    plt.clf()
 
with col2:
    plt.figure(figsize=(8, 6))
    sns.regplot(x='atemp', y='cnt', data=atemp_cnt_df)
    plt.title('Dampak dari temperature yang dirasakan terhadap jumlah penyewa saat Januari')
    st.pyplot(plt)
    plt.clf()

st.caption('Hubungan regresi antara temperatur dan jumlah penyewaan berbanding lurus membuktikan bahwa orang-orang akan menyewa sepeda apabila suhunya semakin hangat. Hal ini berlaku, baik berdasarkan data temperatur secara real dan juga berdasarkan data temperatur yang dirasakan secara subjektif')

season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
season_df['season_name'] = season_df['season'].map(season_mapping)

st.subheader('Perbandingan Penggunaan Rental Sepeda di Antara 4 Musim')
plt.figure(figsize=(6, 4))
sns.barplot(x='season_name', y='cnt', data=season_df)
plt.title('Dampak dari musim terhadap jumlah penyewa')
plt.xlabel('Season')
plt.ylabel('Count')
plt.xticks(rotation=0)
st.pyplot(plt)
plt.clf()

st.caption('Copyright (c) Marsello Ormanda 2023')



