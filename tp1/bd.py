import psycopg2
from psycopg2 import sql

# Função para conectar a um banco de dados específico
def connect_to_db(host, user, password, dbname):
    return psycopg2.connect(host=host, user=user, password=password, dbname=dbname)

# Função para verificar a existência de um banco de dados e criá-lo, se necessário
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
        # Fechar o cursor e a conexão com o banco 'postgres'
        cur.close()
        con.close()

    # Retornar a nova conexão ao banco de dados (novo ou existente)
    return connect_to_db(host, user, password, db_name)

# Função para realizar uma operação simples no banco de dados
def perform_db_operation(connection):
    cur = connection.cursor()
    try:
        # Exemplo de operação: verificar o banco de dados atual
        cur.execute("SELECT current_database();")
        current_db = cur.fetchone()[0]
        print(f"Conectado ao banco de dados: {current_db}")
    finally:
        cur.close()

def create_product_table(connection):
    # Abrir um cursor para realizar operações no banco de dados
    cur = connection.cursor()
    
    # SQL para criar a tabela
    create_table_query = """
    CREATE TABLE product (
        assin INTEGER,
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


# Exemplo de uso das funções
if __name__ == "__main__":
    host = '172.17.0.2'
    user = 'postgres'
    password = '1234'
    db_name = 'TP1BD'

    # Verificar/criar o banco de dados e conectar
    connection = check_and_create_db(host, user, password, db_name)

    # Realizar operações no banco de dados
    perform_db_operation(connection)

    create_product_table(connection)

    # Fechar a conexão
    connection.close()
