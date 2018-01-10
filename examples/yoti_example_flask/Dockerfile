FROM python:3
ARG YOTI_APPLICATION_ID
ARG YOTI_CLIENT_SDK_ID
ARG YOTI_FULL_KEY_FILE_PATH
RUN if [ "$YOTI_APPLICATION_ID" = "your_application_id" ] ; then echo YOTI_APPLICATION_ID not provided in docker-compose file; exit 1; else echo YOTI_APPLICATION_ID is $YOTI_APPLICATION_ID ; fi
RUN if [ "$YOTI_CLIENT_SDK_ID" = "your_client_sdk_id" ] ; then echo YOTI_CLIENT_SDK_ID not provided in docker-compose file; exit 1; else echo YOTI_CLIENT_SDK_ID is $YOTI_CLIENT_SDK_ID ; fi
RUN if [ "$YOTI_FULL_KEY_FILE_PATH" = "path_to_your_pem_file" ] ; then echo YOTI_FULL_KEY_FILE_PATH not provided in docker-compose file; exit 1; else echo YOTI_FULL_KEY_FILE_PATH is $YOTI_FULL_KEY_FILE_PATH ; fi
ADD . /code
WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt
RUN sed -i "s|environ.get('YOTI_APPLICATION_ID')|'$YOTI_APPLICATION_ID' |g" settings.py
RUN sed -i "s|environ.get('YOTI_CLIENT_SDK_ID')|'$YOTI_CLIENT_SDK_ID' |g" settings.py
RUN sed -i "s|environ.get('YOTI_KEY_FILE_PATH')|'$YOTI_FULL_KEY_FILE_PATH' |g" settings.py
CMD ["python", "app.py"]