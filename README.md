# nonebot-plugin-ddcheck

NoneBot2 成分姬插件

查询B站关注列表的VTuber成分，并以图片形式发出

VTB列表数据来源：[vtbs.moe](https://vtbs.moe/)


### 使用方式

**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**

```
查成分 + B站用户名/UID
```


### 安装

- 使用 nb-cli

```
nb plugin install nonebot_plugin_ddcheck
```

- 使用 pip

```
pip install nonebot_plugin_ddcheck
```


### 配置

需要在 `.env.xxx` 文件中添加任意的B站用户cookie：

```
bilibili_cookie=xxx
```

`cookie` 获取方式：

`F12` 打开开发工具，查看 `www.bilibili.com` 请求的响应头，找形如 `SESSDATA=xxx;` 的字段，如：

```
bilibili_cookie="SESSDATA=xxx;"
```

<div align="left">
  <img src="https://s2.loli.net/2022/07/19/AIBmd2Z9V5YwlkF.png" width="500" />
</div>


### 示例

<div align="left">
  <img src="https://s2.loli.net/2022/03/20/Nk3jZJgxforHDsu.png" width="400" />
</div>
