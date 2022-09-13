from flask import request
from flask_restx import Namespace, Resource
from project.container import user_service
from project.setup.api.models import user


api = Namespace('user')


@api.route('/')
class SignupView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get User.
        """
        token = request.headers["Authorization"].split("Bearer ")[-1]
        return user_service.get_user_by_token(token)

    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def patch(self):
        token = request.headers["Authorization"].split("Bearer ")[-1]
        data = request.json
        return user_service.update_user(data=data, token=token)


@api.route('/password/')
class SigninView(Resource):

    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def put(self):
        """
        Update password.
        """
        data = request.json
        token = request.headers["Authorization"].split("Bearer ")[-1]

        return user_service.update_password(data=data, token=token)


