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

### @classes (Study Planner & Delivery)

Automated daily study routines tailored to any topic. Simply define your subject and duration, and the system manages the cycle through two separate commands:

#### 1. Planning (`plan-classes`)
Generates the structured study syllabus for any course in `PLANNING` status.
- **Auto-registration**: If you pass the `SUBJECT` and `DURATION_DAYS` environment variables, the task will automatically register the new class in the database before planning.
- Executes the AI planning prompt (`class-planning.md`) to divide the subject into daily lesson topics.
- Parses the AI response as JSON and persists the generated lessons in the database.
- Sets the plan status to `ACTIVE`.

##### How to run (with new class registration):
```bash
SUBJECT="Programar em python" DURATION_DAYS=30 make run task=plan-classes
```

##### How to run (planning existing pending classes):
```bash
make run task=plan-classes
```

#### 2. Execution (`execute-class`)
Delivers the daily class and advances your progress.
- Retrieves the active study plan and the corresponding lesson for the current day.
- Executes the AI content generator prompt (`class-segment.md`) to generate a complete learning module for the topic.
- Compiles the content into a styled HTML email template (using Jinja2 and predefined themes like `noemi`).
- Sends the daily class email via SMTP.
- Marks the lesson as completed and advances the plan's current day (marking the plan as `COMPLETED` when finished).

##### How to run:
```bash
make run task=execute-class
```

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
