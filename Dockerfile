FROM python:3.10-slim

# Set working directory
WORKDIR /code

# Install system dependencies for XGBoost/Scikit-learn
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files (app.py, index.html, CSVs, etc.)
COPY . .

# Create models directory (just in case)
RUN mkdir -p /code/models

# Expose the mandatory Hugging Face port
EXPOSE 7860

# Run the app using the updated port logic
CMD ["python", "app.py"]
