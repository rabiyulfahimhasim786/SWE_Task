FROM rasa/rasa:latest

WORKDIR /app

# USER root
# RUN pip3 install --upgrade pip

# RUN pip3 install spacy==2.3.2
# RUN python3 -m spacy download en_core_web_md
COPY . /app

RUN rasa telemetry disable

ENV RASA_TELEMETRY_DEBUG=false
# RUN rasa train nlu

CMD [ "run","-m","/app/models/","--enable-api","--debug" ]