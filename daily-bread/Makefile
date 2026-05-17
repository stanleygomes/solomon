# Daily Bread - Makefile de Automação

# Detecta se existe ambiente virtual local, caso contrário usa o python do sistema
PYTHON = $(shell [ -d venv ] && echo "venv/bin/python" || echo "python3")

# Parâmetros padrão (podem ser sobrescritos na chamada do comando)
PROMPT ?= devocional
TEMPLATE ?= devocional
FORCE ?= 0

# Configura as flags para passar ao script python
FLAGS = --prompt $(PROMPT) --template $(TEMPLATE)

ifeq ($(FORCE), 1)
FLAGS += --force
endif

.PHONY: run force list setup help

# Comando padrão para rodar a newsletter do dia
run:
	@$(PYTHON) send_newsletter.py $(FLAGS)

# Comando curto para forçar a execução se já tiver sido gerada hoje
force:
	@$(PYTHON) send_newsletter.py $(FLAGS) --force

# Instala as dependências Python necessárias criando um ambiente virtual local
setup:
	@echo "Criando ambiente virtual local (venv)..."
	@python3 -m venv venv
	@echo "Instalando dependências no ambiente virtual..."
	@venv/bin/pip install -r requirements.txt
	@echo "Pronto! Configuração concluída com sucesso."

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
	@echo "                 DAILY BREAD - NEWSLETTER SISTEMA LOCAL"
	@echo "=========================================================================="
	@echo "Comandos úteis:"
	@echo "  make setup                       - Instala as bibliotecas de dependência."
	@echo "  make list                        - Exibe todos os prompts e templates atuais."
	@echo "  make run                         - Executa a newsletter padrão do dia (devocional)."
	@echo "  make force                       - Executa a newsletter padrão forçando a sobrescrita."
	@echo "  make run PROMPT=personagem TEMPLATE=personagem"
	@echo "                                   - Roda estudo de personagem específico."
	@echo "  make force PROMPT=versiculo TEMPLATE=versiculo"
	@echo "                                   - Roda estudo de versículo forçando re-envio."
	@echo "=========================================================================="
