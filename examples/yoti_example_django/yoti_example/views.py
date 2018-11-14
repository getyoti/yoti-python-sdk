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
        profile = activity_details.profile
        profile_dict = vars(profile)

        context = profile_dict.get('attributes')
        context['base64_selfie_uri'] = getattr(activity_details, 'base64_selfie_uri')
        context['user_id'] = getattr(activity_details, 'user_id')
        context['receipt_id'] = getattr(activity_details, 'receipt_id')
        context['timestamp'] = getattr(activity_details, 'timestamp')

        # change this string according to the age condition defined in dashboard
        age_verified = profile.get_attribute('age_over:18')
        if age_verified is not None:
            context['age_verified'] = age_verified

        selfie = context.get('selfie')
        if selfie is not None:
            self.save_image(selfie.value)
        return self.render_to_response(context)

    @staticmethod
    def save_image(selfie_data):
        fd = open('yoti_example/static/YotiSelfie.jpg', 'wb')
        fd.write(selfie_data)
        fd.close()
