FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt


# Expose the port that the application will run on
EXPOSE 9101
CMD ["python", "my_exporter.py"]