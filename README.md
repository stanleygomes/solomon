![solomon-banner](assets/logo/solomon-banner.png)

# 👑 solomon agent

A personal automation assistant designed to streamline routine tasks and execute recurring processes using Python scripts.

## Use cases

### @daily-bread

Generates and sends a daily bible study. It operates through the following workflow:
1. Executes the AI prompt template (`daily-bread.md`) using the active AI provider (e.g., Copilot or Antigravity).
2. Renders the generated devotional into a styled HTML email template (using Jinja2 templates and predefined color themes).
3. Delivers the compiled email to the configured recipient via SMTP.

> [!IMPORTANT]
> **Once-per-day Execution Lock**: To avoid API quota waste and email spam, this task is restricted to run successfully **only once per calendar day**. Repeat executions on the same day are automatically skipped by checking past database logs.

#### How to run:
```bash
make run task=daily-bread
```

### @classes

Automated daily study routines tailored to any topic. Simply define your subject and duration, and receive structured, digestible daily learning segments.

> WIP

### @tasks

> WIP

### @finances

> WIP

### @feed

Automated scraping and intelligent summarization of new articles from your followed blogs.

> WIP


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
