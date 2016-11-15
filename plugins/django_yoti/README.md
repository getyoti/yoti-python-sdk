# Django Yoti #

Description

## Plugin configuration ##
### General settings ###

* First you need to add `django_yoti` plugin to your INSTALLED_APPS setting like this:
```python
# your_django_project/settings.py
 
...
 
INSTALLED_APPS = [
    ...
    'django_yoti',
]
```

* In order to use context tags inside your template (`{{ yoti_site_verification }}`, `{{ yoti_login_button_*}}`), 
you should include `django_yoti`'s context processors into your templates configuration like this:
```python
# your_django_project/settings.py
 
...
 
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'django_yoti.context_processors.yoti_context',
            ],
        },
    },
]
```

* And then use the following settings to configure the plugin:


```python
# your_django_project/settings.py
 
...
 
YOTI = {
    'YOTI_APPLICATION_ID': '...',
    'YOTI_CLIENT_SDK_ID': '...',
    'YOTI_KEY_FILE_PATH': '...',
    'YOTI_VERIFICATION_KEY': '...',
    ...
}
```
* **`YOTI_APPLICATION_ID`** - **required**, *can be also set by env variable with the same name*<br>
Your Yoti application's ID, found under the `INTEGRATIONS` tab of your 
Yoti application's settings page ([Yoti Dashboard](https://www.yoti.com/dashboard/)).<br>
It is used to configure the [Yoti Login Button](https://www.yoti.com/developers/#login-button-setup).<br>
Example: `ca84f68b-1b48-458b-96bf-963868edc8b6`

* **`YOTI_CLIENT_SDK_ID`** - **required**, *can be also set by env variable with the same name*<br>
Your Yoti application's SDK ID, found under the `INTEGRATIONS` tab of your 
Yoti application's settings page ([Yoti Dashboard](https://www.yoti.com/dashboard/)).<br>
Example: `39aef70a-89d6-4644-a687-b3e891613da6`

* **`YOTI_KEY_FILE_PATH`** - **required**, *can be also set by env variable with the same name*<br>
The full path to your private key downloaded from your Yoti application's 
settings page under the `KEYS` tab ([Yoti Dashboard](https://www.yoti.com/dashboard/)).<br>
Example: `/home/user/.ssh/access-security.pem`

* **`YOTI_VERIFICATION_KEY`** - *can be also set by env variable with the same name*<br>
A key, used to verify your callback URL. Can be found under the 
`INTEGRATIONS` tab of your Yoti application's settings page (Callback URL -> VERIFY).<br>
Example: `b14886f972d0c717`


### Endpoints configuration ###

`django_yoti` plugin provides some default endpoints:
```python
# django_yoti/urls.py
 
urlpatterns = [
    url(r'^auth/', views.auth, name='yoti_auth'),
    url(r'^login/', views.login, name='yoti_login'),
    url(r'^profile/', views.profile, name='yoti_profile')
]
```
`yoti_auth` url is used for receiving token via callback and should'nt be changed.<br>
The last two URLs are examples and can be overridden by the following settings:

```python
# your_django_project/settings.py
 
...
 
YOTI = {
    ...
    'YOTI_LOGIN_VIEW': '...',
    'YOTI_REDIRECT_TO': '...',
    'YOTI_LOGIN_BUTTON_LABEL': '...',
}
```
* **`YOTI_LOGIN_VIEW`**<br>
If *not* authenticated user is trying to access a view with 
`@yoti_authenticated` decorator, he/she will be redirected to this view.
Example: `login`<br>
In this case you should have something like this in your project's `urls.py` file:
```python
urlpatterns = [
    ...
    url(r'^login/', views.login, name='login'),
    ...
]
```
Default value: `yoti_login` (with `/yoti/login/` URL)

* **`YOTI_REDIRECT_TO`**<br>
View name to which user is redirected after successful authentication.<br>
Example: `profile`<br>
In this case you should have something like this in your project's `urls.py` file:
```python
urlpatterns = [
    ...
    url(r'^profile/', views.profile, name='profile'),
    ...
]
```
Default value: `yoti_profile`  (with `/yoti/profile/` URL

<br>

In order to use `django_yoti` plugin in your project, you should include 
the plugin's endpoints in your project's `urls.py` file:
```python
# your_django_project/urls.py
 
 ...
 
urlpatterns = [
    ...
    url(r'^yoti/', include('django_yoti.urls')),
    ...
]
```

### Yoti application configuration ###

Your Yoti application's callback URL should point to `your_site.com/yoti/auth`.<br>
If you want to add a verification tag into any page (other than `/yoti/auth/`), 
you can use a `{{ yoti_site_verification }}` tag inside 'head' tag of that page.

## Using plugin ##

1. First you need to add a login button to some of your view's templates.
- You can do it by using one of the predefined login buttons:
```
{{ yoti_login_button_sm }}
{{ yoti_login_button_md }}
{{ yoti_login_button_lg }}
```
- or with a default one `{{ yoti_login_button }}`, in case you're using DTL 
as a template language)
- or with `{{ yoti_login_button(size='small', text='Log In with Yoti')`, in 
case you're using Jinja2 as your template language<br>
Available button sizes: `small`, `medium`, `large`

By clicking this button, user will be redirected to the Yoti Authentication page.

*Remember to add an appropriate script to your page with login 
button in order for it to work. See: [Yoti Developers Documentation](https://www.yoti.com/developers/#login-button-setup)*

2. After successful authentication, user will be redirected to a view,
provided by the `YOTI_REDIRECT_TO` setting.
3. In order to have an access to an authenticated user's information inside a view,
you should use a `@yoti_authenticated` decorator.
Example:
```python
from django_yoti import yoti_authenticated
 
@yoti_authenticated
def profile_view(request):
    user_id = request.yoti_user_id
    user_profile = request.yoti_user_profile
    return render(request, 'profile.html', user_profile)
```

4. All *not authenticated* users trying to access endpoint with this decorator, 
will be redirected to an endpoint, provided by the `YOTI_LOGIN_VIEW` setting.

## Tests ##

To run unit tests just type: `python django_yoti/runtests.py`
