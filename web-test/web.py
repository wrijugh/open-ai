import streamlit as st
import dataload as dl

# Load data
df = dl.showdata()
# print(df)

# Title
st.title('Books')
st.write('This is a simple example of a data app using Streamlit. Data is loaded from CSV file.')

# Show dataframe
st.write('### List of Books')
st.write(df)
