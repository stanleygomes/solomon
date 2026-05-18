# Daily Bread - Makefile de Automação (Versão Go)

# Parâmetros padrão (podem ser sobrescritos na chamada do comando)
PROMPT ?= devocional
TEMPLATE ?= devocional
FORCE ?= 0

# Configura as flags para passar ao executável Go
FLAGS = -prompt $(PROMPT) -template $(TEMPLATE)

ifeq ($(FORCE), 1)
FLAGS += -force
endif

.PHONY: run force build list setup help

# Comando padrão para compilar e rodar a newsletter do dia
run:
	@go run main.go $(FLAGS)

# Comando curto para forçar a execução se já tiver sido gerada hoje
force:
	@go run main.go $(FLAGS) -force

# Compila o executável binário otimizado
build:
	@echo "Compilando o binário Go..."
	@go build -o daily-bread main.go
	@echo "Pronto! Binário 'daily-bread' gerado com sucesso."

# Instala/baixa as dependências do módulo Go
setup:
	@echo "Obtendo dependências do Go..."
	@go mod download
	@go mod tidy
	@echo "Pronto! Dependências Go configuradas com sucesso."

# Lista de forma dinâmica os prompts e templates disponíveis
list:
	@echo "=================================================="
	@echo "  PROMPTS DISPONÍVEIS (pasta prompts/)"
	@echo "=================================================="
	@ls -1 prompts/ | sed 's/\.md//' | sed 's/^/ - /'
	@echo ""
	@echo "=================================================="
	@echo "  TEMPLATES DISPONÍVEIS (pasta templates/)"
	@echo "=================================================="
	@ls -1 templates/ | sed 's/\.html//' | sed 's/^/ - /'
	@echo "=================================================="
	@echo "Para executar um par específico, use:"
	@echo "make run PROMPT=<nome> TEMPLATE=<nome>"

# Exibe ajuda sobre o uso do Makefile
help:
	@echo "=========================================================================="
	@echo "                 DAILY BREAD - NEWSLETTER SISTEMA LOCAL (GO)"
	@echo "=========================================================================="
	@echo "Comandos úteis:"
	@echo "  make setup                       - Baixa e limpa as dependências Go."
	@echo "  make build                       - Compila o projeto em um binário local."
	@echo "  make list                        - Exibe todos os prompts e templates atuais."
	@echo "  make run                         - Executa a newsletter padrão do dia (devocional)."
	@echo "  make force                       - Executa a newsletter padrão forçando a sobrescrita."
	@echo "  make run PROMPT=personagem TEMPLATE=personagem"
	@echo "                                   - Roda estudo de personagem específico."
	@echo "  make force PROMPT=versiculo TEMPLATE=versiculo"
	@echo "                                   - Roda estudo de versículo forçando re-envio."
	@echo "=========================================================================="
