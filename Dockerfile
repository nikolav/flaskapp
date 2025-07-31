FROM python:3.12.2

# Set work directory
WORKDIR /home/app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy files
COPY . .

# Expose Flask port
EXPOSE 5000

# Run app
# CMD ["python", "app.py"]
CMD ["./wserver.sh"]
