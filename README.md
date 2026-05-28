# 👑 solomon

**Solomon** is a lightweight, reliable task coordinator and automation hub written in **Python**. It's designed to run on personal machines (like laptops) that aren't online 24/7.

Unlike traditional cron engines that completely skip scheduled tasks if your computer is asleep during the designated hour, Solomon runs periodically (e.g., every 5 minutes) and uses a state file (`temp/state.json`) to track executions. This ensures your daily, hourly, or interval-based tasks run exactly once per scheduled period, no matter when your system boots, wakes, or sleeps.

## 📂 File Structure

```text
```

## 🚀 Execution & Automation

All shortcuts are centralized in the [Makefile](./Makefile):

### 1. Installation

Setup the environment and install all dependencies:

```bash
make install
```

### 2. Run

Run the application:

```bash
make run
```

### ⚙️ Configuration & Environment

The application requires a `.env` file in the root directory. Copy the template provided in `.env.example` to start.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
