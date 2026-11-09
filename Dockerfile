FROM python:3.13.5

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit","run","streamlit_app/Home.py","--server.address=0.0.0.0"]