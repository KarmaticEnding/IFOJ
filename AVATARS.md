# 本地头像

用户进入“用户页面 → 修改资料”，将鼠标移到用户名、性别右侧的当前头像上，点击“修改头像”选择图片。选择后自动上传，头像独立保存，不需要再点击下方资料表单的“修改”。

- 支持 JPG、PNG、WebP，原文件最多 2 MiB，每边不超过 4096 像素，最多 1600 万像素。
- 根据 EXIF 方向旋转后，居中裁剪并缩放为 512×512 PNG；不保留原始文件、EXIF 或动画。
- 普通用户只能修改自己的头像；拥有现有用户资料管理权限的用户可管理对应头像。
- 头像查看沿用站点登录限制。
- 未上传时使用仓库内的 `assets/default-avatar.svg`。

文件保存在配置 `upload_dir` 下的 `avatars/<用户编号>.png`，当前目录为 `/home/administrator/IFOJ/uploads/avatars/`。更新头像通过原子替换覆盖旧文件；浏览器不缓存头像。备份与迁移时请包含整个头像目录。

代码入口：`modules/avatar.js`、`libs/avatars.js`、`bin/normalize-avatar.py`。无需修改数据库结构。

图片转换使用 Python 3 和 Pillow。当前实例的 Pillow 独立安装在运行用户的 `~/.local/share/ifoj-avatar/python`，不影响系统 Python 包。迁移时执行：

```sh
python3 -m pip install --target ~/.local/share/ifoj-avatar/python Pillow
```

上传先检查登录、用户编辑权限和会话令牌，再接收文件。文件内容经真实解码验证，统一重新编码后存储；图片处理有像素、内存、执行时间和排队数量限制。不要将头像存储目录直接挂载为可写的静态网站目录。
