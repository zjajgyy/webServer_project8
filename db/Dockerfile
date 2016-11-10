FROM ubuntu:16.04
FROM python:3
RUN pip install python-consul -i https://mirrors.ustc.edu.cn/pypi/web/simple
RUN pip install flask -i https://mirrors.ustc.edu.cn/pypi/web/simple
ADD Database.py /
ADD sqlite.db /
CMD ["python","./Database.py"]
