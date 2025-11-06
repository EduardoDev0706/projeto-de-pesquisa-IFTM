import xml.etree.ElementTree as ET
import pandas as pd
import os

# Nome do Arquivo Analisado
NOME_ARQUIVO_INPUT = 'P2861/Patente_2861_04112025.xml'

# Nome dos arquivos que serão criados
NOME_ARQUIVO_OUTPUT_CSV = 'dados_rpi_extraidos.csv'
NOME_ARQUIVO_OUTPUT_EXCEL = 'dados_rpi_extraidos.xlsx'

def processar_xml_para_tabelas(arquivo_xml, arquivo_csv, arquivo_excel):
    """
    Função principal que lê um XML da RPI e o converte
    em arquivos CSV e Excel.
    """

    # Verifica se o arquivo de entrada existe
    if not os.path.exists(arquivo_xml):
        print(f"ERRO: Arquivo de entrada não encontrado!")
        print(f"Verifique se o nome '{arquivo_xml} está correto e na mesma pasta.")
        return
    
    print(f"Iniciando processamento do arquivo: {arquivo_xml}...")

    try:
        # Lê o arquivo XML
        tree = ET.parse(arquivo_xml)
        root = tree.getroot()

        # Extraindo informações globais da revista
        numero_revista = root.get('numero')
        data_publicacao = root.get('dataPublicacao')
        print(f"Lendo dados da Revista RPI n° {numero_revista} de {data_publicacao}")

        # Lista para armazenar todos os dados
        dados_extraidos = []

        # Parsing (Extração dos Dados)
        for despacho in root.findall('despacho'):

            # Extrai dados diretos
            codigo = despacho.find('codigo').text if despacho.find('codigo') is not None else None
            titulo = despacho.find('titulo').text if despacho.find('titulo') is not None else None

            # Bloco <processo-patente>
            processo_elem = despacho.find('processo-patente')

            numero_processo = None
            data_deposito = None
            titulares = []

            if processo_elem is not None:
                numero_processo = processo_elem.find('numero').text if processo_elem.find is not None else None
                data_deposito = processo_elem.find('data-deposito').text if processo_elem.find('data-deposito') is not None else None


                # Bloco <titular-lista>
                titular_lista_elem = processo_elem.find('titular-lista')
                if titular_lista_elem is not None:
                    # Loop interno que pega todos os titulares
                    for titular_elem in titular_lista_elem.findall('titular'):
                        nome_titular = titular_elem.find('nome-completo').text if titular_elem.find('nome-completo') is not None else None
                        if nome_titular:
                            titulares.append(nome_titular)
            
            # Adiciona os dados encontrados a um dicionário
            dados_despacho = {
                "revista": numero_revista,
                "data_publicacao_rpi": data_publicacao,
                "codigo_despacho": codigo,
                "titulo_despacho": titulo,
                "numero_processo": numero_processo,
                "data_deposito_processo": data_deposito,
                "titulares": ", ".join(titulares) # Junta múltiplos titulares com vírgula
            }

            dados_extraidos.append(dados_despacho)

        if not dados_extraidos:
            print("Aviso: Nenhum despacho foi encontrado no arquivo. Arquivos de saída estarão vazios.")
            return
        
        print(f"Total de {len(dados_extraidos)} despachos encontrados. Convertendo para DataFrame...")

        # Converte a lista de dicionários em uma tabela (DataFrame)
        df = pd.DataFrame(dados_extraidos)

        # Exportação para CSV
        print(f"Salvando em CSV: {arquivo_csv}")
        df.to_csv(arquivo_csv, index=False, encoding='utf-8-sig')

        # Exportação para Excel
        print(f"Salvando em Excel: {arquivo_excel}")
        df.to_excel(arquivo_excel, index=False, sheet_name=f'RPI_{numero_revista}')

        print("\n--- SUCESSO! ---")
        print(f"Arquivos '{arquivo_csv}' e '{arquivo_excel}' foram criados com sucesso.")

    except ET.ParseError:
        print(f"ERRO: Falha ao analisar o XML. O arquivo '{arquivo_xml}' pode estar corrompido.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    processar_xml_para_tabelas(NOME_ARQUIVO_INPUT, 
                               NOME_ARQUIVO_OUTPUT_CSV, 
                               NOME_ARQUIVO_OUTPUT_EXCEL)