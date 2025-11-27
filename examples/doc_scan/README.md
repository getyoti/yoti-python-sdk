# Doc Scan Example

## Running the example

1. Rename the [.env.example](.env.example) file to `.env` and fill in the required configuration values
1. Install the dependencies with `pip install -r requirements.txt`
1. Start the server `flask run --cert=adhoc`
1. Visit `https://localhost:5000`

## Customizing the IDV Session with Brand ID

The SDK now supports applying custom brand themes to the ID Verification iframe using the `brand_id` property. This allows businesses to maintain their brand identity throughout the verification process.

### Usage

When creating a session, you can specify a `brand_id` in the SDK configuration:

```python
from yoti_python_sdk.doc_scan import SdkConfigBuilder

sdk_config = (
    SdkConfigBuilder()
    .with_allows_camera_and_upload()
    .with_primary_colour("#2d9fff")
    .with_brand_id("your-brand-id-here")  # Add your brand ID here
    .with_success_url("https://yoursite.com/success")
    .with_error_url("https://yoursite.com/error")
    .build()
)
```

The `brand_id` is optional. If not provided, the default Yoti branding will be used. Contact Yoti support to obtain a brand ID for your organization.
