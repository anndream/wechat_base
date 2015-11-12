# -*- coding:utf-8 -*-
import openerp.http
from openerp.http import request
from .. import tool
from wechat_sdk import WechatBasic
from wechat_sdk.messages import (
    TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
)


class Weixin(openerp.http.Controller):
    @openerp.http.route("/weixin", type='http', auth="public", methods=["GET", "POST"])
    def index(self, **kwargs):
        ret = kwargs.get("echostr", "")
        print "ret = %s" % ret
        if ret:
            return ret

        signature = kwargs["signature"]
        timestamp = kwargs["timestamp"]
        nonce = kwargs["nonce"]

        body_text = request.httprequest.data

        wechat = tool.token_tool.get_wechat_client()

        if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            wechat.parse_data(body_text)
            message = wechat.get_message()
            response = None
            if isinstance(message, TextMessage):
                response = wechat.response_text(content=u'文字信息')
            elif isinstance(message, VoiceMessage):
                response = wechat.response_text(content=u'语音信息')
            elif isinstance(message, ImageMessage):
                response = wechat.response_text(content=u'图片信息')
            elif isinstance(message, VideoMessage):
                response = wechat.response_text(content=u'视频信息')
            elif isinstance(message, LinkMessage):
                response = wechat.response_text(content=u'链接信息')
            elif isinstance(message, LocationMessage):
                response = wechat.response_text(content=u'地理位置信息')
            elif isinstance(message, EventMessage):  # 事件信息
                if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
                    if message.key and message.ticket:  # 如果 key 和 ticket 均不为空，则是扫描二维码造成的关注事件
                        print u'用户尚未关注时的二维码扫描关注事件'
                        partner_id, partner_name, openid = self._bind_user(message.source, message.key)
                        response = wechat.response_text(
                            content=u'用户尚未关注时的二维码扫描关注事件.绑定成功 partner name:%s openid:%s' % (partner_name, openid))
                    else:
                        response = wechat.response_text(content=u'普通关注事件')
                elif message.type == 'unsubscribe':
                    response = wechat.response_text(content=u'取消关注事件')
                elif message.type == 'scan':
                    if message.key and message.ticket:
                        partner_id, partner_name, openid = self._bind_user(message.source, message.key)
                        response = wechat.response_text(
                            content=u'用户尚未关注时的二维码扫描关注事件.绑定成功 partner name:%s openid:%s' % (partner_name, openid))
                    else:
                        response = wechat.response_text(content=u'用户已关注时的二维码扫描事件.')
                elif message.type == 'location':
                    response = wechat.response_text(content=u'上报地理位置事件')
                elif message.type == 'click':
                    response = wechat.response_text(content=u'自定义菜单点击事件')
                elif message.type == 'view':
                    response = wechat.response_text(content=u'自定义菜单跳转链接事件')
                elif message.type == 'templatesendjobfinish':
                    response = wechat.response_text(content=u'模板消息事件')
            return response  # kwargs.get("echostr","success")

    def _bind_user(self, source, key):
        openid = source
        partner_id = int(key)
        partner = request.env["res.partner"].sudo().search([("id", "=", partner_id)])
        partner.ensure_one()
        partner.wechat_openID = source
        return (partner_id, partner.name, openid)
