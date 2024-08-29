import sys

def process_line(line):
    parts = line.replace(':','').split()
    return parts

def get_value(word_value):
    value = word_value[1]
    return value

def get_title(word_title):
    title = ' '.join(word_title[1:])
    return title

def get_similar(similar_products):
    products = similar_products[2:]
    return products

def describe_product(lineF, index_line, line_processed):

    #Mapping keys to processing functions
    processing_map = { 
        "Id": get_value,
        "ASIN": get_value,
        "title": get_title,
        "group": get_value,
        "salesrank": get_value,
        "similar": get_value
    }

    product_info = {}
    similar_asin = {}

    print("Product Info")

    while index_line < len(lineF):
        #list of strings from one line
        line_processed = process_line(lineF[index_line]) 
        key = line_processed[0]

        if key in processing_map:

            #function from the map processing
            process_function = processing_map[key] 
            product_info[key.lower()] = process_function(line_processed)

            #case for similar: the function returns two values: one for the product info (total) and one for the similar asin dic (a list with the "number" of the asin) 
            if key == "similar":
                similar_asin[product_info["asin"]] = get_similar(line_processed)

            print(f"{key.lower()}: {product_info[key.lower()]}")
            index_line += 1
        else:
            break
    print("\n")    
    print("Asin DIC")
    for chave, valor in similar_asin.items():
        print(f"{chave} : {valor}")

    # Informações adicionais
    '''print(f"inputfile pos {index_line}: {lineF[index_line-1]} and {process_line(lineF[index_line-1])}")
    if index_line < len(lineF):
        print(f"prox line: {lineF[index_line]}")'''

    return index_line, product_info

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