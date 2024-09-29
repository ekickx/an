import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Initialize function that will create df
def create_monthpm_df(df):
    monthpm_df = df.groupby(['month', 'month_name', 'year'])['PM2.5'].mean()
    monthpm_df = monthpm_df.reset_index(name='mean').pivot(columns='year', index=['month', 'month_name'], values='mean')

    return monthpm_df

def create_month_mean(df):
    month_mean = df.resample(rule='M', on='date')['PM2.5'].mean()
    month_mean.index = month_mean.index.strftime('%B')
    month_mean = month_mean.reset_index()
    month_mean.columns = ['month', 'PM2.5']

    return month_mean

df = pd.read_csv('https://github.com/ekickx/an/raw/refs/heads/main/dashboard/df_0.csv')
df['date'] = pd.to_datetime(df['date'])

# Prepare df
trendpm_df = df.groupby("date")["PM2.5"].mean().reset_index()
yearpm_df = df.groupby('year')['PM2.5'].mean().reset_index()
monthpm_df = create_monthpm_df(df)
month_mean = create_month_mean(df)
wdpm_df = df.groupby('wd')['PM2.5'].mean().reset_index()

st.header('Analisis Data Air Quality')
fig, ax = plt.subplots(figsize=(22,5))
plt.plot(trendpm_df['date'], trendpm_df['PM2.5'])
plt.title('Average PM 2.5 from 2013-03 to 2017-02', fontsize=30)
st.pyplot(fig)

# PM 2.5 per Year
st.subheader('Average per Year')
fig, ax = plt.subplots(figsize=(10,5))
plt.title('Average PM 2.5 per Year', fontsize=20)
sns.barplot(data=yearpm_df, x='year', y='PM2.5', ax=ax)
st.pyplot(fig)

# PM 2.5 per Month
st.subheader('Average per Month')

fig, ax = plt.subplots(figsize=(8, 8))
plt.title('Heatmap of Average PM 2.5 per Month for each year', fontsize=15)
sns.heatmap(monthpm_df, annot=True, fmt='.3g', ax=ax)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 5))
plt.title('Average PM 2.5 per Month', fontsize=20)
sns.barplot(y='month', x='PM2.5', data=month_mean, ax=ax)
st.pyplot(fig)

# PM 2.5 & Weather
st.subheader('Correlation with Weather/Environment')
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(20,10))

plt.suptitle('Correlation between PM 2.5 level and Weather/Environment', fontsize=30)
for k, v in enumerate(['RAIN', 'TEMP', 'PRES', 'DEWP']):
  sns.regplot(x=v, y='PM2.5', data=df, ax=ax[k%4//2, k%2])
  ax[k%4//2, k%2].set_title('Correlation of PM2.5 & '+v)
st.pyplot(fig)

# PM 2.5 & Wind Direction
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18,7))
plt.suptitle('Wind Direction & PM 2.5 Level', fontsize=30)

sns.barplot(x='wd', y='PM2.5', data=wdpm_df.sort_values(by='PM2.5', ascending=False).head(), ax=ax[0])
ax[0].set_title('Wind Direction with Highest PM 2.5', fontsize=20)
sns.barplot(x='wd', y='PM2.5', data=wdpm_df.sort_values(by='PM2.5').head(), ax=ax[1])
ax[1].set_title('Wind Direction with Lowest PM 2.5', fontsize=20)
st.pyplot(fig)
