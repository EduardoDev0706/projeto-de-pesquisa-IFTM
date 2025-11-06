## 📄 Documentação do Protótipo de Extração RPI (INPI)

### 1. Ferramentas Utilizadas

O protótipo foi construído em Python e depende das seguintes bibliotecas:

* **`xml.etree.ElementTree`**: Uma biblioteca nativa do Python, usada para a análise (parsing) e navegação na estrutura do arquivo `.xml` da RPI.
* **`pandas`**: Biblioteca essencial para a estruturação dos dados. Foi usada para converter a lista de dados extraídos em um DataFrame (tabela).
* **`openpyxl`**: Dependência utilizada pelo `pandas` para permitir a escrita de dados no formato `.xlsx` (Excel).
* **`os`**: Biblioteca nativa do Python, usada para verificar se o arquivo `.xml` de entrada existe no diretório.

### 2. Lógica do Programa

O script `processar_rpi.py` executa a seguinte lógica:

1.  **Carregar:** O script primeiro localiza e analisa (faz o *parse*) do arquivo `.xml` de entrada (ex: `RPI_2861.xml`) usando a biblioteca `ElementTree`.
2.  **Iterar:** Ele encontra o elemento raiz (`<revista>`) e, em seguida, entra em um loop para localizar cada ocorrência da tag `<despacho>`.
3.  **Extrair:** Dentro de cada `<despacho>`, o script navega pelas tags filhas (como `<processo-patente>`, `<numero>`, `<data-deposito>` e `<titular-lista>`) para extrair os dados de interesse.
    * *Robustez:* O script verifica a existência de elementos-chave (como `<processo-patente>`) antes de tentar extrair dados deles, evitando erros caso um despacho não contenha essa estrutura.
4.  **Estruturar:** Cada conjunto de dados extraídos de um despacho é armazenado em um dicionário Python. Todos os dicionários são agrupados em uma lista única.
5.  **Converter:** Ao final do loop, a lista completa de dicionários é carregada em um DataFrame do `pandas`, transformando os dados em um formato de tabela.
6.  **Exportar:** O DataFrame final é exportado para dois arquivos distintos no mesmo diretório:
    * Um arquivo `.csv` (codificado em `utf-8-sig` para garantir a compatibilidade de acentos).
    * Um arquivo `.xlsx` (Excel), com a aba nomeada dinamicamente com o número da revista.

### 3. Próximos Passos (Expansão do Projeto)

Com a lógica de *parsing* (extração) validada, o próximo passo é automatizar a **aquisição dos dados**. O plano é desenvolver um segundo componente (um *web scraper*) que irá:

1.  **Navegar:** Acessar o portal de publicações do INPI.
2.  **Rastrear:** Identificar e coletar os links de download para os arquivos `.xml` das RPIs desejadas (seja de um período específico ou as mais recentes).
3.  **Baixar:** Fazer o download automático desses arquivos `.xml` para uma pasta local.
4.  **Integrar:** (Opcional) Após o download, o *scraper* pode invocar automaticamente o script de *parsing* que criamos para processar cada novo arquivo baixado, automatizando o fluxo de trabalho do início ao fim.
