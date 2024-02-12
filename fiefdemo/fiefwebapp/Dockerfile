# Use official
FROM python:3.11.2

# Set working dir within the container
WORKDIR /code

# Copy and install requirements
COPY ./requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt --verbose

# Copy source code including config
COPY ./app /code/app
COPY ./config /code/config

# Command to start the fastapi app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
