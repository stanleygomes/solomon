package main

import (
	"bytes"
	"crypto/tls"
	"flag"
	"fmt"
	"io"
	"log"
	"net/smtp"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/joho/godotenv"
	"github.com/yuin/goldmark"
	"github.com/yuin/goldmark/extension"
	"github.com/yuin/goldmark/parser"
)

func getFormattedDate() string {
	months := map[time.Month]string{
		time.January:   "Janeiro",
		time.February:  "Fevereiro",
		time.March:     "Março",
		time.April:     "Abril",
		time.May:       "Maio",
		time.June:      "Junho",
		time.July:      "Julho",
		time.August:    "Agosto",
		time.September: "Setembro",
		time.October:   "Outubro",
		time.November:  "Novembro",
		time.December:  "Dezembro",
	}
	now := time.Now()
	return fmt.Sprintf("%d de %s de %d", now.Day(), months[now.Month()], now.Year())
}


func executeCopilot(promptPath string) (string, error) {
	if _, err := os.Stat(promptPath); os.IsNotExist(err) {
		return "", fmt.Errorf("arquivo de prompt não encontrado em: %s", promptPath)
	}

	fmt.Printf("Lendo prompt de: %s...\n", promptPath)
	promptBytes, err := os.ReadFile(promptPath)
	if err != nil {
		return "", fmt.Errorf("falha ao ler arquivo de prompt: %w", err)
	}
	promptContent := strings.TrimSpace(string(promptBytes))

	if filepath.Base(promptPath) != "_base.md" {
		basePromptPath := filepath.Join(filepath.Dir(promptPath), "_base.md")
		if _, err := os.Stat(basePromptPath); err == nil {
			fmt.Printf("Mesclando com o prompt base de: %s...\n", basePromptPath)
			baseBytes, err := os.ReadFile(basePromptPath)
			if err == nil {
				baseContent := strings.TrimSpace(string(baseBytes))
				if baseContent != "" {
					promptContent = baseContent + "\n\n" + promptContent
				}
			} else {
				fmt.Printf("Aviso: Falha ao ler arquivo de prompt base: %v\n", err)
			}
		}
	}

	fmt.Println("Executando o Copilot CLI (isso pode levar alguns instantes)...")
	
	// Executa copilot com as flags para não interagir e rodar silenciosamente
	cmd := exec.Command("copilot", "-s", "-p", promptContent, "--no-ask-user", "--yolo")
	
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	
	err = cmd.Run()
	if err != nil {
		return "", fmt.Errorf("erro crítico ao executar o Copilot CLI: %v\nStderr: %s\nStdout: %s", err, stderr.String(), stdout.String())
	}
	
	outputText := strings.TrimSpace(stdout.String())
	if outputText == "" {
		return "", fmt.Errorf("copilot CLI retornou uma resposta vazia")
	}
	
	fmt.Println("Conteúdo gerado pelo Copilot com sucesso!")
	return outputText, nil
}

func compileNewsletter(contentMarkdown, templatePath, dateDisplay string) (string, error) {
	if _, err := os.Stat(templatePath); os.IsNotExist(err) {
		return "", fmt.Errorf("arquivo de template não encontrado em: %s", templatePath)
	}

	log.Println("Convertendo Markdown para HTML...")
	
	// Configura o Goldmark com extensões GFM (inclui suporte a tabelas)
	md := goldmark.New(
		goldmark.WithExtensions(extension.GFM),
		goldmark.WithParserOptions(
			parser.WithAutoHeadingID(),
		),
	)
	
	var buf bytes.Buffer
	if err := md.Convert([]byte(contentMarkdown), &buf); err != nil {
		return "", fmt.Errorf("erro ao converter markdown: %w", err)
	}
	contentHTML := buf.String()

	log.Printf("Carregando template de: %s...", templatePath)
	templateBytes, err := os.ReadFile(templatePath)
	if err != nil {
		return "", fmt.Errorf("falha ao ler template: %w", err)
	}
	templateHTML := string(templateBytes)

	// Injeta placeholders
	compiledHTML := strings.ReplaceAll(templateHTML, "{{date}}", dateDisplay)
	compiledHTML = strings.ReplaceAll(compiledHTML, "{{content}}", contentHTML)

	return compiledHTML, nil
}

func saveLog(htmlContent, dateStr string) (string, error) {
	err := os.MkdirAll(filepath.Join("logs", "html"), 0755)
	if err != nil {
		return "", fmt.Errorf("falha ao criar pasta logs/html: %w", err)
	}
	
	logFile := filepath.Join("logs", "html", fmt.Sprintf("%s.html", dateStr))
	err = os.WriteFile(logFile, []byte(htmlContent), 0644)
	if err != nil {
		return "", fmt.Errorf("falha ao gravar log HTML: %w", err)
	}
	
	log.Printf("Histórico salvo com sucesso em: %s", logFile)
	return logFile, nil
}

