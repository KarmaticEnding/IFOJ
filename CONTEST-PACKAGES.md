# 比赛下载包

比赛页的粉色“下载包”按钮访问 `/contest/<编号>/download/zip`。下载文件名为 `contest-<编号>.zip`，外层 ZIP 使用 AES-256 加密，只包含一个未加密的 `down.zip`。解压外层时使用“编辑比赛 → 下发包解压密码”，未设置时拒绝生成。取出 `down.zip` 后无需再次输入密码。

已登录用户可提前下载公开比赛的加密包；未公开比赛仅管理员可下载。密码提示仍在开赛后向普通选手公布，管理员可提前查看。

## 内容来源

- 题目通过 `problem-database/problem-index.json` 关联原始 tuack 工程。
- 题目必须与所属比赛日 `conf.yaml` 的 `subdir` 顺序一致。
- PDF 使用该工程已生成的 `statements/noi/<比赛日名>.pdf`。修改题面后，须先用 tuack 重新生成 PDF；下载接口不会重新渲染题面。
- 下发附件只取每个题目自己的 `down/`，按题目 `name` 分目录存放。
- 单日比赛：`day1.pdf`、`vector/`、`sub/`、`letter/`、`mex/`。多日比赛外加比赛日目录。
- 不复制正式 `data/`、标程目录、题解目录或整个工程。

密码通过子进程标准输入传递，不写入命令行。加密库 pyzipper 安装在运行用户的 `~/.local/share/ifoj-contest-packages/python`。迁移时可使用：

```sh
python3 -m pip install --target ~/.local/share/ifoj-contest-packages/python pyzipper
```

加密成品缓存在配置 `upload_dir` 下的 `contest-packages/`，不对外提供静态访问。缓存键包含打包格式版本、密码、文件名和文件内容；密码、PDF 或 `down/` 文件变化后自动重打包。旧缓存可在停机维护时清理。解压外层 ZIP 需要支持 AES 加密 ZIP 的解压工具。
