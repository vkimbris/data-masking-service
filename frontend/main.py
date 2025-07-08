import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="admin-masking",
    page_icon="🌶️",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Админ-панель сервиса Маскирования")


vocabulary_name = st.selectbox(label="Словарь", options=["NAME", "MIDNAME", "SURNAME"])


df = pd.DataFrame({
    "name": ["1", "2", "3", "4"],
})

edited_df = st.data_editor(df, num_rows="dynamic", column_config={
    "name": st.column_config.TextColumn("Name")
})