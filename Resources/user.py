from flask_restful import Resource, reqparse
from Models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                           type=str,
                           required=True,
                           help="This field cannot be left blank")
_user_parser.add_argument('password',
                           type=str,
                           required=True,
                           help="This field cannot be left blank")

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists."}, 400

        user = UserModel(**data) #data['username'], data['password']
        user.save_to_db()

        return {"message": "User created succesfully."},201

class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'},200

class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        #'authenticate()' function
        if user and safe_str_cmp(user.password, data['password']):
            #'identity()' function
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_access_token(user.id)
            return {'access_token': access_token,
                    'refresh_token': refresh_token}, 200
        return {'message': 'Invalid credentials'}, 401