# coding=utf-8
from wechat_sdk import WechatBasic
import time

wechat_appid = "wxf7b5bd13112fe9fc"
wechat_appsecret = "2d150d1243c72816c3d67645c39154b4"
wechat_token = "o1q3XK7oem2dCAp8H2EiTiFB9DsoSJxefDmj6xjcMxIJ_lqkhRtt3c9Y_wZEfp1C4aDD6Yy3LF4gIZTPdpJOV1u5FocWUCGzepLn2N3H4RUMEMgAEAZRZ-EVPwCyNWgSOQZ17Na970QP4dC4unJGwYQIlz9TfpwFXSaABASKF"

wechat = WechatBasic(token=wechat_token, appid=wechat_appid, appsecret=wechat_appsecret)


# 最简单的单例实现，需要改进。
def get_wechat_client():
    return wechat
