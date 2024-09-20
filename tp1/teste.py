from bd import connect_to_db
from tabulate import tabulate
import streamlit as st
import pandas as pd
import altair as alt



host = 'localhost'
user = 'postgres'
password = '1234'
db_name = 'tp1bd'

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




def option_1(cur, assin):
    # Query para listar os 5 comentários mais úteis
    cur.execute(f"SELECT COSTUMER, HELPFUL, RATING FROM REVIEW WHERE ASSIN = '{assin}' AND HELPFUL > 0 ORDER BY RATING ASC, HELPFUL DESC LIMIT 5;")
    data_1 = cur.fetchall()
    columns = ['Costumer', 'Helpful', 'Rating']

    # Criar um DataFrame usando pandas para definir as colunas
    df_1 = pd.DataFrame(data_1, columns=columns)

    # Mostrar a primeira tabela
    st.write("Tabela 1: 5 comentários mais úteis com menor rating")
    st.table(df_1)

    # Suponha que você queira exibir outra tabela com comentários mais recentes, por exemplo
    cur.execute(f"SELECT COSTUMER, HELPFUL, RATING FROM REVIEW WHERE ASSIN = '{assin}' AND HELPFUL > 0 ORDER BY HELPFUL DESC, RATING DESC LIMIT 5;")
    data_2 = cur.fetchall()
    columns_2 = ['Costumer', 'Review Date', 'Rating']

    # Criar um segundo DataFrame
    df_2 = pd.DataFrame(data_2, columns=columns_2)

    # Mostrar a segunda tabela
    st.write("Tabela 1: 5 comentários mais úteis com maior rating")
    st.table(df_2)


def option_2(cur, assin):
    # Query para listar os produtos similares com maiores vendas
    cur.execute(f"SELECT p2.assin AS similar_assin, p2.title AS similar_title, p2.salerank AS similar_salerank FROM similar_product sp JOIN product p1 ON sp.assin = p1.assin JOIN product p2 ON sp.assin_similar = p2.assin WHERE p1.assin = '{assin}' -- O produto original AND p2.salerank < p1.salerank;  -- Comparação do salerank")
    data = cur.fetchall()
    columns = ['Similar assin', 'Similar title', 'Similar salerank']

    # Criar um DataFrame usando pandas para definir as colunas
    df = pd.DataFrame(data, columns=columns)
    st.table(df)

def option_3(cur, assin):
    # Query para mostrar a evolução diária das médias de avaliação
    cur.execute(f"SELECT DATA, ROUND(AVG(RATING), 0) AS MEDIA FROM REVIEW WHERE ASSIN = '{assin}' GROUP BY DATA; -- EVOLUÇÃO")
    data = cur.fetchall()
    
    # Converter o resultado para um DataFrame
    df = pd.DataFrame(data, columns=['Data', 'Média'])

    # Converter a coluna de datas para o formato datetime
    df['Data'] = pd.to_datetime(df['Data'])

    # Certifique-se de que a coluna 'Média' seja do tipo float (pode ser decimal no banco de dados)
    df['Média'] = df['Média'].astype(float)

    # Criar o gráfico com Altair, especificando explicitamente o tipo dos eixos
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('Data:T', title='Data'),   # Eixo X com a data formatada como temporal
        y=alt.Y('Média:Q', title='Média de Avaliações')  # Eixo Y com valores quantitativos
    ).properties(
        title='Evolução da Média de Avaliações por Data'
    )

    # Exibir o gráfico no Streamlit
    st.altair_chart(chart, use_container_width=True)

def option_4(cur):
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
    # Query para listar os 10 produtos líderes de venda em cada grupo de produtos
    cur.execute(consult_query)
    columns = ['Assin', 'Title', 'Group', 'Salerank']

    # Criar um DataFrame usando pandas para definir as colunas
    df = pd.DataFrame(data, columns=columns)
    st.table(df)

def option_5(cur):
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
    # Query para listar os 10 produtos com maior média de avaliações úteis positivas
    cur.execute(consult_query)
    columns = ['Product Title', 'Avg Helpful Reviews']

    # Criar um DataFrame usando pandas para definir as colunas
    df = pd.DataFrame(data, columns=columns)
    st.table(df)

def option_6(cur):
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
    # Query para listar as 5 categorias com maior média de avaliações úteis positivas
    cur.execute(consult_query)
    data = cur.fetchall()
    columns = ['Category Name', 'Average Helpful Reviews']

    # Criar um DataFrame usando pandas para definir as colunas
    df = pd.DataFrame(data, columns=columns)

    # Exibir a tabela formatada no Streamlit
    st.table(df)

def option_7(cur):
    # Query para listar os 10 clientes que mais fizeram comentários por grupo de produto
    cur.execute("SELECT * FROM clientes ORDER BY comentarios DESC LIMIT 10")
    data = cur.fetchall()
    st.table(data)

def main():
    st.title("Dashboard de Avaliação de Produtos")

    # Conexão com o banco de dados
    con = connect_to_db(host, user, password, db_name)
    cur = con.cursor()

    # Menu de opções
    option = st.sidebar.selectbox(
        "Selecione uma das Opções:",
        ("Listar os 5 comentários mais úteis",
         "Listar os produtos similares com maiores vendas",
         "Mostrar a evolução diária das médias de avaliação",
         "Listar os 10 produtos líderes de venda em cada grupo",
         "Listar os 10 produtos com maior média de avaliações úteis positivas",
         "Listar as 5 categorias de produto com maior média de avaliações úteis positivas",
         "Listar os 10 clientes que mais fizeram comentários")
    )

    grupo = None
    if option in ("Listar os 5 comentários mais úteis", "Listar os produtos similares com maiores vendas", "Mostrar a evolução diária das médias de avaliação"):
        grupo = st.text_input("Digite o nome do grupo")

    if st.button("Executar"):
        if option == "Listar os 5 comentários mais úteis":
            option_1(cur, grupo)
        elif option == "Listar os produtos similares com maiores vendas":
            option_2(cur, grupo)
        elif option == "Mostrar a evolução diária das médias de avaliação":
            option_3(cur, grupo)
        elif option == "Listar os 10 produtos líderes de venda em cada grupo":
            option_4(cur)
        elif option == "Listar os 10 produtos com maior média de avaliações úteis positivas":
            option_5(cur)
        elif option == "Listar as 5 categorias de produto com maior média de avaliações úteis positivas":
            option_6(cur)
        elif option == "Listar os 10 clientes que mais fizeram comentários":
            option_7(cur)

    # Fechar a conexão
    cur.close()
    con.close()

if __name__ == '__main__':
    main()
