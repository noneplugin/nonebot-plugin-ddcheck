from nonebot import get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    bilibili_cookie: str = ""


ddcheck_config = get_plugin_config(Config)
