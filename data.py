# %%
import pandas as pd

df = pd.read_excel('ABASTECIMENTOS.xlsx')

def setor (rua):
    if 1 <= rua <= 12:
        return 'Varejo'
    elif 13 <= rua <=36:
        return 'Volumoso'
    else:
        return 'Confinado'


# %%
## Total de Abastecimentos por Empilhador.

total_abastecimento = df.groupby('Úsuario').size().reset_index(name='Quantidade').sort_values(by='Quantidade', ascending=False)
total_abastecimento
# %%
#Produtos abastecimentos mais vezes
pr_visitados = df.groupby('Cód.Produto')['Descrição'].value_counts().reset_index(name='Total').sort_values(by='Total', ascending=False)
ranking_produtos = pr_visitados.head(10)
ranking_produtos
# %%
df['Rua'] = df['End. Destino'].str.split('.').str[1].str.replace('CO', '', regex=False)

df = df[df['Rua'] != '']

df = df[df['Rua'].str.strip() != '']

df['Rua'] = df['Rua'].astype(int)

df['Setor'] = df['Rua'].apply(setor)
# %%

#Total de abastecimento por setor

total_setores = df.groupby('Setor').size().reset_index(name='Total').sort_values(by='Total', ascending=False)
# %%

varejo = df[df['Setor'] == 'Varejo']

ranking_varejo = varejo.groupby('Cód.Produto')['Descrição'].value_counts().reset_index(name='Total').sort_values(by='Total', ascending=False).head(13)
# %%
volumoso = df[df['Setor'] == 'Volumoso']
volumoso_ranking = volumoso.groupby('Cód.Produto')['Descrição'].value_counts().reset_index(name='Total').sort_values(by='Total', ascending=False).head(13)
# %%
df['Data Inicial'] = pd.to_datetime(df['Data Inicial'], format="%d/%m/%Y %H:%M:%S")
df['Data Final'] = pd.to_datetime(df['Data Final'], format="%d/%m/%Y %H:%M:%S")
# %%

df['Temp.Abastecimento'] = (df['Data Final'] - df['Data Inicial']).dt.total_seconds() / 60
# %%

# %%

# %%
import matplotlib.pyplot as plt

# Dados
labels = ['Fora da Zona de Armazenagem', 'Dentro da Zona de Armazenagem']
valores = [38, 171]
cores = ['#66c2a5', '#b3b3b3']

# Gráfico de pizza
fig, ax = plt.subplots(figsize=(6, 6))
wedges, texts, autotexts = ax.pie(
    valores, labels=labels, colors=cores, autopct='%.1f%%', startangle=90,
    wedgeprops=dict(width=0.4)  # Donut
)

# Título
plt.title('Distribuição dos Abastecimentos (Total = 209)', fontsize=14)
plt.axis('equal')  # Mantém o círculo redondo
plt.tight_layout()
plt.show()



# %%
total = 209
fora = 38