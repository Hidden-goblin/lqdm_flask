from behave import When


@When('I subscribe')
def subscribe(context):
    try:
        context.response = context.model.sign_up(**context.pre_requisite)
    except Exception as exception:
        context.model.push_event(f"Retrieve error : {exception}")
        raise AssertionError(exception)


@When(u'I list users')
def list_user(context):
    try:
        context.response = context.model.users(**context.pre_requisite)
    except Exception as exception:
        context.model.push_event(f"Retrieve error : {exception}")
        raise AssertionError(exception)


@When(u'I delete "{user_name}" user')
def delete_user(context, user_name):
    try:
        user = context.data["users"][user_name]
        context.response = context.model.delete_user(email=user["email"])
    except Exception as exception:
        context.model.push_event(f"Retrieve error : {exception}")
        raise AssertionError(exception)