### Install all dependencies
FROM ubuntu
RUN apt-get update -y
RUN apt-get install python3.7 -y
RUN apt-get install python3-pip -y
RUN pip3 install pyyaml 
RUN apt-get install wget -y

### Download and install our app
RUN wget https://www.dropbox.com/s/9xeqnc8l6wderaq/smarthouse-1.1.0.tar.gz
RUN pip3 install smarthouse-1.1.0.tar.gz

### Set up port
#EXPOSE 50000