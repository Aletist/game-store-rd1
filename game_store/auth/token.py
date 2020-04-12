import datetime as dt
import jwt


class AuthError(Exception):
    pass


class InvalidToken(AuthError):
    pass


class ExpiredToken(AuthError):
    pass


def encode_auth_token(user_data, config):
    """
    Generates the Auth Token
    :return: string
    """
    ttl_days = config.get('JWT_TTL_DAYS', 0)
    ttl_seconds = config.get('JWT_TTL_SECONDS', 0)
    secret_key = config['JWT_SECRET_KEY']

    now = dt.datetime.utcnow()
    try:
        payload = {
            'exp': now + dt.timedelta(days=ttl_days, seconds=ttl_seconds),
            'iat': now,
            'sub': user_data
        }
        return jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )
    except Exception:
        raise


def decode_auth_token(auth_token, config):
    """
    Decodes the auth token
    :param auth_token:
    :return: string
    """
    secret_key = config['JWT_SECRET_KEY']
    try:
        payload = jwt.decode(auth_token, secret_key, algorithms='HS256')
        return payload['sub']
    except jwt.ExpiredSignatureError as error:
        raise ExpiredToken from error
    except (jwt.InvalidTokenError, jwt.DecodeError) as error:
        raise InvalidToken from error
