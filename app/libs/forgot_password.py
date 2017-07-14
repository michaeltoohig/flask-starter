from uuid import uuid4
from app.models.user import User
from app.models.forgot_password_token import ForgotPasswordToken


class InvalidTokenException(Exception):
    pass


def decode(token):
    '''Decode a token created with __generate_token'''

    [id, token] = token.split('_')
    try:
        return ForgotPasswordToken.validate_and_delete_token(id, token)
    except ForgotPasswordToken.DoesNotExist:
        raise InvalidTokenException('Token could not be decoded')


def forgot_password(email, sender):
    '''Generate a forgot password token and pass it to sender function
    The sender function should take one argument (the token) and it's
    expected to send the token to the user with email 'email' via
    email/sms/or other.
    '''
    user = User.objects.get(email=email)
    token_string = uuid4().hex
    token = ForgotPasswordToken(
        user=user,
        token=token_string
    )
    token.save()
    sender('{}_{}'.format(token.id, token_string))