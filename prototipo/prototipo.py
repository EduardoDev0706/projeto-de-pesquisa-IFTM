import pandas as pd
import os

# Configurações de Leitura
ARQUIVO_CSV = 'conjunto-dados.csv'
ENCODING_ARQUIVO = 'utf-8'
SEPARADOR_ARQUIVO = ';'

def carregar_dados_csv(arquivo_csv):
    """
    Carrega dados de um arquivo CSV do INPI para um DataFrame do Pandas.
    """
    if not os.path.exists(arquivo_csv):
        print(f"Erro: Arquivo não encontrado em '{arquivo_csv}'")
        print("Por favor, baixe o arquivo CSV e coloque-o nesta pasta.")
        return None

    print(f"Iniciando leitura do arquivo: {arquivo_csv}")

    try:
        df = pd.read_csv(
            arquivo_csv,
            encoding=ENCODING_ARQUIVO,
            delimiter=SEPARADOR_ARQUIVO,
            on_bad_lines='skip',
            low_memory=False
        )

    # Tratamento simples de exceções
    except UnicodeDecodeError:
        print(f"Erro de Codificação! Tente mudar ENCODING_ARQUIVO para 'latin-1'.")
        return None
    except Exception as e:
        print(f"Erro ao ler o CSV: {e}. Verifique o SEPARADOR_ARQUIVO.")
        return None

    print(f"Leitura concluída com sucesso. {len(df)} registros carregados.")
    return df

def analisar_e_exportar(df):
    """
    Realiza filtro relevantes para metadados de datasets e exporta.
    """
    
    print("\n--- Iniciando Análise e Filtragem ---")
    COLUNA_ORG = "Organização"
    COLUNA_DESC = "Descrição"
    COLUNA_TAGS = "Tags"
    COLUNA_DOWNLOADS = "Quantidade Downloads"

    # Prototipo: Filtrar por Organização (Ex: INPI)
    org_alvo = 'INPI'
    print(f"\nFiltrando por datasets onde a '{COLUNA_ORG}' contém '{org_alvo}'...")

    df_filtrado_inpi = df[
        df[COLUNA_ORG].str.contains(org_alvo, case=False, na=False)
    ]

    print(f"Encontrados: {len(df_filtrado_inpi)} registros.")

    if not df_filtrado_inpi.empty:
        print("Amostra dos datasets do INPI encontrados:")
        print(df_filtrado_inpi[['Nome', 'Organização', COLUNA_DOWNLOADS]].head())

        # Exportação 1: Salva o filtro em um novo arquivo CSV
        print("Exportando filtro para CSV...")
        nome_arquivo_csv = 'filtro_datasets_inpi.csv'
        df_filtrado_inpi.to_csv(nome_arquivo_csv, index=False, sep=';', encoding='utf-8-sig')
        print(f"Salvo em '{nome_arquivo_csv}'")
    
    # Prototipo: Filtrar por palavra-chave em 'Descrição' ou 'Tags'
    palavra_chave = 'patente'
    print(f"\nFiltrando por datasets que contêm '{palavra_chave}' na descrição ou tags...")
    
    # Garante que as colunas sejam string para evitar erros
    df[COLUNA_DESC] = df[COLUNA_DESC].astype(str)
    df[COLUNA_TAGS] = df[COLUNA_TAGS].astype(str)

    filtro_desc = df[COLUNA_DESC].str.contains(palavra_chave, case=False, na=False)
    filtro_tags = df[COLUNA_TAGS].str.contains(palavra_chave, case=False, na=False)

    df_filtrado_palavra = df[filtro_desc | filtro_tags]

    print(f"Encontrados: {len(df_filtrado_palavra)} registros.")

    if not df_filtrado_palavra.empty:
        # --- Exportação 2: Salvar o filtro em Excel ---
        print("Exportando filtro para Excel...")
        nome_arquivo_excel = 'filtro_palavra_patente.xlsx'
        df_filtrado_palavra.to_excel(nome_arquivo_excel, index=False, sheet_name='Datasets com "patente"')
        print(f"Salvo em '{nome_arquivo_excel}'")

    # Prototipo: Filtrar por popularidade (Mais de 500 downloads)
    print(f"\nFiltrando por datasets com mais de 500 downloads...")
    
    # Converte a coluna de downloads para número
    df[COLUNA_DOWNLOADS] = pd.to_numeric(df[COLUNA_DOWNLOADS], errors='coerce').fillna(0)

    limite_downloads = 500
    df_filtrado_popular = df[df[COLUNA_DOWNLOADS] > limite_downloads]

    print(f"Encontrados: {len(df_filtrado_popular)} registros populares.")

    if not df_filtrado_popular.empty:
        # Ordena para os mais populares primeiro
        df_popular_ordenado = df_filtrado_popular.sort_values(by=COLUNA_DOWNLOADS, ascending=False)

        print("Amostra dos datasets mais populares:")
        print(df_popular_ordenado[['Nome', 'Organização', COLUNA_DOWNLOADS]].head())

# --- Execução do Protótipo ---
if __name__ == "__main__":
    
    # 1. Carregar os dados
    df_datasets = carregar_dados_csv(ARQUIVO_CSV)
    
    if df_datasets is not None and not df_datasets.empty:
        
        # 2. Mostrar informações de Estrutura
        print("\n--- Informações da Estrutura (Colunas e Tipos) ---")
        df_datasets.info()
        
        # 3. Chamar a função de análise e exportação
        analisar_e_exportar(df_datasets)
    else:
        print("\nNão foi possível carregar os dados. Análise cancelada.")