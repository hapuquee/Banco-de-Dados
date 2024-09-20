import sys
import re
import threading

import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

host = 'localhost'
user = 'postgres'
password = '1234'
db_name = 'tp1bd'

def process_line(line):
    parts = line.replace(':','').split()
    return parts

def get_value(word_value):
    value = word_value[1]
    return str(value)

#for salesrank
def get_int_value(word_value):
    int_n = int(word_value[1])
    if int_n<=0:
        int_n=9798351
    else:
        return int_n

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
        return string_date
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
            reviews.append((
                product_info[0],
                date,
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

# Função para conectar a um banco de dados específico
def connect_to_db(host, user, password, dbname):
    return psycopg2.connect(host=host, user=user, password=password, dbname=dbname)

def create_product_table():
    con = connect_to_db(host, user, password, db_name)
    con.autocommit = True
    # Abrir um cursor para realizar operações no banco de dados
    cur = con.cursor()
    
    # SQL para criar a tabela
    create_table_query = """
    CREATE TABLE product (
        assin VARCHAR (20) PRIMARY KEY,
        title VARCHAR(500),
        "group" VARCHAR(50),
        salerank INTEGER
    );
    """
    
    try:
        # Executar o comando SQL
        cur.execute(create_table_query)
        #print("Tabela 'product' criada com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        # Fechar o cursor
        cur.close()
        con.close()

def create_category_table():
    con = connect_to_db(host, user, password, db_name)
    con.autocommit = True
    # Abrir um cursor para realizar operações no banco de dados
    cur = con.cursor()

    # SQL para criar a tabela category
    create_table_query = """
    CREATE TABLE category (
        category_key INTEGER PRIMARY KEY,
        name VARCHAR(60) NOT NULL
    );
    """
    
    try:
        # Executar o comando SQL para criar a tabela
        cur.execute(create_table_query)
        #print("Tabela 'category' criada com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao criar a tabela 'category': {e}")
    finally:
        # Fechar o cursor
        cur.close()
        con.close()
 

def create_product_category_table():
    con = connect_to_db(host, user, password, db_name)
    con.autocommit = True
    # Abrir um cursor para realizar operações no banco de dados
    cur = con.cursor()

    # SQL para criar a tabela product_category
    create_table_query = """
    CREATE TABLE product_category (
        assin VARCHAR(20),
        id_category INTEGER,
        PRIMARY KEY (assin, id_category),
        FOREIGN KEY (assin) REFERENCES product(assin),
        FOREIGN KEY (id_category) REFERENCES category(category_key)

    );
    """
    
    try:
        # Executar o comando SQL para criar a tabela
        cur.execute(create_table_query)
        #print("Tabela 'product_category' criada com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao criar a tabela 'product_category': {e}")
    finally:
        # Fechar o cursor
        cur.close()
        con.close()


def create_similar_product_table():
    con = connect_to_db(host, user, password, db_name)
    con.autocommit = True
    # Abrir um cursor para realizar operações no banco de dados
    cur = con.cursor()

    # SQL para criar a tabela similar
    create_table_query = """
    CREATE TABLE similar_product (
        assin VARCHAR(20),
        assin_similar VARCHAR(20),
        PRIMARY KEY (assin, assin_similar),
        FOREIGN KEY (assin) REFERENCES product(assin)
    );
    """
    
    try:
        # Executar o comando SQL para criar a tabela
        cur.execute(create_table_query)
    except Exception as e:
        print(f"Ocorreu um erro ao criar a tabela 'similar_product': {e}")
    finally:
        # Fechar o cursor
        cur.close()
        con.close()

def create_product_subcategory_table():
    con = connect_to_db(host, user, password, db_name)
    con.autocommit = True
    # Abrir um cursor para realizar operações no banco de dados
    cur = con.cursor()

    # SQL para criar a tabela product_subcategory
    create_table_query = """
    CREATE TABLE product_subcategory (
        assin VARCHAR(20),
        id_category INTEGER,
        subcategory INTEGER,
        PRIMARY KEY (assin, id_category, subcategory),
        FOREIGN KEY (assin, id_category) REFERENCES product_category(assin, id_category),
        FOREIGN KEY (subcategory) REFERENCES category(category_key )
    );
    """
    
    try:
        # Executar o comando SQL para criar a tabela
        cur.execute(create_table_query)
    except Exception as e:
        print(f"Ocorreu um erro ao criar a tabela 'product_subcategory': {e}")
    finally:
        # Fechar o cursor
        cur.close()
        con.close()

def create_review_table():
    con = connect_to_db(host, user, password, db_name)
    con.autocommit = True
    # Abrir um cursor para realizar operações no banco de dados
    cur = con.cursor()

    # SQL para criar a tabela review
    create_table_query = """
    CREATE TABLE review (
        id SERIAL PRIMARY KEY,
        assin VARCHAR(20),
        data DATE,
        costumer VARCHAR(20),
        rating INTEGER,
        votes INTEGER,
        helpful INTEGER,
        FOREIGN KEY (assin) REFERENCES product(assin)
    );
    """
    
    try:
        # Executar o comando SQL para criar a tabela
        cur.execute(create_table_query)
    except Exception as e:
        print(f"Ocorreu um erro ao criar a tabela 'review': {e}")
    finally:
        # Fechar o cursor
        cur.close()
        con.close()

def check_and_create_db():
    con = connect_to_db(host, user, password, 'postgres')  # Conectar ao banco 'postgres'
    con.autocommit = True
    cur = con.cursor()

    try:
        # Verificar se o banco de dados já existe
        cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [db_name])
        
        if not cur.fetchone():
            # Se não existir, criar o banco de dados
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Banco de dados '{db_name}' criado com sucesso.")
        else:
            print(f"O banco de dados '{db_name}' já existe.")
        
    finally:

        cur.close()
        con.close()

    # Retornar a nova conexão ao banco de dados (novo ou existente)
    return 

def insert_product(dados):
    # Conectar ao banco de dados
    con = connect_to_db(host, user, password, db_name)
    con.autocommit = True
    cur = con.cursor()
    
    # SQL para inserir dados na tabela product
    insert_query = """
    INSERT INTO product (assin, title, "group", salerank)
    VALUES %s;
    """
    
    try:
        # Executar o comando de inserção
        execute_values(cur, insert_query, dados)
        #print("Produto inserido com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir o produto: {e}")
    finally:
        # Fechar o cursor e a conexão
        cur.close()
        con.close()

def insert_product_category(dados):
    #Conectar ao bd
    con = connect_to_db(host, user, password, db_name)
    con.autocommit = True
    cur = con.cursor()

    #query para inserção
    insert_query = """
    INSERT INTO product_category (assin, id_category)
    VALUES %s;
    """

    try:
        #executar comando de inserção
        execute_values(cur, insert_query, dados)
        #print("Product_category inserido com sucesso")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir product_category: {e}")
    finally:
        cur.close()
        con.close()
   
def insert_category(dados):
    #Conectar ao bd
    con = connect_to_db(host, user, password, db_name)
    con.autocommit = True
    cur = con.cursor()

    #query para inserção
    insert_query = """
    INSERT INTO category (category_key, name)
    VALUES %s;
    """

    try:
        #executar comando de inserção
        execute_values(cur, insert_query, dados)
        #print("Category inserido com sucesso")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir category: {e}")
    finally:
        cur.close()
        con.close()

def insert_similar(dados):
    #Conectar ao bd
    con = connect_to_db(host, user, password, db_name)
    con.autocommit = True
    cur = con.cursor()

    #query para inserção
    insert_query = """
    INSERT INTO similar_product (assin, assin_similar)
    VALUES %s;
    """

    try:
        #executar comando de inserção
        execute_values(cur, insert_query, dados)
        #print("Similar inserido com sucesso")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir Similar: {e}")
    finally:
        cur.close()
        con.close()

def insert_product_subcategory(dados):
    #Conectar ao bd
    con = connect_to_db(host, user, password, db_name)
    con.autocommit = True
    cur = con.cursor()

    #query para inserção
    insert_query = """
    INSERT INTO product_subcategory (assin, id_category, subcategory)
    VALUES %s;
    """

    try:
        #executar comando de inserção
        execute_values(cur, insert_query, dados)
        #print("Product_subcategory inserido com sucesso")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir product_subcategory: {e}")
    finally:
        cur.close()
        con.close()

def insert_review(dados):
    #Conectar ao bd
    con = connect_to_db(host, user, password, db_name)
    con.autocommit = True
    cur = con.cursor()

    #query para inserção
    insert_query = """
    INSERT INTO review (assin, data, costumer, rating, votes, helpful)
    VALUES %s;
    """

    try:
        #executar comando de inserção
        execute_values(cur, insert_query, dados)
        #print("Review inserido com sucesso")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir review: {e}")
    finally:
        cur.close()
        con.close()

# Função para gerenciar as threads
def insert_concurrently(function_names, dados_list):
    threads = []

    # Iterar pelos nomes das funções e dados correspondentes
    for i, function_name in enumerate(function_names):
        function = "insert_" + function_name
        insert_function = globals().get(function)

        # Verifica se a função foi encontrada
        if insert_function is None:
            print(f"Erro: A função '{function}' não foi encontrada.")
            return
    

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
    check_and_create_db()
    create_product_table()
    create_category_table()
    create_product_category_table()
    create_review_table()
    create_similar_product_table()
    create_product_subcategory_table()
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

    print("Banco de Dados Populado com Sucesso!")

