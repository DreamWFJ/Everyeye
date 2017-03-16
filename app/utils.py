# -*- coding: utf-8 -*-
# ===================================
# ScriptName : utils.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-16 11:05
# ===================================
import sys
import hmac
import base64
import hashlib
from werkzeug.local import LocalProxy

_security = ""
_datastore = ""
_pwd_context = LocalProxy(lambda: _security.pwd_context)

PY3 = sys.version_info[0] == 3

if PY3:  # pragma: no cover
    string_types = str,  # pragma: no flakes
    text_type = str  # pragma: no flakes
else:  # pragma: no cover
    string_types = basestring,  # pragma: no flakes
    text_type = unicode  # pragma: no flakes


def encode_string(string):
    """Encodes a string to bytes, if it isn't already.

    :param string: The string to encode"""

    if isinstance(string, text_type):
        string = string.encode('utf-8')
    return string


def get_hmac(password):
    """Returns a Base64 encoded HMAC+SHA512 of the password signed with the salt specified
    by ``SECURITY_PASSWORD_SALT``.

    :param password: The password to sign
    """
    salt = _security.password_salt

    if salt is None:
        raise RuntimeError(
            'The configuration value `SECURITY_PASSWORD_SALT` must '
            'not be None when the value of `SECURITY_PASSWORD_HASH` is '
            'set to "%s"' % _security.password_hash)

    h = hmac.new(encode_string(salt), encode_string(password), hashlib.sha512)
    return base64.b64encode(h.digest())


def verify_password(password, password_hash):
    """Returns ``True`` if the password matches the supplied hash.

    :param password: A plaintext password to verify
    :param password_hash: The expected hash value of the password (usually from your database)
    """
    if _security.password_hash != 'plaintext':
        password = get_hmac(password)

    return _pwd_context.verify(password, password_hash)


def verify_and_update_password(password, user):
    """Returns ``True`` if the password is valid for the specified user. Additionally, the hashed
    password in the database is updated if the hashing algorithm happens to have changed.

    :param password: A plaintext password to verify
    :param user: The user to verify against
    """

    if _pwd_context.identify(user.password) != 'plaintext':
        password = get_hmac(password)
    verified, new_password = _pwd_context.verify_and_update(
        password, user.password)
    if verified and new_password:
        user.password = encrypt_password(password)
        _datastore.put(user)
    return verified


def encrypt_password(password):
    """Encrypts the specified plaintext password using the configured encryption options.

    :param password: The plaintext password to encrypt
    """
    if _security.password_hash == 'plaintext':
        return password
    signed = get_hmac(password).decode('ascii')
    return _pwd_context.encrypt(signed)


def valid_email(email):
    return True
    