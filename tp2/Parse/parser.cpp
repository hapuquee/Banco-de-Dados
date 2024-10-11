#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>
#include <cctype>
#include <algorithm>
#include <../Registro/registro.hpp>

using namespace std;

// Função para remover aspas em um stream de entrada
//quot -> aspas
void clean_quot(istream& stream, string& resultado) {
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
string format_str(string str) {
    // Remove caracteres não ASCII, novas linhas e aspas
    str.erase(remove_if(str.begin(), str.end(), [](unsigned char c) {
        return c > 127 || c == '\n' || c == '\"';
    }), str.end());

    // Remove múltiplos espaços
    auto new_end = unique(str.begin(), str.end(), [](char left, char right) {
        return isspace(static_cast<unsigned char>(left)) && isspace(static_cast<unsigned char>(right));
    });
    str.erase(new_end, str.end());

    // Remove espaços no início e no fim
    str.erase(0, str.find_first_not_of(' '));  // Remove espaços do início
    str.erase(str.find_last_not_of(' ') + 1);  // Remove espaços do fim

    return str;
}

void ler_arquivo_csv(const string& nome_arquivo)
{
    ifstream arquivo(nome_arquivo, ios::in);
    
    if (!arquivo.is_open())
    {
        cerr << "Nao foi possivel abrir o arquivo: " << nome_arquivo << "\n";
        return;
    }
    int id_str =0 ;

    string linha;
    while (getline(arquivo, linha))
    {
        id_str++;
        stringstream linha_analisada(linha);
        string dado;
    
        int id, year, citations;
        string title, authors, update, snippet;

        try
        {
            // atualiza o campo id apos a remocao das aspas
            getline(linha_analisada, dado, '"');
            clean_quot(linha_analisada, dado);
            id = stoi(dado);

            // atualiza o campo titulo apos a remocao das aspas
            getline(linha_analisada, dado, '"');
            clean_quot(linha_analisada, dado);
            title = dado;

            // atualiza o campo ano apos a remocao das aspas
            getline(linha_analisada, dado, '"');
            clean_quot(linha_analisada, dado);
            year = stoi(dado);

            // atualiza o campo autores após a remocao das aspas
            getline(linha_analisada, dado, '"');
            clean_quot(linha_analisada, dado);
            authors = dado;

            // atualiza o campo citacoes apos a remocao das aspas
            getline(linha_analisada, dado, '"');
            clean_quot(linha_analisada, dado);
            citations = stoi(dado);

            // atualiza o campo update apos a remocao das aspas
            getline(linha_analisada, dado, '"');
            clean_quot(linha_analisada, dado);
            update = dado;

            // atualiza o snippet apos a remocao das aspas
            getline(linha_analisada, dado, '"');
            clean_quot(linha_analisada, dado);
            snippet = dado;

            // normaliza todas as strings
            title = format_str(title);
            authors = format_str(authors);
            update = format_str(update);
            snippet = format_str(snippet);

            REGISTRO registro;
            try{
                criarRegistro(registro, id, title, year,authors,citations,update,snippet);
                //exibirRegistro(registro);
            }
            catch(const invalid_argument& e){
                cerr<< "ERRO AO CRIAR REGISTRO NA LINHA: " << id<< endl;
            }

          /*   Registro* novo_registro = criar_registro(id, title, year, authors, citations, update, snippet);
            size_t posicao = hash.inserir_registro_bucket(novo_registro);

            RegistroBPT* reg1 = new RegistroBPT(id, posicao);
            RegistroString* reg2 = new RegistroString(title, posicao);

            arvore1.inserir_arvore(reg1);
            arvore2.inserir_arvore_s(reg2);
            
            delete novo_registro; */
        } catch (const invalid_argument& e) {
            //cout << "Erro de conversão na linha: " << id_str << endl;
            continue; // Pula para a próxima linha em caso de erro
        } catch (const out_of_range& e) {
            //cout << "Valor fora do intervalo na linha: " << id_str << endl;
            continue;
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
    ler_arquivo_csv(nome_arquivo);

    return 0;
}
