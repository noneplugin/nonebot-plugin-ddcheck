import traceback
from loguru import logger
from nonebot.params import CommandArg
from nonebot import on_command, require
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.log import logger

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_htmlrender")

from .config import Config
from .data_source import get_reply

__plugin_meta__ = PluginMetadata(
    name="成分姬",
    description="查询B站用户关注的VTuber成分",
    usage="查成分 B站用户名/UID",
    config=Config,
    extra={
        "unique_name": "ddcheck",
        "example": "查成分 小南莓Official",
        "author": "meetwq <meetwq@gmail.com>",
        "version": "0.1.15",
    },
)


ddcheck = on_command("查成分", block=True, priority=12)


@ddcheck.handle()
async def _(msg: Message = CommandArg()):
    text = msg.extract_plain_text().strip()
    if not text:
        await ddcheck.finish()

    try:
        res = await get_reply(text)
    except:
        logger.warning(traceback.format_exc())
        await ddcheck.finish("出错了，请稍后再试")

    if isinstance(res, str):
        await ddcheck.finish(res)
    else:
        await ddcheck.finish(MessageSegment.image(res))
