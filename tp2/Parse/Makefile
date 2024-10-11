# Nome do executável
EXECUTABLE = parser

# Compilador
CXX = g++

# Diretórios
REGISTRO_DIR = ../Registro

# Arquivos fonte
SRC = parser.cpp
REGISTRO_SRC = $(REGISTRO_DIR)/registro.cpp

# Flags do compilador
CXXFLAGS = -I$(REGISTRO_DIR)

# Regra padrão
all: $(EXECUTABLE)

# Regra para compilar o executável
$(EXECUTABLE): $(SRC) $(REGISTRO_SRC)
	$(CXX) $(CXXFLAGS) $(SRC) $(REGISTRO_SRC) -o $(EXECUTABLE)

# Limpar arquivos gerados
clean:
	rm -f $(EXECUTABLE)
