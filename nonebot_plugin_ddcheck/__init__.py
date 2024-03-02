import traceback

from nonebot import on_command, require
from nonebot.adapters import Message
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_alconna")
require("nonebot_plugin_apscheduler")
require("nonebot_plugin_htmlrender")
require("nonebot_plugin_localstore")

from nonebot_plugin_alconna import UniMessage

from .config import Config
from .data_source import get_reply

__plugin_meta__ = PluginMetadata(
    name="成分姬",
    description="查询B站用户关注的VTuber成分",
    usage="查成分 B站用户名/UID",
    type="application",
    homepage="https://github.com/noneplugin/nonebot-plugin-ddcheck",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={
        "example": "查成分 小南莓Official",
    },
)


ddcheck = on_command("查成分", block=True, priority=12)


@ddcheck.handle()
async def _(
    matcher: Matcher,
    msg: Message = CommandArg(),
):
    text = msg.extract_plain_text().strip()
    if not text:
        matcher.block = False
        await matcher.finish()

    try:
        result = await get_reply(text)
    except Exception:
        logger.warning(traceback.format_exc())
        await matcher.finish("出错了，请稍后再试")

    if isinstance(result, str):
        await matcher.finish(result)

    await UniMessage.image(raw=result).send()
