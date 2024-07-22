[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Dependabot](https://badgen.net/badge/Dependabot/enabled/green?icon=dependabot)](https://dependabot.com/)

### How to Install.

Fork the repository `https://github.com/Granville-Technologies-UG/Chatbot`

Clone the forked repository

```bash
git clone https://github.com/<account-username>/Chatbot
```

Install the dependencies

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

### Folder Structure

```bash
.
├── app
│   ├── config.py
│   ├── decorators
│   │   ├── __init__.py
│   │   └── security.py
│   ├── fonts
│   │   ├── font-awesome
│   │   │   └── fontawesome-webfont.ttf
│   │   └── montserrat
│   │       ├── AUTHORS.txt
│   │       ├── CONTRIBUTORS.txt
│   │       ├── DESCRIPTION.en_us.html
│   │       ├── fonts
│   │       │   ├── otf
│   │       │   │   ├── MontserratAlternates-BlackItalic.otf
│   │       │   │   ├── MontserratAlternates-Black.otf
│   │       │   │   ├── MontserratAlternates-BoldItalic.otf
│   │       │   │   ├── MontserratAlternates-Bold.otf
│   │       │   │   ├── MontserratAlternates-ExtraBoldItalic.otf
│   │       │   │   ├── MontserratAlternates-ExtraBold.otf
│   │       │   │   ├── MontserratAlternates-ExtraLightItalic.otf
│   │       │   │   ├── MontserratAlternates-ExtraLight.otf
│   │       │   │   ├── MontserratAlternates-Italic.otf
│   │       │   │   ├── MontserratAlternates-LightItalic.otf
│   │       │   │   ├── MontserratAlternates-Light.otf
│   │       │   │   ├── MontserratAlternates-MediumItalic.otf
│   │       │   │   ├── MontserratAlternates-Medium.otf
│   │       │   │   ├── MontserratAlternates-Regular.otf
│   │       │   │   ├── MontserratAlternates-SemiBoldItalic.otf
│   │       │   │   ├── MontserratAlternates-SemiBold.otf
│   │       │   │   ├── MontserratAlternates-ThinItalic.otf
│   │       │   │   ├── MontserratAlternates-Thin.otf
│   │       │   │   ├── Montserrat-BlackItalic.otf
│   │       │   │   ├── Montserrat-Black.otf
│   │       │   │   ├── Montserrat-BoldItalic.otf
│   │       │   │   ├── Montserrat-Bold.otf
│   │       │   │   ├── Montserrat-ExtraBoldItalic.otf
│   │       │   │   ├── Montserrat-ExtraBold.otf
│   │       │   │   ├── Montserrat-ExtraLightItalic.otf
│   │       │   │   ├── Montserrat-ExtraLight.otf
│   │       │   │   ├── Montserrat-Italic.otf
│   │       │   │   ├── Montserrat-LightItalic.otf
│   │       │   │   ├── Montserrat-Light.otf
│   │       │   │   ├── Montserrat-MediumItalic.otf
│   │       │   │   ├── Montserrat-Medium.otf
│   │       │   │   ├── Montserrat-Regular.otf
│   │       │   │   ├── Montserrat-SemiBoldItalic.otf
│   │       │   │   ├── Montserrat-SemiBold.otf
│   │       │   │   ├── Montserrat-ThinItalic.otf
│   │       │   │   └── Montserrat-Thin.otf
│   │       │   ├── ttf
│   │       │   │   ├── MontserratAlternates-BlackItalic.ttf
│   │       │   │   ├── MontserratAlternates-Black.ttf
│   │       │   │   ├── MontserratAlternates-BoldItalic.ttf
│   │       │   │   ├── MontserratAlternates-Bold.ttf
│   │       │   │   ├── MontserratAlternates-ExtraBoldItalic.ttf
│   │       │   │   ├── MontserratAlternates-ExtraBold.ttf
│   │       │   │   ├── MontserratAlternates-ExtraLightItalic.ttf
│   │       │   │   ├── MontserratAlternates-ExtraLight.ttf
│   │       │   │   ├── MontserratAlternates-Italic.ttf
│   │       │   │   ├── MontserratAlternates-LightItalic.ttf
│   │       │   │   ├── MontserratAlternates-Light.ttf
│   │       │   │   ├── MontserratAlternates-MediumItalic.ttf
│   │       │   │   ├── MontserratAlternates-Medium.ttf
│   │       │   │   ├── MontserratAlternates-Regular.ttf
│   │       │   │   ├── MontserratAlternates-SemiBoldItalic.ttf
│   │       │   │   ├── MontserratAlternates-SemiBold.ttf
│   │       │   │   ├── MontserratAlternates-ThinItalic.ttf
│   │       │   │   ├── MontserratAlternates-Thin.ttf
│   │       │   │   ├── Montserrat-BlackItalic.ttf
│   │       │   │   ├── Montserrat-Black.ttf
│   │       │   │   ├── Montserrat-BoldItalic.ttf
│   │       │   │   ├── Montserrat-Bold.ttf
│   │       │   │   ├── Montserrat-ExtraBoldItalic.ttf
│   │       │   │   ├── Montserrat-ExtraBold.ttf
│   │       │   │   ├── Montserrat-ExtraLightItalic.ttf
│   │       │   │   ├── Montserrat-ExtraLight.ttf
│   │       │   │   ├── Montserrat-Italic.ttf
│   │       │   │   ├── Montserrat-LightItalic.ttf
│   │       │   │   ├── Montserrat-Light.ttf
│   │       │   │   ├── Montserrat-MediumItalic.ttf
│   │       │   │   ├── Montserrat-Medium.ttf
│   │       │   │   ├── Montserrat-Regular.ttf
│   │       │   │   ├── Montserrat-SemiBoldItalic.ttf
│   │       │   │   ├── Montserrat-SemiBold.ttf
│   │       │   │   ├── Montserrat-ThinItalic.ttf
│   │       │   │   └── Montserrat-Thin.ttf
│   │       │   └── webfonts
│   │       │       ├── MontserratAlternates-BlackItalic.woff
│   │       │       ├── MontserratAlternates-BlackItalic.woff2
│   │       │       ├── MontserratAlternates-Black.woff
│   │       │       ├── MontserratAlternates-Black.woff2
│   │       │       ├── MontserratAlternates-BoldItalic.woff
│   │       │       ├── MontserratAlternates-BoldItalic.woff2
│   │       │       ├── MontserratAlternates-Bold.woff
│   │       │       ├── MontserratAlternates-Bold.woff2
│   │       │       ├── MontserratAlternates-ExtraBoldItalic.woff
│   │       │       ├── MontserratAlternates-ExtraBoldItalic.woff2
│   │       │       ├── MontserratAlternates-ExtraBold.woff
│   │       │       ├── MontserratAlternates-ExtraBold.woff2
│   │       │       ├── MontserratAlternates-ExtraLightItalic.woff
│   │       │       ├── MontserratAlternates-ExtraLightItalic.woff2
│   │       │       ├── MontserratAlternates-ExtraLight.woff
│   │       │       ├── MontserratAlternates-ExtraLight.woff2
│   │       │       ├── MontserratAlternates-Italic.woff
│   │       │       ├── MontserratAlternates-Italic.woff2
│   │       │       ├── MontserratAlternates-LightItalic.woff
│   │       │       ├── MontserratAlternates-LightItalic.woff2
│   │       │       ├── MontserratAlternates-Light.woff
│   │       │       ├── MontserratAlternates-Light.woff2
│   │       │       ├── MontserratAlternates-MediumItalic.woff
│   │       │       ├── MontserratAlternates-MediumItalic.woff2
│   │       │       ├── MontserratAlternates-Medium.woff
│   │       │       ├── MontserratAlternates-Medium.woff2
│   │       │       ├── MontserratAlternates-Regular.woff
│   │       │       ├── MontserratAlternates-Regular.woff2
│   │       │       ├── MontserratAlternates-SemiBoldItalic.woff
│   │       │       ├── MontserratAlternates-SemiBoldItalic.woff2
│   │       │       ├── MontserratAlternates-SemiBold.woff
│   │       │       ├── MontserratAlternates-SemiBold.woff2
│   │       │       ├── MontserratAlternates-ThinItalic.woff
│   │       │       ├── MontserratAlternates-ThinItalic.woff2
│   │       │       ├── MontserratAlternates-Thin.woff
│   │       │       ├── MontserratAlternates-Thin.woff2
│   │       │       ├── Montserrat-BlackItalic.woff
│   │       │       ├── Montserrat-BlackItalic.woff2
│   │       │       ├── Montserrat-Black.woff
│   │       │       ├── Montserrat-Black.woff2
│   │       │       ├── Montserrat-BoldItalic.woff
│   │       │       ├── Montserrat-BoldItalic.woff2
│   │       │       ├── Montserrat-Bold.woff
│   │       │       ├── Montserrat-Bold.woff2
│   │       │       ├── Montserrat.css
│   │       │       ├── Montserrat-ExtraBoldItalic.woff
│   │       │       ├── Montserrat-ExtraBoldItalic.woff2
│   │       │       ├── Montserrat-ExtraBold.woff
│   │       │       ├── Montserrat-ExtraBold.woff2
│   │       │       ├── Montserrat-ExtraLightItalic.woff
│   │       │       ├── Montserrat-ExtraLightItalic.woff2
│   │       │       ├── Montserrat-ExtraLight.woff
│   │       │       ├── Montserrat-ExtraLight.woff2
│   │       │       ├── Montserrat-Italic.woff
│   │       │       ├── Montserrat-Italic.woff2
│   │       │       ├── Montserrat-LightItalic.woff
│   │       │       ├── Montserrat-LightItalic.woff2
│   │       │       ├── Montserrat-Light.woff
│   │       │       ├── Montserrat-Light.woff2
│   │       │       ├── Montserrat-MediumItalic.woff
│   │       │       ├── Montserrat-MediumItalic.woff2
│   │       │       ├── Montserrat-Medium.woff
│   │       │       ├── Montserrat-Medium.woff2
│   │       │       ├── Montserrat-Regular.woff
│   │       │       ├── Montserrat-Regular.woff2
│   │       │       ├── Montserrat-SemiBoldItalic.woff
│   │       │       ├── Montserrat-SemiBoldItalic.woff2
│   │       │       ├── Montserrat-SemiBold.woff
│   │       │       ├── Montserrat-SemiBold.woff2
│   │       │       ├── Montserrat-ThinItalic.woff
│   │       │       ├── Montserrat-ThinItalic.woff2
│   │       │       ├── Montserrat-Thin.woff
│   │       │       ├── Montserrat-Thin.woff2
│   │       │       └── README.MD
│   │       ├── OFL.txt
│   │       ├── README.md
│   │       └── sources
│   │           ├── Montserrat_autospace.py
│   │           ├── Montserrat.glyphs
│   │           ├── Montserrat-Italic_autospace.py
│   │           └── Montserrat-Italic.glyphs
│   ├── __init__.py
│   ├── README.md
│   ├── services
│   │   ├── __init__.py
│   │   ├── openai_service.py
│   │   ├── threads_db.bak
│   │   ├── threads_db.dat
│   │   └── threads_db.dir
│   ├── start
│   │   ├── assistants_quickstart.py
│   │   └── whatsapp_quickstart.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── pdf.py
│   │   └── whatsapp_utils.py
│   └── views.py
├── codecov.yml
├── LICENSE.md
├── main.py
├── poetry.lock
├── pyproject.toml
├── README.md
└── tests
    └── test_utils.py
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
