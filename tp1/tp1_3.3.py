from bd import connect_to_db

host = 'localhost'
user = 'postgres'
password = '1234'
db_name = 'tp1bd'

def option_1(cur):
    #query para inserção
    #Menor avaliação
    consult_query = """
    (SELECT COSTUMER, HELPFUL, RATING
    FROM REVIEW
    WHERE ASSIN = '0670672238'
    ORDER BY HELPFUL DESC, RATING ASC LIMIT 5);
    """

    try:
        #executar comando de inserção
        cur.execute(consult_query)
        results = cur.fetchall()  # Use fetchone() se você espera apenas uma linha

        # Verificar se resultados foram retornados
        if results:
            print(f"results {results}")
            for row in results:
                print(f"COSTUMER: {row[0]}, HELPFUL: {row[1]}, RATING: {row[2]}")
        else:
            print("Nenhum resultado encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir review: {e}")

    consult_query = """
    (SELECT COSTUMER, HELPFUL, RATING
    FROM REVIEW
    WHERE ASSIN = 'B00000C2CU'
    ORDER BY HELPFUL DESC, RATING DESC LIMIT 5);
    """

    try:
        #executar comando de inserção
        cur.execute(consult_query)
        results = cur.fetchall()  # Use fetchone() se você espera apenas uma linha

        # Verificar se resultados foram retornados
        if results:
            print(f"results {results}")
            for row in results:
                print(f"COSTUMER: {row[0]}, HELPFUL: {row[1]}, RATING: {row[2]}")
        else:
            print("Nenhum resultado encontrado.")
    
    except Exception as e:
        print(f"Ocorreu um erro ao inserir review: {e}")



def option_2(cur):
    #query para inserção
    consult_query = """
    SELECT p2.assin AS similar_assin, 
       p2.title AS similar_title, 
       p2.salerank AS similar_salerank
    FROM similar_product sp
    JOIN product p1 ON sp.assin = p1.assin
    JOIN product p2 ON sp.assin_similar = p2.assin
    WHERE p1.assin = '1559362022'  -- O produto original
    AND p2.salerank < p1.salerank;  -- Comparação do salerank

    """

    try:
        #executar comando de inserção
        cur.execute(consult_query)
        results = cur.fetchall()  # Use fetchone() se você espera apenas uma linha

        # Verificar se resultados foram retornados
        if results:
            print(f"results {results}")
            print("| similar_assin | similar_title | similar_salerank |")
            print("|---------------|---------------|------------------|")
            for row in results:
                similar_assin, similar_title, similar_salerank = row
                print(f"| {similar_assin} | {similar_title} | {similar_salerank} |")
        else:
            print("Nenhum resultado encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir review: {e}")


def option_3(cur):
    #query para inserção
    consult_query = """
        SELECT 
            DATE(r.ano || '-' || r.mes || '-' || r.dia) AS review_date,
            AVG(r.rating) AS avg_daily_rating
        FROM 
            review r
        WHERE 
            r.assin = '1559362022'
        GROUP BY 
            review_date
        ORDER BY 
            review_date ASC;
    """

    try:
        #executar comando de inserção
        cur.execute(consult_query)
        results = cur.fetchall()  # Use fetchone() se você espera apenas uma linha

        # Verificar se resultados foram retornados
        if results:
            print(f"results {results}")
            for row in results:
                date, avg= row
                print(f"| {date} | {avg}")
        else:
            print("Nenhum resultado encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir review: {e}")


def option_4(cur):
    #query para inserção
    consult_query = """
    WITH RankedProducts AS (
        SELECT 
            assin,
            title,
            "group",
            salerank,
            ROW_NUMBER() OVER (PARTITION BY "group" ORDER BY salerank) AS rank
        FROM 
            product
    )

    SELECT 
        assin,
        title,
        "group",
        salerank
    FROM 
        RankedProducts
    WHERE 
        rank <= 10
    ORDER BY 
        "group", rank;


    """

    try:
        #executar comando de inserção
        cur.execute(consult_query)
        results = cur.fetchall()  # Use fetchone() se você espera apenas uma linha

        # Verificar se resultados foram retornados
        if results:
            print(f"results {results}")
            for row in results:
                assin, title, group, salerank = row
                print(f"| {assin} | {title} | {group} | {salerank} |")
        else:
            print("Nenhum resultado encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir review: {e}")


