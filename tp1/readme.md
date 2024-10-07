# Trabalho prático 1 BD

## Participantes
Ricardo Eliel Xavier da Silva 22250556  
Karen Hapuque Ferreira Ponce de Leão 22250541

## Sumário

- [Pré-Instalação](#configuração)
- [Instalação](#instalação)
- [Uso](#uso)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Configuração 
Para que sua máquina execute nosso código sem problema algum, é necessário que você execute os seguintes comandos:
```bash
pip install psycopg2-binary  
```  

Essa bibliotecaa é essencial para o código. Vale ressaltar que o código também faz uso de expressões regulares.  
Caso você queira usar o docker para executar nosso programa isso também é possível. Contudo, é necessário que você tenha:  
 - Docker compose
 - Docker

## Instalação

Siga as instruções abaixo para que o projeto execute perfeitamente em sua maquina local.
1. Clone o repositório através do comnado:
```bash
git clone git@github.com:bd1-icomp-ufam/trabalho-pr-tico-i-bancos-de-dados-1-tp1-ricardo_eliel-karen_hapuque.git
```
2. Baixe o arquivo Amazon product co-purchasing network metadata
Para baixar esse arquivo é necessário que você acesse o link a seguir: https://snap.stanford.edu/data/amazon-meta.html e baixe o arquivo amazon-meta.txt.gz  

3. Mova o arquivo amazon-meta.txt.gz para o diretório onde você executou o git clone.

4. Caso queira utilizar o docker, basta executar o seguinte comando:
```bash
sudo docker-compose up
```

5. Altere as variáveis de ambiente que estão no início dos scripts `tp1_3.2.py` e `tp1_3.3.py` de acordo com a configuração do seu banco de dados. Mantenha os valores default caso esteja utilizando o Postgres com o `docker-compose.yml` fornecido.

| Nome    |`Default     |
| ------- | ----------- |
| DB_HOST | `localhost` |
| DB_PORT | `5437`      |
| DB_NAME | `database`  |
| DB_USER | `username`  |
| DB_PASS | `password`  |

### Execução
1. Extraia o arquivo amazon-meta.txt.gz.

1. Execute o script `tp1_3.2.py` junto do arquivo `amazon-meta.txt` para extrair os dados do arquivo e popular o banco de dados.

```
$ python3 tp1_3.2.py amazon-meta.txt
```

2. Execute o script `tp1_3.3.py` para iniciar o dashboard e realizar as consultas.

```
$ python3 tp1_3.3.py