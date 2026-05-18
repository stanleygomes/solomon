package state

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"time"
)

type State struct {
	LastRuns map[string]time.Time `json:"last_runs"`
}

func Load(path string) (*State, error) {
	file, err := os.Open(path)
	if err != nil {
		if errors.Is(err, os.ErrNotExist) {
			return &State{LastRuns: make(map[string]time.Time)}, nil
		}
		return nil, fmt.Errorf("failed to open state file: %w", err)
	}
	defer file.Close()

	var state State
	dec := json.NewDecoder(file)
	if err := dec.Decode(&state); err != nil {
		return nil, fmt.Errorf("failed to decode state JSON: %w", err)
	}
	if state.LastRuns == nil {
		state.LastRuns = make(map[string]time.Time)
	}
	return &state, nil
}

func Save(path string, s *State) error {
	dir := filepath.Dir(path)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("failed to create directory for state file: %w", err)
	}

	file, err := os.OpenFile(path, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0644)
	if err != nil {
		return fmt.Errorf("failed to open state file for writing: %w", err)
	}
	defer file.Close()

	enc := json.NewEncoder(file)
	enc.SetIndent("", "  ")
	if err := enc.Encode(s); err != nil {
		return fmt.Errorf("failed to encode state JSON: %w", err)
	}
	return nil
}
