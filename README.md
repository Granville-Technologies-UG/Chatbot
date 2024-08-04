[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Dependabot](https://badgen.net/badge/Dependabot/enabled/green?icon=dependabot)](https://dependabot.com/)

### How to Install.

**Fork the Repository**: Click the "Fork" button on the [Granville Technologies UG Chatbot Repository](https://github.com/Granville-Technologies-UG/Chatbot) to create a copy of the repository in your GitHub account.

**Clone the forked repository**

```bash
git clone https://github.com/<account-username>/Chatbot
```

**Install the dependencies**

```bash
# Navigate to Cloned Repository
cd Chatbot

# Create Conda Environment
conda create -n bot python=3.10
conda activate bot

# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Configure Poetry to Use Conda Environment
poetry config virtualenvs.create false

# Install Poetry Dependencies
poetry install

```

### Adding New Dependencies

To add new dependencies to the project, run the following command:

```bash
poetry add <dependency-name>
```

### Run flake8

```bash
poetry run flake8
```

### Run black

```bash
poetry run black .
```

### Git Workflows

Our project uses a structured Git workflow to ensure code quality, efficient collaboration, and smooth deployment processes. Below is an overview of our branching strategy and the purpose of each branch.

#### Branching Strategy

1. **production**

   - **Purpose**: The live, stable version of our codebase. Code pushed to this branch should be fully tested and tagged for release.
   - **Tags**: Every deployment to production should have an associated tag for version tracking (e.g., `v1.0.0`).
   - **Hotfixes**: Quick fixes for urgent issues should be branched from and merged directly into production.

2. **staging**

   - **Purpose**: A pre-production environment that mirrors our production environment. Used for final testing before production deployment.
   - **Blue/Green Deployment**: Two identical environments (blue and green) where one is live (production) and the other is idle (staging). After successful testing, we can swap staging with production.
   - **Merging**: Code from the `main` branch is merged here after passing all tests.

3. **main**

   - **Purpose**: The primary branch for ongoing development. All new features and fixes are eventually merged here.
   - **Features**: New features are developed in feature branches created from and merged back into `main`.

   Example workflow for a feature:

   ```bash
   git checkout -b feature/my-new-feature
   # work on feature
   git push origin feature/my-new-feature
   # create a pull request for code review
   ```

#### Workflow Overview

1. **Feature Development**

   - Developers create feature branches from `main`.
   - Feature branches follow the naming convention: `feature/description-of-feature`.
   - Completed features are merged back into main through pull requests (PRs) after code review.

2. **QA Testing**

   - After merging feature branches into `main`, the `main` branch is merged into `staging`.
   - The `staging` branch undergoes rigorous testing.
   - Any issues found in `staging` are fixed in new branches off `main` or directly in `staging` if necessary.

3. **Staging Deployment**

   - Once all tests pass in staging, the `staging` branch is merged into `production`.
   - The staging environment is a replica of production, allowing for final validation.
   - If staging tests are successful, the staging branch is prepared for production deployment.

4. **Production Deployment**
   - The code is merged from staging into `production`.
   - Each deployment is tagged with a version number for tracking.
   - Hotfixes are managed by creating branches directly off `production` and merging back after fixes.

#### Hotfix Workflow

1. Create a hotfix branch from `production`:
   ```bash
   git checkout -b hotfix/urgent-fix production
   ```
2. Implement the necessary fix.
3. Push the hotfix branch and create a pull request to production.
4. Once the hotfix is approved, merge it into `production` and tag the commit.
   ```bash
   git tag -a v1.0.1 -m "Description of the fix"
   git push origin --tags
   ```
