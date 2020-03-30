FROM ubuntu:latest
RUN apt-get update -y && apt-get install python3-pip -y && pip3 install pip --upgrade && apt-get clean
RUN pip install --upgrade setuptools
RUN pip install python-novaclient
RUN pip install credentials
RUN pip install python-openstacksdk
RUN apt update
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY DataObj.py /
COPY RebootGroupsObj.py /
COPY RebootMachinesObj.py /
COPY action.py /
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
