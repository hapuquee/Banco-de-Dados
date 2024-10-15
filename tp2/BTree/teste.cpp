
#include "block_size.hpp"
#include "device_name.hpp"
#include "string"

int main() {
    const char *device = "/dev/sda6";// Substitua pelo seu dispositivo
    std::cout << "device: " << device << '\n';
    unsigned int block_size = getBlockSize(device);

    if (block_size > 0) {
        std::cout << "Tamanho do bloco (setor lógico) em " << device << ": " << block_size << " bytes" << std::endl;
    } else {
        std::cerr << "Falha ao obter o tamanho do bloco." << std::endl;
    }

    return 0;
}
