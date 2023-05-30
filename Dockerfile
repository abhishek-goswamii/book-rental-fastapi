FROM python:3.10.6

WORKDIR /usr/src/app 

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "main:app", "-w", "4", "-b", "0.0.0.0:8000"]