# 1. Start from an image that already has Python installed
FROM python:3.11-slim

# 2. Set the working directory inside the image
WORKDIR /app

# 3. Copy ONLY requirements first, so the install layer is cached
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the code (changes often, so it comes last)
COPY . .

# 5. Document the port and define the start command
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
