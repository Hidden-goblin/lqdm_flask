from common_steps.environments import common_before_all, create_evidence, common_after_all
from models.LqdmAPI import LqdmAPI


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
    context.model.history_reset()


def after_all(context):
    common_after_all(context)
