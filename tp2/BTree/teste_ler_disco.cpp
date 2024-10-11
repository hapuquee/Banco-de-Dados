#include <iostream>
#include <fstream>

using namespace std;

int main(int argc, char** argv){
    ifstream file("btree.dat",ios::binary);

    file.seekg(0, ios::end);
    streamsize size = file.tellg();
    file.seekg(0, ios::beg);

    char* buffer = new char[size];

    if(file.read(buffer, size)){
        cout.write(buffer, size);
    }else{
        cerr << "erro ao ler o arquivo" << endl;
    }

    delete[] buffer;
    file.close();

    return 0;
}