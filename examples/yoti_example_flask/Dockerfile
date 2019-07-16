FROM python:3.6.3
ARG YOTI_SCENARIO_ID
ARG YOTI_CLIENT_SDK_ID
ARG YOTI_KEY_FILE_PATH
RUN if [ "$YOTI_SCENARIO_ID" = "yourScenarioId" ] ; then echo YOTI_SCENARIO_ID not set; exit 1; else echo YOTI_SCENARIO_ID is $YOTI_SCENARIO_ID ; fi
RUN if [ "$YOTI_CLIENT_SDK_ID" = "yourClientSdkId" ] ; then echo YOTI_CLIENT_SDK_ID not set; exit 1; else echo YOTI_CLIENT_SDK_ID is $YOTI_CLIENT_SDK_ID ; fi
RUN if [ "$YOTI_KEY_FILE_PATH" = "yourKeyFilePath" ] ; then echo YOTI_KEY_FILE_PATH not set; exit 1; else echo YOTI_KEY_FILE_PATH is $YOTI_KEY_FILE_PATH ; fi
ADD . /code
WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]