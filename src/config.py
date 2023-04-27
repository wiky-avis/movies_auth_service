import os
from datetime import timedelta

from dotenv import load_dotenv


load_dotenv()


TEST_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDIzi1aV7xG1BGjwf1ZsCxiMO5jdYEPVfdPDLbBQtMD4VZlNb4p
s2B6bExyLisOUxnlhEqdVn424EHIFRwNAV3eo0GcRrEGT4u57+Esqy9QQmvknJaA
+oBFlzCpMLV3clQIm6ropbVtgqQtnLH19WJMfal3nwB/v8Nle2XNQ7DJKwIDAQAB
AoGAHNj5zPvDsY0vx43L3sGfbq/G34T2+IQKFlImQxddhzYtGjchTY5Wct/yD4kw
aEtp8f4SVg4h7bJD4QGfWQL0QBGdk84Q5y29vau3XxHMmZn6URHqMs6RciQDzKdB
De/zb1rn3vOQuZIXO+ODhbK4cWPm/u4QyObzSAX2sYigyzkCQQDnaTqyNuE8LLxN
QVxJIaRARr4Y8UvxtS+sVhK4NqeIgw9x+TsDoMeePZuZZ6HW9azzSlGERnMuQnil
GgypQUUXAkEA3iRsB+jN25P5YY5PHTA/XbLCEM/ZhFc78dD4p5j24J2hB1ibBdoa
U9xHfXlV4S/nSYnlqS+0NLlfqBRZ+hxRDQJBAJyL/HA5Xg+mN9CPic3TW1k8Qjd/
bR/bsZ+FLu690oIwH0+8Cec/aisrhEq3560Sz+hZ+2Ffg2XlA9a1E6GgjQsCQQCa
cvxhq22lo4aaW5WKF8eW3/iqM7lqmDRndwHLlUDg/ve84dA3C2OOtvNFvB0HyoSm
zqfNMAu9NL3bYPsGOLXpAkABkLj2TbaFGbMVceGAeVbTR0OrU8DC4x+HcQMBYwsy
BT/C0/PFVtrscU8wbMsXizjYfz5MVyeglVB0ToZeQ8mZ
-----END RSA PRIVATE KEY-----
"""

TEST_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDIzi1aV7xG1BGjwf1ZsCxiMO5j
dYEPVfdPDLbBQtMD4VZlNb4ps2B6bExyLisOUxnlhEqdVn424EHIFRwNAV3eo0Gc
RrEGT4u57+Esqy9QQmvknJaA+oBFlzCpMLV3clQIm6ropbVtgqQtnLH19WJMfal3
nwB/v8Nle2XNQ7DJKwIDAQAB
-----END PUBLIC KEY-----
"""


class Config:
    NGINX_PORT = int(os.getenv("NGINX_PORT", default=80))

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DB_URL",
        default="postgresql://app:123qwe@db:5432/auth_database",
    )

    POSTGRES_USER = os.getenv("POSTGRES_USER", default="app")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", default="123qwe")
    POSTGRES_DB = os.getenv("POSTGRES_DB", default="auth_database")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", default=5432))
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", default="db")
    DB_URL = os.getenv(
        "DB_URL",
        default="postgresql://app:123qwe@db:5432/auth_database",
    )

    HTTP_PORT = int(os.getenv("HTTP_PORT", default=5000))
    HTTP_HOST = os.getenv("HTTP_HOST", default="api")

    REDIS_PORT = int(os.getenv("REDIS_PORT", default=6379))
    REDIS_HOST = os.getenv("REDIS_HOST", default="redis")

    FLASK_APP = "src.app.py"

    JWT_PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY", default=TEST_PRIVATE_KEY)
    JWT_PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY", default=TEST_PUBLIC_KEY)
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", default="RS256")
    JWT_EXPIRES_IN = int(os.getenv("JWT_EXPIRES_IN", default=600))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", default=15))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", default=30))
    )
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_CSRF_PROTECT = int(os.getenv("JWT_COOKIE_CSRF_PROTECT"))

    MAIL_SERVER = os.getenv("MAIL_SERVER", default="smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", default=465))
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", default="your-email@gmail.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", default="your-password")

    BCRYPT_LOG_ROUNDS = 13


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
