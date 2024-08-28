import sys
def get_value(word_value):
    value = word_value[1]
    return value

def get_title(word_title):
    title = ' '.join(word_title[1:])
    return title

def describe_product(lineF, index_line, line_processed):
    """
    Primeiro de tudo: eu te amo acima de todas as coisas :)

    agora partindo pro trabalho:

    Processa as informações de um produto a partir de uma lista de linhas (lineF) e retorna os dados extraídos.

    Esta função percorre as linhas de um arquivo ou lista de strings, processando cada linha para extrair
    informações específicas sobre um produto, como ID, ASIN, título, grupo e classificação de vendas. As informações
    são extraídas com base no primeiro elemento de cada linha processada (como "Id", "ASIN", etc.), e armazenadas em 
    um dicionário. A função utiliza um mapeamento (`processing_map`) que associa identificadores a funções de 
    processamento adequadas.

    Parâmetros:
    -----------
    lineF : list
        Uma lista de strings onde cada string representa uma linha de um arquivo ou dados a serem processados.

    index_line : int
        O índice atual dentro da lista `lineF`, indicando qual linha está sendo processada.

    line_processed : list
        A linha já processada correspondente ao índice `index_line`. Normalmente, é o resultado de uma 
        chamada inicial à função `process_line`.

    Retorna:
    --------
    index_line : int
        O índice atualizado após o processamento das linhas relevantes. Pode ser usado para continuar o processamento 
        de onde a função parou.

    product_info : dict
        Um dicionário contendo as informações extraídas sobre o produto. As chaves do dicionário são os identificadores 
        em minúsculas (como "id", "asin", "title", etc.), e os valores são os dados extraídos correspondentes.

    Exemplo de Uso:
    ---------------
    >>> lineF = [
    ...    "Id: 12345",
    ...    "ASIN: B0000C9F5R",
    ...    "title: A Great Product",
    ...    "group: Book",
    ...    "salesrank: 56789"
    ... ]
    >>> index_line = 0
    >>> line_processed = process_line(lineF[index_line])
    >>> describe_product(lineF, index_line, line_processed)
    id: 12345
    asin: B0000C9F5R
    title: A Great Product
    group: Book
    salesrank: 56789
    inputfile pos 5: salesrank: 56789 and ['salesrank', '56789']
    
    (5, {'id': '12345', 'asin': 'B0000C9F5R', 'title': 'A Great Product', 'group': 'Book', 'salesrank': '56789'})

    Notas:
    ------
    - A função assume que cada linha processada tem um identificador na primeira posição (como "Id", "ASIN", etc.).
    - Se uma linha não tiver um identificador conhecido, o loop de processamento é interrompido.
    - `processing_map` é usado para mapear identificadores a funções específicas que processam e retornam os dados
      relevantes.
    - A função imprime o status do processamento para cada dado extraído e também fornece informações sobre a linha 
      processada mais recentemente e a próxima linha na sequência.
    """



    processing_map = {
        "Id": get_value,
        "ASIN": get_value,
        "title": get_title,
        "group": get_value,
        "salesrank": get_value
    }

    product_info = {}

    while index_line < len(lineF):
        line_processed = process_line(lineF[index_line])
        key = line_processed[0]

        if key in processing_map:
            process_function = processing_map[key]
            product_info[key.lower()] = process_function(line_processed)
            print(f"{key.lower()}: {product_info[key.lower()]}")
            index_line += 1
        else:
            break

    # Informações adicionais
    print(f"inputfile pos {index_line}: {lineF[index_line-1]} and {process_line(lineF[index_line-1])}")
    if index_line < len(lineF):
        print(f"prox line: {lineF[index_line]}")

    return index_line, product_info

def process_line(line):
    parts = line.replace(':','').split()
    return parts

def process_file(input_file):
    with open(input_file, "r") as inputF:
        linesF = inputF.readlines()
        index_line = 0

        while index_line < len(linesF):
            line_processed = process_line(linesF[index_line])
            if "Id" in line_processed[0]:
                describe_product(linesF, index_line, line_processed)
            index_line += 1

input_file = sys.argv[1]
process_file(input_file)