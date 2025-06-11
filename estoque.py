# %%
import pandas as pd

def extrair_rua(codigo):
    cod_rua = str(codigo) 
    partes = cod_rua.split('.')
    if len(partes) >= 2:
        return partes[1]
    return None

def classificar_area(rua):
    try:
        num = int(rua)  # Converte a string para inteiro
        if num <= 12:
            return 'Varejo'
        elif num <= 36:
            return 'Volumoso'
        elif num <= 50:
            return 'Confinado'
        elif num <= 53:
            return 'Tubo/Lonado'
    except:
        return None  # Caso a conversão falhe

df = pd.read_excel('Estoque___Enderecamento.xls', header=2)

colunas = ['End. Reduzido', 'Cód. Produto',	'Picking', 'Endereço',	'Desc. Produto', 'Desc. Endereço',	'Est. Atual Un. Padrão','Referência','Un. Padrão']

df = df[colunas]

df['RUA'] = df['Desc. Endereço'].apply(extrair_rua)

df['SETOR'] = df['RUA'].apply(classificar_area)

#%%
linhas_drop = ['ÁREA EXTERNA','AVARIA DESCARTE', 'AVARIA FEIRINHA', 'AVARIA TROCA FORNECEDOR', 'Baixa uso consumo', 'COBRANÇA TRANSPORTADORA', 'Recebimento avaria e perda', 'TRIAGEM AVARIA', 'TRIAGEM TRATATIVA']

df = df[~df['Desc. Endereço'].isin(linhas_drop)]



# %%
df_pulmao = df[df['Picking'] == 'Não']

df_picking = df[df['Picking'] == 'Sim']


# %%
df_pulmao['Tem Pulmão'] = 1

df_pivot = df_pulmao.pivot_table(
    index='Cód. Produto',
    columns='RUA',
    values='Tem Pulmão',
    fill_value=0
).reset_index()

df_final = pd.merge(df_picking, df_pivot, on='Cód. Produto', how='left')

# Substituir NaN por 0
for col in df_final.columns:
    if isinstance(col, int):
        df_final[col] = df_final[col].fillna(0).astype(int)


colunas = ["End. Reduzido",'Picking', 'Desc. Endereço','Desc. Produto', 'Est. Atual Un. Padrão','Referência','Un. Padrão']

df_final = df_final.drop(columns= colunas)
# %%
df_merged = pd.merge(df_picking, df_pulmao, on='Cód. Produto', how='inner', suffixes=('_Picking', '_Pulmão'))

# Filtrar onde os setores são diferentes
df_fora_zona = df_merged[df_merged['SETOR_Picking'] != df_merged['SETOR_Pulmão']]

df_fora_zona = df_fora_zona[['Cód. Produto', 'SETOR_Picking', 'RUA_Picking','Endereço_Picking','Est. Atual Un. Padrão_Picking', 'SETOR_Pulmão','Endereço_Pulmão']]
# %%
df_fora_zona[df_fora_zona['SETOR_Picking'] == 'Varejo']
# %%
total_itens = df_merged.shape[0]

# Total fora da zona
total_fora_zona = df_fora_zona.shape[0]

# Porcentagem
porcentagem_fora = (total_fora_zona / total_itens) * 100

print(f"Total de itens analisados: {total_itens}")
print(f"Total fora da zona de armazenagem: {total_fora_zona}")
print(f"Porcentagem fora da zona: {porcentagem_fora:.2f}%")
# %%
# Total de itens analisados por SETOR de Picking
total_por_setor = df_merged.groupby('SETOR_Picking').size()

# Total fora da zona por SETOR de Picking
fora_por_setor = df_fora_zona.groupby('SETOR_Picking').size()

# DataFrame para porcentagem
porcentagem_por_setor = (fora_por_setor / total_por_setor) * 100

# Deixar mais bonito
resultado = pd.DataFrame({
    'Total Analisado': total_por_setor,
    'Fora da Zona': fora_por_setor,
    'Porcentagem Fora (%)': porcentagem_por_setor.round(2)
}).fillna(0)

print(resultado)


# %%
df_fora_zona.to_excel('fora_da_zona.xlsx')
# %%
df_merged.head()
# %%
