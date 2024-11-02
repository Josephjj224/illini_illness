from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash
import uuid
from werkzeug.security import generate_password_hash
from ..common.utils import res
from ..models.user import UserModel
from ..models.revoked_token import RevokedTokenModel
from flask_jwt_extended import get_jwt


class AuthService:
    def login(self, email, password):
        user_tuple = UserModel.find_by_email(email)
        user = user_tuple

        if user:
            try:
                pwd, salt = user.get('password'), user.get('salt')
                valid = check_password_hash(pwd, '{}{}'.format(salt, password))

                if valid:
                    # Generate tokens
                    response_data = self.generate_tokens(email)
                    return res(data=response_data, message="Register successfully!", code=200)
                else:
                    raise ValueError('Invalid password!')
            except Exception as e:
                return res(success=False, message='Error: {}'.format(e), code=500)
        else:
            return res(success=False, message='Unregistered email!', code=400)

    def generate_tokens(self, identity):
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        return {
            'accessToken': 'Bearer ' + access_token,
            'refreshToken': 'Bearer ' + refresh_token,
        }

    def register(self, data):
        # Check if the email is already taken
        if UserModel.find_by_email(data['email']):
            return res(success=False, message="Repeated email!", code=400)
        else:
            try:
                # Generate a unique salt for each user
                data['salt'] = uuid.uuid4().hex
                # Hash the password using the generated salt
                data['pwd'] = generate_password_hash('{}{}'.format(data['salt'], data['pwd']))
                data['password'] = data.pop('pwd')

                # Create a new user using the UserModel
                user = UserModel(**data)
                user.add_user()

                return res(message="Register succeed!")
            except Exception as e:
                return res(success=False, message="Error: {}".format(e), code=500)

    def logout(self):
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return res()
        except Exception as e:
            return res(success=False, message='Server is busy. Please try again later.', code=500)

    def get_all_users(self) -> object:
        user_list = UserModel.get_all_users()

        users = []
        for data in user_list:
            user = UserModel(data['email'], data['password'], data['salt'], data['created_at'], data['updated_at'],
                             data['userID'])
            users.append(user)

        result = [user.to_dict() for user in users]
        return res(data=result)

    def get_current_user(self, email) -> UserModel:
        user_dict = UserModel.find_by_email(email)
        user = UserModel(**user_dict)
        return user

