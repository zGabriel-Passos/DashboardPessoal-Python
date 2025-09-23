import streamlit as st
import pandas as pd
import json

data_json = "dados_rotina.json"

st.write(
    '<img src="https://i.pinimg.com/236x/11/0f/59/110f59578288d703475e31c3b22ad66c.jpg" width="70" style="border-radius: 6px; margin: 5px 0px 5px 0px;" />',
    unsafe_allow_html=True,
)
st.write(
    '<span style="font-family: Arial; font-size: 34px; font-weight: 600;">- Dashboard Pessoal - Python</span>',
    unsafe_allow_html=True,
)

st.write(
    '<span style="color: #8f8f8f; font-family: Lucida sans; font-size: 14px">@Gabriel</span><span style="font-size: 14px; padding-left: 5px;">Você consegue tudo com Deus.</span>',
    unsafe_allow_html=True,
)

st.write(
    '<span style="font-family: Lucida sans; font-size: 20px; font-weight: 600;">"Never give up on your dreams"</span>',
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
    if selecionar:
        df = df[df["concluida"].isin(selecionar)]
        st.write(df)

    contagem = df["concluida"].value_counts().reset_index()
    contagem.columns = ["Status", "Quantidade"]

    st.bar_chart(contagem.set_index("Status"))

else:
    st.write("Nenhuma tarefa adicionada ainda.")
