import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import datetime
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

st.set_option('deprecation.showPyplotGlobalUse', False)

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]

skey = st.secrets["gcp_service_account"]
credentials = Credentials.from_service_account_info(
    skey,
    scopes=scopes,
)
client = gspread.authorize(credentials)



# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=60)
def load_data(url, sheet_name):
    sh = client.open_by_key(url)
    worksheet = sh.get_worksheet(0)
    # Recupere os dados do Google Sheets em um DataFrame do pandas
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    return df
@st.cache_data(ttl=60)
def send_data(url, sheet_name, nome, idade, attendance, tstamp):
    sh = client.open_by_key(url)
    worksheet = sh.get_worksheet(0)
    # Recupere os dados do Google Sheets em um DataFrame do pandas
    #row = ["Erika", "fish"]
    df = pd.DataFrame([[nome, int(idade),attendance, tstamp]])
    df_values = df.values.tolist()
    sh.values_append('data', {'valueInputOption': 'RAW'}, {'values': df_values})

    return 
# Print results.

url = "121dX2d0j51lOYaKXM-vtW0bfYsUEtMU5bY9Lyy8x_F8"
sheet = "data"
df = load_data(url, sheet)
#df.time = datetime.datetime.strptime(df.time, "%Y-%m-%d")
df.time = pd.to_datetime(df['time'], format="%Y-%m-%d")

date = st.sidebar.date_input(

     "Select Confirmation Date Range",

    (datetime.date(2023, 7, 1),datetime.date(2023,7,30)))

st.write(date)
start_date =  pd.to_datetime(date[0], format="%Y-%m-%d")
end=pd.to_datetime(date[1], format="%Y-%m-%d")
print("arroz")
print(type(start_date))
print(type(df.time))


#data = df.loc[start_date:end]
data = df.loc[(df['time'] > start_date) & (df['time'] <end)]

# Crie um histograma
plt.title('Distribuição por idade')

# plt.hist(data_on, bins = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65])
# plt.hist(data_pre, bins = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65])
# Exiba o gráfico no Streamlit
sns.histplot(data, x = "idade", hue = "attendance", binwidth=3, shrink=.8, multiple="dodge")
st.pyplot()

perc = df['attendance'].value_counts(normalize = True) * 100
st.bar_chart(perc)

m = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(m)



with st.form('form1', clear_on_submit = True):
    nome= st.text_input("Nome")
    idade= st.text_input("Idade")
    now = datetime.date.today()
    attendance = st.radio(
    "Você está participando",
    ('Online', 'Presencial'))


    submitted = st.form_submit_button("Submit")
    if submitted:
        send_data(url, sheet, nome, idade, attendance, str(now))



