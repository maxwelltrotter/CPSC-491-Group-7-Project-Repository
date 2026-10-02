# CPSC-491-Group-7-Project-Repository

## CI/CD Pipeline

We use GitHub Actions for CI. The workflow lives at `.github/workflows/ci.yml` and runs automatically on every push and pull request into `main`.

What it does:
1. Checks out the code
2. Sets up Python 3.12
3. Installs dependencies from both `requirements.txt` (root, detection/model code) and `backend/requirements.txt` (Flask app)
4. Runs the root-level tests (`pytest tests/`)
5. Runs the backend tests (`pytest backend/tests/`)
6. Confirms the Flask app can actually import and start
7. Prints the current version from the `VERSION` file

**Versioning:** The `VERSION` file at the root follows `major.sprint.patch` (e.g. `0.2.0` for Sprint 2). Bump the middle number each sprint. GitHub Actions also gives every run its own build number automatically under the Actions tab, so any two builds can always be told apart.

**Adding to the pipeline:** If you want to add your own step (a linter, more tests, etc.), add it to the existing `ci.yml` rather than creating a new workflow file, we're keeping everything in one pipeline so it's easy to follow.