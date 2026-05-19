package mailer

import (
	"bytes"
	"crypto/tls"
	"fmt"
	"net/smtp"
	"os"
)

// Config holds SMTP server configuration.
type Config struct {
	Host     string
	Port     string
	Username string
	Password string
}

// ConfigFromEnv loads SMTP configuration from environment variables.
func ConfigFromEnv() Config {
	return Config{
		Host:     os.Getenv("SMTP_HOST"),
		Port:     os.Getenv("SMTP_PORT"),
		Username: os.Getenv("SMTP_USER"),
		Password: os.Getenv("SMTP_PASSWORD"),
	}
}

// Message represents an email to be sent.
type Message struct {
	From    string
	To      string
	Subject string
	Body    string
}

// Mailer provides functionality to send emails via SMTP.
type Mailer struct {
	config Config
}

// New creates a new Mailer instance.
func New(cfg Config) *Mailer {
	return &Mailer{config: cfg}
}

// Send dispatches the email message.
func (m *Mailer) Send(msg Message) error {
	if m.config.Host == "" || m.config.Port == "" || m.config.Username == "" || m.config.Password == "" || msg.To == "" {
		return fmt.Errorf("mailer: missing configuration or recipient")
	}

	// Build MIME message
	header := make(map[string]string)
	header["From"] = msg.From
	header["To"] = msg.To
	header["Subject"] = msg.Subject
	header["MIME-Version"] = "1.0"
	header["Content-Type"] = `text/html; charset="utf-8"`

	var mailContent bytes.Buffer
	for k, v := range header {
		mailContent.WriteString(fmt.Sprintf("%s: %s\r\n", k, v))
	}
	mailContent.WriteString("\r\n")
	mailContent.WriteString(msg.Body)

	addr := m.config.Host + ":" + m.config.Port
	auth := smtp.PlainAuth("", m.config.Username, m.config.Password, m.config.Host)

	if m.config.Port == "465" {
		return m.sendSSL(addr, auth, msg.To, mailContent.Bytes())
	}

	return m.sendStandard(addr, auth, msg.To, mailContent.Bytes())
}

func (m *Mailer) sendSSL(addr string, auth smtp.Auth, to string, msg []byte) error {
	tlsconfig := &tls.Config{
		InsecureSkipVerify: false,
		ServerName:         m.config.Host,
	}

	conn, err := tls.Dial("tcp", addr, tlsconfig)
	if err != nil {
		return fmt.Errorf("failed SSL/TLS connection dial: %w", err)
	}
	defer conn.Close()

	client, err := smtp.NewClient(conn, m.config.Host)
	if err != nil {
		return fmt.Errorf("failed SMTP client instantiation: %w", err)
	}
	defer client.Close()

	if err = client.Auth(auth); err != nil {
		return fmt.Errorf("failed SMTP authentication: %w", err)
	}

	if err = client.Mail(m.config.Username); err != nil {
		return fmt.Errorf("failed SMTP MAIL FROM envelope: %w", err)
	}

	if err = client.Rcpt(to); err != nil {
		return fmt.Errorf("failed SMTP RCPT TO envelope: %w", err)
	}

	w, err := client.Data()
	if err != nil {
		return fmt.Errorf("failed SMTP DATA stream start: %w", err)
	}

	_, err = w.Write(msg)
	if err != nil {
		return fmt.Errorf("failed to write SMTP payload: %w", err)
	}

	err = w.Close()
	if err != nil {
		return fmt.Errorf("failed to close SMTP DATA stream: %w", err)
	}

	return client.Quit()
}

func (m *Mailer) sendStandard(addr string, auth smtp.Auth, to string, msg []byte) error {
	// For other ports (e.g. 587), use smtp.SendMail which handles STARTTLS if available
	// Note: smtp.SendMail uses a slice of recipients
	return smtp.SendMail(addr, auth, m.config.Username, []string{to}, msg)
}
