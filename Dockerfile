from w505703394/centos:dev_base

ENV PYTHONPATH=${PYTHONPATH}:/root/gencode \
    GOPATH=/root/go

COPY . /root/gencode

WORKDIR /root/gencode

CMD ["python3", "examply.py"]
