#!/usr/bin/env python3
import os
import sys
import argparse
import datetime
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Aviso: 'python-dotenv' não está instalado. Usando variáveis de ambiente do sistema.")

try:
    import markdown
except ImportError:
    print("Erro: A biblioteca 'markdown' é necessária para converter o resultado do Copilot.")
    print("Execute 'pip install markdown' ou use o Makefile.")
    sys.exit(1)


def get_formatted_date():
    """Retorna a data atual formatada de forma elegante em português."""
    months = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    today = datetime.date.today()
    return f"{today.day} de {months[today.month]} de {today.year}"


def parse_arguments():
    """Configura e analisa os argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Daily Bread - Gerador e Enviador de Newsletter Cristã Local"
    )
    parser.add_argument(
        "--prompt", "-p",
        default="devocional",
        help="Nome do arquivo de prompt na pasta prompts/ (sem extensão). Padrão: devocional"
    )
    parser.add_argument(
        "--template", "-t",
        default="devocional",
        help="Nome do arquivo de template na pasta templates/ (sem extensão). Padrão: devocional"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Força a execução mesmo se a edição de hoje já tiver sido gerada."
    )
    return parser.parse_args()


def check_already_run(date_str, force=False):
    """Valida se o script já foi executado hoje, checando o histórico em logs/."""
    log_file = os.path.join("logs", f"{date_str}.html")
    if os.path.exists(log_file):
        if force:
            print(f"Aviso: A edição de hoje ({log_file}) já existe, mas a execução foi forçada.")
            return True
        else:
            print(f"Erro de Validação: O e-mail de hoje já foi gerado e enviado! ({log_file})")
            print("Para forçar o envio e sobrescrever, execute com '--force' (ou 'make force').")
            return False
    return True


def execute_copilot(prompt_path):
    """Lê o arquivo de prompt e executa o Copilot CLI para gerar o conteúdo."""
    if not os.path.exists(prompt_path):
        print(f"Erro: Arquivo de prompt não encontrado em: {prompt_path}")
        sys.exit(1)

    print(f"Lendo prompt de: {prompt_path}...")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_content = f.read().strip()

    print("Executando o Copilot CLI (isso pode levar alguns instantes)...")
    
    # Executa copilot com as flags para não interagir e rodar silenciosamente
    cmd = [
        "copilot",
        "-s",  # silent: apenas o output do agente
        "-p", prompt_content,
        "--no-ask-user",
        "--yolo"
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        output_text = result.stdout.strip()
        if not output_text:
            print("Erro: Copilot CLI retornou uma resposta vazia.")
            sys.exit(1)
            
        print("Conteúdo gerado pelo Copilot com sucesso!")
        return output_text
        
    except subprocess.CalledProcessError as e:
        print("Erro crítico ao executar o Copilot CLI!")
        print(f"Código de saída: {e.returncode}")
        print(f"Stderr: {e.stderr}")
        print(f"Stdout: {e.stdout}")
        sys.exit(1)
    except FileNotFoundError:
        print("Erro: O executável 'copilot' não foi encontrado no PATH do sistema.")
        print("Certifique-se de que o Copilot CLI está instalado globalmente.")
        sys.exit(1)


def compile_newsletter(content_markdown, template_path, date_display):
    """Converte o Markdown em HTML e injeta no template escolhido."""
    if not os.path.exists(template_path):
        print(f"Erro: Arquivo de template não encontrado em: {template_path}")
        sys.exit(1)

    # Converter o markdown gerado pelo copilot para HTML
    print("Convertendo Markdown para HTML...")
    # Habilitamos tabelas e cercas de código (fenced code blocks) no parser de markdown
    content_html = markdown.markdown(
        content_markdown,
        extensions=["tables", "fenced_code"]
    )

    print(f"Carregando template de: {template_path}...")
    with open(template_path, "r", encoding="utf-8") as f:
        template_html = f.read()

    # Injeta a data formatada e o conteúdo convertido nos placeholders do template
    compiled_html = template_html.replace("{{date}}", date_display)
    compiled_html = compiled_html.replace("{{content}}", content_html)

    return compiled_html


def save_log(html_content, date_str):
    """Salva o HTML gerado na pasta de logs."""
    os.makedirs("logs", exist_ok=True)
    log_file = os.path.join("logs", f"{date_str}.html")
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Histórico salvo com sucesso em: {log_file}")
    return log_file


def send_email(html_content):
    """Envia o e-mail HTML via SMTP usando as configurações do .env."""
    print("Preparando envio de e-mail...")
    
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    smtp_use_tls = os.getenv("SMTP_USE_TLS", "True").lower() in ("true", "1", "yes")

    email_from = os.getenv("EMAIL_FROM")
    email_to = os.getenv("EMAIL_TO")
    email_subject = os.getenv("EMAIL_SUBJECT", "Daily Bread - Edição de Hoje")

    if not all([smtp_host, smtp_port, smtp_user, smtp_pass, email_to]):
        print("Erro: Configurações de SMTP ou Destinatário incompletas no arquivo .env!")
        print("Por favor, preencha o arquivo .env com suas credenciais SMTP.")
        sys.exit(1)

    smtp_port = int(smtp_port)

    # Configuração da mensagem MIME
    msg = MIMEMultipart("alternative")
    msg["Subject"] = email_subject
    msg["From"] = email_from if email_from else smtp_user
    msg["To"] = email_to

    # Anexa o conteúdo HTML
    msg.attach(MIMEText(html_content, "html"))

    try:
        print(f"Conectando ao servidor SMTP {smtp_host}:{smtp_port}...")
        
        # Conexão SSL direta na porta 465, ou normal com STARTTLS na 587/outras
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port)
            if smtp_use_tls:
                print("Iniciando conexão segura TLS (STARTTLS)...")
                server.starttls()

        if smtp_user and smtp_pass:
            print(f"Autenticando usuário {smtp_user}...")
            server.login(smtp_user, smtp_pass)

        print(f"Enviando e-mail para: {email_to}...")
        server.sendmail(msg["From"], [email_to], msg.as_string())
        server.quit()
        
        print("E-mail enviado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro crítico ao enviar o e-mail: {e}")
        return False


def main():
    args = parse_arguments()
    
    today_iso = datetime.date.today().isoformat()
    date_display = get_formatted_date()
    
    # 1. Validação de Execução Diária
    if not check_already_run(today_iso, force=args.force):
        sys.exit(0)  # Sai pacificamente para evitar quebra em rotinas automáticas (cron)

    # Define os caminhos dos arquivos baseados nos argumentos
    prompt_file = os.path.join("prompts", f"{args.prompt}.md")
    template_file = os.path.join("templates", f"{args.template}.html")

    # 2. Executa o Copilot CLI
    markdown_content = execute_copilot(prompt_file)

    # 3. Compila o HTML
    html_content = compile_newsletter(markdown_content, template_file, date_display)

    # 4. Salva no Histórico (logs/)
    save_log(html_content, today_iso)

    # 5. Envia o E-mail via SMTP
    success = send_email(html_content)
    
    if success:
        print("Processo concluído com êxito absoluto!")
    else:
        print("Newsletter gerada e registrada, porém houve erro no envio do e-mail.")
        sys.exit(1)


if __name__ == "__main__":
    main()