func sendEmail(htmlContent string) error {
	log.Println("Preparando envio de e-mail...")
	
	host := os.Getenv("SMTP_HOST")
	portStr := os.Getenv("SMTP_PORT")
	user := os.Getenv("SMTP_USER")
	pass := os.Getenv("SMTP_PASSWORD")
	useTLS := strings.ToLower(os.Getenv("SMTP_USE_TLS")) != "false"

	emailFrom := os.Getenv("EMAIL_FROM")
	if emailFrom == "" {
		emailFrom = fmt.Sprintf("Pão Diário <%s>", user)
	}
	emailTo := os.Getenv("EMAIL_TO")
	emailSubject := os.Getenv("EMAIL_SUBJECT")
	if emailSubject == "" {
		emailSubject = "Pão Diário - Edição de Hoje"
	}

	if host == "" || portStr == "" || user == "" || pass == "" || emailTo == "" {
		return fmt.Errorf("configurações de SMTP ou Destinatário incompletas no arquivo .env")
	}

	// Constrói a mensagem MIME
	header := make(map[string]string)
	header["From"] = emailFrom
	header["To"] = emailTo
	header["Subject"] = emailSubject
	header["MIME-Version"] = "1.0"
	header["Content-Type"] = `text/html; charset="utf-8"`

	var msg bytes.Buffer
	for k, v := range header {
		msg.WriteString(fmt.Sprintf("%s: %s\r\n", k, v))
	}
	msg.WriteString("\r\n")
	msg.WriteString(htmlContent)

	addr := host + ":" + portStr
	auth := smtp.PlainAuth("", user, pass, host)

	log.Printf("Conectando ao servidor SMTP %s...", addr)
	
	if portStr == "465" {
		// Conexão direta SSL/TLS
		tlsconfig := &tls.Config{
			InsecureSkipVerify: false,
			ServerName:         host,
		}
		
		conn, err := tls.Dial("tcp", addr, tlsconfig)
		if err != nil {
			return fmt.Errorf("erro ao conectar via SSL/TLS: %w", err)
		}
		defer conn.Close()

		client, err := smtp.NewClient(conn, host)
		if err != nil {
			return fmt.Errorf("erro ao criar cliente SMTP: %w", err)
		}
		defer client.Close()

		if err = client.Auth(auth); err != nil {
			return fmt.Errorf("erro de autenticação SMTP: %w", err)
		}

		// Para o envelope SMTP (MAIL FROM), usamos o e-mail limpo (user)
		if err = client.Mail(user); err != nil {
			return fmt.Errorf("erro ao definir remetente: %w", err)
		}

		if err = client.Rcpt(emailTo); err != nil {
			return fmt.Errorf("erro ao definir destinatário: %w", err)
		}

		w, err := client.Data()
		if err != nil {
			return fmt.Errorf("erro ao iniciar transferência de dados: %w", err)
		}

		_, err = w.Write(msg.Bytes())
		if err != nil {
			return fmt.Errorf("erro ao escrever corpo do e-mail: %w", err)
		}

		err = w.Close()
		if err != nil {
			return fmt.Errorf("erro ao fechar transmissão: %w", err)
		}

		log.Printf("Enviando e-mail para: %s...", emailTo)
		return client.Quit()
	} else {
		// STARTTLS padrão (porta 587)
		if useTLS {
			log.Println("Iniciando conexão segura TLS (STARTTLS)...")
		}
		log.Printf("Enviando e-mail para: %s...", emailTo)
		
		// Para o envelope SMTP (MAIL FROM), usamos o e-mail limpo (user)
		err := smtp.SendMail(addr, auth, user, []string{emailTo}, msg.Bytes())
		if err != nil {
			return fmt.Errorf("erro ao enviar via STARTTLS: %w", err)
		}
		return nil
	}
}

func main() {
	// Garante que a pasta logs/logs existe
	_ = os.MkdirAll(filepath.Join("logs", "logs"), 0755)

	// Arquivo de log rotacionado por ano-mes-dia (ex: 2026-05-18.log)
	todayISO := time.Now().Format("2006-01-02")
	logFilePath := filepath.Join("logs", "logs", fmt.Sprintf("%s.log", todayISO))

	logFile, err := os.OpenFile(logFilePath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	if err == nil {
		defer logFile.Close()
		// Define a saída do log padrão para o console e o arquivo de log
		log.SetOutput(io.MultiWriter(os.Stdout, logFile))
	} else {
		log.Printf("Aviso: Não foi possível criar o arquivo de log: %v", err)
	}

	// Carrega variáveis de ambiente
	_ = godotenv.Load()

	// Flags de linha de comando
	tFlag := flag.String("t", "", "Nome do template/prompt na pasta templates/ e prompts/ (sem extensão)")
	templateFlag := flag.String("template", "devocional", "Nome do template/prompt na pasta templates/ e prompts/ (sem extensão)")

	flag.Parse()

	// Consolida flags de forma correta (respeitando shorthands)
	templateVal := *templateFlag
	if *tFlag != "" {
		templateVal = *tFlag
	}

	promptVal := templateVal

	dateDisplay := getFormattedDate()

	promptFile := filepath.Join("prompts", fmt.Sprintf("%s.md", promptVal))
	templateFile := filepath.Join("templates", fmt.Sprintf("%s.html", templateVal))

	// 2. Executa Copilot CLI
	markdownContent, err := executeCopilot(promptFile)
	if err != nil {
		log.Fatalf("Erro crítico: %v", err)
	}

	// 3. Compila HTML
	htmlContent, err := compileNewsletter(markdownContent, templateFile, dateDisplay)
	if err != nil {
		log.Fatalf("Erro crítico: %v", err)
	}

	// 4. Salva no Histórico (logs/)
	_, err = saveLog(htmlContent, todayISO)
	if err != nil {
		log.Fatalf("Erro crítico: %v", err)
	}

	// 5. Envia o E-mail via SMTP
	err = sendEmail(htmlContent)
	if err != nil {
		log.Fatalf("Erro de envio de e-mail: %v", err)
	}

	log.Println("E-mail enviado com sucesso!")
	log.Println("Processo concluído com êxito absoluto!")
}
