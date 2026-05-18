package config

import (
	"encoding/json"
	"fmt"
	"os"
)

type TaskConfig struct {
	ID       string   `json:"id"`
	Name     string   `json:"name"`
	Command  string   `json:"command"`
	Args     []string `json:"args"`
	Dir      string   `json:"dir"`      // Working directory (can be absolute or relative to cron/ dir)
	Schedule string   `json:"schedule"` // e.g., "daily", "hourly", "12h", "30m"
}

type Config struct {
	Tasks []TaskConfig `json:"tasks"`
}

func Load(path string) (*Config, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, fmt.Errorf("failed to open config file: %w", err)
	}
	defer file.Close()

	var cfg Config
	dec := json.NewDecoder(file)
	if err := dec.Decode(&cfg); err != nil {
		return nil, fmt.Errorf("failed to decode config JSON: %w", err)
	}

	return &cfg, nil
}
