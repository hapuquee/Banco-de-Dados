#include <iostream>
#include <cstdio>
#include <memory>
#include <stdexcept>
#include <string>
#include <array>

std::string execCommand(const char* cmd) {
    std::array<char, 128> buffer;
    std::string result;
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd, "r"), pclose);
    if (!pipe) {
        throw std::runtime_error("Falha ao executar comando.");
    }
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}

const char* getDeviceName() {
    std::string output = execCommand("sudo fdisk -l");
    std::string vazio = "";

    // Exemplo de parse simples para encontrar o primeiro dispositivo listado
    // Neste exemplo, assumimos que o nome do dispositivo é algo como "/dev/sda"
    size_t pos = output.find("/dev/");
    std::cout << pos << '\n'; 
    if (pos != std::string::npos) {
        std::string device = output.substr(pos, 12); // Captura "/dev/sda" ou algo semelhante
        std::cout << device << '\n';
        return device.c_str();
    }
    return vazio.c_str();
}


