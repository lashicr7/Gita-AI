FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --default-timeout=100 future
COPY . .
EXPOSE 8000
CMD ["sh", "-c", "python upload.py && chainlit run model.py -w"]


