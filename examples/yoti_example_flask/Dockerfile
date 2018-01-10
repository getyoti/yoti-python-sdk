FROM python:3
ARG YOTI_APPLICATION_ID
ARG YOTI_CLIENT_SDK_ID
ARG YOTI_FULL_KEY_FILE_PATH
ADD . /code
WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt
RUN sed -i "s|environ.get('YOTI_APPLICATION_ID')|'$YOTI_APPLICATION_ID' |g" settings.py
RUN sed -i "s|environ.get('YOTI_CLIENT_SDK_ID')|'$YOTI_CLIENT_SDK_ID' |g" settings.py
RUN sed -i "s|environ.get('YOTI_KEY_FILE_PATH')|'$YOTI_FULL_KEY_FILE_PATH' |g" settings.py
CMD ["python", "app.py"]