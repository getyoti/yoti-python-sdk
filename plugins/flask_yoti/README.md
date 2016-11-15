# Flask Yoti #

## Plugin configuration ##
### General settings ###

* `flask_yoti` is a [Flask Blueprint](http://flask.pocoo.org/docs/0.11/blueprints/) 
and all you have to do to add it to your Flask app is register it like this:
```python
# your_flask_project/app.py
from flask import Flask
from flask_yoti import flask_yoti_blueprint

app = Flask(__name__)
app.register_blueprint(flask_yoti_blueprint, url_prefix='/yoti')
```
*Don't forget to set an `app.secret_key` to be able to use `sessions`*

* And then use the following settings to configure the plugin:


```python
# your_flask_project/app.py
 
...
 
app.config.update({
    'YOTI_APPLICATION_ID': '...',
    'YOTI_CLIENT_SDK_ID': '...',
    'YOTI_KEY_FILE_PATH': '...',
    'YOTI_VERIFICATION_KEY': '...',
    ...
})
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

`flask_yoti` plugin provides some default endpoints:
- `yoti_auth` (`/yoti/auth`) - is a callback used for receiving an 
authentication token (shouldn't be changed)
- `yoti_login` (`/yoti/login`) - a view with just a login button. Can (and should) 
be overridden by `'YOTI_LOGIN_VIEW'` setting
- `yoti_profile` (`/yoti/profile`) - a view with user profile details. It's 
also given just for example and should be overridden by your view, using 
`'YOTI_REDIRECT_TO'` setting

```python
# your_flask_project/app.py
 
...
 
app.config.update({
    ...
    'YOTI_LOGIN_VIEW': '...',
    'YOTI_REDIRECT_TO': '...',
    'YOTI_LOGIN_BUTTON_LABEL': '...',
})
```
* **`YOTI_LOGIN_VIEW`**<br>
If *not* authenticated user is trying to access a view with 
`@yoti_authenticated` decorator, he/she will be redirected to this view.
Example: `login`<br>
In this case you should have something like this in your Flask app:
```python
@app.route('/login')
def login():
    render_template('login.html')
```
Default value: `flask_yoti.login` (with `/yoti/login/` URL)

* **`YOTI_REDIRECT_TO`**<br>
View name to which user is redirected after successful authentication.<br>
Example: `profile`<br>
In this case you should have something like this in your Flask app::
```python
@app.route('/profile')
@yoti_authenticated
def login():
    user_profile = session.get('yoti_user_profile')
    render_template('profile.html', **user_profile)
```
Default value: `flask_yoti.profile`  (with `/yoti/profile/` URL)

<br>


### Yoti application configuration ###

Your Yoti application's callback URL should point to `your_site.com/yoti/auth`.<br>
If you want to add a verification tag into any template using Jinja2 or DTL as a 
template language (other than `/yoti/auth/`, because it's already has one),
you can use a `{{ yoti_site_verification }}` tag inside `<head>` of that template.

## Plugin usage ##

1. First you need to add a login button to some of your view's templates.
- You can do it by using one of the predefined login buttons:
```
{{ yoti_login_button_sm }}
{{ yoti_login_button_md }}
{{ yoti_login_button_lg }}
```
- or with `{{ yoti_login_button(size='small', text='Log In with Yoti')`<br>
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
from flask_yoti import yoti_authenticated
 
@yoti_authenticated
def profile_view(request):
    user_id = request.yoti_user_id
    user_profile = request.yoti_user_profile
    return render(request, 'profile.html', user_profile)
```

4. All *not authenticated* users trying to access endpoint with this decorator, 
will be redirected to an endpoint, provided by the `YOTI_LOGIN_VIEW` setting.

## Tests ##

To run unit tests just type `py.test` inside `flask_yoti` dir.
