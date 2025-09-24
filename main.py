import streamlit as st
import pandas as pd
import json

st.markdown(
    """
    <style>
    [data-testid="stHeader"] {
        background-image: url("https://img.freepik.com/fotos-gratis/folhas-molhadas-de-monstera-deliciosa-em-um-jardim_53876-139814.jpg?semt=ais_hybrid&w=740&q=80");
        opacity: 0.9;
        background-size: cover;
        background-position: center;
        height: 70px;
        border-bottom: 1px solid #fafafa5e;
        background-repeat: no-repeat;
    }


    [data-testid="stSidebar"] {
        background-color: #080a0e;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


data_json = "dados_rotina.json"

st.write(
    '<img src="https://i.pinimg.com/236x/11/0f/59/110f59578288d703475e31c3b22ad66c.jpg" width="70" style="border-radius: 6px; margin: 5px 0px 5px 0px;" />',
    unsafe_allow_html=True,
)
st.write(
    '<div style="display: flex; flex-direction: column;"><span style="font-family: Arial; font-size: 34px; font-weight: 600; display: flex; align-items: center; gap: 10px">LifeOS <span style="font-size: 10px; font-weight: normal; margin-top: 10px;">Feito com python.</span></span></div>',
    unsafe_allow_html=True,
)
st.write(
    '<span style="color: #8f8f8f; font-family: Arial; font-size: 14px">@Gabriel</span><span style="font-size: 14px; padding-left: 5px; font-family: Arial;">Você consegue tudo com Deus.</span>',
    unsafe_allow_html=True,
)
st.write(
    '<span style="font-family: Lucida Sans; font-size: 20px; font-weight: 600;">"Never give up on your dreams...🍃"</span>',
    unsafe_allow_html=True,
)

try:
    with open(data_json, "r", encoding="utf-8") as arquivo_leitura:
        dados_existentes = json.load(arquivo_leitura)
except (IOError, json.JSONDecodeError):
    dados_existentes = []

with st.sidebar:
    adicionar_rotina = st.text_input("Adicione sua tarefa:")
    if adicionar_rotina:
        st.write(f"Tarefa '{adicionar_rotina}' adicionada")

        nova_tarefa = {"tarefa": adicionar_rotina, "concluida": "Não concluida"}
        dados_existentes.append(nova_tarefa)

        with open(data_json, "w", encoding="utf-8") as arquivo:
            json.dump(dados_existentes, arquivo, indent=4, ensure_ascii=False)

    if st.button("Board"):
        st.switch_page("pages/board.py")

    if st.button("Limpar lista"):
        with open(data_json, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo, indent=4, ensure_ascii=False)
        dados_existentes = []

if dados_existentes:
    df = pd.DataFrame(dados_existentes)
    df_editado = st.data_editor(df, num_rows="dynamic")

    if st.button("Salvar alterações"):
        with open(data_json, "w", encoding="utf-8") as arquivo:
            json.dump(
                df_editado.to_dict(orient="records"),
                arquivo,
                indent=4,
                ensure_ascii=False,
            )
        st.success("Alterações salvas com sucesso!")

    st.write("<br><br>", unsafe_allow_html=True)

    st.write(
        '<span style="font-family: Arial; font-size: 34px; font-weight: 600;">🎯 Progresso das tarefas</span>',
        unsafe_allow_html=True,
    )

    selecionar = st.multiselect("Selecione para filtrar", df["concluida"].unique())
    st.write("<br>", unsafe_allow_html=True)
    if selecionar:
        df = df[df["concluida"].isin(selecionar)]
        st.write(df)

    contagem = df["concluida"].value_counts().reset_index()
    contagem.columns = ["Status", "Quantidade"]

    st.bar_chart(contagem.set_index("Status"))

else:
    st.write("Nenhuma tarefa adicionada ainda.")
