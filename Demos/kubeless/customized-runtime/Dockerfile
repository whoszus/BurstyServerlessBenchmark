FROM bitnami/minideb:jessie

RUN install_packages python2.7 curl ca-certificates git nano
RUN curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py
RUN python2.7 ./get-pip.py

RUN pip install Flask==0.10.1 Flask-API Jinja2==2.7.3 MarkupSafe==0.23 Werkzeug==0.10.4 argparse==1.2.1 itsdangerous==0.24 wsgiref==0.1.2 wsgi-request-logger prometheus_client

ADD custom-lib /lib/
ADD kubeless.py /

USER 1000

CMD ["python2.7", "/kubeless.py"]