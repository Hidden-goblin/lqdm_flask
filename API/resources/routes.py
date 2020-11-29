from .childhood import ChildhoodAPI, ChildhoodsApiFull, ChildhoodsApiList
from .skills import SkillApi, SkillsApi
from .auth import SignupApi, LoginApi


def initialize_routes(api):
    api.add_resource(SkillsApi, "/api/skills")
    api.add_resource(SkillApi, "/api/skill/<string:name>")

    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')

    api.add_resource(ChildhoodAPI, '/api/childhood/<string:name>')
    api.add_resource(ChildhoodsApiFull, '/api/childhoods/full')
    api.add_resource(ChildhoodsApiList, '/api/childhoods')
