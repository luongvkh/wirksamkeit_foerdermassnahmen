import streamlit as st

st.set_page_config(page_title="Maßnahmenwirksamkeit", page_icon=":material/content_paste_search:", layout="wide")

pages = [
    st.Page(
        "pages/01_Startseite.py",
        title="Startseite",
        icon=":material/home:",
        default=True,
    ),
    st.Page(
        "pages/02_Massnahmenwirksamkeit.py",
        title="Maßnahmenwirksamkeit",
        icon=":material/bar_chart:",
    ),
]

pg = st.navigation(pages)
pg.run()
