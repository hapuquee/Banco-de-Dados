
#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>
using namespace std;

template <typename T>
class BPlusTree {
public:
    // Estrutura de um nó
    struct Node {
        bool isLeaf;
        vector<T> keys;
        vector<int> children;  // IDs dos filhos (endereço no disco)
        int next;              // ID do próximo nó folha

        Node(bool leaf = false) : isLeaf(leaf), next(-1) {}

        // Serializa o nó para um arquivo binário
        void serialize(ofstream &out) {
            out.write(reinterpret_cast<char*>(&isLeaf), sizeof(isLeaf));
            int keysSize = keys.size();
            out.write(reinterpret_cast<char*>(&keysSize), sizeof(keysSize));
            for (const auto& key : keys) {
                out.write(reinterpret_cast<const char*>(&key), sizeof(key));
            }
            int childrenSize = children.size();
            out.write(reinterpret_cast<char*>(&childrenSize), sizeof(childrenSize));
            for (const auto& child : children) {
                out.write(reinterpret_cast<const char*>(&child), sizeof(child));
            }
            out.write(reinterpret_cast<char*>(&next), sizeof(next));
        }

        // Desserializa o nó a partir de um arquivo binário
        void deserialize(ifstream &in) {
            in.read(reinterpret_cast<char*>(&isLeaf), sizeof(isLeaf));
            int keysSize;
            in.read(reinterpret_cast<char*>(&keysSize), sizeof(keysSize));
            keys.resize(keysSize);
            for (int i = 0; i < keysSize; ++i) {
                in.read(reinterpret_cast<char*>(&keys[i]), sizeof(keys[i]));
            }
            int childrenSize;
            in.read(reinterpret_cast<char*>(&childrenSize), sizeof(childrenSize));
            children.resize(childrenSize);
            for (int i = 0; i < childrenSize; ++i) {
                in.read(reinterpret_cast<char*>(&children[i]), sizeof(children[i]));
            }
            in.read(reinterpret_cast<char*>(&next), sizeof(next));
        }
    };

private:
    Node* root;              // Ponteiro para a raiz
    int t;                   // Grau mínimo da árvore
    string filename;         // Nome do arquivo para armazenamento no disco
    int nodeCounter;         // Contador para IDs de nós

public:
    BPlusTree(int degree, const string &fname) : root(nullptr), t(degree), filename(fname), nodeCounter(0) {}

    // Salva um nó no disco e retorna sua posição (ID)
    int saveNodeToDisk(Node* node) {
        ofstream file(filename, ios::binary | ios::app);
        int pos = file.tellp();  // Posição no arquivo (ID do nó)
        node->serialize(file);
        file.close();
        return pos;
    }

    // Carrega um nó do disco a partir de uma posição (ID)
    Node* loadNodeFromDisk(int pos) {
        ifstream file(filename, ios::binary);
        file.seekg(pos);
        Node* node = new Node();
        node->deserialize(file);
        file.close();
        return node;
    }

    // Função para dividir um nó filho
    void splitChild(Node* parent, int index, int childId) {
        Node* child = loadNodeFromDisk(childId);
        Node* newChild = new Node(child->isLeaf);

        // Divide as chaves
        newChild->keys.assign(child->keys.begin() + t, child->keys.end());
        child->keys.resize(t - 1);

        // Se não for folha, divide os filhos
        if (!child->isLeaf) {
            newChild->children.assign(child->children.begin() + t, child->children.end());
            child->children.resize(t);
        }

        // Atualiza as ligações entre folhas
        if (child->isLeaf) {
            newChild->next = child->next;
            child->next = nodeCounter;
        }

        // Atualiza o pai com a nova chave e novo filho
        parent->keys.insert(parent->keys.begin() + index, child->keys[t - 1]);
        parent->children.insert(parent->children.begin() + index + 1, nodeCounter);

        // Salva os nós no disco
        saveNodeToDisk(child);
        saveNodeToDisk(newChild);
        nodeCounter++;
    }

