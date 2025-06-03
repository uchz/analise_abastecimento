import streamlit as st
import pandas as pd
import altair as alt

# --- Carregar dados ---
df = pd.read_excel('ABASTECIMENTOS.xlsx')

# --- Função para definir Setor ---
def setor(rua):
    if 1 <= rua <= 12:
        return 'Varejo'
    elif 13 <= rua <= 36:
        return 'Volumoso'
    else:
        return 'Confinado'

# --- Pré-processamento ---
df['Rua'] = df['End. Destino'].str.split('.').str[1].str.replace('CO', '', regex=False)
df = df[df['Rua'].notnull()]
df = df[df['Rua'].str.strip() != '']
df['Rua'] = df['Rua'].astype(int)
df['Setor'] = df['Rua'].apply(setor)

df['Data Inicial'] = pd.to_datetime(df['Data Inicial'], format="%d/%m/%Y %H:%M:%S")
df['Data Final'] = pd.to_datetime(df['Data Final'], format="%d/%m/%Y %H:%M:%S")
df['Temp.Abastecimento'] = (df['Data Final'] - df['Data Inicial']).dt.total_seconds() / 60

# --- Filtros ---
st.sidebar.header("🔍 Filtros")

# Filtro Setor
setores = ['Todos'] + df['Setor'].unique().tolist()
setor_selecionado = st.sidebar.selectbox("Selecione o Setor", setores)

# Filtro Data
data_min = df['Data Inicial'].min().date()
data_max = df['Data Final'].max().date()

data_inicio = st.sidebar.date_input("Data Inicial", data_min)
data_fim = st.sidebar.date_input("Data Final", data_max)

# Filtro Usuário
usuarios = ['Todos'] + sorted(df['Úsuario'].unique().tolist())
usuario_selecionado = st.sidebar.selectbox("Selecione o Usuário", usuarios)

# --- Aplicar filtros ---
df_filtrado = df.copy()

if setor_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Setor'] == setor_selecionado]

if usuario_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Úsuario'] == usuario_selecionado]

df_filtrado = df_filtrado[
    (df_filtrado['Data Inicial'].dt.date >= data_inicio) &
    (df_filtrado['Data Final'].dt.date <= data_fim)
]

total_abastecimentos = df_filtrado.shape[0]

st.title("Dashboard de Abastecimentos")


# --- Total de Abastecimentos por Setor ---




col1,col2 = st.columns(2)


with col1:
        
        

    st.markdown(
        f"""
        <div style="
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 120px;
            width: 100%;
            background-color: #FFFAFA;
            border-radius: 15px;
            box-shadow: 3px 3px 20px rgba(0, 0, 0, 0.1);
            font-size: 18px;
            font-weight: bold;
            color: black;
            text-align: center;
            padding: 16px;
            margin-bottom: 20px;">
            <div>Total de Abastecimentos</div>
            <div style="font-size: 32px; margin-top: 10px;">{total_abastecimentos}</div>
        </div>
        """,
        unsafe_allow_html=True)
    



    st.header("Abastecimentos por Empilhador")

    total_abastecimento = df_filtrado.groupby('Úsuario').size().reset_index(name='Quantidade').sort_values(by='Quantidade', ascending=False)

    if not total_abastecimento.empty:
        chart1 = alt.Chart(total_abastecimento).mark_bar().encode(
            y=alt.Y('Úsuario:N', sort='-x', title='Empilhador'),
            x=alt.X('Quantidade:Q', title='Quantidade de Abastecimentos'),
            tooltip=['Úsuario', 'Quantidade']
        ).properties(
            width=600,
            height=300
        )

        text1 = chart1.mark_text(
            align='left',
            baseline='middle',
            dx=3
        ).encode(
            text='Quantidade:Q'
        )

        st.altair_chart(chart1 + text1, use_container_width=True)
    else:
        st.info("Nenhum dado disponível para os filtros selecionados.")


    st.divider()

            # --- Ranking de Produtos Abastecidos ---
    st.header("Produtos mais Abastecidos")

    produtos = df_filtrado.groupby(['Cód.Produto', 'Descrição']).size().reset_index(name='Total').sort_values(by='Total', ascending=False).head(10)

    if not produtos.empty:
        chart3 = alt.Chart(produtos).mark_bar().encode(
            y=alt.Y('Descrição:N', sort='-x', title='Produto'),
            x=alt.X('Total:Q', title='Quantidade Abastecida'),
            tooltip=['Cód.Produto', 'Descrição', 'Total']
        ).properties(
            width=600,
            height=400
        )

        text3 = chart3.mark_text(
            align='left',
            baseline='middle',
            dx=3
        ).encode(
            text='Total:Q'
        )

        st.altair_chart(chart3 + text3, use_container_width=True)
    else:
        st.info("Nenhum dado disponível para os filtros selecionados.")



with col2:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    st.header("Abastecimentos por Setor")

    total_setores = df_filtrado.groupby('Setor').size().reset_index(name='Total').sort_values(by='Total', ascending=False)

    if not total_setores.empty:
        chart2 = alt.Chart(total_setores).mark_bar().encode(
            x=alt.X('Setor:N', title='Setor', sort='-y'),
            y=alt.Y('Total:Q', title='Total de Abastecimentos'),
            color=alt.Color('Setor:N', legend=None),
            tooltip=['Setor', 'Total']
        ).properties(
            width=500,
            height=400
        )

        text2 = chart2.mark_text(
            align='center',
            baseline='bottom',
            dy=-2
        ).encode(
            text='Total:Q'
        )

        st.altair_chart(chart2 + text2, use_container_width=True)
    else:
        st.info("Nenhum dado disponível para os filtros selecionados.")
            
        



