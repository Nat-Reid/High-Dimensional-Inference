# High-Dimensional-Inference
A project exploring high dimensional density estimation schemes given empirical data with a focus on describing distributions of cell markers from flow cytometry data.



Jupyter notebooks and Python scripts, developed in VS Code on macOS and Windows.
Environment management uses [**uv**](https://docs.astral.sh/uv/). Two files define the environment and are committed to git:

| File | Purpose |
|---|---|
| `pyproject.toml` | The packages we *want* (edit via `uv add`, not by hand) |
| `uv.lock` | The exact versions of everything, for all platforms |
| `.python-version` | Python version (uv downloads it automatically) |

**Golden rule: never use `pip install`.** Always `uv add`. This keeps both machines identical.

---

## One-time setup

### 1. Install prerequisites
- **Git**, **VS Code**, and the VS Code extensions *Python* and *Jupyter* (VS Code will offer them via `.vscode/extensions.json`).
- **uv**
  - macOS: `brew install uv` (or `curl -LsSf https://astral.sh/uv/install.sh | sh`)
  - Windows (PowerShell): `winget install --id=astral-sh.uv -e` (or `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`)

  Restart the terminal afterwards and check with `uv --version`. You do **not** need to install Python yourself.

### 2. Clone and build the environment
```bash
git clone <repo-url>
cd myproject
uv sync                        # creates .venv, installs Python + exact locked packages
uv run pre-commit install      # strips notebook outputs on commit (once per clone)
```

### 3. Point VS Code at the environment
1. `code .` (or File → Open Folder) — open the **repo root**, not a subfolder.
2. `Cmd/Ctrl+Shift+P` → **Python: Select Interpreter** → choose the one inside `.venv`.
3. Open any notebook → top right **Select Kernel** → **Python Environments** → `.venv`.
   (If it's missing: `Cmd/Ctrl+Shift+P` → *Developer: Reload Window*.)

### 4. Verify
```bash
uv run python scripts/check_env.py
```
Open `notebooks/00_check_env.ipynb` and run it. Both should report an interpreter inside `.venv` and the same package versions on both machines.

---

## Everyday workflow

### Start of every session
```bash
git pull
uv sync
```
`uv sync` is fast when nothing changed. If the other person added packages, this installs them.

### Adding or removing a package
```bash
uv add scikit-learn           # runtime dependency
uv add --dev pytest           # dev-only tool
uv remove scikit-learn
git add pyproject.toml uv.lock
git commit -m "Add scikit-learn"
git push
```
Always commit **both** `pyproject.toml` and `uv.lock` together. Tell your collaborator to `git pull && uv sync`.

### Running scripts
```bash
uv run python scripts/my_script.py
```
This works identically on both OSes and never depends on which shell/venv is active. The VS Code "Run Python File" button also works once the interpreter is selected.

### Notebooks
- Select the `.venv` kernel (see setup step 3).
- Keep notebooks in `notebooks/`. Reusable logic goes in `src/myproject/` and is imported: `from myproject import ...`.
  Changes to those modules are picked up immediately (editable install); use `%load_ext autoreload` / `%autoreload 2` in the notebook to avoid restarting the kernel.
- Outputs are stripped automatically on commit by `nbstripout`. Your local notebook keeps its outputs; git just doesn't store them.

### Upgrading packages (one person does this, then pushes)
```bash
uv lock --upgrade-package pandas     # one package
uv lock --upgrade && uv sync         # everything
```

---

## Cross-platform code rules

- Build paths with `pathlib`: `DATA_DIR / "file.csv"`. Never hard-code `/` or `\`, or absolute paths like `/Users/...` or `C:\...`.
- Always specify encoding: `open(path, encoding="utf-8")`, `pd.read_csv(path, encoding="utf-8")` (Windows defaults to a different encoding).
- Use `from myproject import DATA_DIR` for locations instead of relative `../data` paths, so scripts and notebooks behave the same from any working directory.
- Large data goes in `data/` (git-ignored). Share it another way, or document how to download it here.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Kernel doesn't list `.venv` | Run `uv sync`, then *Developer: Reload Window*, then reselect the kernel |
| `ModuleNotFoundError` | Wrong interpreter/kernel selected, or you forgot `uv sync` after pulling |
| `uv.lock` merge conflict | `git checkout --theirs uv.lock` (or `--ours`), then `uv lock`, then commit |
| Windows: "running scripts is disabled" when activating | You don't need to activate; use `uv run ...`. Or: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Everything seems broken | Delete `.venv/` and run `uv sync` — it rebuilds exactly from the lockfile |
| Whole-file diffs in notebooks/scripts | Line-ending issue; `.gitattributes` should prevent it. Run `git add --renormalize .` once |
| Package needs compiling on one OS | Prefer packages with wheels; mention it so we can pin a version |

## Layout
```
.
├── pyproject.toml / uv.lock / .python-version
├── src/myproject/        # shared importable code
├── scripts/              # run with: uv run python scripts/x.py
├── notebooks/            # Jupyter notebooks
├── data/                 # git-ignored contents
└── .vscode/              # shared editor settings
```
