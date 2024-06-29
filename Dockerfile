FROM python:3.11
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY . .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


