import traceback
from typing import Union

from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot import on_command, require
from nonebot.plugin import PluginMetadata

from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.adapters.onebot.v11 import Message as V11Msg
from nonebot.adapters.onebot.v11 import MessageSegment as V11MsgSeg

from nonebot.adapters.onebot.v12 import Bot as V12Bot
from nonebot.adapters.onebot.v12 import Message as V12Msg
from nonebot.adapters.onebot.v12 import MessageSegment as V12MsgSeg

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_htmlrender")
require("nonebot_plugin_localstore")

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
        "version": "0.2.0",
    },
)


ddcheck = on_command("查成分", block=True, priority=12)


@ddcheck.handle()
async def _(
    bot: Union[V11Bot, V12Bot],
    matcher: Matcher,
    msg: Union[V11Msg, V12Msg] = CommandArg(),
):
    text = msg.extract_plain_text().strip()
    if not text:
        matcher.block = False
        await matcher.finish()

    try:
        result = await get_reply(text)
    except:
        logger.warning(traceback.format_exc())
        await matcher.finish("出错了，请稍后再试")

    if isinstance(result, str):
        await matcher.finish(result)

    if isinstance(bot, V11Bot):
        await matcher.finish(V11MsgSeg.image(result))
    elif isinstance(bot, V12Bot):
        resp = await bot.upload_file(type="data", name="ddcheck", data=result)
        file_id = resp["file_id"]
        await matcher.finish(V12MsgSeg.image(file_id))
