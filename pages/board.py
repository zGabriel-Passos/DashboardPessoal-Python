import streamlit as st
import pandas as pd
import json
import os
from datetime import date

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #080a0e;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎯")
st.write(
    '<div style="display: flex; flex-direction: column;"><span style="font-family: Arial; font-size: 34px; font-weight: 600; display: flex; align-items: center; gap: 10px">Vision Board<span style="font-family: lucida sans;">- 2026</span></span></div>',
    unsafe_allow_html=True,
)
st.write("teste")


st.write("<br>", unsafe_allow_html=True)
st.subheader("Metas:")
st.markdown(
    """
- Comer saudável (low carbs, low sugar)
- Ler 2 livros
- Ir à academia 250 dias
- Estudar programação (pelo menos) todo sábado
"""
)

st.write("<br><br>", unsafe_allow_html=True)

JSON_FILE = "vision_board_log.json"


def get_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
            df = pd.DataFrame(data)
    else:
        df = pd.DataFrame(
            columns=["Day of year", "Gym", "Eat Healthy", "Read Book", "Study"]
        )
        df["Day of year"] = pd.to_datetime(df["Day of year"])
        df = df.set_index("Day of year")
    return df


df = get_data()

today = date.today().isoformat()
if today not in df.index:
    new_row = pd.DataFrame(
        [
            {
                "Day of year": today,
                "Gym": False,
                "Eat Healthy": False,
                "Read Book": False,
                "Study": False,
            }
        ]
    ).set_index("Day of year")
    df = pd.concat([df, new_row])

edited_df = st.data_editor(
    df,
    hide_index=False,
    column_config={
        "Day of year": st.column_config.DatetimeColumn(
            "Dia do ano",
            format="DD-MM-YYYY",
            disabled=True,
        ),
        "Gym": st.column_config.CheckboxColumn("Academia"),
        "Eat Healthy": st.column_config.CheckboxColumn("Comer Saudável"),
        "Read Book": st.column_config.CheckboxColumn("Ler Livro"),
        "Study": st.column_config.CheckboxColumn("Estudar programação"),
    },
    num_rows="fixed",
)

if st.button("Salvar Progresso"):
    edited_df.to_json(JSON_FILE, orient="index", date_format="iso")
    st.success("Progresso salvo com sucesso!")

st.write("---")
st.write("Última atualização: ", pd.Timestamp.now().strftime("%d/%m/%Y %H:%M:%S"))
