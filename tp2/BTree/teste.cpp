
#include "block_size.h"
#include "device_name.h"
#include "string"

int main() {
    const char *device = getDeviceName();// Substitua pelo seu dispositivo
    std::cout << "device: " << device << '\n';
    unsigned int block_size = getBlockSize(device);

    if (block_size > 0) {
        std::cout << "Tamanho do bloco (setor lógico) em " << device << ": " << block_size << " bytes" << std::endl;
    } else {
        std::cerr << "Falha ao obter o tamanho do bloco." << std::endl;
    }

    return 0;
}
