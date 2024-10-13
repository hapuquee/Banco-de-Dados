#ifndef BLOCK_SIZE_H
#define BLOCK_SIZE_H

#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/fs.h> // BLKSSZGET e BLKPBSZGET

// Função que retorna o tamanho do bloco lógico de um dispositivo
unsigned int getBlockSize(const char* device) {
    int fd = open(device, O_RDONLY);
    if (fd == -1) {
        std::cerr << "Erro ao abrir o dispositivo: " << device << std::endl;
        return 0;
    }

    // Variável para armazenar o tamanho do bloco
    unsigned int block_size;

    // Obter o tamanho do setor lógico
    if (ioctl(fd, BLKBSZGET, &block_size) == -1) {
        std::cerr << "Erro ao obter o tamanho do setor lógico." << std::endl;
        close(fd);
        return 0;
    }

    close(fd);
    return block_size;
}

#endif
