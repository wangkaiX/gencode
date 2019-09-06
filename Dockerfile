from w505703394/centos:base

ENV PYTHONPATH=${PYTHONPATH}:/root/gencode \
    GOPATH=/root/go

COPY . /root/gencode

WORKDIR /root/gencode

CMD ["./examply.py"]
