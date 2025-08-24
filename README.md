# Thanos

Minimal README for the repository. Replace placeholders with your actual project description.

## 📦 Description

Short description of the **Thanos** project – what it does, what problem it solves, and who it is for.

> *Example:* "Thanos is a lightweight Python application skeleton with `main.py` and `src/` directory, prepared for quick start, development, and deployment."

## 🚀 Quickstart

### Requirements

* Python **3.10+** (3.11 recommended)
* `git`, `pip`
* (optional) **WSL** on Windows, Docker

### Installation & Run

```bash
# 1) Clone the repo
git clone https://github.com/mgardzina/thanos.git
cd thanos

# 2) (Optional) create virtualenv
python -m venv .venv
# Windows PowerShell:  .venv\Scripts\Activate.ps1
# Linux/macOS:        source .venv/bin/activate

# 3) Upgrade pip
python -m pip install --upgrade pip

# 4) Install dependencies (if requirements.txt exists)
# If not, skip this step
pip install -r requirements.txt || echo "No requirements.txt – skipping"

# 5) Run the app
python main.py
```

### Usage (example)

```bash
python main.py --help
# add description of available flags/arguments, e.g.:
# python main.py --input data/in.csv --output out/result.json --verbose
```

## 🧭 Project Structure

```
.
├── src/              # source code (modules/packages)
├── main.py           # entry point / CLI
├── .gitignore
└── README.md
```

> Adjust `src/` description to actual layout.

## ⚙️ Configuration

* Environment variables (example):

  * `THANOS_ENV=dev|prod`
  * `THANOS_LOG_LEVEL=INFO|DEBUG`
* Config file (optional): `config.yaml` / `.env`

## 🧪 Tests & Code Quality (optional)

Recommended tooling:

```bash
pip install pytest black ruff pre-commit

# tests
pytest -q

# formatting
black .

# linting
ruff check .

# pre-commit hooks
pre-commit install
pre-commit run --all-files
```

Configure `.pre-commit-config.yaml` if you want to use hooks.

## 🐳 Docker (optional)

Minimal Dockerfile example:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt || true
CMD ["python", "main.py"]
```

Build and run:

```bash
docker build -t thanos:latest .
docker run --rm -it thanos:latest
```

## 🛣️ Roadmap (example)

* [ ] Fill in project description and goals
* [ ] Add `requirements.txt` / `pyproject.toml`
* [ ] Design CLI interface (argparse/typer)
* [ ] Add unit tests (pytest)
* [ ] Configure CI (GitHub Actions)

## 🤝 Contributing

Contributio
