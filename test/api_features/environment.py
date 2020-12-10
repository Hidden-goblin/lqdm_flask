from common_steps.environments import common_before_all, create_evidence, common_after_all
from models.LqdmAPI import LqdmAPI
from logging import getLogger

log = getLogger(__name__)


def before_all(context):
    context.data_filename = "resources/lqdm.json"
    common_before_all(context, LqdmAPI, True)


def before_scenario(context, scenario):
    context.pre_requisite = dict()
    context.post_conditions = dict()
    context.response = None


def before_step(context, step):
    context.model.step = step


def after_scenario(context, scenario):
    context.response = None
    create_evidence(scenario, context.model.history)

    if "user" in context.post_conditions:
        user = context.data["users"][context.post_conditions["user"]]
        if 'is_temporary' in user and user['is_temporary']:
            response = context.model.login(user['email'], user['password'])
            if response.status_code == 200:
                response = context.model.delete_user(user['email'])
                if response.status_code != 204:
                    log.error(f"Cannot delete user {user['email']}")

    context.model.reset()


def after_all(context):
    common_after_all(context)
