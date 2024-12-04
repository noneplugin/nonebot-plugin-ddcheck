import json
import math
from http.cookies import SimpleCookie
from pathlib import Path
from typing import Any, Optional

import httpx
import jinja2
from nonebot.log import logger
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_htmlrender import html_to_pic
from nonebot_plugin_localstore import get_cache_dir

from .config import ddcheck_config

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 "
        "Safari/537.36 Edg/114.0.1823.67"
    ),
    "Referer": "https://www.bilibili.com/",
}


data_path = get_cache_dir("nonebot_plugin_ddcheck")
vtb_list_path = data_path / "vtb_list.json"

dir_path = Path(__file__).parent
template_path = dir_path / "template"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path), enable_async=True
)

raw_cookie = ddcheck_config.bilibili_cookie
cookie = SimpleCookie()
cookie.load(raw_cookie)
cookies = {key: value.value for key, value in cookie.items()}

homepage_cookies: dict[str, str] = {}


async def update_vtb_list():
    vtb_list = []
    urls = [
        "https://api.vtbs.moe/v1/short",
        "https://cfapi.vtbs.moe/v1/short",
        "https://hkapi.vtbs.moe/v1/short",
        "https://kr.vtbs.moe/v1/short",
    ]
    async with httpx.AsyncClient() as client:
        for url in urls:
            try:
                resp = await client.get(url, timeout=20)
                result = resp.json()
                if not result:
                    continue
                for info in result:
                    if info.get("uid", None) and info.get("uname", None):
                        vtb_list.append(
                            {"mid": int(info["uid"]), "uname": info["uname"]}
                        )
                    if info.get("mid", None) and info.get("uname", None):
                        vtb_list.append(info)
                break
            except httpx.TimeoutException:
                logger.warning(f"Get {url} timeout")
            except Exception:
                logger.exception(f"Error when getting {url}, ignore")
    dump_vtb_list(vtb_list)


scheduler.add_job(
    update_vtb_list,
    "cron",
    hour=3,
    id="update_vtb_list",
)


def load_vtb_list() -> list[dict]:
    if vtb_list_path.exists():
        with vtb_list_path.open("r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.decoder.JSONDecodeError:
                logger.warning("vtb列表解析错误，将重新获取")
                vtb_list_path.unlink()
    return []


def dump_vtb_list(vtb_list: list[dict]):
    data_path.mkdir(parents=True, exist_ok=True)
    json.dump(
        vtb_list,
        vtb_list_path.open("w", encoding="utf-8"),
        indent=4,
        separators=(",", ": "),
        ensure_ascii=False,
    )


async def get_vtb_list() -> list[dict]:
    vtb_list = load_vtb_list()
    if not vtb_list:
        await update_vtb_list()
    return load_vtb_list()


async def get_homepage_cookies(client: httpx.AsyncClient) -> dict[str, str]:
    if not homepage_cookies:
        headers = {"User-Agent": HEADERS["User-Agent"]}
        resp = await client.get(
            "https://data.bilibili.com/v/", headers=headers, follow_redirects=True
        )
        homepage_cookies.update(resp.cookies)
    return homepage_cookies


async def get_uid_by_name(name: str) -> Optional[int]:
    url = "https://api.bilibili.com/x/web-interface/wbi/search/type"
    params = {"search_type": "bili_user", "keyword": name}
    async with httpx.AsyncClient(timeout=10) as client:
        cookies.update(await get_homepage_cookies(client))
        resp = await client.get(url, params=params, headers=HEADERS, cookies=cookies)
        cookies.update(resp.cookies)
        result = resp.json()
        for user in result["data"]["result"]:
            if user["uname"] == name:
                return user["mid"]


async def get_medal_list(uid: int) -> list[dict]:
    url = "https://api.live.bilibili.com/xlive/web-ucenter/user/MedalWall"
    params = {"target_id": uid}
    async with httpx.AsyncClient(timeout=10) as client:
        cookies.update(await get_homepage_cookies(client))
        resp = await client.get(url, params=params, headers=HEADERS, cookies=cookies)
        cookies.update(resp.cookies)
        result = resp.json()
        return result["data"]["list"]


async def get_user_info(uid: int) -> dict:
    url = "https://account.bilibili.com/api/member/getCardByMid"
    params = {"mid": uid}
    async with httpx.AsyncClient(timeout=10) as client:
        cookies.update(await get_homepage_cookies(client))
        resp = await client.get(url, params=params, headers=HEADERS, cookies=cookies)
        cookies.update(resp.cookies)
        result = resp.json()
        return result["card"]


def format_color(color: int) -> str:
    return f"#{color:06X}"


def format_vtb_info(info: dict, medal_dict: dict) -> dict:
    name = info["uname"]
    uid = info["mid"]
    medal = {}
    if name in medal_dict:
        medal_info = medal_dict[name]["medal_info"]
        medal = {
            "name": medal_info["medal_name"],
            "level": medal_info["level"],
            "color_border": format_color(medal_info["medal_color_border"]),
            "color_start": format_color(medal_info["medal_color_start"]),
            "color_end": format_color(medal_info["medal_color_end"]),
        }
    return {"name": name, "uid": uid, "medal": medal}


async def render_ddcheck_image(
    user_info: dict[str, Any], vtb_list: list[dict], medal_list: list[dict]
) -> bytes:
    attentions = user_info.get("attentions", [])
    follows_num = int(user_info["attention"])

    vtb_dict = {info["mid"]: info for info in vtb_list}
    medal_dict = {medal["target_name"]: medal for medal in medal_list}
    vtbs = [info for uid, info in vtb_dict.items() if uid in attentions]
    vtbs = [format_vtb_info(info, medal_dict) for info in vtbs]

    vtbs_num = len(vtbs)
    percent = vtbs_num / follows_num * 100 if follows_num else 0
    num_per_col = math.ceil(vtbs_num / math.ceil(vtbs_num / 100)) if vtbs_num else 1
    result = {
        "name": user_info["name"],
        "uid": user_info["mid"],
        "face": user_info["face"],
        "fans": user_info["fans"],
        "follows": follows_num,
        "percent": f"{percent:.2f}% ({vtbs_num}/{follows_num})",
        "vtbs": vtbs,
        "num_per_col": num_per_col,
    }
    template = env.get_template("info.html")
    content = await template.render_async(info=result)
    return await html_to_pic(content, wait=0, viewport={"width": 100, "height": 100})
