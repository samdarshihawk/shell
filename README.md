=

# 🐚 Shell — Built from Scratch

I'm building a fully functional shell **from scratch** in Python, integrated with **modern tooling** and **AI capabilities**. This goes beyond a standard POSIX shell — it's a platform for experimenting with intelligent command-line interfaces, hacking utilities, and AI-assisted workflows.

## Features & Vision

- ⚙️ **POSIX-compliant core** — supports `cd`, `pwd`, `echo`, piping, redirection, and more
- 🤖 **AI integration** — natural language command suggestions and shell assistance powered by LLMs
- 🛠️ **Hacking tools** — built-in support for recon, enumeration, and penetration testing workflows
- 🔁 **REPL architecture** — interactive, extensible Read-Eval-Print Loop
- 🧱 **Built from scratch** — no shell wrappers; every component is hand-crafted in Python

## Getting Started

### Prerequisites

Ensure you have [`uv`](https://github.com/astral-sh/uv) installed locally.

### Run the Shell

```sh
./your_program.sh
```

The entry point is `app/main.py`.

### Submit a Stage

```sh
git commit -am "your message"
git push origin master
```

Test output will be streamed to your terminal via CodeCrafters.

## Roadmap

- [x] Basic REPL loop
- [x] Built-in commands (`echo`, `cd`, `pwd`, `type`, `exit`)
- [ ] Piping and redirection
- [ ] AI command assistant (LLM-powered)
- [ ] Integrated hacking tool shortcuts
- [ ] Plugin/extension system
