FROM python:3.13.3-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x script/entrypoint.sh

ENTRYPOINT ["bash", "script/entrypoint.sh"]