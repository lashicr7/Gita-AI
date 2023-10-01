# Build the Docker image
docker build -t gitaaiimg .
docker run -p 8000:8000 gitaaiimg