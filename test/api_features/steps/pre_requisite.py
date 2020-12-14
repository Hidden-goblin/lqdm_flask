from dpath.util import get as dp_get
from behave import Given
from api_features.steps.actions import subscribe

@Given('I am "{user_name}"')
def set_user(context, user_name):
    try:
        if user_name == "JohnDoe":
            context.model.push_event(f"Set user {user_name} with nothing as JohnDoe is an anonymous user")
        else:
            context.pre_requisite["email"] = dp_get(context.data, f"users/{user_name}/email")
            context.pre_requisite["password"] = dp_get(context.data, f"users/{user_name}/password")
            context.post_conditions["user"] = user_name
            context.model.push_event(f"Set user {user_name} credential\n "
                                     f"Email : {context.pre_requisite['email']}\n"
                                     f"Password : {context.pre_requisite['password']}")
    except Exception as exception:
        context.model.push_event(f"Retrieve error : {exception}")
        raise AssertionError(exception)


@Given(u'I am authenticated')
def authentication(context):
    try:
        response = context.model.login(email=context.pre_requisite["email"],
                                       password=context.pre_requisite["password"])

        if response.status_code != 200:
            raise AssertionError(f"Login failed. Get {response.json()['message']} error message")
        context.pre_requisite.pop("email")
        context.pre_requisite.pop("password")
    except Exception as exception:
        context.model.push_event(f"Retrieve error : {exception}")
        raise AssertionError(exception)


@Given(u'I want to modify "{payload_key}" to "{value}"')
def update_payload():
    pass


@Given(u'I forgive "{field}" field')
def forgive_data(context, field):
    try:
        if field in context.pre_requisite:
            context.pre_requisite.pop(field)
            context.model.push_event(f"Remove {field} from payload")
        elif field == "none":
            context.model.push_event(f"Remove no field from payload")
        else:
            AssertionError(f"No field {field} to remove")
    except Exception as exception:
        context.model.push_event(f"Retrieve error : {exception}")
        raise AssertionError(exception)


@Given(u'"{user_name}" exists')
def check_user_existence(context, user_name):
    try:
        requested_user = context.data["users"][user_name]
        admin = context.data["users"]["BobAdmin"]

        context.model.login(email=admin["email"], password=admin["password"])
        response = context.model.users(email=requested_user["email"])
        context.model.logout(email=admin["email"])

        if response.status_code != 200:
            context.model.push_event(f"Create {user_name} account")
            context.model.sign_up(email=requested_user['email'],
                                  password=requested_user['password'])

    except Exception as exception:
        context.model.push_event(f"Retrieve error : {exception}")
        raise AssertionError(exception)


@Given(u'I have subscribed')
def have_subscribed(context):
    try:
        subscribe(context)
        if context.response.status_code != 200:
            context.model.push_event("User may already have subscribed")
    except Exception as exception:
        context.model.push_event(f"Retrieve error : {exception}")
        raise AssertionError(exception)


@Given(u'There is "{number}" account with role "{role}"')
def check_number_of_account_type(context, number, role):
    try:
        admin = context.data["users"]["BobAdmin"]

        context.model.login(email=admin["email"], password=admin["password"])
        response = context.model.users()
        context.model.logout(email=admin["email"])

        assert response.status_code == 200, "Get an error when retrieving user's account"
        admin_account = [item for item in response.json() if item["role"] == role]
        assert len(admin_account) == int(number), f"Retrieve {len(admin_account)} while expecting {number}"
    except Exception as exception:
        context.model.push_event(f"Retrieve error : {exception}")
        raise AssertionError(exception)