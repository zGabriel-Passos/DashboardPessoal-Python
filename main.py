import streamlit as st
import pandas as pd
import json

data_json = "dados_rotina.json"

st.write("## Dashboard Pessoal - Python")

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

    selecionar = st.multiselect("Selecione para filtrar", df["concluida"].unique())
    if selecionar:
        df = df[df["concluida"].isin(selecionar)]
        st.write(df)

    st.subheader("Progresso das Tarefas")
    contagem = df["concluida"].value_counts().reset_index()
    contagem.columns = ["Status", "Quantidade"]

    st.bar_chart(contagem.set_index("Status"))

else:
    st.write("Nenhuma tarefa adicionada ainda.")
