# Protótipo de Análise de Dados Abertos - Foco em INPI

Este projeto é um protótipo em Python para identificar, filtrar e analisar conjuntos de dados públicos, com foco em propriedade industrial (patentes, marcas, etc.) e no Instituto Nacional da Propriedade Industrial (INPI).

## 1. Propósito do Projeto (O Porquê)

O objetivo desta "Fase 1" é automatizar a descoberta de dados relevantes dentro do catálogo massivo do Portal de Dados Abertos do Governo Federal (`dados.gov.br`).

Em vez de navegar manualmente por milhares de datasets, este script filtra o catálogo principal para identificar rapidamente:
1.  Quais datasets são publicados pelo INPI.
2.  Quais datasets (de qualquer organização) são relevantes para o tema "patentes".
3.  Quais desses datasets são os mais populares (baseado em downloads).

O resultado final são planilhas limpas que servem como ponto de partida para a "Fase 2" (a análise dos dados finais).

## 2. Base de Dados Utilizada

* **Fonte:** Portal de Dados Abertos do Governo Federal.
* **Arquivo:** `conjunto-dados.csv`
* **Descrição:** Este arquivo é um **metadado**; um catálogo que descreve *outros* conjuntos de dados. Ele **não** contém os dados finais (ex: as patentes em si).
* **Colunas-Chave Analisadas:**
    * `Organização`: Usada para filtrar pelo "INPI".
    * `Nome`: Nome descritivo do dataset.
    * `Descrição`: Detalhes sobre o conteúdo do dataset (usado para buscar "patente").
    * `Tags`: Palavras-chave (usado para buscar "patente").
    * `Quantidade Downloads`: Métrica de popularidade.
    * `Quantidade Reusos`: Métrica de popularidade.

## 3. Ferramentas e Configuração do Ambiente

* **Sistema Operacional:** Arch Linux
* **Linguagem:** Python 3.x
* **Ambiente Virtual:** `venv` (padrão do Python)
    * Ativação: `source venv/bin/activate`
* **Bibliotecas (requirements.txt):**
    * `pandas`: Usada para carregar o CSV, realizar a filtragem e manipulação dos dados.
    * `openpyxl`: Dependência necessária para o `pandas` conseguir *escrever* arquivos Excel (`.xlsx`).

## 4. Próximos Passos (Roadmap)

Os arquivos gerados por este protótipo (`filtro_...csv` e `filtro_...xlsx`) são o ponto de partida para a próxima fase.

1.  **[Análise Manual]**: Inspecionar os arquivos filtrados para identificar os 2-3 datasets mais promissores (pelo "Nome" e "Quantidade Downloads").
2.  **[Coleta - Fase 2]**: Localizar e baixar os "Recursos" (os arquivos de dados reais, ex: `patentes.zip`, `marcas.csv`) referentes a esses datasets no portal `dados.gov.br`.
3.  **[Protótipo - Fase 2]**: Criar um novo script Python focado em ler e analisar esse novo arquivo (que pode ser um CSV de milhões de linhas ou um XML complexo).
4.  **[Pesquisa]**: Aplicar a análise estatística/qualitativa real sobre os dados finais.