FROM python:3.8
LABEL maintainer="ying"
COPY . /app
ENV TZ Asia/Taipei
RUN wget --no-check-certificate -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    pip install update && \
    pip install google-chrome-stable fonts-arphic-ukai && \
    rm /etc/apt/sources.list.d/google-chrome.list && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
RUN cd /app && pip install -r requirements.txt
WORKDIR /app
EXPOSE 5000
CMD celery -A tasks worker -l info --pool=solo & python app.py