def option_5(cur):
    #query para inserção
    consult_query = """
        SELECT 
            p.title AS product_title, 
            AVG(r.helpful) AS avg_helpful_reviews
        FROM 
            review r
        JOIN 
            product p ON r.assin = p.assin
        GROUP BY 
            p.title
        ORDER BY 
            avg_helpful_reviews DESC
        LIMIT 10;
    """

    try:
        #executar comando de inserção
        cur.execute(consult_query)
        results = cur.fetchall()  # Use fetchone() se você espera apenas uma linha

        # Verificar se resultados foram retornados
        if results:
            print(f"results {results}")
            for row in results:
                tittle, avg = row
                print(f"| {tittle} | {avg} ")
        else:
            print("Nenhum resultado encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir review: {e}")


def option_6(cur):
    #query para inserção
    consult_query = """
        SELECT 
        c.name AS category_name,
        AVG(r.helpful) AS avg_helpful_reviews
        FROM 
            review r
        JOIN 
            product_category pc ON r.assin = pc.assin
        JOIN 
            category c ON pc.id_category = c.category_key
        GROUP BY 
            c.name
        ORDER BY 
            avg_helpful_reviews DESC
        LIMIT 5;
    """

    try:
        #executar comando de inserção
        cur.execute(consult_query)
        results = cur.fetchall()  # Use fetchone() se você espera apenas uma linha

        # Verificar se resultados foram retornados
        if results:
            print(f"results {results}")
            for row in results:
                category, avg = row
                print(f"| {category} | {avg} ")
        else:
            print("Nenhum resultado encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir review: {e}")


def option_7(cur):
    consult_query = """
        SELECT 
            p."group", 
            r.costumer, 
            COUNT(r.id) AS total_reviews
        FROM 
            review r
        JOIN 
            product p ON r.assin = p.assin
        GROUP BY 
            p."group", r.costumer
        ORDER BY 
            total_reviews DESC
        LIMIT 10;
    """
    try:
        #executar comando de inserção
        cur.execute(consult_query)
        results = cur.fetchall()  # Use fetchone() se você espera apenas uma linha

        # Verificar se resultados foram retornados
        if results:
            print(f"results {results}")
            for row in results:
                group, costumer, total_reviews = row
                print(f'{group} | {costumer} | {total_reviews}')
           
        else:
            print("Nenhum resultado encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir review: {e}")



if __name__ == '__main__':
    con = connect_to_db(host, user, password, db_name)
    con.autocommit = True
    cur = con.cursor()

    condition = True
    while(condition):
        print("1 - Listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação")
        print("2 - Listar os produtos similares com maiores vendas")
        print("3 - Mostrar a evolução diária das médias de avaliação")
        print("4 - Listar os 10 produtos líderes de venda em cada grupo de produtos")
        print("5 - Listar os 10 produtos com a maior média de avaliações úteis positivas por produto")
        print("6 - Listar as 5 categorias de produto com a maior média de avaliações úteis positivas por produto")
        print("7 - Listar os 10 clientes que mais fizeram comentários por grupo de produto")
        print("0 - Fechar Progama")
        option = int(input("Selecione uma das Opções:"))
        print("\n")

        match option:
            case 0:
                condition =False
            case 1:
                option_1(cur)
            case 2:
                option_2(cur)
            case 3:
                option_3(cur)
            case 4:
                option_4(cur)
            case 5:
                option_5(cur)
            case 6:
                option_6(cur)
            case 7:
                option_7(cur)
            case _:
                print("Opção inválida, escolhe uma opção válida")
                print("\n")

    cur.close()
    con.close()
