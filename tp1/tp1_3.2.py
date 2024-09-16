import sys
import re

def process_line(line):
    parts = line.replace(':','').split()
    return parts

def get_value(word_value):
    value = word_value[1]
    return value

def get_title(word_title):
    title = ' '.join(word_title[1:])
    return title

def get_similar(word_similar):
    similar = word_similar[2:]
    return similar

#OBS : mesma categoria com dois ids, precisamos tratar
#OBS2: ver oq fica melhor como chave
def process_categories(unpro_categories):
    categories_dic = {}
    #the paramater is a list with all the lines of categories
    for line in unpro_categories:
        #take one line at time and divide the categories
        categories = line.replace("\n", "").split("|")

        for category  in categories[1:]:
            #check if is not empthy
            parts = category.split('[')

            # Check if the string has multiple brackets (special case)
            if len(parts) == 3:
                # Handle special case where you have two brackets
                name = parts[0].strip() + ', ' + parts[1].replace(']', '').strip()  # "Williams, John, guitar"
                id = parts[2].replace(']', '').strip()  # "63054"
            elif len(parts) == 2:
                # Handle regular case where only one bracket exists
                name = parts[0].strip()
                id = parts[1].replace(']', '').strip()
            else:
                # Handle cases where the format doesn't match expected patterns
                name = category
                id = None
                
            if (id not in categories_dic) and name:
                categories_dic[id] = name
            
    return categories_dic

def is_date(string_date): 
    date = r'^\d{4}-\d{1,2}-\d{1,2}$' # 'YYYY-M-D' date format, with 4 dig. year, 1-2 dig. month, and 1-2 digs. day.
    return bool(re.match(date, string_date))

def describe_product(lineF, index_line): 

    #Mapping keys to processing functions
    processing_map = { 
        "ASIN": get_value,
        "title": get_title,
        "group": get_value,
        "salesrank": get_value,
    }

    product_info = {}
    similar_asin = []
    reviews = []
    categories_dic = {}

    print("----------Product Info----------")

    while index_line < len(lineF):
        #list of strings from one line
        line_processed = process_line(lineF[index_line]) 
        if line_processed:
            key = line_processed[0]
            
            if key in processing_map:
                #function from the map processing
                process_function = processing_map[key] 
                product_info[key.lower()] = process_function(line_processed)
                index_line += 1

            #case for similar: the function returns two values: one for the product info (total) and one for the similar asin dic (a list with the "number" of the asin) 
            elif key == "similar":
                #if the categories is 0, the rest os list is empthy
                if len(line_processed[2:])>0:
                    for similar in get_similar(line_processed):
                        similar_asin.append((product_info["asin"], similar))
                index_line+=1

            #special case: save the categories/sub categories for the prodduct, the key is (id, asin)
            elif key == "categories":
                #list to save each line of categorie
                categories_list = []
                while True:
                    index_line += 1
                    line_categorie = lineF[index_line]

                    #if is not empthy or in review section stops
                    if not line_categorie or ("reviews" in line_categorie):
                        index_line -= 1
                        break
                    
                    #just get each line of categorie
                    categories_list.append(line_categorie)

                if categories_list:
                    #for each line of categorie, this function get the id and name of the categories and return a dic
                    categories_dic = process_categories(categories_list)

                index_line += 1

            elif key == "reviews":
                index_line += 1
                
            elif is_date(key):
                    comment = []
                    comment.append(f"asin: {product_info['asin']}")
                    comment.append(f"date: {line_processed[0]}")
                    comment.append(f"{line_processed[1]} = {line_processed[2]}")
                    comment.append(f"{line_processed[3]} = {line_processed[4]}")
                    comment.append(f"{line_processed[5]} = {line_processed[6]}")
                    comment.append(f"{line_processed[7]} = {line_processed[8]}")
                    index_line+=1
                    reviews.append(comment)
            
            else:
                break
        else:
            break
        
            
    for key, value in product_info.items():
        print(f'{key}:{value}')
    if similar_asin:
        print("--------Similar Products:--------")
        for x in similar_asin:
            print(x[1])
    if categories_dic:
        print("--------Categories:--------")
        for id, nome in categories_dic.items():
            print(f'{id}:{nome}')

    if reviews:
        print("--------Reviews:--------")
        for review in reviews:
            print(review)

    print("\n")
    # Informações adicionais
    """ print(f"inputfile pos {index_line}: {lineF[index_line-1]} and {process_line(lineF[index_line-1])}")
    if index_line < len(lineF):
        print(f"prox line: {lineF[index_line]}") """
    
    print('PRODUCT INFO')
    print(product_info)
    print('PRODUCT SIMILAR')
    print(similar_asin)

    return index_line, product_info

def process_file(input_file):
    with open(input_file, "r") as inputF:
        linesF = inputF.readlines()
        index_line = 0

        while index_line < len(linesF):
            line_processed = process_line(linesF[index_line])
            if line_processed:
                if "ASIN" in line_processed[0]:
                    describe_product(linesF, index_line)
            index_line +=1  

input_file = sys.argv[1]
process_file(input_file)