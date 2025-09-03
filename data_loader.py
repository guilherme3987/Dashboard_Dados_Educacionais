import pandas as pd
import os

# Lista de colunas 
colunas_principais_desejadas = [
    'Ano',
    'Unidade Geográfica',
    'Localização',
    'Dependência Administrativa',
    'Taxa de Aprovação',
    'Taxa de Reprovação',
    'Taxa de Abandono'
]

def carregar_dados_e_limpar_colunas():
    """Função para carregar os dados e padronizar os nomes das colunas."""
    arquivo_excel = 'file/tx_rend_brasil_regioes_ufs_2024.xlsx'
    
    if not os.path.exists(arquivo_excel):
        raise FileNotFoundError(f"Arquivo {arquivo_excel} não encontrado.")
    
    df = pd.read_excel(arquivo_excel, header=5)
    
    # Renomear as colunas para simplificar o acesso
    df.rename(columns={
        'Ano': 'Ano',
        'Unidade Geográfica': 'Unidade Geográfica',
        'Localização': 'Localização',
        'Dependência Administrativa': 'Dependência Administrativa',
        'Taxa de Aprovação': 'Taxa de Aprovação',
        'Taxa de Reprovação': 'Taxa de Reprovação',
        'Taxa de Abandono': 'Taxa de Abandono'
    }, inplace=True)
    
    # Remove as colunas que não são necessárias
    df = df[colunas_principais_desejadas]
    
    # Converter colunas numéricas, tratando valores não numéricos
    for col in ['Taxa de Aprovação', 'Taxa de Reprovação', 'Taxa de Abandono']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Preenche valores nulos com zero para evitar erros de JSON
    df = df.fillna(0)
    
    return df