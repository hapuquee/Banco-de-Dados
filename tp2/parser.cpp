#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>

using namespace std;


// Definindo a struct REGISTRO
struct REGISTRO {
    int ID;
    string Titulo;
    int Ano;
    string Autores;
    int Citacoes;
    string Atualizacao;
    string Snippet;
};

// Função global para inicializar um registro a partir de strings
void inicializarRegistro(REGISTRO& registro, const string& id, const string& titulo, const string& ano, const string& autores, const string& citacoes, const string& atualizacao, const string& snippet) {
    try {
        registro.ID = stoi(id);
    } catch (invalid_argument& e) {
        cerr << "Erro ao converter ID: " << id << endl;
        registro.ID = 0;
    }

    registro.Titulo = titulo.length() <= 300 ? titulo : titulo.substr(0, 300);
    try {
        registro.Ano = stoi(ano);
    } catch (invalid_argument& e) {
        cerr << "Erro ao converter Ano: " << ano << endl;
        registro.Ano = 0;
    }

    registro.Autores = autores.length() <= 150 ? autores : autores.substr(0, 150);
    try {
        registro.Citacoes = stoi(citacoes);
    } catch (invalid_argument& e) {
        cerr << "Erro ao converter Citações: " << citacoes << endl;
        registro.Citacoes = 0;
    }

    registro.Atualizacao = atualizacao;
    registro.Snippet = (snippet.length() >= 100 && snippet.length() <= 1024) ? snippet : snippet.substr(0, 1024);
}

// Função global para exibir os dados de um registro
void exibirRegistro(const REGISTRO& registro) {
    cout << "ID: " << registro.ID << endl;
    cout << "Título: " << registro.Titulo << endl;
    cout << "Ano: " << registro.Ano << endl;
    cout << "Autores: " << registro.Autores << endl;
    cout << "Citações: " << registro.Citacoes << endl;
    cout << "Última Atualização: " << registro.Atualizacao << endl;
    cout << "Snippet: " << registro.Snippet << endl;
}
int main() {
    string nome_arquivo;

    // Solicitar o nome do arquivo ao usuário
    cout << "Digite o nome do arquivo CSV: ";
    cin >> nome_arquivo;

    // Abrir o arquivo CSV
    ifstream file(nome_arquivo);
    if (!file.is_open()) {
        cerr << "Erro ao abrir o arquivo!" << endl;
        return 1;
    }

    string linha;
    vector<REGISTRO> registros;

    // Ler o arquivo linha por linha
    while (getline(file, linha)) {
        stringstream ss(linha);
        string valor;
        vector<string> linha_dados;

        // Separar os valores por ponto e vírgula e remover as aspas duplas
        while (getline(ss, valor, ';')) {
            if (!valor.empty() && valor[0] == '"') {
                valor = valor.substr(1, valor.length() - 2);  // Remove aspas duplas
            }
            linha_dados.push_back(valor);
        }

        // Certificar-se de que temos a quantidade correta de dados (7 colunas)
        if (linha_dados.size() == 7) {
            REGISTRO registro;
            // Inicializar o registro com os valores lidos do CSV
            inicializarRegistro(registro, linha_dados[0], linha_dados[1], linha_dados[2], linha_dados[3], linha_dados[4], linha_dados[5], linha_dados[6]);
            registros.push_back(registro); // Adicionar o registro à lista de registros
        } else {
            cerr << "Formato inválido na linha: " << linha << endl;
        }
    }

    // Fechar o arquivo
    file.close();

    // Exibir os registros lidos
    for (const auto& registro : registros) {
        exibirRegistro(registro);
        cout << endl;
    }

    return 0;
}
