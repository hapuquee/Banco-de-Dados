import sys
import re
import bd
import threading

def process_line(line):
    parts = line.replace(':','').split()
    return parts

def get_value(word_value):
    value = word_value[1]
    return str(value)

#for salesrank
def get_int_value(word_value):
    return int(word_value[1])

def get_title(word_title):
    title = ' '.join(word_title[1:])
    return title

def get_similar(word_similar):
    similar = word_similar[2:]
    return similar

def process_categories(unpro_categories):
    categories_list = []
    seen_id = []
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
                
            if (id not in seen_id) and name:
                categories_list.append((int(id),name))
                seen_id.append(id)
                
            
    return categories_list

def is_date(string_date): 
    if re.match(r'^\d{4}-\d{1,2}-\d{1,2}$', string_date): # 'YYYY-M-D' date format, with 4 dig. year, 1-2 dig. month, and 1-2 digs. day.
        year, month, day = map(int, string_date.split('-'))
        return year, month, day
    else:
        return None

def to_int(value):
    #returns a list of the match
    number_str = re.findall(r'\d+', value)
    #check if is has somenthing
    if number_str:  
        #transform to int
        return int(number_str[0])  
    return None  


def describe_product(lineF, index_line):
    # Mapping keys to processing functions
    processing_map = {
        "ASIN": get_value,
        "title": get_title,
        "group": get_value,
        "salesrank": get_int_value,
    }

    product_info = []
    similar_asin = []
    reviews = []
    prod_category = {}
    category_list = []
    prod_subcategory = []

    # verify if the product is discontinued
    if any("discontinued product" in lineF[i].lower() for i in range(index_line, min(index_line + 2, len(lineF)))):
        return index_line + 1, {}, [], {}, [], [], []

    while index_line < len(lineF):
        #list of strings from one line
        line_processed = process_line(lineF[index_line])
        if not line_processed:
            break

        key = line_processed[0]

        if key in processing_map:
            #process product information by the functions on map
            product_info.append(processing_map[key](line_processed))
            index_line += 1

        #case for similar: returns a list of similar asins
        elif key == "similar":
            #if the similar is 0, the rest of list is empthy
            if len(line_processed[2:]) > 0:
                similar_asin.extend((
                    product_info[0],
                    similar
                 ) for similar in get_similar(line_processed))
            index_line += 1

        elif key == "categories":
            #process categories and subcategories
            categories_list = []
            while index_line + 1 < len(lineF):
                index_line += 1
                line_category = lineF[index_line]
                #if is not empthy or in reviews section stops
                if not line_category or "reviews" in line_category:
                    index_line -= 1
                    break
                categories_list.append(line_category)

            if categories_list:
                category_list = process_categories(categories_list)
                #takes the first category as main category
                main_category = category_list[0]
                prod_category = (product_info[0],main_category[0])
                #save the rest as subcategory
                prod_subcategory.extend((
                    product_info[0],
                    main_category[0],
                    category[0]
                ) for category in category_list[1:])
            index_line += 1

        elif key == "reviews":
            index_line += 1

        #verify if is a data and already get the values
        elif (date := is_date(key)):
            # Process reviews with date
            year, month, day = date
            reviews.append((
                product_info[0],
                year,
                month,
                day,
                line_processed[2],
                to_int(line_processed[4]),
                to_int(line_processed[6]),
                to_int(line_processed[8])
            ))
            index_line += 1

        else:
            break

    return index_line, tuple(product_info), category_list, similar_asin, prod_category, prod_subcategory, reviews



def process_file(input_file):
    #list for each table
    products = []
    categories = set() #more efficient to get unique values
    similars = []
    prods_categories = []
    prods_subcategories = []
    prods_reviews = []

    index_line = 0

    with open(input_file, "r") as inputF:
        linesF = inputF.readlines()

    while index_line < len(linesF):
        line_processed = process_line(linesF[index_line])
        if not line_processed:
            index_line += 1
            continue

        if "ASIN" in line_processed[0]:
            index_line, product_info, category_list, similar_asin, prod_category, prod_subcategory, reviews = describe_product(linesF, index_line)

            #get every information of one product to their respective list
            if product_info:
                products.append(product_info)

            if category_list:
                categories.update(category for category in category_list)

            if similar_asin:
                similars.extend(similar_asin)

            if prod_category:
                prods_categories.append(prod_category)

            if prod_subcategory:
                prods_subcategories.extend(prod_subcategory)

            if reviews:
                prods_reviews.extend(reviews)
        index_line += 1

    return products, list(categories), similars, prods_categories, prods_subcategories, prods_reviews


# Função para gerenciar as threads
def insert_concurrently(function_names, dados_list):
    threads = []

    # Iterar pelos nomes das funções e dados correspondentes
    for i, function_name in enumerate(function_names):
        # Usar getattr para obter a função do módulo bd a partir do nome
        insert_function = getattr(bd, "insert_"+function_name)

        dados = dados_list[i]
        tam_dados = len(dados)
        # Criar uma thread para cada função de inserção, passando os dados correspondentes
        thread = threading.Thread(target=insert_function, args=(dados[0:(tam_dados//2)],))
        threads.append(thread)
        thread = threading.Thread(target=insert_function, args=(dados[(tam_dados//2):],))
        threads.append(thread)
       
    # Iniciar todas as threads
    for thread in threads:
        thread.start()

    # Esperar que todas as threads terminem
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    input_file = sys.argv[1]

    bd.check_and_create_db()
    bd.create_product_table()
    bd.create_category_table()
    bd.create_product_category_table()
    bd.create_review_table()
    bd.create_similar_product_table()
    bd.create_product_subcategory_table()
    product, category, similar, product_category, product_subcategory, review = process_file(input_file) 
    
    função = ["product", "category"]
    dados = [product, category]
    insert_concurrently(função, dados)

    função = ["similar", "product_category"]
    dados = [similar, product_category]
    insert_concurrently(função, dados)

    função = ["product_subcategory", "review"]
    dados = [product_subcategory, review]
    insert_concurrently(função, dados)

""" 
    print(f"quantidade de produtos: {len(product)}")
    print(f"quantidade de categories: {len(category)}")
    print(f"quantidade de produtos_categoria: {len(product_category)}")
    print(f"quantidade de similares: {len(similar)}")
    print(f"quantidade de subcat: {len(product_subcategory)}")
    print(f"quantidade de reviews: {len(review)}")
     """
"""     print("PRODUCTS")
    for i in products:
        print(i)
    print('\n')

    print("CATEGORIES")
    for i in categories_list:
        print(i)
    print('\n')

    
    print("SIMILARS")
    for i in similars:
        print(i)
    print('\n')

    
    print("MAIN_CATEGORIES")
    for i in prods_categories:
        print(i)
    print('\n')

    
    print("SUBCATEGORIES")
    for i in prods_subcategories:
        print(i)
    print('\n')

    
    print("REVIEWS")
    for i in prods_reviews:
        print(i) """


    
