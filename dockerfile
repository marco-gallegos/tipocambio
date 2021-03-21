# @Author   Marco A. Gallegos Loaeza <ma_galeza@hotmail.com>
# @Date     2020/03/11
# @Update     2020/03/11 -> initial
# @Description
#   This a docker file to deploy the app on production using gunicorn.
FROM python:3.8-alpine

WORKDIR /app

ENV TZ=America/Mexico_City

COPY requirements.txt .

COPY migrate.py .

RUN pip install -r requirements.txt

EXPOSE 5555

# CMD python api.py
# CMD gunicorn -w 2 -k gthread -b 0.0.0.0:5555 api:API
CMD uvicorn --workers 2 --host 0.0.0.0 --port 5555 api:app