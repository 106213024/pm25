FROM python:3.8
LABEL maintainer="ying"
COPY . /app
ENV TZ Asia/Taipei
ENV DBUSER web
ENV DBPASSWORD password
RUN wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update -qqy 
RUN apt-get -qqy install google-chrome-stable fonts-arphic-ukai 
RUN rm /etc/apt/sources.list.d/google-chrome.list 
RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/*
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
RUN cd /app && pip install -r requirements.txt
WORKDIR /app
EXPOSE 4399
CMD celery -A tasks worker -l info --pool=solo & python app.py
