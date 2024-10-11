# CSV Parser Project

Este projeto implementa um parser para processar arquivos CSV contendo dados de artigos. O programa é desenvolvido em C++ e está dividido em dois módulos principais: `Parser` e `Registro`.

## Estrutura de Diretórios

tp2/  
*├── Parser/  
    *├── parser.cpp # Código-fonte do parser  
    *├── artigo.csv # Exemplo de arquivo CSV    
    *├── parser # Executável gerado pelo Makefile   
    *└── README.md # Este arquivo de instruções  
*└── Registro/  
    *├── registro.cpp # Código-fonte do módulo Registro  
    *├── registro.hpp # Arquivo de cabeçalho para o Registro  



## Pré-requisitos

Para compilar e executar este projeto, você precisará de:

- Um compilador C++ (por exemplo, `g++`)
- `make` instalado no sistema

## Compilação

Siga as instruções abaixo para compilar o projeto usando `make`.

1. **Navegue até o diretório `Parse`:**

   ```bash
   cd Parse

2. **Compile o projeto usando o make**

    ```bash
    make

3. **Execute chamando o "parser"**
    
    ```bash
    ./parser

4. **Insira o nome do csv desejado**

5. **Caso queira limpar os arquivos compilados utilize o make clean**

    ```bash
    make clean

## Observações

O arquivo apenas faz leitura dos dados e cria um "Registro" de acordo com a struct, retirei os prints. Caso queiram ver o funcionamento 
é so descomentar as linhas 113, 130 e 133 do "parser.cpp"
