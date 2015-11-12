from wechat_sdk import WechatBasic
import time

wechat_appid = "wxf7b5bd13112fe9fc"
wechat_appsecret = "2d150d1243c72816c3d67645c39154b4"
wechat_token = "o1q3XK7oem2dCAp8H2EiTiFB9DsoSJxefDmj6xjcMxIJ_lqkhRtt3c9Y_wZEfp1C4aDD6Yy3LF4gIZTPdpJOV1u5FocWUCGzepLn2N3H4RUMEMgAEAZRZ-EVPwCyNWgSOQZ17Na970QP4dC4unJGwYQIlz9TfpwFXSaABASKF"
wechat_access_token = None


def access_token_refresh_decorator(wechat_function):
    def wrapper(*args, **kwargs):
        global wechat_access_token
        if not wechat_access_token or wechat_access_token["access_token_expires_at"] - 60 < int(time.time()):
            wechat = WechatBasic(token=wechat_token, appid=wechat_appid, appsecret=wechat_appsecret)
            wechat.grant_token(True)
            wechat_access_token = wechat.get_access_token()
        return wechat_function(*args, **kwargs)

    return wrapper


@access_token_refresh_decorator
def get_wechat_client():
    wechat = WechatBasic(token=wechat_token, appid=wechat_appid, appsecret=wechat_appsecret,
                         access_token=wechat_access_token["access_token"])
    return wechat
