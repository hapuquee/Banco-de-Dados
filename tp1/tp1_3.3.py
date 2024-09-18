""" #conection
import sqlite3
conn = sqlite3.connect('database.db')

#database query 
customer_id = 123
query = "SELECT products.name FROM products JOIN orders ON products.id = orders.product_id WHERE orders.customer_id = ?"
    
#executation
cursor = conn.cursor()
cursor.execute(query, (customer_id,))
results = cursor.fetchall()
      

 """

query_1 = ""
query_2 = ""
query_3 = ""
query_4 = ""
query_5 = ""
query_6 = ""
query_7 = ""



def option_1(query_1):
    print("executando função 1")

def option_2(query_2):
    print("executando função 2")

def option_3(query_3):
    print("executando função 3")

def option_4(query_4):
    print("executando função 4")

def option_5(query_5):
    print("executando função 5")

def option_6(query_6):
    print("executando função 6")

def option_7(query_7):
    print("executando função 7")
     

if __name__ == '__main__':
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
                option_1()
            case 2:
                option_2()
            case 3:
                option_3()
            case 4:
                option_4()
            case 5:
                option_5()
            case 6:
                option_6()
            case 7:
                option_7()
            case _:
                print("Opção inválida, escolhe uma opção válida")
                print("\n")
