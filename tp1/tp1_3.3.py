from bd import connect_to_db
from tabulate import tabulate


host = 'localhost'
user = 'postgres'
password = '1234'
db_name = 'tp1bd'

def option_1(cur, assin):
    # Query para menor avaliação e mais útil
    consult_query = """
    SELECT COSTUMER, HELPFUL, RATING 
    FROM REVIEW
    WHERE ASSIN = %s AND HELPFUL > 0
    ORDER BY RATING ASC, HELPFUL DESC
    LIMIT 5; --pegar menos rating e mais helpful
    """

    try:
        # Executar comando de consulta com parâmetro
        cur.execute(consult_query, (assin,))
        results = cur.fetchall()

        # Verificar se resultados foram retornados
        if results:
            # Exibir os resultados com tabulate
            print("Menor avaliação e mais útil:")
            headers = ["Customer", "Helpful", "Rating"]
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print("Nenhum resultado encontrado para menor avaliação.")
    except Exception as e:
        print(f"Ocorreu um erro ao consultar os reviews: {e}")

    # Query para mais útil e maior avaliação
    consult_query = """
    SELECT COSTUMER, HELPFUL, RATING 
    FROM REVIEW
    WHERE ASSIN = %s AND HELPFUL > 0
    ORDER BY HELPFUL DESC, RATING DESC
    LIMIT 5; --pegar mais helpful e mais rating
    """

    try:
        # Executar comando de consulta com parâmetro
        cur.execute(consult_query, (assin,))
        results = cur.fetchall()

        # Verificar se resultados foram retornados
        if results:
            # Exibir os resultados com tabulate
            print("\nMais útil e maior avaliação:")
            headers = ["Customer", "Helpful", "Rating"]
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print("Nenhum resultado encontrado para mais útil e maior avaliação.")
    except Exception as e:
        print(f"Ocorreu um erro ao consultar os reviews: {e}")

def option_2(cur, assin):
    # Query para produtos similares com menor salerank
    consult_query = """
    SELECT p2.assin AS similar_assin, 
           p2.title AS similar_title, 
           p2.salerank AS similar_salerank
    FROM similar_product sp
    JOIN product p1 ON sp.assin = p1.assin
    JOIN product p2 ON sp.assin_similar = p2.assin
    WHERE p1.assin = %s  -- O produto original
    AND p2.salerank < p1.salerank;  -- Comparação do salerank
    """

    try:
        # Executar comando de consulta com parâmetro
        cur.execute(consult_query, (assin,))
        results = cur.fetchall()

        # Verificar se resultados foram retornados
        if results:
            # Exibir os resultados com tabulate
            headers = ["Similar ASSIN", "Similar Title", "Similar SaleRank"]
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print("Nenhum produto similar encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao consultar produtos similares: {e}")

def option_3(cur, assin):
    # Query para calcular a média de avaliação ao longo do tempo
    consult_query = """
        SELECT DATA, ROUND(AVG(RATING), 1) AS MEDIA
        FROM REVIEW
        WHERE ASSIN = %s
        GROUP BY DATA; -- EVOLUÇÃO
    """

    try:
        # Executar comando de consulta com o parâmetro assin
        cur.execute(consult_query, (assin,))
        results = cur.fetchall()

        # Verificar se resultados foram retornados
        if results:
            # Exibir os resultados com tabulate
            headers = ["Date", "Average Rating"]
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print("Nenhum resultado encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao consultar a média de avaliações: {e}")


def option_4(cur):
    # Query para pegar os 10 produtos com melhor rank por grupo
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
        # Executar comando de consulta
        cur.execute(consult_query)
        results = cur.fetchall()

        # Verificar se resultados foram retornados
        if results:
            # Exibir os resultados com tabulate
            headers = ["ASSIN", "Title", "Group", "SaleRank"]
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print("Nenhum resultado encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao consultar produtos: {e}")


def option_5(cur):
    # Query para os 10 produtos com a maior média de avaliações úteis
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
        # Executar comando de consulta
        cur.execute(consult_query)
        results = cur.fetchall()

        # Verificar se resultados foram retornados
        if results:
            # Exibir os resultados com tabulate
            headers = ["Product Title", "Avg Helpful Reviews"]
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print("Nenhum resultado encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao consultar as avaliações: {e}")


def option_6(cur):
    # Query para as 5 categorias com maior média de avaliações úteis
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
        # Executar comando de consulta
        cur.execute(consult_query)
        results = cur.fetchall()

        # Verificar se resultados foram retornados
        if results:
            # Exibir os resultados com tabulate
            headers = ["Category Name", "Avg Helpful Reviews"]
            print(tabulate(results, headers=headers, tablefmt="grid"))
        else:
            print("Nenhum resultado encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao consultar as categorias: {e}")


def option_7(cur):
    # Passo 1: Obter todos os grupos distintos
    distinct_groups_query = """
        SELECT DISTINCT "group"
        FROM product;
    """

    try:
        cur.execute(distinct_groups_query)
        distinct_groups = cur.fetchall()

        if distinct_groups:
            for group_row in distinct_groups:
                group = group_row[0]
                print(f"\nResultados para o grupo: {group}")
                
                # Passo 2: Executar a consulta para cada grupo distinto
                consult_query = """
                    SELECT COSTUMER, COUNT(*) AS APARICAO
                    FROM REVIEW, (SELECT assin FROM product 
                                    WHERE "group" = %s) AS PROD
                    WHERE REVIEW.ASSIN = PROD.ASSIN
                    GROUP BY COSTUMER
                    ORDER BY APARICAO DESC
                    LIMIT 10;
                """
                cur.execute(consult_query, (group,))
                results = cur.fetchall()

                # Exibir resultados formatados
                if results:
                    headers = ["Customer", "Appearances"]
                    print(tabulate(results, headers=headers, tablefmt="grid"))
                else:
                    print(f"Nenhum resultado encontrado para o grupo {group}.")
        else:
            print("Nenhum grupo distinto encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao consultar os dados: {e}")


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

        match option:
            case 0:
                condition =False
            case 1:
                print(f"qual o nome do grupo?")
                grupo = str(input())
                option_1(cur,grupo)
                print("\n\n")
            case 2:
                print(f"qual o nome do grupo?")
                grupo = str(input())
                option_2(cur, grupo)
                print("\n\n")
            case 3:
                print(f"qual o nome do grupo?")
                grupo = str(input())
                option_3(cur, grupo)
                print("\n\n")
            case 4:
                option_4(cur)
                print("\n\n")
            case 5:
                option_5(cur)
                print("\n\n")
            case 6:
                option_6(cur)
                print("\n\n")
            case 7:
                option_7(cur)
                print("\n\n")
            case _:
                print("Opção inválida, escolhe uma opção válida")
                print("\n")

    cur.close()
    con.close()
