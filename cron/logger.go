package main

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

func NewLogger(logDir string) (*Logger, error) {
	if err := os.MkdirAll(logDir, 0755); err != nil {
		return nil, fmt.Errorf("failed to create log directory: %w", err)
	}
	return &Logger{logDir: logDir}, nil
}

func (l *Logger) Log(format string, v ...interface{}) {
	now := time.Now()
	msg := fmt.Sprintf(format, v...)
	timestamp := now.Format("2006-01-02 15:04:05.000")
	line := fmt.Sprintf("[%s] %s\n", timestamp, msg)

	// Print to stdout
	fmt.Print(line)

	// Write to daily file
	l.mu.Lock()
	defer l.mu.Unlock()

	logFileName := now.Format("2006-01-02") + ".log"
	logFilePath := filepath.Join(l.logDir, logFileName)

	file, err := os.OpenFile(logFilePath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Fprintf(os.Stderr, "ERROR: Failed to open log file %s: %v\n", logFilePath, err)
		return
	}
	defer file.Close()

	if _, err := io.WriteString(file, line); err != nil {
		fmt.Fprintf(os.Stderr, "ERROR: Failed to write to log file %s: %v\n", logFilePath, err)
	}
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
