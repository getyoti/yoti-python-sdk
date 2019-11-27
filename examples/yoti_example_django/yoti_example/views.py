from django.views.generic import TemplateView
from dotenv import load_dotenv, find_dotenv


from yoti_python_sdk import Client
from yoti_python_sdk.dynamic_sharing_service import (
    DynamicScenarioBuilder,
    create_share_url,
)
from yoti_python_sdk.dynamic_sharing_service.policy import (
    DynamicPolicyBuilder,
    SourceConstraintBuilder,
)

load_dotenv(find_dotenv())

from app_settings import (
    YOTI_SCENARIO_ID,
    YOTI_CLIENT_SDK_ID,
    YOTI_KEY_FILE_PATH,
)  # noqa


class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            {"scenario_id": YOTI_SCENARIO_ID, "client_sdk_id": YOTI_CLIENT_SDK_ID}
        )


class DynamicShareView(TemplateView):
    template_name = "dynamic-share.html"

    def get(self, request, *args, **kwargs):
        client = Client(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
        policy = (
            DynamicPolicyBuilder()
            .with_full_name()
            .with_age_over(18)
            .with_email()
            .build()
        )
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


class SourceConstraintsView(TemplateView):
    template_name = "dynamic-share.html"

    def get(self, request, *args, **kwargs):
        client = Client(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
        constraint = (
            SourceConstraintBuilder().with_driving_licence().with_passport().build()
        )
        policy = (
            DynamicPolicyBuilder()
            .with_full_name(constraints=constraint)
            .with_structured_postal_address(constraints=constraint)
            .build()
        )
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
        context["base64_selfie_uri"] = profile.selfie.value.base64_content()
        context["user_id"] = activity_details.remember_me_id
        context["parent_remember_me_id"] = getattr(
            activity_details, "parent_remember_me_id"
        )
        context["receipt_id"] = getattr(activity_details, "receipt_id")
        context["timestamp"] = getattr(activity_details, "timestamp")

        # change this number according to the age condition defined in Yoti Hub
        age_verified = profile.find_age_over_verification(18)

        # Age verification objects don't have the same properties as an attribute,
        # so for this example we had to mock an object with the same properties
        if age_verified is not None:
            context["age_verified"] = {
                "name": "age_verified",
                "value": age_verified,
                "sources": age_verified.attribute.sources,
                "verifiers": age_verified.attribute.verifiers,
            }

        return self.render_to_response(context)

    @staticmethod
    def save_image(selfie_data):
        fd = open("yoti_example/static/YotiSelfie.jpg", "wb")
        fd.write(selfie_data)
        fd.close()
