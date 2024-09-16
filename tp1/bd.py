import psycopg2
from psycopg2 import sql

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
        assin INTEGER PRIMARY KEY,
        title VARCHAR(200),
        "group" VARCHAR(50),
        salerank INTEGER
    );
    """
    
    try:
        # Executar o comando SQL
        cur.execute(create_table_query)
        print("Tabela 'product' criada com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
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
        assin INTEGER,
        id_category INTEGER,
        PRIMARY KEY (assin, id_category),
        FOREIGN KEY (assin) REFERENCES product(assin)
    );
    """
    
    try:
        # Executar o comando SQL para criar a tabela
        cur.execute(create_table_query)
        print("Tabela 'product_category' criada com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao criar a tabela 'product_category': {e}")
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
        id SERIAL PRIMARY KEY,
        name VARCHAR(60) NOT NULL
    );
    """
    
    try:
        # Executar o comando SQL para criar a tabela
        cur.execute(create_table_query)
        print("Tabela 'category' criada com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao criar a tabela 'category': {e}")
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
        assin INTEGER,
        assin_similar INTEGER,
        PRIMARY KEY (assin, assin_similar),
        FOREIGN KEY (assin) REFERENCES product(assin),
        FOREIGN KEY (assin_similar) REFERENCES product(assin)
    );
    """
    
    try:
        # Executar o comando SQL para criar a tabela
        cur.execute(create_table_query)
        print("Tabela 'similar_product' criada com sucesso.")
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
        assin INTEGER,
        id_category INTEGER,
        subcategory INTEGER,
        PRIMARY KEY (assin, id_category, subcategory),
        FOREIGN KEY (assin, id_category) REFERENCES product_category(assin, id_category),
        FOREIGN KEY (subcategory) REFERENCES category(id)
    );
    """
    
    try:
        # Executar o comando SQL para criar a tabela
        cur.execute(create_table_query)
        print("Tabela 'product_subcategory' criada com sucesso.")
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
        assin INTEGER,
        costumer VARCHAR(20),
        data VARCHAR(15),
        rating INTEGER,
        votes INTEGER,
        helpful INTEGER,
        FOREIGN KEY (assin) REFERENCES product(assin)
    );
    """
    
    try:
        # Executar o comando SQL para criar a tabela
        cur.execute(create_table_query)
        print("Tabela 'review' criada com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao criar a tabela 'review': {e}")
    finally:
        # Fechar o cursor
        cur.close()
        con.close()


def check_and_create_db(host, user, password, db_name):
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


# Exemplo de uso das funções
if __name__ == "__main__":
    host = '172.17.0.2'
    user = 'postgres'
    password = '1234'
    db_name = 'tp1bd'

    # Verificar/criar o banco de dados e conectar
    check_and_create_db(host, user, password, db_name)
    
    # Realizar operações no banco de dados
    #perform_db_operation()

    create_product_table()
    create_product_category_table()
    create_category_table()
    create_similar_product_table()
    create_product_subcategory_table()
    create_review_table()
    
