#include <registro.hpp>

// Função global para inicializar um registro a partir de strings
void criarRegistro(REGISTRO& registro, const int& id, const string& titulo, const int& ano, const string& autores, const int& citacoes, const string& atualizacao, const string& snippet) {
    try {
        registro.ID = id;
    } catch (invalid_argument& e) {
        cerr << "Erro ao converter ID: " << id << endl;
        registro.ID = 0;
    }

    registro.Titulo = titulo.length() <= 300 ? titulo : titulo.substr(0, 300);
    try {
        registro.Ano = ano;
    } catch (invalid_argument& e) {
        cerr << "Erro ao converter Ano: " << ano << endl;
        registro.Ano = 0;
    }

    registro.Autores = autores.length() <= 150 ? autores : autores.substr(0, 150);
    try {
        registro.Citacoes = citacoes;
    } catch (invalid_argument& e) {
        cerr << "Erro ao converter Citações: " << citacoes << endl;
        registro.Citacoes = 0;
    }

    registro.Atualizacao = atualizacao;
    registro.Snippet = (snippet.length() >= 100 && snippet.length() <= 1024) ? snippet : snippet.substr(0, 1024);
}

// Função global para exibir os dados de um registro
void exibirRegistro(const REGISTRO& registro) {
    cout<<endl;
    cout << "ID: " << registro.ID << endl;
    cout << "Título: " << registro.Titulo << endl;
    cout << "Ano: " << registro.Ano << endl;
    cout << "Autores: " << registro.Autores << endl;
    cout << "Citações: " << registro.Citacoes << endl;
    cout << "Última Atualização: " << registro.Atualizacao << endl;
    cout << "Snippet: " << registro.Snippet << endl;
    cout<<endl;
}
