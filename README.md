# zhenxun-nonebot-plugin-ddcheck

NoneBot2 成分姬插件
目前已经修改为真寻版本
主要以适配win端为主

查询B站关注列表的VTuber成分，并以图片形式发出

VTB列表数据来源：[vtbs.moe](https://vtbs.moe/)


### 使用方式


```
查成分 + B站用户名/UID
```


### 安装

- 首先

在你的win中安装chrome


- 然后

在你的cmd中输入


```
pip install html2image
```


- 最后

将 zhenxun_plugin_ddcheck 拖入 真寻目录下的 plugin 文件夹或者自己创建的插件文件夹。

若要显示主播牌子，需要在 `config.py` 文件中添加任意的B站用户cookie：


### 示例

<div align="left">
  <img src="https://s2.loli.net/2022/03/20/Nk3jZJgxforHDsu.png" width="400" />
</div>


### 更新日志

**2022/5/30**

1. 修复了超过100位vtb关注时无法全部显示
