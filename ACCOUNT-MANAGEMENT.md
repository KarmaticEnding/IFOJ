# 账号管理

IFOJ 默认关闭公开注册（`allow_registration: false`）。注册页面、注册接口、邮件确认链接和旧版验证链接均返回 403，导航栏和登录页隐藏注册入口。

在 Linux 终端中运行：

```bash
cd ~/IFOJ
./bin/create-user 用户名
./bin/create-user 管理员用户名 --admin
```

可选：添加 `--email 地址`。按提示输入两次密码，输入不会显示，也不需要 sudo。

此命令使用 `config.json` 中的数据库连接直接插入账号，自动生成当前 SYZOJ 登录所要求的密码摘要及默认字段。默认创建普通账号，只有显式指定 `--admin` 才创建管理员。重复用户名会拒绝创建，不会覆盖现有账号。

不要把明文密码直接写进数据库的 `password` 字段。当前版本保存的是 `MD5(密码 + "syzoj2_xxx")`，与原有登录机制一致。
