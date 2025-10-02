# RPC Hub 示例

该仓库实现了一个遵循 Linux 之父极简、模块化哲学的 RPC Hub 框架：

- **Hub 平台**：FastAPI 应用负责服务发现、注册、路由与权限校验。
- **RPC 模块**：独立的 `backend/hub/rpc.py` 提供轻量级的消息总线，支持服务之间的异步调用。
- **插件系统**：服务以插件形式通过配置加载，实现业务模块的热插拔。
- **前端控制台**：基于 Vue + Vite 的可拔插 UI，展示服务列表与元数据。

## 目录结构

```
backend/
  hub/                 # Hub 核心能力
  services/            # 示例插件（博客、评论、数据库）
config/services.yaml   # 服务注册表
frontend/              # Vue 前端工程
```

## 运行后端

```bash
pip install fastapi uvicorn pyyaml
uvicorn backend.hub.main:app --reload
```

## 运行前端

```bash
cd frontend
npm install
npm run dev
```

前端开发服务器默认代理 `/api` 到 `http://localhost:8000`，可直接联动后端。

## 身份令牌示例

| 角色   | Token          |
| ------ | -------------- |
| public | `public-token` |
| editor | `editor-token` |
| admin  | `admin-token`  |

在调用 Hub 的路由接口时，通过 `token` 参数传入对应的令牌即可完成权限校验。
