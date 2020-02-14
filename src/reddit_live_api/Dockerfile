FROM python:3.5-alpine3.10
RUN apk update
RUN apk add --update python3 py-pip make automake gcc g++ subversion python3-dev libpng-dev freetype-dev graphviz libjpeg
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h;
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN alias python=python3
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python" ]
CMD [ "run.sh" ]