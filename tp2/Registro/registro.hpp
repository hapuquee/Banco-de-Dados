#ifndef REGISTRO_HPP  
#define REGISTRO_HPP

#include <string>
#include <iostream>

using namespace std;

struct REGISTRO {
    int ID;
    string Titulo;
    int Ano;
    string Autores;
    int Citacoes;
    string Atualizacao;
    string Snippet;
};

void criarRegistro(REGISTRO& registro, const int& id, const string& titulo, 
                   const int& ano, const string& autores, 
                   const int& citacoes, const string& atualizacao, 
                   const string& snippet);

void exibirRegistro(const REGISTRO& registro);

#endif // REGISTRO_HPP
