package scheduler

import (
	"flag"
	"fmt"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"solomon-cron/internal/config"
	"solomon-cron/internal/dailybread"
	"solomon-cron/internal/logger"
	"solomon-cron/internal/state"
)

type Scheduler struct {
	config    *config.Config
	state     *state.State
	statePath string
	logger    *logger.Logger
}

func New(cfg *config.Config, s *state.State, statePath string, l *logger.Logger) *Scheduler {
	return &Scheduler{
		config:    cfg,
		state:     s,
		statePath: statePath,
		logger:    l,
	}
}

func (s *Scheduler) Run() {
	s.logger.Log("=== Scheduler Execution Started ===")
	now := time.Now()

	stateChanged := false

	for _, task := range s.config.Tasks {
		lastRun := s.state.LastRuns[task.ID]
		
		should, reason, err := shouldRun(task.Schedule, lastRun, now)
		if err != nil {
			s.logger.Log("ERROR [%s]: Invalid schedule configuration: %v", task.ID, err)
			continue
		}

		if !should {
			s.logger.Log("SKIP [%s]: %s", task.ID, reason)
			continue
		}

		s.logger.Log("EXECUTE [%s]: Running task (Reason: %s)", task.ID, reason)
		
		err = s.runTask(task)
		if err != nil {
			s.logger.Log("ERROR [%s]: Task execution failed: %v", task.ID, err)
		} else {
			s.logger.Log("SUCCESS [%s]: Task completed successfully", task.ID)
		}

		s.state.LastRuns[task.ID] = time.Now()
		stateChanged = true
	}

	if stateChanged {
		if err := state.Save(s.statePath, s.state); err != nil {
			s.logger.Log("ERROR: Failed to save execution state: %v", err)
		} else {
			s.logger.Log("State saved successfully to %s", s.statePath)
		}
	}

	s.logger.Log("=== Scheduler Execution Finished ===")
}

func (s *Scheduler) ForceRunTask(taskID string) error {
	s.logger.Log("=== Force-Running Task %s ===", taskID)
	
	var targetTask *config.TaskConfig
	for _, task := range s.config.Tasks {
		if task.ID == taskID {
			targetTask = &task
			break
		}
	}
	
	if targetTask == nil {
		return fmt.Errorf("task ID %q not found in config", taskID)
	}

	err := s.runTask(*targetTask)
	if err != nil {
		s.logger.Log("ERROR [%s]: Task execution failed: %v", taskID, err)
		return err
	}
	
	s.logger.Log("SUCCESS [%s]: Task completed successfully", taskID)
	return nil
}

func (s *Scheduler) runTask(task config.TaskConfig) error {
	if strings.HasPrefix(task.Command, "internal:") {
		return s.runInternalService(task)
	}

	cmdPath := task.Command
	cmd := exec.Command(cmdPath, task.Args...)
	
	if task.Dir != "" {
		absDir, err := filepath.Abs(task.Dir)
		if err != nil {
			return fmt.Errorf("failed to resolve absolute path for working directory %q: %w", task.Dir, err)
		}
		cmd.Dir = absDir
	}

	output, err := cmd.CombinedOutput()
	if len(output) > 0 {
		s.logger.LogTaskOutput(task.ID, output)
	}

	if err != nil {
		return fmt.Errorf("command returned error: %w", err)
	}

	return nil
}

func (s *Scheduler) runInternalService(task config.TaskConfig) error {
	serviceName := strings.TrimPrefix(task.Command, "internal:")
	
	switch serviceName {
	case "daily-bread":
		templateName := "devocional"
		// 1. Check task configuration args
		for i, arg := range task.Args {
			if (arg == "-template" || arg == "-t") && i+1 < len(task.Args) {
				templateName = task.Args[i+1]
				break
			}
		}
		// 2. Override with CLI flags if provided
		if tVal := flag.Lookup("template").Value.String(); tVal != "" && tVal != "devocional" {
			templateName = tVal
		}
		if tVal := flag.Lookup("t").Value.String(); tVal != "" {
			templateName = tVal
		}

		// Resolve assets directory in the root of the cron scheduler app
		baseDir, err := filepath.Abs("assets")
		if err != nil {
			return fmt.Errorf("failed to resolve absolute path for assets: %w", err)
		}

		dbService := dailybread.New(s.logger, baseDir)
		return dbService.Run(templateName)
		
	default:
		return fmt.Errorf("unknown internal service: %s", serviceName)
	}
}

func shouldRun(schedule string, lastRun time.Time, now time.Time) (bool, string, error) {
	if lastRun.IsZero() {
		return true, "Task has never run before", nil
	}

	switch schedule {
	case "daily":
		yearL, monthL, dayL := lastRun.Date()
		yearN, monthN, dayN := now.Date()
		if yearL != yearN || monthL != monthN || dayL != dayN {
			return true, "Last run was on a different day", nil
		}
		return false, fmt.Sprintf("Already ran today at %s", lastRun.Format("15:04:05")), nil

	case "hourly":
		yearL, monthL, dayL := lastRun.Date()
		yearN, monthN, dayN := now.Date()
		hourL := lastRun.Hour()
		hourN := now.Hour()
		if yearL != yearN || monthL != monthN || dayL != dayN || hourL != hourN {
			return true, "Last run was in a different hour", nil
		}
		return false, fmt.Sprintf("Already ran this hour at %s", lastRun.Format("15:04:05")), nil

	default:
		dur, err := time.ParseDuration(schedule)
		if err != nil {
			return false, "", fmt.Errorf("unknown schedule type or invalid duration: %q", schedule)
		}
		
		elapsed := now.Sub(lastRun)
		if elapsed >= dur {
			return true, fmt.Sprintf("Interval of %s exceeded (elapsed: %s)", dur, elapsed.Round(time.Second)), nil
		}
		
		remaining := (dur - elapsed).Round(time.Second)
		return false, fmt.Sprintf("Interval of %s not met (elapsed: %s, remaining: %s)", dur, elapsed.Round(time.Second), remaining), nil
	}
}
