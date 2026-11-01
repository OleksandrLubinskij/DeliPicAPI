FROM python:3.14.5-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /DeliPicAPI
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]