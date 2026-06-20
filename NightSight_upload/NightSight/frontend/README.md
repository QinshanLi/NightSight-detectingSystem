# NightSight 守夜者前端原型

这是根据 `NightSight系统_物联网设计大赛.docx` 里的功能说明和界面预想图整理出的 Vue 3 + Vite + Element Plus + ECharts 前端页面。布局采用左侧导航、顶部标题、中央增强前后对比、事件趋势、时间轴、风险规则、结构化事件、右侧实时预警与系统状态的驾驶舱风格。

## 运行方式

```bash
cd nightsight-frontend
npm install
npm run dev
```

浏览器打开：`http://127.0.0.1:5173`

## 对接后端

复制 `.env.example` 为 `.env`，按你的 FastAPI 地址修改：

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000/api
VITE_WS_URL=ws://127.0.0.1:8000/ws/events
```

页面会优先请求后端接口。如果后端还没写好，会自动使用前端模拟数据，所以可以先演示页面，再逐步替换为真实接口。

## 建议后端接口

- `GET /api/events/recent`：最近风险事件列表
- `GET /api/devices/status`：设备状态、MySQL、报警设备、补光灯等状态
- `GET /api/dashboard/stats`：今日事件统计、风险等级分布、24小时趋势
- `GET /api/events/timeline`：集成测试视频的事件流时间轴
- `POST /api/control/action`：增强、检测、语音、联动设备等开关控制
- `WS /ws/events`：实时推送结构化风险事件

## 目录说明

- `src/views/NightSightDashboard.vue`：主界面
- `src/styles.css`：整体大屏暗蓝风格样式
- `src/api/dashboard.js`：接口封装
- `src/api/mockData.js`：后端未完成时的模拟数据
- `src/components/ChartCard.vue`：ECharts 图表组件
