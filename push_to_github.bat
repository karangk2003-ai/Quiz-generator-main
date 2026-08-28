@echo off
echo ===================================================
echo   Pushing AI Quiz Generator to GitHub
echo   Repository: https://github.com/VinayGT2002/Quiz-generator.git
echo ===================================================
echo.

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not in your PATH.
    echo Please download and install Git from: https://git-scm.com/download/win
    echo Then run this script again!
    pause
    exit /b
)

echo [1/5] Initializing Git repository...
git init

echo [2/5] Staging files (ignoring .env and local data)...
git add .

echo [3/5] Creating initial commit...
git commit -m "Initial commit: AI-Powered Quiz Generator (Flask, Groq, ChromaDB)"

echo [4/5] Setting main branch and remote origin...
git branch -M main
git remote remove origin >nul 2>&1
git remote add origin https://github.com/VinayGT2002/Quiz-generator.git

echo [5/5] Pushing to GitHub...
git push -u origin main

echo.
echo ===================================================
echo   Done! Your project is now on GitHub!
echo ===================================================
pause
