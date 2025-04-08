# 🤖 AutoPR ReviewBot

**AutoPR ReviewBot** is a GitHub App that automatically reviews the code quality of pull requests using AI. Whenever a new pull request is opened or updated, the app analyzes the diff and commit messages, then posts a concise, helpful comment reviewing the changes.

Powered by [Ollama](https://ollama.com) and integrated via webhooks, this tool brings intelligent, automated feedback to your code review workflow.

---

## ✨ Features

- 🔄 **Automatic Trigger on PRs**: Listens for `opened` and `synchronize` pull request events.
- 💬 **AI-Powered Feedback**: Uses a local language model (e.g., `qwen2.5-coder:1.5b`) to generate insightful comments.
- 🔧 **Diff + Commit Analysis**: Combines the PR diff and latest commit message for better context.
- ⚡ **FastAPI Webhook Endpoint**: Lightweight, asynchronous server for handling GitHub webhook payloads.

---

## 🛠️ How It Works

1. GitHub triggers a webhook when a PR is opened or updated.
2. The FastAPI app receives the webhook and extracts:
   - The diff of the PR
   - The latest commit message
3. A system prompt concatenated with the diff and commit messages and sent to the language model using Ollama.
4. The generated review is sent back to the FastAPI app and posted as a comment on the pull request.

---

## 🏛️Architectural Overview

![PR-Review-Diagram](https://github.com/user-attachments/assets/ac3acde1-2f88-4dde-bcde-cc831d48a7db)

