FROM python:3.9
WORKDIR /kjell/hello_world
COPY requirements.txt .
RUN python -m venv venv
ENV PATH="/kjell/hello_world/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]