#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

using namespace std;

int main() {
    string nome_arquivo;
    
    // Solicitar o nome do arquivo ao usuário
    cout << "Digite o nome do arquivo CSV: ";
    cin >> nome_arquivo;

    // Abrir o arquivo
    ifstream file(nome_arquivo);
    if (!file.is_open()) {
        cerr << "Erro ao abrir o arquivo!" << endl;
        return 1;
    }

    string linha;
    vector<vector<string>> dados;

    // Ler o arquivo linha por linha
    while (getline(file, linha)) {
        stringstream ss(linha);
        string valor;
        vector<string> linha_dados;

        

        // Separar os valores por vírgula
        while (getline(ss, valor, ';')) {
            linha_dados.push_back(valor);
            cout<<"valor: " << valor<<endl;
            
        }
        cout<< endl;
        dados.push_back(linha_dados); // Adiciona a linha ao vetor de dados
    }

    // Fechar o arquivo
    file.close();

    // Exibir os dados lidos
    for (const auto& linha : dados) {
        for (const auto& valor : linha) {
            cout << valor << " ";
        }
        cout << endl;
    }

    return 0;
}
