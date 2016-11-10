FROM ubuntu:16.04
FROM python:3

RUN pip install python-consul -i https://mirrors.ustc.edu.cn/pypi/web/simple
RUN pip install flask -i https://mirrors.ustc.edu.cn/pypi/web/simple
RUN pip install requests -i https://mirrors.ustc.edu.cn/pypi/web/simple

ADD Server.py /
ADD templates/ /templates/
ADD static/ /static/
CMD ["python","./Server.py"]

