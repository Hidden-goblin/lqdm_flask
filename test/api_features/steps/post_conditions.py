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
