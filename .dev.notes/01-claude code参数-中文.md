# Claude Code 命令行参数说明

```bash
(base) QH7T3GDXQN:network101 bytedance$ claude code --help
用法: claude [选项] [命令] [提示词]

Claude Code - 默认启动交互式会话，使用 -p/--print 进行非交互式输出

参数:
  prompt                                            你的提示词

选项:
  -d, --debug [过滤器]                              启用调试模式，可选择类别过滤 (例如 "api,hooks" 或 "!statsig,!file")
  --verbose                                         覆盖配置中的详细模式设置
  -p, --print                                       打印响应并退出 (适用于管道)。注意：使用 -p 模式运行 Claude 时会跳过工作区信任对话框。仅在你信任的目录中使用此标志。
  --output-format <格式>                            输出格式 (仅适用于 --print): "text" (默认), "json" (单个结果), 或 "stream-json" (实时流式传输) (选择: "text", "json", "stream-json")
  --include-partial-messages                        包含到达时的部分消息块 (仅适用于 --print 和 --output-format=stream-json)
  --input-format <格式>                             输入格式 (仅适用于 --print): "text" (默认), 或 "stream-json" (实时流式输入) (选择: "text", "stream-json")
  --mcp-debug                                       [已弃用。请使用 --debug] 启用 MCP 调试模式 (显示 MCP 服务器错误)
  --dangerously-skip-permissions                    绕过所有权限检查。仅建议在无互联网访问的沙盒环境中使用。
  --replay-user-messages                            将用户消息从 stdin 重新发送到 stdout 进行确认 (仅适用于 --input-format=stream-json 和 --output-format=stream-json)
  --allowedTools, --allowed-tools <工具...>         允许的工具名称列表，用逗号或空格分隔 (例如 "Bash(git:*) Edit")
  --disallowedTools, --disallowed-tools <工具...>   禁止的工具名称列表，用逗号或空格分隔 (例如 "Bash(git:*) Edit")
  --mcp-config <配置...>                            从 JSON 文件或字符串加载 MCP 服务器 (空格分隔)
  --append-system-prompt <提示词>                   在默认系统提示词后追加系统提示词
  --permission-mode <模式>                          会话使用的权限模式 (选择: "acceptEdits", "bypassPermissions", "default", "plan")
  -c, --continue                                    继续最近的对话
  -r, --resume [会话ID]                             恢复对话 - 提供会话 ID 或交互式选择要恢复的对话
  --model <模型>                                    当前会话的模型。提供最新模型的别名 (例如 'sonnet' 或 'opus') 或模型的完整名称 (例如 'claude-sonnet-4-20250514')。
  --fallback-model <模型>                           当默认模型过载时启用自动回退到指定模型 (仅适用于 --print)
  --settings <文件或JSON>                           设置 JSON 文件的路径或要加载其他设置的 JSON 字符串
  --add-dir <目录...>                               允许工具访问的其他目录
  --ide                                             如果恰好有一个有效的 IDE 可用，则在启动时自动连接到 IDE
  --strict-mcp-config                               仅使用来自 --mcp-config 的 MCP 服务器，忽略所有其他 MCP 配置
  --session-id <uuid>                               为对话使用特定的会话 ID (必须是有效的 UUID)
  -v, --version                                     输出版本号
  -h, --help                                        显示命令帮助

命令:
  config                                            管理配置 (例如 claude config set -g theme dark)
  mcp                                               配置和管理 MCP 服务器
  migrate-installer                                 从全局 npm 安装迁移到本地安装
  setup-token                                       设置长期身份验证令牌 (需要 Claude 订阅)
  doctor                                            检查 Claude Code 自动更新器的健康状态
  update                                            检查更新并在可用时安装
  install [选项] [目标]                             安装 Claude Code 原生构建。使用 [目标] 指定版本 (stable, latest, 或特定版本)
```