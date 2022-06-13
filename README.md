# nonebot-plugin-ddcheck

NoneBot2 成分姬插件

查询B站关注列表的VTuber成分，并以图片形式发出

VTB列表数据来源：[vtbs.moe](https://vtbs.moe/)


### 分支说明

此分支 使用了 ```playwright``` 

我本人测试py3.9、3.8都可以使用

但是另外一个小伙伴死活用不了 就独立出一个分支了

该分支的图片大小会更友善（更少的白边）

那个分支需要计算宽高
另外一个解决办法[html2image](https://github.com/po-lan/zhenxun-nonebot-plugin-ddcheck/tree/html2image)


### 使用方式

**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**

```
查成分 + B站用户名/UID
```


### 安装

```
拖入到 zhenxun 的 插件目录就行
```

也许 你需要
```
pip install jinja2
```

若要显示主播牌子，需要在 `.env.xxx` 文件中添加任意的B站用户cookie：

```
bilibili_cookie=xxx
```


### 示例

<div align="left">
  <img src="https://s2.loli.net/2022/03/20/Nk3jZJgxforHDsu.png" width="400" />
</div>
