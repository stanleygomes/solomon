# 👑 Solomon - My AI & Automation Hub

<p align="center">
  <img src="https://img.shields.io/badge/Status-In_Development-blue?style=for-the-badge&logo=github" alt="Status" />
  <img src="https://img.shields.io/badge/Made%20with-Go-00ADD8?style=for-the-badge&logo=go" alt="Go" />
  <img src="https://img.shields.io/badge/Integration-GitHub%20Copilot%20CLI-black?style=for-the-badge&logo=github" alt="Copilot" />
  <img src="https://img.shields.io/badge/OS-Ubuntu-E95420?style=for-the-badge&logo=ubuntu" alt="Ubuntu" />
</p>

---

## 📖 About Solomon

**Solomon** is my personal operations center for research, validation, testing, and process automation powered by **Artificial Intelligence (AI)**. Here, I consolidate structured backups of highly refined prompts, agent definitions, task automations, robust mini-apps, and utility scripts.

This repository is built to serve as a living knowledge base and local execution infrastructure to automate workflows and optimize routine tasks using the state-of-the-art in prompt engineering and enterprise-grade AI.

---

## 📂 Repository Structure

The project follows a modular, highly scalable design:

```text
solomon/
├── apps/               # Self-contained automation mini-apps and executables
│   └── daily-bread/    # Devotional newsletter automation in Go with AI and SMTP
├── cron/               # Scheduled scripts and system-level automatic hooks
├── AGENTS.md           # Persona, rules, and context definitions for AI agents
├── SOUL.md             # Custom behavior and soul instructions for the local assistant
└── README.md           # This glorious and comprehensive documentation guide
```

### 🗺️ Active Components Map

| Component                                                                  | Type / Language        | Description                                                                               | Status                  |
| :------------------------------------------------------------------------- | :--------------------- | :---------------------------------------------------------------------------------------- | :---------------------- |
| [AGENTS.md](file:///home/stanley/projects/solomon/AGENTS.md)               | Persona & Guidelines   | Personality guide and technical stack for AI assistants                                   | Active                  |
| [SOUL.md](file:///home/stanley/projects/solomon/SOUL.md)                   | Behavior Configuration | Custom behavior configuration for the Hermes Agent                                        | Active                  |
| [apps/daily-bread](file:///home/stanley/projects/solomon/apps/daily-bread) | Application / **Go**   | Automated newsletter that generates daily studies via Copilot CLI and sends them via SMTP | Active                  |
| [cron/](file:///home/stanley/projects/solomon/cron)                        | Orchestrator / **Go**   | State-persistent task scheduler and automation coordinator                                | Active                  |

---

## ⚡ Featured Mini-Apps & Utilities

### 🍞 Daily Bread (`apps/daily-bread`)

**Daily Bread** is a **Go**-based application designed to automate the generation and delivery of daily devotional emails with high aesthetic and theological quality. It integrates directly with the **GitHub Copilot CLI** to generate deep reflections based on structured prompts and dynamic HTML templates.

> [!TIP]
> **Complete Documentation:** All technical details, system workflow diagram, environment setup instructions, and custom execution options can be found in the dedicated [apps/daily-bread/README.md](file:///home/stanley/projects/solomon/apps/daily-bread/README.md).

### ⏰ Solomon Cron Scheduler (`cron/`)

A lightweight, reliable, and state-persistent task coordinator written in **Go** to orchestrate automations on local machines (like laptops) that are not online 24/7. It uses `state.json` execution locks to guarantee jobs run exactly once per period (daily, hourly, or custom intervals).

#### Setup
Add the following entry to your local system `crontab -e`:

```text
*/5 * * * * cd /home/stanley/projects/solomon/cron && ./solomon-cron > /dev/null 2>&1
```

> [!TIP]
> **Complete Documentation:** Check the dedicated [cron/README.md](file:///home/stanley/projects/solomon/cron/README.md) for full configuration options, commands, and reset shortcuts.

---

## 🛡️ Local Contribution Guidelines (For AI Agents)

> [!IMPORTANT]
> If you are an AI agent operating in this repository, please consult the strict quality and personality guidelines defined in [AGENTS.md](file:///home/stanley/projects/solomon/AGENTS.md).

## 🤝 Como Contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 🔗 Links Úteis

- [Turborepo Docs](https://turborepo.dev/docs)
- [Next.js Docs](https://nextjs.org/docs)
- [Vercel](https://vercel.com)

Made with 🔥 by Lumen HQ
