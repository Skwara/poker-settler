FROM python:3
ADD requirements-prod.txt /
RUN pip install -r requirements-prod.txt
ADD src /poker-settler
WORKDIR /poker-settler
ENTRYPOINT [ "python", "app.py" ]
