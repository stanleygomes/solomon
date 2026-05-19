package ai

import (
	"bytes"
	"fmt"
	"os"
	"os/exec"
	"strings"
)

// Provider defines the interface for different AI backends.
type Provider interface {
	Generate(prompt string) (string, error)
}

// CopilotProvider implements Provider using the GitHub Copilot CLI.
type CopilotProvider struct{}

func (c *CopilotProvider) Generate(prompt string) (string, error) {
	cmd := exec.Command("copilot", "-s", "-p", prompt, "--no-ask-user", "--yolo")
	
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	
	err := cmd.Run()
	if err != nil {
		return "", fmt.Errorf("copilot CLI error: %v\nStderr: %s", err, stderr.String())
	}
	
	output := strings.TrimSpace(stdout.String())
	if output == "" {
		return "", fmt.Errorf("copilot CLI returned empty response")
	}
	
	return output, nil
}

// NewProvider returns the configured AI provider based on environment variables.
func NewProvider() (Provider, error) {
	providerType := strings.ToLower(os.Getenv("AI_PROVIDER"))
	if providerType == "" {
		providerType = "copilot" // default
	}

	switch providerType {
	case "copilot":
		return &CopilotProvider{}, nil
	default:
		return nil, fmt.Errorf("unsupported AI provider: %s", providerType)
	}
}
