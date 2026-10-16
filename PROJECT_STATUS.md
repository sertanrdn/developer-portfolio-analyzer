
# Developer Portfolio Analyzer
 
A Python application that analyzes a developer's public GitHub portfolio and presents factual, descriptive insights through a command-line interface and a Streamlit dashboard.
 
The project is primarily a learning project focused on Python and backend development. Its goal is to understand what a public GitHub portfolio communicates through repository metadata, programming languages, documentation, and activity—not to assign developers an arbitrary overall score.
 
> **Current status:** The core GitHub data-fetching and analysis functionality is implemented, and the Streamlit dashboard contains all six major sections plus a sticky section navigation bar. The ui_design branch is complete and ready for a pull request. The next planned work is better error handling in the API layer and the UI.
 
## Table of contents
 
- [Project goals](#project-goals)
- [Technology stack](#technology-stack)
- [Features implemented](#features-implemented)
- [Application architecture](#application-architecture)
- [Project structure](#project-structure)
- [Getting started](#getting-started)
- [Environment configuration](#environment-configuration)
- [Running the application](#running-the-application)
- [Current UI design](#current-ui-design)
- [Current issues and troubleshooting](#current-issues-and-troubleshooting)
- [Roadmap](#roadmap)
- [Development workflow](#development-workflow)
- [Learning objectives](#learning-objectives)
- [Project principles](#project-principles)
---
 
## Project goals
 
The Developer Portfolio Analyzer examines public GitHub information to help people understand how their projects are presented.
 
The application aims to:
 
- Retrieve public GitHub profile and repository information through the GitHub REST API.
- Analyze repository structure, programming languages, documentation, metadata, and recent activity.
- Distinguish original repositories from forks and identify archived repositories.
- Present the findings in a clear, recruiter-friendly dashboard.
- Report observable facts instead of assigning a generic developer score.
- Build practical Python and backend development skills through incremental implementation.
The project is being developed incrementally. The CLI provides an initial environment for learning Python and API integration, while Streamlit provides a more visual way to present the analysis.
 
## Technology stack
 
| Technology | Purpose |
|---|---|
| Python | Application logic and data analysis |
| GitHub REST API | Public profile and repository data |
| `requests` | HTTP requests |
| `python-dotenv` | Loading environment variables from `.env` |
| Streamlit | Interactive dashboard |
| Altair | Language visualizations |
| pytest | Testing dependency for the project |
 
Current pinned dependencies:
 
```text
requests==2.34.2
python-dotenv==1.2.3
pytest==9.1.1
streamlit==1.64.0
```
 
Python is the main learning focus. The implementation favors readable code and introduces additional architecture or dependencies when there is a clear reason to do so.
 
## Features implemented
 
### 1. GitHub profile information
 
The application can fetch and process a public GitHub user profile.
 
The dashboard displays:
 
- Profile avatar.
- Display name, falling back to the GitHub username when no name is available.
- GitHub username.
- Biography, with a fallback when no biography is provided.
- Location and company when available.
- Link to the GitHub profile.
- Public repository count.
- Follower count.
- Following count.
- Account creation year.
The username input is stripped of surrounding whitespace, and an empty username is rejected before the application attempts to fetch the profile.
 
### 2. Repository fetching and pagination
 
The GitHub API layer retrieves repositories through the user's public repositories endpoint.
 
Repository fetching supports pagination using:
 
- `per_page=100`
- An incrementing `page` parameter.
- Repeated requests until an empty page is returned.
This allows the application to retrieve more than the first page of repositories.
 
The application processes repository information into a consistent structure containing fields such as:
 
- Repository name and URL.
- Description.
- Primary language.
- Topics.
- Fork status.
- Archived status.
- Star count.
- Fork count.
- Creation timestamp.
- Last-pushed timestamp.
### 3. Repository overview
 
The repository overview summarizes the public repositories returned by the API.
 
It distinguishes:
 
- **Total repositories:** All repositories retrieved.
- **Original repositories:** Repositories that are not forks.
- **Forked repositories:** Repositories marked as forks.
- **Archived repositories:** Archived original repositories.
The dashboard presents the overview as three metric cards for original, forked, and archived repositories. The profile section separately displays the public repository count provided by GitHub.
 
### 4. Programming language analysis
 
The application analyzes programming languages in two complementary ways.
 
#### Primary-language distribution
 
The analyzer examines GitHub's primary language field for each original repository.
 
It calculates language counts and percentages, while also tracking repositories without a primary language.
 
The dashboard displays the distribution in a donut-style chart with a corresponding language legend.
 
#### Languages across repositories
 
The application also fetches the GitHub `/languages` endpoint for each original repository.
 
This endpoint provides a more detailed view of the languages GitHub detects in a repository. The analyzer counts how many original repositories contain each language.
 
The dashboard displays these counts in a horizontal bar chart.
 
The application defines colors for common programming languages and uses a default color for languages not explicitly listed.
 
The analysis distinguishes between repositories with no detected language data and requests whose results are unknown. These situations should not be interpreted as equivalent.
 
### 5. Portfolio metadata and README coverage
 
The application examines whether original repositories provide useful descriptive information.
 
#### Description coverage
 
Counts original repositories with and without a description and calculates the percentage that include one.
 
#### Topics coverage
 
Counts original repositories with and without GitHub topics and calculates the corresponding percentage.
 
#### README coverage
 
The API layer checks whether each original repository has a README.
 
The analyzer distinguishes three outcomes:
 
- README found.
- README not found.
- README status unknown because the request did not produce a reliable result.
Coverage is calculated using known results, rather than incorrectly treating failed requests as repositories without READMEs.
 
The dashboard presents README, description, and topics coverage in three cards with percentages, progress bars, and repository counts.
 
### 6. Repository activity
 
The activity analysis focuses on original repositories.
 
It:
 
- Reads repository `pushed_at` timestamps.
- Sorts repositories by most recent update.
- Counts repositories updated within the last 90 days.
- Groups repository activity into four freshness periods.
The periods displayed in the dashboard are:
 
| Period | Meaning |
|---|---|
| Last 90 days | Updated within the last 90 days |
| 91–365 days | Updated between 91 days and one year ago |
| 1–2 years | Updated between one and two years ago |
| Over 2 years | Updated more than two years ago |
 
The dashboard also displays the three most recently updated original repositories and their update dates.
 
These observations describe public repository activity. They do not determine whether a developer is productive or whether a repository is good or bad.
 
### 7. Repository cards
 
The dashboard displays original repositories as individual cards.
 
The cards can present:
 
- Repository name and GitHub link.
- Description.
- Primary language.
- Detected languages.
- Topics.
- README status.
- Star count.
- Fork count.
- Last-pushed date.
Repositories are displayed in a three-column layout, with six repositories per page.
 
Pagination uses `st.session_state.repository_page` to retain the selected page across Streamlit reruns. After a new analysis, the repository page resets to page one.
 
### 8. Streamlit dashboard
 
The Streamlit application currently contains the following sections:
 
1. Developer Profile
2. Repository Overview
3. Languages
4. Portfolio Metadata
5. Repository Activity
6. Repositories
7. Section navigation
The dashboard includes a GitHub username input and an Analyze button. Analysis results are stored in `st.session_state`, allowing the dashboard to render from the stored result rather than requiring a new GitHub analysis on every interaction.
 
The interface is organized into separate modules under `ui/`, with shared styling maintained in `ui/styles.py`.

The dashboard also includes a sticky, full-width navigation bar below Streamlit's header. It contains links with icons to all six sections and is defined in `ui/navigation.py`. The links point to anchors that Streamlit generates from each section heading (for example `#languages`), so renaming a heading requires updating its link.
 
### 9. GitHub API request handling
 
The GitHub API module includes several basic request safeguards:
 
- A shared helper for constructing Bearer authentication headers.
- Ten-second request timeouts.
- Handling for timeout exceptions.
- Handling for connection errors.
- General `requests` exception handling.
- Basic status handling for common responses, including 401, 403, and 404.
- Basic rate-limit detection using GitHub response headers.
- Partial results for some README and language requests that fail.
The API functions generally print error messages and return `None` or partial data. Improving how the UI receives and presents these errors is a future task.
 
---
 
## Application architecture
 
The project currently separates data retrieval, analysis, command-line execution, and dashboard presentation.
 
### Main responsibilities
 
**`github_api.py`**
 
Responsible for communication with GitHub, including profile fetching, repository pagination, README checks, and detailed language requests.
 
**`analysis.py`**
 
Responsible for processing API data and calculating repository summaries, language statistics, metadata coverage, README coverage, activity freshness, and repository presentation data.
 
**`main.py`**
 
The intended command-line entry point for coordinating the analysis workflow and presenting results in the terminal.
 
**`streamlit_app.py`**
 
Coordinates the dashboard workflow. It loads configuration, calls the API and analysis functions, stores the analysis result in session state, and renders the dashboard sections.
 
**`ui/`**
 
Contains the individual Streamlit presentation modules and shared CSS.
 
The CLI and Streamlit entry points currently perform similar orchestration. Reviewing and reducing this duplication is planned for a later architecture phase, not the current UI design work.
 
## Project structure
 
The current dashboard and backend are organized approximately as follows:
 
```text
developer-portfolio-analyzer/
├── main.py
├── github_api.py
├── analysis.py
├── streamlit_app.py
├── requirements.txt
├── README.md
├── PROJECT_STATUS.md
├── .gitignore
├── .env
├── .streamlit/
    └── config.toml
├── ui/
    ├── __init__.py
    ├── profile.py
    ├── overview.py
    ├── languages.py
    ├── metadata.py
    ├── activity.py
    ├── repositories.py
    ├── navigation.py
    └── styles.py
└── tests
    ├── test_analysis.py
    └── test_github_api.py
```
 
The `.env` file is a local configuration file and must not be committed. It should be excluded by `.gitignore`.
 
## Getting started
 
### Prerequisites
 
- Python installed.
- Git.
- A GitHub account.
- A GitHub personal access token for authenticated API requests.
- A terminal and code editor.
### 1. Clone the repository
 
```bash
git clone <repository-url>
cd developer-portfolio-analyzer
```
 
Replace `<repository-url>` with the actual GitHub repository URL.
 
### 2. Create a virtual environment
 
On macOS or Linux:
 
```bash
python3 -m venv .venv
source .venv/bin/activate
```
 
On Windows:
 
```powershell
python -m venv .venv
.venv\Scripts\activate
```
 
Use the virtual environment for installing dependencies and running the application.
 
### 3. Install dependencies
 
```bash
python -m pip install -r requirements.txt
```
 
### 4. Configure the GitHub token
 
Create a `.env` file in the project root:
 
```dotenv
GITHUB_TOKEN=your_github_token_here
```
 
Replace the placeholder with your own token. Do not commit the token or share it publicly.
 
The application uses `python-dotenv` to load environment variables from this file.
 
## Running the application
 
### Streamlit dashboard
 
From the project root, activate the virtual environment and run:
 
```bash
streamlit run streamlit_app.py
```
 
Streamlit should provide a local URL in the terminal. Open that URL in your browser.
 
Enter a GitHub username and select **Analyze** to load the profile and dashboard.
 
If the dashboard does not start, first check that the virtual environment is active and that the dependencies installed successfully.
 
### Command-line interface
 
The project also has a `main.py` entry point intended for the CLI workflow.
 
```bash
python main.py
```
 
The exact CLI behavior should be verified against the current working-tree version of `main.py` before treating it as a supported, tested workflow.
 
## Current UI design
 
The dashboard uses a dark navy theme with restrained indigo accents.
 
| Purpose | Color |
|---|---|
| Page background | `#0B1120` |
| Card surface | `#111C30` |
| Primary text | `#E2E8F0` |
| Heading text | `#F1F5F9` |
| Secondary text | `#94A3B8` |
| Accent | `#818CF8` |
| Primary button | `#6366F1` |
| Existing subtle divider | `#263449` |
| Card border (set in `.streamlit/config.toml`) | `#475569` |
 
The shared CSS in `ui/styles.py` controls headings, section spacing, card content, language legends, coverage progress bars, activity rows, repository badges, buttons, and other presentation details.
 
The white strip at the top of the application has already been addressed by styling Streamlit's native header:
 
```css
header[data-testid="stHeader"] {
    background-color: #0B1120;
}
```

Card borders are set through Streamlit's theme rather than custom CSS. `.streamlit/config.toml` contains:

```toml
[theme]
borderColor = "#475569"
```

Streamlit's native widgets (the charts and the username input) intentionally keep their light styling. Setting `base = "dark"` was tried and rejected because the light panels were preferred.

Vertical spacing between sections is controlled by `.section-header` in `ui/styles.py` (`margin-top: 1.75rem`, reduced from `3.5rem`).
 
The dashboard width is currently set to a maximum of `1180px`. It appeared narrow in earlier screenshots because the browser was zoomed out to 50%; at 100% zoom, the width was considered acceptable. Do not change the width as part of the border fix.

---

## Current issues and troubleshooting

### 1. Resolved: card and panel borders were too subtle

**Status: Fixed.**

The earlier CSS targeted `div[data-testid="stVerticalBlockBorderWrapper"]`, which does not exist in Streamlit 1.64.0, so the rules matched nothing. In this version, `st.container(border=True)` renders a `div.stVerticalBlock` whose border is drawn by Streamlit from the theme's `borderColor`.

**Fix:** a new `.streamlit/config.toml` containing:

```toml
[theme]
borderColor = "#475569"
```

This was verified in the browser's DevTools: the container's computed rule is `border: 1px solid rgb(71, 85, 105)`. The internal dividers still use `#263449` from `ui/styles.py`.

**Limitations:**

- The setting is global, so every Streamlit-drawn border (including the text input) uses this color.
- Border thickness is still Streamlit's default 1px. No theme option for width was found, and a CSS workaround would depend on generated class names.

**Lesson:** inspect the rendered DOM for the installed Streamlit version before writing selectors, and do not rely on generated `st-emotion-cache-*` class names.

### 2. Navigation and vertical scrolling

**Status: Implemented. Grouping was reviewed and dropped.**

- A sticky, full-width bar with links and icons for the six sections is defined in `ui/navigation.py` and styled in `ui/styles.py`.
- The links use the anchors Streamlit generates from heading text: `#developer-profile`, `#repository-overview`, `#languages`, `#portfolio-metadata`, `#repository-activity` and `#repositories`. All six were tested.
- The bar sticks at `top: 60px`, which is the height of Streamlit's own header. `.stMain` has `scroll-padding-top: 100px` so section titles are not hidden behind the bar after a jump.
- The bar is made sticky by applying `position: sticky` to its Streamlit wrapper (`.stElementContainer:has(.section-nav)`). This uses the CSS `:has()` selector and has been tested in Chrome only.
- Vertical spacing was reduced (`.section-header` margin-top is now `1.75rem`) instead of regrouping sections.
- The dashboard width (max `1180px`) was not changed.

### 3. Responsive layout

**Status: Checked at phone (390px) and tablet widths. No further problems found.**

Fixes made:

- Repository pagination buttons are wider so "← Previous" is not truncated on tablet.
- Streamlit stacks columns at 640px. Below that width, the "Page X of Y" text needed different spacing to sit evenly between the stacked buttons, so `.repo-pagination` has a `@media (max-width: 640px)` rule.

Known minor leftover:

- Repository cards in the same row can differ in height when their language badges wrap onto extra lines. Equalizing heights would need CSS on several of Streamlit's wrapper layers, so it was left as optional polish.

Any other narrow-screen problems found later should be fixed individually.

### 4. Error presentation in Streamlit

**Status: Next planned work (Phase B, step 7).**

The API layer currently prints many error messages and returns `None` or partial results. That approach is not ideal for a browser interface.

Observed behavior: entering a username that does not exist shows only the generic message "Could not load this GitHub profile." in the dashboard. The specific cause (404, rate limit, bad token) is only printed to the terminal.

The application should present useful messages for cases such as invalid usernames, authentication failures, rate limits, network failures, and incomplete analysis results.

### 5. Testing and verification

**Status: Backend tests pass. The dashboard was checked manually.**

- `python -m pytest` runs 19 tests (9 in `tests/test_analysis.py` and 10 in `tests/test_github_api.py`), and all pass.
- The tests cover the API layer and the analysis functions. There are no automated UI tests.
- The dashboard workflow was exercised manually in Chrome: navigation links, sticky behavior, pagination, card borders, and the phone and tablet widths.
- The diff against `main` contains no changes to `github_api.py`, `analysis.py` or `main.py`.

Future backend tests should cover API failure behavior, pagination, empty portfolios, timestamp handling, and unknown README or language results.

---

## Roadmap

The roadmap is split into two parts: finishing the current `ui_design` branch and continuing the broader project afterward.

### Phase A — Finish the current `ui_design` branch

#### 1. Fix card border visibility — **Status: Done.**

- Diagnose why the two previous CSS attempts had no visible effect.
- Verify the actual Streamlit container styling mechanism.
- Apply a targeted, consistent border treatment.
- Confirm the result on profile, metric, chart, metadata, activity, and repository cards.
**Completion criterion:** Card boundaries are visibly distinct from the page background, with no unnecessary nested outlines.

#### 2. Add simple dashboard navigation - **Status: Done.**

- Experiment with links or navigation anchors to the major dashboard sections.
- Keep the navigation straightforward and consistent with the existing design.
- Avoid introducing a complex navigation system without a clear need.
**Completion criterion:** Users can move between major sections without excessive manual scrolling.

#### 3. Improve grouping and vertical rhythm - **Status: Done. Spacing reduced; regrouping sections was reviewed and not needed.**
 
- Review how the dashboard sections relate to each other.
- Reduce unnecessary vertical scrolling where possible.
- Keep cards readable and preserve the existing information hierarchy.
- Do not change the overall width without evidence that it is needed.
**Completion criterion:** The dashboard feels cohesive and is easier to scan.
 
#### 4. Check responsive behavior - **Status: Done at phone and tablet widths.**
 
- Check desktop, tablet, and mobile widths.
- Fix observed wrapping, spacing, chart, button, or overflow problems.
- Keep the existing desktop layout unless the testing reveals an actual issue.
**Completion criterion:** The main dashboard sections remain usable across the checked viewport sizes.

#### 5. Perform a final visual review - **Status: Done. Charts and the input intentionally keep light styling.**

Review:

- Card outlines and internal dividers.
- Spacing and section headings.
- Text contrast.
- Buttons and link buttons.
- Language charts and legends.
- Metadata progress bars.
- Repository badges and pagination.
**Completion criterion:** The design is consistent across all six dashboard sections.

#### 6. Verify and finish the branch - **Status: Tests pass and the manual check is done. Remaining: open and merge the pull request.**

- Run the Streamlit app.
- Run the tests that exist.
- Inspect `git diff`.
- Commit the completed UI changes on `ui_design`.
- Prepare a concise pull request description.
**Completion criterion:** The branch contains a coherent, tested UI polish pass without unrelated backend scope expansion.
 
### Phase B — Future application improvements
 
These are follow-up tasks, not requirements for the current visual-design branch.
 
#### 7. Improve API and UI error handling
 
- Review missing-token behavior.
- Improve how network errors, timeouts, authentication failures, rate limits, and server errors are represented.
- Avoid treating failed requests as confirmed missing data.
- Make the Streamlit UI show meaningful feedback when analysis cannot be completed.
- Preserve useful partial results where appropriate.

#### 8. Review API-layer architecture

- Review responsibilities across `main.py`, `github_api.py`, `analysis.py`, and `streamlit_app.py`.
- Reduce duplicated orchestration between the CLI and Streamlit where it makes sense.
- Keep API fetching separate from analysis and presentation.
- Avoid introducing abstractions that do not solve an actual problem.

#### 9. Build and expand automated tests

- Establish a practical test structure using pytest.
- Test repository summaries and analysis functions.
- Test pagination and API response handling without depending on live GitHub requests.
- Cover empty input data, missing values, timestamps, and unknown request results.
- Add regression tests for bugs discovered during development.

#### 10. Review remaining analysis opportunities

Evaluate whether further descriptive insights would materially improve the analyzer.

Possible areas to consider include:

- Additional project-diversity observations.
- More useful repository-level presentation details.
- Further activity or freshness insights.
- Additional descriptive metadata, where reliable data is available.
Any new signal should have a clear purpose and should communicate observable information. Do not add features merely to increase the number of metrics.
 
#### 11. Review the CLI workflow
 
- Confirm the CLI works reliably with the current API behavior.
- Improve its handling of configuration and incomplete requests where needed.
- Keep the CLI useful as a simple way to exercise and understand the backend.
#### 12. Deployment
 
Once the dashboard and API behavior are stable:
 
- Choose a deployment platform.
- Configure environment variables securely.
- Test the deployed application.
- Document any limitations, such as API rate limits or expected loading times.
#### 13. Documentation and portfolio presentation
 
After the application reaches a stable milestone:
 
- Keep the README aligned with the implemented features.
- Add setup and usage examples that have been verified.
- Include representative screenshots once the design is finished.
- Document the project's architecture and key learning outcomes.
- Prepare a concise project description for a CV or LinkedIn portfolio.
---
 
## Development workflow
 
The project is developed on feature branches so that each stage remains understandable and reviewable.
 
A typical workflow is:
 
```bash
git status
git switch ui_design
```
 
Make and test the intended changes, then inspect the diff:
 
```bash
git diff
git status
```
 
When the changes are ready, commit them with a message describing the work:
 
```bash
git add .
git commit -m "Improve dashboard card styling"
```
 
Push the branch when appropriate:
 
```bash
git push
```
 
Use the actual branch name and review the staged changes before committing. Avoid committing `.env` or unrelated changes.
 
The current branch should stay focused on UI presentation, navigation, responsive behavior, and final UI verification. Backend robustness, broader refactoring, and new analysis features belong in later work.
 
## Learning objectives
 
This project is intended to develop practical Python and backend skills through implementation, not simply produce an application as quickly as possible.
 
Key learning areas include:
 
- Python functions, dictionaries, lists, loops, and data transformations.
- Working with external APIs using `requests`.
- HTTP status codes, authentication, pagination, timeouts, and exceptions.
- Separating data fetching from analysis and presentation.
- Handling missing and unknown data correctly.
- Managing environment variables and virtual environments.
- Understanding Streamlit's execution and session-state model.
- Building charts from structured data.
- Writing tests and debugging failures.
- Using Git branches, commits, and pull requests.
- Making incremental architectural decisions based on actual needs.
The implementation should remain readable and understandable to a developer learning Python, while still following sensible engineering practices.

## Project principles

1. **No arbitrary developer score.** Report descriptive evidence rather than a simplistic overall rating.
2. **Distinguish missing data from unknown data.** Failed API requests should not automatically count as absent information.
3. **Build incrementally.** Finish a focused stage before expanding the scope.
4. **Keep responsibilities clear.** Fetching, analysis, and presentation should remain conceptually distinct.
5. **Avoid premature architecture.** Add abstractions when they solve a demonstrated problem.
6. **Preserve the learning objective.** Understand the implementation rather than treating the project as a code-generation exercise.
7. **Verify visual changes in the running application.** Do not assume that a CSS rule works just because it has been added.
8. **Keep the documentation honest.** Distinguish implemented functionality, unresolved issues, and planned improvements.

---

## Current next step

Open the pull request for `ui_design` and merge it. Then start Phase B, step 7 (API and UI error handling) on a new branch, beginning with the generic "Could not load this GitHub profile." message.
