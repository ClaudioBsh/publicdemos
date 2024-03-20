# Use official
FROM python:3.12

# Set working dir within the container
WORKDIR /code

# Create a virtual environment and activate it
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy and install requirements
COPY ./requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt --verbose

# Copy source code including config
COPY ./app /code/app
COPY ./config /code/config

# Command to start the fastapi app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
