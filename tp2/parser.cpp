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

// Função para remover aspas e ignorar o resto se encontrar ";"
std::string remover_aspas_input(const std::string& entrada) {
    std::string resultado;

    for (size_t i = 0; i < entrada.length(); ++i) {
        if (entrada[i] == '"' && i + 1 < entrada.length() && entrada[i + 1] == ';') {
            break; // Para se encontrar aspas seguidas de ponto e vírgula
        }
        resultado += entrada[i];
    }

    return resultado;
}

// Função para remover aspas em um stream de entrada
void remover_aspas(std::istream& stream, std::string& resultado) {
    resultado.clear();
    char ch;

    while (stream.get(ch)) {
        if (ch == '"' && stream.peek() == ';') {
            stream.get(); // Consome o próximo caractere (;) e sai do loop
            break;
        }
        resultado += ch;
    }
}

// Função para normalizar uma string (remove caracteres inválidos, múltiplos espaços)
std::string normalizar_string(std::string str) {
    // Substitui caracteres não ASCII, novas linhas e aspas por espaços
    for (char &c : str) {
        if (static_cast<unsigned char>(c) > 127 || c == '\n' || c == '\"') {
            c = ' ';
        }
    }

    // Remove espaços extras
    std::string resultado;
    bool inSpace = false;

    for (char c : str) {
        if (std::isspace(static_cast<unsigned char>(c))) {
            if (!inSpace) {
                resultado += ' ';
                inSpace = true;
            }
        } else {
            resultado += c;
            inSpace = false;
        }
    }

    // Remove espaços no início e fim
    size_t start = resultado.find_first_not_of(' ');
    if (start == std::string::npos) return ""; // String apenas contém espaços

    size_t end = resultado.find_last_not_of(' ');
    return resultado.substr(start, end - start + 1);
}

void ler_arquivo_csv(const string& nome_arquivo)
{
    ifstream arquivo(nome_arquivo, ios::in);
    
    if (!arquivo.is_open())
    {
        cerr << "Nao foi possivel abrir o arquivo: " << nome_arquivo << "\n";
        return;
    }

    string linha;
    while (getline(arquivo, linha))
    {
        stringstream linha_analisada(linha);
        string dado;

        int id, year, citations;
        string title, authors, update, snippet;

        try
        {
            // atualiza o campo id apos a remocao das aspas
            getline(linha_analisada, dado, '"');
            remover_aspas(linha_analisada, dado);
            id = stoi(dado);

            // atualiza o campo titulo apos a remocao das aspas
            getline(linha_analisada, dado, '"');
            remover_aspas(linha_analisada, dado);
            title = dado;

            // atualiza o campo ano apos a remocao das aspas
            getline(linha_analisada, dado, '"');
            remover_aspas(linha_analisada, dado);
            year = stoi(dado);

            // atualiza o campo autores após a remocao das aspas
            getline(linha_analisada, dado, '"');
            remover_aspas(linha_analisada, dado);
            authors = dado;

            // atualiza o campo citacoes apos a remocao das aspas
            getline(linha_analisada, dado, '"');
            remover_aspas(linha_analisada, dado);
            citations = stoi(dado);

            // atualiza o campo update apos a remocao das aspas
            getline(linha_analisada, dado, '"');
            remover_aspas(linha_analisada, dado);
            update = dado;

            // atualiza o snippet apos a remocao das aspas
            getline(linha_analisada, dado, '"');
            remover_aspas(linha_analisada, dado);
            snippet = dado;

            // normaliza todas as strings
            title = normalizar_string(title);
            authors = normalizar_string(authors);
            update = normalizar_string(update);
            snippet = normalizar_string(snippet);

            cout << title << endl;

          /*   Registro* novo_registro = criar_registro(id, title, year, authors, citations, update, snippet);
            size_t posicao = hash.inserir_registro_bucket(novo_registro);

            RegistroBPT* reg1 = new RegistroBPT(id, posicao);
            RegistroString* reg2 = new RegistroString(title, posicao);

            arvore1.inserir_arvore(reg1);
            arvore2.inserir_arvore_s(reg2);
            
            delete novo_registro; */
        } 
        catch (const std::exception& e)
        {
            //std::cerr << "Caught an exception: " << e.what() << " " << id << std::endl;
        }
    }
    arquivo.close();

    return;
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
