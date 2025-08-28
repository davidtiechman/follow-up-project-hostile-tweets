@echo off
REM -------------------------------
REM Persister Service Docker Build & Push
REM -------------------------------

REM Set image name and tag
SET IMAGE_NAME=your_dockerhub_username/persister_service
SET IMAGE_TAG=latest

REM Navigate to the project root (where Dockerfile is)
cd /d %~dp0

REM Build the Docker image
echo Building Docker image...
docker build -t %IMAGE_NAME%:%IMAGE_TAG% .

REM Push the Docker image to Docker Hub
echo Pushing Docker image...
docker push %IMAGE_NAME%:%IMAGE_TAG%

echo Done!
pause