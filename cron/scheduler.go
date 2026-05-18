package main

import (
	"fmt"
	"os/exec"
	"path/filepath"
	"time"
)

type Scheduler struct {
	config    *Config
	state     *State
	statePath string
	logger    *Logger
}

func NewScheduler(cfg *Config, state *State, statePath string, logger *Logger) *Scheduler {
	return &Scheduler{
		config:    cfg,
		state:     state,
		statePath: statePath,
		logger:    logger,
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
			// We still record the execution attempt if it started, or do we?
			// Generally, if the script failed, we still want to block it from running again immediately
			// to avoid spamming/looping. The user can retry manually or it will run next time.
			// Let's update last run so it follows the configured interval / daily limit even if it failed.
		} else {
			s.logger.Log("SUCCESS [%s]: Task completed successfully", task.ID)
		}

		s.state.LastRuns[task.ID] = time.Now()
		stateChanged = true
	}

	if stateChanged {
		if err := SaveState(s.statePath, s.state); err != nil {
			s.logger.Log("ERROR: Failed to save execution state: %v", err)
		} else {
			s.logger.Log("State saved successfully to %s", s.statePath)
		}
	}

	s.logger.Log("=== Scheduler Execution Finished ===")
}

func (s *Scheduler) runTask(task TaskConfig) error {
	cmdPath := task.Command
	
	cmd := exec.Command(cmdPath, task.Args...)
	
	if task.Dir != "" {
		// Resolve absolute path for task.Dir
		absDir, err := filepath.Abs(task.Dir)
		if err != nil {
			return fmt.Errorf("failed to resolve absolute path for working directory %q: %w", task.Dir, err)
		}
		cmd.Dir = absDir
	}

	// Capture combined stdout and stderr
	output, err := cmd.CombinedOutput()
	if len(output) > 0 {
		s.logger.LogTaskOutput(task.ID, output)
	}

	if err != nil {
		return fmt.Errorf("command returned error: %w", err)
	}

	return nil
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
		// Attempt to parse as standard duration (e.g. "12h", "30m")
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
