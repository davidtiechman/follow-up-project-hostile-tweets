:: Build Docker image
docker build -t data_retrieval_service:latest .

:: Tag for Docker Hub
docker tag data_retrieval_service:latest yourdockerhubusername/data_retrieval_service:latest

:: Push to Docker Hub
docker push yourdockerhubusername/data_retrieval_service:latest