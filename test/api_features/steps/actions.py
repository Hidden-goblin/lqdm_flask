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