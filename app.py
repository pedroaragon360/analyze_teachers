import streamlit as st

import requests
import pandas as pd
from io import BytesIO
import openpyxl


# URL of the Excel file
url = st.secrets["url"]

# Fetch the file
response = requests.get(url)
response.raise_for_status()  # This will raise an error if the download failed

# Read the file into a pandas DataFrame
file = BytesIO(response.content)
df = pd.read_csv(file)

def search(val):
    # PALABRA CLAVE A BUSCAR
    keyword = val

    # Filter to include only records containing 'marketing' in 'nombreSesion'
    data_df = df[df['nombreSesion'].str.contains(keyword, na=False, case=False)]

    # Group by 'Profesor' and calculate the mean of 'media' for each group
    grouped = data_df.groupby('Profesor')

    # Filter to include only those groups with at least 10 entries
    filtered_grouped = grouped.filter(lambda x: len(x) >= 1)

    # Calculate the mean of 'media' for each group in the filtered DataFrame
    grouped_df = filtered_grouped.groupby('Profesor')['media'].agg(['mean', 'count'])

    # Sort the DataFrame in descending order by 'media'
    st.table(grouped_df.sort_values(by='mean',ascending=False))

st.set_page_config(layout="wide")

with st.form("my_form"):
   st.title("Buscar profesores")
   title = st.text_input('Nombre de sesión', 'analitica|analytics')
   submitted = st.form_submit_button("Buscar")
if submitted:
    search(title)

