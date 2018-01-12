FROM python:3
ARG YOTI_APPLICATION_ID
ARG YOTI_CLIENT_SDK_ID
ARG YOTI_FULL_KEY_FILE_PATH
RUN if [ "$YOTI_APPLICATION_ID" = "" ] ; then echo YOTI_APPLICATION_ID not provided; exit 1; else echo YOTI_APPLICATION_ID is $YOTI_APPLICATION_ID ; fi
RUN if [ "$YOTI_CLIENT_SDK_ID" = "" ] ; then echo YOTI_CLIENT_SDK_ID not provided; exit 1; else echo YOTI_CLIENT_SDK_ID is $YOTI_CLIENT_SDK_ID ; fi
RUN if [ "$YOTI_FULL_KEY_FILE_PATH" = "" ] ; then echo YOTI_FULL_KEY_FILE_PATH not provided; exit 1; else echo YOTI_FULL_KEY_FILE_PATH is $YOTI_FULL_KEY_FILE_PATH ; fi
ADD . /code
WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]