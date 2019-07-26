from django.views.generic import TemplateView
from dotenv import load_dotenv, find_dotenv


from yoti_python_sdk import Client
from yoti_python_sdk.dynamic_sharing_service import (
    DynamicScenarioBuilder,
    create_share_url,
)
from yoti_python_sdk.dynamic_sharing_service.policy import DynamicPolicyBuilder

load_dotenv(find_dotenv())

from app_settings import (
    YOTI_SCENARIO_ID,
    YOTI_CLIENT_SDK_ID,
    YOTI_KEY_FILE_PATH,
)  # noqa


class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response({"scenario_id": YOTI_SCENARIO_ID})


class DynamicShareView(TemplateView):
    template_name = "dynamic_share.html"

    def get(self, request, *args, **kwargs):
        client = Client(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
        policy = DynamicPolicyBuilder().with_full_name().with_age_over(18).build()
        scenario = (
            DynamicScenarioBuilder()
            .with_policy(policy)
            .with_callback_endpoint("/yoti/auth")
            .build()
        )
        share = create_share_url(client, scenario)
        context = {
            "yoti_client_sdk_id": YOTI_CLIENT_SDK_ID,
            "yoti_share_url": share.share_url,
        }
        return self.render_to_response(context)


class AuthView(TemplateView):
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        client = Client(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
        activity_details = client.get_activity_details(request.GET["token"])
        profile = activity_details.profile
        profile_dict = vars(profile)

        context = profile_dict.get("attributes")
        context["base64_selfie_uri"] = getattr(activity_details, "base64_selfie_uri")
        context["user_id"] = getattr(activity_details, "user_id")
        context["parent_remember_me_id"] = getattr(
            activity_details, "parent_remember_me_id"
        )
        context["receipt_id"] = getattr(activity_details, "receipt_id")
        context["timestamp"] = getattr(activity_details, "timestamp")

        # change this string according to the age condition defined in Yoti Hub
        age_verified = profile.get_attribute("age_over:18")
        if age_verified is not None:
            context["age_verified"] = age_verified

        selfie = context.get("selfie")
        if selfie is not None:
            self.save_image(selfie.value)
        return self.render_to_response(context)

    @staticmethod
    def save_image(selfie_data):
        fd = open("yoti_example/static/YotiSelfie.jpg", "wb")
        fd.write(selfie_data)
        fd.close()
