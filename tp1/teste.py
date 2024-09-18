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


def divide_file(lines):
    
    total_lines = len(lines)
    if total_lines == 0:
        print("The file is empty.")
        return
    
    half_index = total_lines // 2
    half_line_product = find_product(lines, half_index)

    # Process first half
    primeiro_quartoI = find_product(lines, 0)
    segundo_quartoF = half_line_product - 1
    half_pm_index = (segundo_quartoF - primeiro_quartoI) // 2
    segundo_quartoI = find_product(lines, half_pm_index)
    primeiro_quartoF = segundo_quartoI-1

    # Process second half
    terceiro_quartoI = half_line_product
    quarto_quartoF = total_lines
    half_sm_index = (quarto_quartoF - terceiro_quartoI) // 2
    quarto_quartoI = find_product(lines, half_sm_index)
    terceiro_quartoF = quarto_quartoI -1

    return primeiro_quartoI, primeiro_quartoF, segundo_quartoI, segundo_quartoF, terceiro_quartoI, terceiro_quartoF, quarto_quartoI, quarto_quartoF


def process_file(initial, end, lines):
    # Conjuntos para cada tipo de dado (garante unicidade)
    products = set()
    categories = set()
    similars = set()
    prods_categories = set()
    prods_subcategories = set()
    prods_reviews = set()

    while initial < end:
        line_processed = process_line(lines[initial])
        if not line_processed:
            initial += 1
            continue

        if "ASIN" in line_processed[0]:
            initial, product_info, category_list, similar_asin, prod_category, prod_subcategory, reviews = describe_product(lines, initial)

            # Armazena as informações em conjuntos
            if product_info:
                products.add(product_info)  # Adiciona produto ao conjunto

            if category_list:
                categories.update(category_list)  # Atualiza o conjunto de categorias

            if similar_asin:
                similars.update(similar_asin)  # Atualiza o conjunto de similares

            if prod_category:
                prods_categories.add(prod_category)  # Adiciona categoria principal ao conjunto

            if prod_subcategory:
                prods_subcategories.update(prod_subcategory)  # Atualiza o conjunto de subcategorias

            if reviews:
                prods_reviews.update(reviews)  # Atualiza o conjunto de reviews

        initial += 1

    # Retorna os conjuntos
    return products, categories, similars, prods_categories, prods_subcategories, prods_reviews

def process_file_in_thread(initial, end, lines, results, index):
    # Executa process_file e armazena o resultado na lista 'results' na posição 'index'
    products, categories, similars, prods_categories, prods_subcategories, prods_reviews = process_file(initial, end, lines)
    results[index] = (products, categories, similars, prods_categories, prods_subcategories, prods_reviews)

def open_file(input_file):
    with open(input_file, "r") as inputF:
        lines = inputF.readlines()

        # Divide o arquivo em quatro partes
        primeiro_quartoI, primeiro_quartoF, segundo_quartoI, segundo_quartoF, terceiro_quartoI, terceiro_quartoF, quarto_quartoI, quarto_quartoF = divide_file(lines)
        
        # Lista para armazenar os resultados de cada thread
        results = [None] * 4

        # Cria as threads, passando as partes do arquivo para cada uma
        threads = []
        threads.append(threading.Thread(target=process_file_in_thread, args=(primeiro_quartoI, primeiro_quartoF, lines, results, 0)))
        threads.append(threading.Thread(target=process_file_in_thread, args=(segundo_quartoI, segundo_quartoF, lines, results, 1)))
        threads.append(threading.Thread(target=process_file_in_thread, args=(terceiro_quartoI, terceiro_quartoF, lines, results, 2)))
        threads.append(threading.Thread(target=process_file_in_thread, args=(quarto_quartoI, quarto_quartoF, lines, results, 3)))

        # Inicia as threads
        for thread in threads:
            thread.start()

        # Aguarda todas as threads finalizarem
        for thread in threads:
            thread.join()

        # Combina os resultados das quatro threads
        all_products = []
        all_categories = set()
        all_similars = []
        all_prods_categories = []
        all_prods_subcategories = []
        all_prods_reviews = []

        for result in results:
            products, categories, similars, prods_categories, prods_subcategories, prods_reviews = result
            all_products.extend(products)
            all_categories.update(categories)
            all_similars.extend(similars)
            all_prods_categories.extend(prods_categories)
            all_prods_subcategories.extend(prods_subcategories)
            all_prods_reviews.extend(prods_reviews)

        # Agora 'all_products', 'all_categories', etc. contém todos os dados combinados
        print(f"PRODUCTS {len(all_products)}")
        """ for i in all_products:
            print(i)
        print('\n') """

        print(f"CATEGORIES {len(all_categories)}")
        """ for i in all_categories:
            print(i)
        print('\n') """

        print(f"SIMILARS {len(all_similars)}")
        """ for i in all_similars:
            print(i)
        print('\n') """

        print(f"MAIN_CATEGORIES {len(all_prods_categories)}")
        """ for i in all_prods_categories:
            print(i)
        print('\n') """

        print(f"SUBCATEGORIES {len(all_prods_subcategories)}")
        """ for i in all_prods_subcategories:
            print(i)
        print('\n') """

        print(f"REVIEWS {len(all_prods_reviews)}")
        """ for i in all_prods_reviews:
            print(i)
        print('\n') """


def find_product(lines, index):
    while index < len(lines):
        if "ASIN" in lines[index]:
            return index
        index += 1
    return len(lines)




if __name__ == "__main__":
    input_file = sys.argv[1]
    open_file(input_file)
   