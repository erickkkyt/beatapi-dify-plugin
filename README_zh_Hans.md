# BeatAPI for Dify

BeatAPI Dify 工具插件可以在 Workflow、Chatflow 和 Agent 中创建并查询异步
AI 音乐视频任务。

- 官网：https://beatapi.io/
- API 文档：https://docs.beatapi.io/
- 创建 API Key：https://beatapi.io/dashboard/apikeys

## 工具

### 创建音乐视频任务

使用 1-7 个公开 HTTPS 图片 URL 和一个公开 HTTPS 音频 URL 启动 BeatAPI
`music-video` 工作流。工具会立即返回任务 ID，不会让长时间渲染阻塞
Dify 工具调用。

### 查询任务

返回任务的当前状态、阶段、输出、用量、请求 ID 和公开错误信息。建议每 5-10 秒
查询一次，并设置有上限的循环。

## 安装与授权

1. 在 Dify 中打开 **Plugins > Install Plugin > GitHub**。
2. 输入 `erickkkyt/beatapi-dify-plugin`。
3. 在 https://beatapi.io/dashboard/apikeys 创建可撤销的 API Key。
4. 打开 **Tools > BeatAPI > Authorize** 并粘贴 API Key。

API Key 只会通过 `Authorization: Bearer` 请求头发送到
`https://api.beatapi.io`，请不要把 Key 写入提示词或工具参数。

## 支持

联系 support@beatapi.io 或访问 https://beatapi.io/。

