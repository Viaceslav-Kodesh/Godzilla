FROM ubuntu:latest

RUN apt-get update && apt-get install python-pip -y && apt-get install git -y
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
