package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"

	"solomon-cron/internal/config"
	"solomon-cron/internal/logger"
	"solomon-cron/internal/scheduler"
	"solomon-cron/internal/state"
)

func main() {
	// 1. Parse command line flags
	configFlag := flag.String("config", "", "Path to the configuration file (config.json)")
	stateFlag := flag.String("state", "", "Path to the execution state file (state.json)")
	logsFlag := flag.String("logs", "", "Path to the logs directory")
	flag.Parse()

	// 2. Resolve default directories
	baseDir, err := getBaseDir()
	if err != nil {
		fmt.Fprintf(os.Stderr, "FATAL: Failed to determine base directory: %v\n", err)
		os.Exit(1)
	}

	configPath := *configFlag
	if configPath == "" {
		configPath = filepath.Join(baseDir, "config.json")
	}

	statePath := *stateFlag
	if statePath == "" {
		statePath = filepath.Join(baseDir, "state.json")
	}

	logsDir := *logsFlag
	if logsDir == "" {
		logsDir = filepath.Join(baseDir, "logs")
	}

	// 3. Initialize Logger
	loggerInstance, err := logger.New(logsDir)
	if err != nil {
		fmt.Fprintf(os.Stderr, "FATAL: Failed to initialize logger: %v\n", err)
		os.Exit(1)
	}

	loggerInstance.Log("Initializing Solomon Cron Coordinator")
	loggerInstance.Log("Base Directory: %s", baseDir)
	loggerInstance.Log("Config Path:    %s", configPath)
	loggerInstance.Log("State Path:     %s", statePath)
	loggerInstance.Log("Logs Directory: %s", logsDir)

	// 4. Load Config
	cfg, err := config.Load(configPath)
	if err != nil {
		loggerInstance.Log("FATAL: Failed to load configuration: %v", err)
		os.Exit(1)
	}

	// 5. Load State
	stateInstance, err := state.Load(statePath)
	if err != nil {
		loggerInstance.Log("FATAL: Failed to load execution state: %v", err)
		os.Exit(1)
	}

	// 6. Run Scheduler
	schedulerInstance := scheduler.New(cfg, stateInstance, statePath, loggerInstance)
	schedulerInstance.Run()
}

// getBaseDir returns the directory of the executable as the fallback base directory,
// or the current working directory if that fails.
func getBaseDir() (string, error) {
	// First, check if config.json exists in the current working directory.
	// If it does, we use the current working directory as base.
	if _, err := os.Stat("config.json"); err == nil {
		cwd, err := os.Getwd()
		if err == nil {
			return cwd, nil
		}
	}

	// Otherwise, fallback to the executable's directory.
	execPath, err := os.Executable()
	if err != nil {
		return "", fmt.Errorf("failed to get executable path: %w", err)
	}

	// If running under 'go run', the executable is in a temp folder.
	// In that case, use current working directory.
	dir := filepath.Dir(execPath)
	if filepath.Base(filepath.Dir(dir)) == "go-build" || filepath.Base(dir) == "exe" || filepath.Base(filepath.Dir(filepath.Dir(dir))) == "go-build" {
		return os.Getwd()
	}

	return dir, nil
}
