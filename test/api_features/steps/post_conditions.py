from behave import Then


@Then(u'I get "{status_code}" http status code')
def check_status_code(context, status_code):
    try:
        assert context.response.status_code == int(status_code), f"Expecting status_code {status_code}. Retrieve" \
                                                                 f" {context.response.status_code}"
        context.model.push_event("Status code is as expected")
    except Exception as exception:
        context.model.push_event(f"Retrieve error : {exception}")
        raise AssertionError(exception)


@Then(u'I retrieve at least "{number}" users')
def check_number_of_users(context, number):
    try:
        assert len(context.response.json()) >= int(number), f"Expecting at least {number} user(s). Retrieve" \
                                                            f" {len(context.response.json())} user(s)"
        context.model.push_event(f"Retrieved at least {number} user(s)")
    except Exception as exception:
        context.model.push_event(f"Retrieve error : {exception}")
        raise AssertionError(exception)


@Then(u'The error message is "{message}"')
def check_error_message(context, message):
    check_message(context, message, "error")


def check_message(context, message, message_type=""):
    try:
        assert context.response.json()["message"] == message, f"Expecting '{message}' {message_type} message. " \
                                                              f"Retrieve '{context.response.json()['message']}'" \
                                                              f" {message_type} message"
        context.model.push_event(f"Retrieved '{message}' {message_type} message")
    except Exception as exception:
        context.model.push_event(f"Retrieve error : {exception}")
        raise AssertionError(exception)


@Then(u'I receive "{message}" message')
def check_received_message(context, message):
    check_message(context, message)


@Then(u'The "{user_name}" account "{status}" exist')
def check_user_existence(context, user_name, status):
    try:
        requested_user = context.data["users"][user_name]
        admin = context.data["users"]["BobAdmin"]

        context.model.login(email=admin["email"], password=admin["password"])
        response = context.model.users(email=requested_user["email"])
        context.model.logout(email=admin["email"])

        if status == "does":
            assert response.status_code == 200, f"User {user_name} is not found while he should be"
        elif status == "does not":
            assert response.status_code == 404, f"User {user_name} is found while he should not be"
    except Exception as exception:
        context.model.push_event(f"Retrieve error : {exception}")
        raise AssertionError(exception)