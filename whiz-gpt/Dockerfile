# Use the official Python image as a base
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the Python dependencies from requirements.txt
RUN pip3 install -r requirements.txt

# Expose the port that the Streamlit app will run on
EXPOSE 8080

# Specify the command to run the Streamlit application
CMD ["streamlit", "run", "--server.port", "8080", "main.py"]

