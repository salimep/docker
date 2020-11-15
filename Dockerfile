FROM python:3.6.5
WORKDIR /opt/
RUN  apt-get install -y bash
ADD blog/requirements.txt /opt/
RUN pip install -r requirements.txt
RUN mkdir -p /opt/blog/
COPY blog/static /opt/blog/static/
COPY blog/templates /opt/blog/templates/
COPY blog/blog/*.py /opt/blog/
COPY blog/run.py /opt/
COPY blog/blog/__init__.py /opt/blog/
VOLUME /opt/:/opt/blog/
ENTRYPOINT [ "python","./run.py"]
