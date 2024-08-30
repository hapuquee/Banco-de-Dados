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

def process_categories(categories):
    parts = categories.replace("\n", "").split("|")
    return parts[1:]

def get_review(string_review):
    info_review = []
    i = 1
    #start in index 1 (0 = review)
    while i < len(string_review) - 1:
        info = string_review[i]
        value = string_review[i + 1]
        
        if info == 'avg':
            info = 'avg_rating'
            value = string_review[i + 2]
            #already process 3 positions: avg, rating, value
            i += 3  
        else:
            #process 2 itens: info, value, jump to next one info
            i += 2  
        
        info_review.append((info, value))
    
    #a list of tuples 
    return info_review

def keys_reviews(product_info):
    #delete the key review in the product dict and add others keys 
    infos = product_info["reviews"]

    for info, value in infos:
        product_info[f'{info}_review'] = value

    del product_info['reviews']


def describe_product(lineF, index_line, line_processed):

    #Mapping keys to processing functions
    processing_map = { 
        "Id": get_value,
        "ASIN": get_value,
        "title": get_title,
        "group": get_value,
        "salesrank": get_value,
        "similar": get_value,
        "categories": get_value,
        "reviews": get_review
    }

    product_info = {}
    similar_asin = {}
    categories = {}
    reviews = {}

    print("----------Product Info----------")

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

            #special case: save the categories/sub categories for the prodduct, the key is (id, asin)
            if key == "categories":
                #list to save each line of categorie
                categories_list = []
                while True:
                    index_line += 1
                    line_categorie = process_categories(lineF[index_line])

                    #if is not empthy or in review section stops
                    if not line_categorie or line_categorie[0] == "reviews":
                        index_line -= 1
                        break
                    
                    categories_list.append(line_categorie)
                #create the dic for the categories with id,asin as key
                categories[f'{product_info["id"]}, {product_info["asin"]}'] = categories_list

            if key == "reviews":
                keys_reviews(product_info)
            #print(f"{key.lower()}: {product_info[key.lower()]}")
            index_line += 1

        else:
            break
        
    for key, value in product_info.items():
        print(f'{key}:{value}')
    print("--------Similar Products:--------")
    print(similar_asin[product_info["asin"]])
    print("--------Categories:--------")
    for categorie in categories[f'{product_info["id"]}, {product_info["asin"]}']:
        print(categorie)

    print("\n")
    # Informações adicionais
    """ print(f"inputfile pos {index_line}: {lineF[index_line-1]} and {process_line(lineF[index_line-1])}")
    if index_line < len(lineF):
        print(f"prox line: {lineF[index_line]}")
 """
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