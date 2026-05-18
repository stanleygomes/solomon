package logger

import (
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sync"
	"time"
)

type Logger struct {
	mu     sync.Mutex
	logDir string
}

func New(logDir string) (*Logger, error) {
	if err := os.MkdirAll(logDir, 0755); err != nil {
		return nil, fmt.Errorf("failed to create log directory: %w", err)
	}

	return &Logger{logDir: logDir}, nil
}

func (l *Logger) Log(format string, v ...interface{}) {
	now := time.Now()
	line := l.formatLine(now, format, v...)

	// Print to stdout
	l.writeToStdout(line)

	// Write to daily file
	l.writeToDailyFile(now, line)
}

func (l *Logger) formatLine(t time.Time, format string, v ...interface{}) string {
	msg := fmt.Sprintf(format, v...)
	timestamp := t.Format("2006-01-02 15:04:05.000")
	return fmt.Sprintf("[%s] %s\n", timestamp, msg)
}

func (l *Logger) writeToStdout(line string) {
	fmt.Print(line)
}

func (l *Logger) writeToDailyFile(t time.Time, line string) {
	l.mu.Lock()
	defer l.mu.Unlock()

	logFileName := t.Format("2006-01-02") + ".log"
	logFilePath := filepath.Join(l.logDir, logFileName)

	file, err := l.openLogFile(logFilePath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "ERROR: Failed to open log file %s: %v\n", logFilePath, err)
		return
	}
	defer file.Close()

	if err := l.writeStringToFile(file, line); err != nil {
		fmt.Fprintf(os.Stderr, "ERROR: Failed to write to log file %s: %v\n", logFilePath, err)
	}
}

func (l *Logger) openLogFile(path string) (*os.File, error) {
	return os.OpenFile(path, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
}

func (l *Logger) writeStringToFile(file *os.File, content string) error {
	_, err := io.WriteString(file, content)
	return err
}

// LogTaskOutput logs execution outputs block-by-block beautifully.
func (l *Logger) LogTaskOutput(taskID string, output []byte) {
	if len(output) == 0 {
		return
	}
	l.Log("[%s] --- Output Start ---", taskID)
	l.Log("[%s]\n%s", taskID, string(output))
	l.Log("[%s] --- Output End ---", taskID)
}
