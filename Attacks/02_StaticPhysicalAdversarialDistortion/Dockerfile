FROM ubuntu:18.04

WORKDIR /usr/src/app

RUN apt-get update && apt-get install python2.7 curl libsm6 libxext6 libxrender-dev libglib2.0-0 wget -y
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py

RUN python2.7 get-pip.py
RUN pip install pipenv

RUN pipenv install tensorflow==1.4.1
RUN pipenv install keras==1.2.0
RUN pipenv install scipy
RUN pipenv install opencv-python==4.1.1.26
RUN pipenv install pillow
RUN pipenv install scikit_learn

RUN echo "alias python='python2.7'" >> ~/.bash_aliases

CMD [ "bash" ]
