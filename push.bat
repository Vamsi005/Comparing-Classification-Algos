:: push.bat – push Project‑Final Year to GitHub
@echo off
rem -------------------------------------------------
rem 1️⃣  Fill in your Personal Access Token (PAT) below.
rem    The token must have the **repo** scope.
rem -------------------------------------------------
set "GITHUB_PAT=YOUR_PERSONAL_ACCESS_TOKEN_HERE"

rem -------------------------------------------------
rem 2️⃣  Repository URL (do NOT edit unless the URL changes)
rem -------------------------------------------------
set "REPO_URL=https://github.com/Vamsi005/Comparing-Classification-Algos.git"

rem -------------------------------------------------
rem 3️⃣  Target branch (most new repos use `main`; change if needed)
rem -------------------------------------------------
set "BRANCH=main"

rem -------------------------------------------------
rem 4️⃣  Initialise repo (skip if .git already exists)
rem -------------------------------------------------
if not exist ".git" (
    git init
) else (
    echo Git repo already initialised.
)

rem -------------------------------------------------
rem 5️⃣  Stage & commit everything
rem -------------------------------------------------
git add .
git commit -m "Initial commit – project files"

rem -------------------------------------------------
rem 6️⃣  Add remote (skip if already added)
rem -------------------------------------------------
git remote remove origin 2>nul
git remote add origin %REPO_URL%

rem -------------------------------------------------
rem 7️⃣  Push using the token (the token is embedded in the URL)
rem -------------------------------------------------
git push https://%GITHUB_PAT%@github.com/Vamsi005/Comparing-Classification-Algos.git %BRANCH%

echo.
echo ==============================
echo   PUSH COMPLETE (or error)
echo ==============================
pause
