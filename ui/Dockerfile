FROM python:3.5-alpine
WORKDIR /app
# for building c++
RUN apk add --update-cache g++
# for converting ppm -> png
RUN apk add imagemagick

# python server
COPY requirements.txt  ./
RUN pip install wheel
RUN pip install -r requirements.txt
COPY server.py ./

# c++ program
COPY main.cpp ./

# Frontend
COPY templates/ ./templates
COPY static/ ./static

EXPOSE 5000

CMD [ "python", "server.py" ]