    // Função para inserir uma chave em um nó não cheio
    void insertNonFull(Node* node, int nodeId, T key) {
        if (node->isLeaf) {
            node->keys.insert(upper_bound(node->keys.begin(), node->keys.end(), key), key);
            saveNodeToDisk(node);  // Grava a mudança no disco
        } else {
            int i = node->keys.size() - 1;
            while (i >= 0 && key < node->keys[i]) i--;

            i++;
            Node* child = loadNodeFromDisk(node->children[i]);
            if (child->keys.size() == 2 * t - 1) {
                splitChild(node, i, node->children[i]);
                if (key > node->keys[i]) i++;
            }

            insertNonFull(loadNodeFromDisk(node->children[i]), node->children[i], key);
            saveNodeToDisk(node);  // Grava o nó atual no disco
        }
    }

    // Função de inserção
    void insert(T key) {
      cout << "inserindo" << "\n"; 
        if (!root) {
            root = new Node(true);
            root->keys.push_back(key);
            nodeCounter = 1;
            saveNodeToDisk(root);  // Salva o nó raiz no disco
        } else {
            if (root->keys.size() == 2 * t - 1) {
                Node* newRoot = new Node();
                newRoot->children.push_back(nodeCounter);
                splitChild(newRoot, 0, nodeCounter - 1);
                root = newRoot;
                nodeCounter++;
                saveNodeToDisk(root);  // Salva a nova raiz
            }
            insertNonFull(root, nodeCounter - 1, key);
        }
    }

    // Função de busca
    bool search(T key) {
        Node* current = root;
        while (current != nullptr) {
            int i = 0;
            while (i < current->keys.size() && key > current->keys[i]) i++;

            if (i < current->keys.size() && key == current->keys[i]) {
                return true;
            }

            if (current->isLeaf) {
                return false;
            }

            current = loadNodeFromDisk(current->children[i]);
        }
        return false;
    }

    // Função para consulta de intervalo
    vector<T> rangeQuery(T lower, T upper) {
        vector<T> result;
        Node* current = root;

        // Encontrar a folha inicial
        while (!current->isLeaf) {
            int i = 0;
            while (i < current->keys.size() && lower > current->keys[i]) i++;
            current = loadNodeFromDisk(current->children[i]);
        }

        // Realiza a varredura em folhas até o limite superior
        while (current != nullptr) {
            for (const T& key : current->keys) {
                if (key >= lower && key <= upper) {
                    result.push_back(key);
                }
                if (key > upper) {
                    return result;
                }
            }
            current = loadNodeFromDisk(current->next);  // Vai para a próxima folha
        }
        return result;
    }

    // Função auxiliar para imprimir a árvore (somente para depuração)
    void printTree(Node* node, int level) {
        if (node != nullptr) {
            for (int i = 0; i < level; ++i) {
                cout << "  ";
            }
            for (const T& key : node->keys) {
                cout << key << " ";
            }
            cout << endl;
            for (int i = 0; i < node->children.size(); ++i) {
                Node* child = loadNodeFromDisk(node->children[i]);
                printTree(child, level + 1);
                delete child;  // Liberar a memória temporária
            }
        }
    }

    // Função de impressão da árvore
    void printTree() {
        printTree(root, 0);
    }
};

// Função principal
int main() {
    BPlusTree<int> tree(3, "btree.dat");

    // Insere elementos
    tree.insert(10);
    tree.insert(20);
    tree.insert(5);
    tree.insert(15);
    tree.insert(25);
    tree.insert(30);


    cout << "B+ Tree após inserções:" << endl;
    tree.printTree();

    // Busca um elemento
    int searchKey = 15;
    cout << "\nBuscando chave " << searchKey << ": "
         << (tree.search(searchKey) ? "Encontrado" : "Não Encontrado") << endl;

    // Consulta de intervalo
    int lower = 10, upper = 25;
    vector<int> rangeResult = tree.rangeQuery(lower, upper);
    cout << "\nConsulta de intervalo [" << lower << ", " << upper << "]: ";
    for (int key : rangeResult) {
        cout << key << " ";
    }
    cout << endl;

    return 0;
}
