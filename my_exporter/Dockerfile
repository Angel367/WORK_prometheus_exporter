FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the local code to the container
COPY . .

# Download Go modules
RUN pip install -r requirements.txt

# Build the Go application


# Expose the port that the application will run on
EXPOSE 9101
CMD ["python", "my_exporter.py"]