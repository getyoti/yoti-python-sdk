from django.views.generic import TemplateView
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from yoti_python_sdk import Client
from app_settings import (
    YOTI_APPLICATION_ID,
    YOTI_CLIENT_SDK_ID,
    YOTI_KEY_FILE_PATH
)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'app_id': YOTI_APPLICATION_ID})


class AuthView(TemplateView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        client = Client(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
        activity_details = client.get_activity_details(request.GET['token'])
        context = activity_details.user_profile
        context['base64_selfie_uri'] = getattr(activity_details, 'base64_selfie_uri')

        selfie = context.get('selfie')
        if selfie is not None:
            self.save_image(selfie)
        return self.render_to_response(context)

    @staticmethod
    def save_image(selfie_data):
        fd = open('yoti_example/static/YotiSelfie.jpg', 'wb')
        fd.write(selfie_data)
        fd.close()
