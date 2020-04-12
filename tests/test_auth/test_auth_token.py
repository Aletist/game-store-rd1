import datetime as dt
import pytest

from unittest import mock

from game_store.auth.token import encode_auth_token, decode_auth_token, InvalidToken, ExpiredToken


def test_decode_encode_token(config):
    user_data = 'some_name@adomain.com'
    encoded = encode_auth_token(user_data, config)
    decoded = decode_auth_token(encoded, config)

    assert decoded == user_data


def test_invalid_token(config):
    with pytest.raises(InvalidToken):
        user_data = 'some_name@adomain.com'
        encoded = encode_auth_token(user_data, config)
        decode_auth_token(encoded, {'JWT_SECRET_KEY': 'blah/blah!blah#x0256'})


def test_expired_token(config):
    with pytest.raises(ExpiredToken):
        user_data = 'some_name@adomain.com'
        encoded = encode_auth_token(user_data, config)

        with mock.patch("jwt.api_jwt.datetime") as jwt_datetime:
            jwt_datetime.utcnow = mock.Mock(
                return_value=dt.datetime.utcnow() + dt.timedelta(seconds=500)
            )
            decode_auth_token(encoded, config)
