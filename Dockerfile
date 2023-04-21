FROM python:3
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD src /poker-settler
WORKDIR /poker-settler
ENTRYPOINT [ "python", "app.py" ]
