from .childhood import ChildhoodAPI, ChildhoodsApiFull, ChildhoodsApiList
from .skills import SkillApi, SkillsApi
from .auth import SignupApi, LoginApi, UserApi, LogoutApi


def initialize_routes(api):
    api.add_resource(SkillsApi, "/v1/api/skills")
    api.add_resource(SkillApi, "/v1/api/skills/<string:name>")

    api.add_resource(SignupApi, '/v1/api/auth/signup')
    api.add_resource(LoginApi, '/v1/api/auth/login')
    api.add_resource(LogoutApi, '/v1/api/auth/logout')
    api.add_resource(UserApi, '/v1/api/users/<string:user_id>')

    api.add_resource(ChildhoodAPI, '/v1/api/childhood/<string:name>')
    api.add_resource(ChildhoodsApiFull, '/v1/api/childhoods/full')
    api.add_resource(ChildhoodsApiList, '/v1/api/childhoods')
