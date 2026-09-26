# BeatAPI for Dify

BeatAPI Dify 工具插件可以在 Workflow、Chatflow 和 Agent 中创建并查询异步
图片、视频、Effect 和音乐视频任务。

- 官网：https://beatapi.io/
- API 文档：https://docs.beatapi.io/
- 创建 API Key：https://beatapi.io/dashboard/apikeys

## 工具

新增 **搜索能力**、**查看能力参数** 和 **调用能力**，覆盖当前模型、社媒数据、
联网工具和工作流。它们适合智能体按需求动态发现能力；调用前须按 Inspect 返回的
可用状态和执行策略选择 Run 或对应的直接 API，Run 的开始操作可能扣费。
人工编排的工作流优先使用已有的图片、视频、Effect 和音乐视频专用工具。
文本模型若需显示在 Dify 原生 LLM 节点，仍需另行配置 OpenAI 兼容模型供应商，
API 地址为 `https://api.beatapi.io/v1`。

插件按照当前 BeatAPI API 契约提供 11 个工具：

- **查询生成模型**：读取稳定的图片/视频模型别名和输入模式。
- **创建图片任务**：支持 `nano-banana`、`nano-banana-pro`、`gpt-image-2`、
  `seedream-5-pro`。
- **创建视频任务**：支持 `minimax-h3`、`seedance-2`、`seedance-2-fast`、
  `seedance-2-mini`、`veo-3.1`、`seedance-2.5`、`kling-3`。
- **查询 Effects**、**获取 Effect**：先读取已发布 Effect 的不可变版本和输入契约。
- **创建 Effect 任务**：使用幂等键运行图片或视频 Effect。
- **创建音乐视频任务**：运行高层 Music Video 工作流。
- **查询任务**：统一查询所有异步任务。

这些模型名是 BeatAPI 的公开稳定别名；插件不会暴露或选择内部供应商、模板和路由 ID。

### 创建音乐视频任务

使用 1-7 个公开 HTTPS 图片 URL 和一个公开 HTTPS 音频 URL 启动 BeatAPI
`music-video` 工作流。工具会立即返回任务 ID，不会让长时间渲染阻塞
Dify 工具调用。

### 查询任务

返回任务的当前状态、阶段、输出、用量、请求 ID 和公开错误信息。建议每 5-10 秒
查询一次，并设置有上限的循环。

当前任务都会返回 `task_kind`、`capability_id` 和 `capability_version`。
用量为十进制美元金额；为兼容旧客户端，响应仍保留 `credits_reserved` 等字段名，
其中 1 Credit = 1 美元。

## 安装与授权

1. 在 Dify 中打开 **Plugins > Install Plugin > GitHub**。
2. 输入 `erickkkyt/beatapi-dify-plugin`。
3. 在 https://beatapi.io/dashboard/apikeys 创建可撤销的 API Key。
4. 打开 **Tools > BeatAPI > Authorize** 并粘贴 API Key。

建议先用“查询生成模型”或“查询 Effects”确认能力，再调用对应创建工具；所有创建工具
返回的任务 ID 都交给“查询任务”轮询，成功后从 `output.media` 或 `output.r2_url`
读取 BeatAPI 托管结果。

API Key 只会通过 `Authorization: Bearer` 请求头发送到
`https://api.beatapi.io`，请不要把 Key 写入提示词或工具参数。

## 支持

联系 support@beatapi.io 或访问 https://beatapi.io/。
