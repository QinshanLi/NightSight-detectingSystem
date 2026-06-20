<template>
  <div class="nightsight-page">
    <aside class="side-bar">
      <div class="brand">
        <div class="brand-icon">🛡</div>
        <div>
          <div class="brand-title">NightSight守夜者</div>
          <div class="brand-subtitle">AIoT智能交通</div>
        </div>
      </div>

      <nav class="nav-list">
        <button
          v-for="item in menus"
          :key="item.key"
          class="nav-item"
          :class="{ active: activeMenu === item.key }"
          @click="activeMenu = item.key"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
          <span v-if="item.children" class="nav-arrow">⌄</span>
        </button>
      </nav>

      <div class="side-status">
        <div class="side-status-title">系统运行状态</div>
        <div class="status-ring">
          <div class="ring-inner">
            <span>{{ streamConnected ? '正常' : '待机' }}</span>
          </div>
        </div>
        <div class="status-small">
          运行时间：{{ streamConnected ? runningTimeText : '未接入' }}
        </div>
        <div class="status-small">版本：v1.0.0</div>
      </div>
    </aside>

    <main class="main-layout">
      <header class="top-header">
        <div class="page-title">
          NightSight守夜者：面向机器视觉的暗光增强检测与AIoT联动预警系统
        </div>

        <div class="top-meta">
          <span>☁ 多云 24℃</span>
          <span>{{ currentTime }}</span>
          <span>{{ currentDate }}</span>
          <span class="user-badge">👤 管理员</span>
        </div>
      </header>

      <section v-if="activeMenu === 'home'" class="work-area">
        <section class="center-area">
          <div class="mode-tabs">
            <button
              v-for="tab in modeTabs"
              :key="tab.key"
              :class="{ active: activeTab === tab.key }"
              @click="activeTab = tab.key"
            >
              {{ tab.label }}
            </button>
          </div>

          <section class="video-grid">
            <div class="video-card">
              <div class="video-label">原始暗光画面</div>

              <div v-if="streamConnected" class="video-frame raw-frame">
                <div class="road road-raw">
                  <div class="lane lane-left"></div>
                  <div class="lane lane-right"></div>
                  <div class="car-light light-a"></div>
                  <div class="car-light light-b"></div>
                  <div class="person-shape person-raw"></div>
                  <div class="dark-car raw-car"></div>
                </div>

                <div class="video-metric">
                  <p>亮度：32.1 lux</p>
                  <p>对比度：0.28</p>
                  <p>增强状态：未增强</p>
                </div>
              </div>

              <div v-else class="empty-video">
                <div class="empty-icon">📷</div>
                <div class="empty-title">未接入视频流</div>
                <div class="empty-desc">
                  当前仅展示前端框架，点击下方按钮后进入离线演示模式。
                </div>
              </div>
            </div>

            <div class="video-card">
              <div class="video-label">增强后检测画面</div>

              <div v-if="streamConnected" class="video-frame enhanced-frame">
                <div class="road road-enhanced">
                  <div class="lane lane-left"></div>
                  <div class="lane lane-right"></div>
                  <div class="car-light light-a bright"></div>
                  <div class="car-light light-b bright"></div>

                  <div class="detect-box car-box">
                    <span>car 0.92</span>
                  </div>
                  <div class="detect-box person-box">
                    <span>person 0.89</span>
                  </div>

                  <div class="person-shape person-detect"></div>
                  <div class="dark-car detect-car"></div>
                </div>

                <div class="video-metric">
                  <p>亮度：128.7 lux ↑</p>
                  <p>对比度：0.62 ↑</p>
                  <p>增强算法：已增强 TGE-YOLO</p>
                </div>
              </div>

              <div v-else class="empty-video">
                <div class="empty-icon">🧠</div>
                <div class="empty-title">检测结果待生成</div>
                <div class="empty-desc">
                  接入视频后，系统才会显示增强画面、目标框和风险结果。
                </div>
              </div>
            </div>

            <div v-if="streamConnected && currentRisk" class="risk-floating">
              <div class="risk-floating-icon">⚠</div>
              <div>
                <strong>{{ currentRisk.type }}</strong>
                <span>{{ currentRisk.level }}｜请减速慢行，注意避让！</span>
              </div>
            </div>
          </section>

          <section class="control-row">
            <button class="control-btn primary" @click="toggleStream">
              <span>☼</span>
              {{ streamConnected ? '断开视频' : '接入演示视频' }}
              <i>{{ streamConnected ? 'ON' : 'OFF' }}</i>
            </button>

            <button class="control-btn" :class="{ active: detectEnabled }" @click="detectEnabled = !detectEnabled">
              <span>◎</span>
              检测开启
              <i>{{ detectEnabled ? 'ON' : 'OFF' }}</i>
            </button>

            <button class="control-btn danger" :class="{ active: alertEnabled }" @click="alertEnabled = !alertEnabled">
              <span>🔔</span>
              风险预警
            </button>

            <button class="control-btn" :class="{ active: voiceEnabled }" @click="voiceEnabled = !voiceEnabled">
              <span>🔊</span>
              语音播报
            </button>

            <button class="control-btn" :class="{ active: recording }" @click="recording = !recording">
              <span>⏺</span>
              {{ recording ? '录制中' : '开始录制' }}
            </button>

            <button class="control-btn" :class="{ active: deviceLinked }" @click="deviceLinked = !deviceLinked">
              <span>🔗</span>
              联动设备
              <i>{{ deviceLinked ? 'ON' : 'OFF' }}</i>
            </button>
          </section>

          <section class="summary-grid">
            <div class="panel card-stat">
              <div class="panel-title">今日事件统计</div>
              <div class="donut">
                <div class="donut-center">
                  <b>{{ streamConnected ? totalEvents : 0 }}</b>
                  <span>事件</span>
                </div>
              </div>
              <div class="legend-list">
                <p><span class="dot red"></span>车人共现风险 {{ streamConnected ? 8 : 0 }}（25%）</p>
                <p><span class="dot orange"></span>强光干扰风险 {{ streamConnected ? 7 : 0 }}（22%）</p>
                <p><span class="dot yellow"></span>弱光小目标风险 {{ streamConnected ? 6 : 0 }}（19%）</p>
                <p><span class="dot blue"></span>盲区接近风险 {{ streamConnected ? 6 : 0 }}（19%）</p>
                <p><span class="dot purple"></span>危险区域入侵 {{ streamConnected ? 5 : 0 }}（15%）</p>
              </div>
            </div>

            <div class="panel">
              <div class="panel-title">事件趋势（近24小时）</div>
              <svg class="line-chart" viewBox="0 0 400 150" preserveAspectRatio="none">
                <polyline
                  class="grid-line"
                  points="0,120 400,120"
                />
                <polyline
                  class="grid-line"
                  points="0,80 400,80"
                />
                <polyline
                  class="grid-line"
                  points="0,40 400,40"
                />
                <polyline
                  v-if="streamConnected"
                  class="risk-line red-line"
                  points="0,120 30,118 60,110 90,95 120,100 150,82 180,88 210,60 240,75 270,42 300,62 330,35 360,55 400,25"
                />
                <polyline
                  v-if="streamConnected"
                  class="risk-line yellow-line"
                  points="0,128 30,125 60,115 90,118 120,105 150,100 180,86 210,92 240,75 270,80 300,62 330,70 360,55 400,48"
                />
              </svg>
              <div class="chart-axis">
                <span>00:00</span>
                <span>06:00</span>
                <span>12:00</span>
                <span>18:00</span>
                <span>24:00</span>
              </div>
            </div>

            <div class="panel mini-risk">
              <div class="panel-title">风险等级分布</div>
              <div class="donut small">
                <div class="donut-center">
                  <b>{{ streamConnected ? 32 : 0 }}</b>
                  <span>风险</span>
                </div>
              </div>
              <div class="risk-rate-list">
                <p><span class="risk-pill high"></span>高风险 {{ streamConnected ? '12' : '0' }}（38%）</p>
                <p><span class="risk-pill mid"></span>中风险 {{ streamConnected ? '14' : '0' }}（44%）</p>
                <p><span class="risk-pill low"></span>低风险 {{ streamConnected ? '6' : '0' }}（18%）</p>
              </div>
            </div>

            <div class="panel iot-card">
              <div class="panel-title">AIoT联动设备状态</div>
              <div class="iot-map">
                <div class="iot-node main">边缘网关</div>
                <div class="iot-node">警示灯</div>
                <div class="iot-node">蜂鸣器</div>
                <div class="iot-node">补光灯</div>
                <div class="iot-node">ESP32</div>
                <div class="iot-node">云平台</div>
              </div>
              <div class="iot-state">
                <span :class="{ on: streamConnected }">在线中</span>
                <span :class="{ on: deviceLinked }">联动中</span>
              </div>
            </div>
          </section>

          <section class="timeline-panel">
            <div class="panel-title">事件流时间轴（通过视频流、低光增强、YOLO、light_event_stream_v1.mp4）</div>
            <div class="timeline">
              <div
                v-for="event in timelineEvents"
                :key="event.time"
                class="timeline-item"
                :class="event.levelClass"
              >
                <span class="timeline-time">{{ event.time }}</span>
                <b>{{ streamConnected ? event.type : '等待视频' }}</b>
                <em>{{ streamConnected ? event.level : '未触发' }}</em>
              </div>
            </div>
          </section>

          <section class="bottom-grid">
            <div class="panel rule-panel">
              <div class="panel-title">风险规则解释</div>
              <div v-if="streamConnected" class="rule-content">
                <h3>{{ currentRisk?.type || '暂无风险' }}</h3>
                <p>
                  系统通过暗光增强、目标检测、ROI区域判断、目标距离估计和事件规则融合，对当前视频流进行风险识别。
                </p>
                <div class="rule-preview">
                  <div class="mini-video">
                    <div class="mini-box car">car</div>
                    <div class="mini-box person">person</div>
                  </div>
                  <ul>
                    <li>person置信度 ≥ 0.6</li>
                    <li>car置信度 ≥ 0.6</li>
                    <li>目标中心点落入重点ROI</li>
                    <li>持续帧数 ≥ 5</li>
                  </ul>
                </div>
              </div>
              <div v-else class="empty-block">
                未接入视频流，风险规则暂不触发。
              </div>
            </div>

            <div class="panel json-panel">
              <div class="panel-title">事件详情（结构化事件）</div>
              <pre>{{ streamConnected ? eventJson : emptyJson }}</pre>
            </div>

            <div class="panel record-panel">
              <div class="panel-title">最近事件记录</div>
              <table>
                <thead>
                  <tr>
                    <th>时间</th>
                    <th>风险类型</th>
                    <th>等级</th>
                    <th>设备ID</th>
                    <th>截图</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="event in visibleEvents" :key="event.id">
                    <td>{{ event.time }}</td>
                    <td>{{ event.type }}</td>
                    <td :class="event.levelClass">{{ event.level }}</td>
                    <td>{{ event.device }}</td>
                    <td><span class="thumb"></span></td>
                    <td>👁 ⬇</td>
                  </tr>
                  <tr v-if="!streamConnected">
                    <td colspan="6" class="empty-table">暂无事件，等待视频流接入。</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>
        </section>

        <aside class="right-rail">
          <section class="panel alert-panel">
            <div class="rail-title">
              <span>实时风险预警</span>
              <button>查看全部</button>
            </div>

            <div v-if="streamConnected" class="alert-list">
              <div
                v-for="event in visibleEvents"
                :key="event.id"
                class="alert-item"
                :class="event.levelClass"
              >
                <div class="alert-thumb"></div>
                <div class="alert-info">
                  <b>{{ event.type }}</b>
                  <span>{{ event.time }}</span>
                  <small>{{ event.location }}</small>
                </div>
                <strong>{{ event.level }}</strong>
              </div>
            </div>

            <div v-else class="empty-block">
              暂无预警。接入演示视频后，右侧会实时滚动显示五类风险事件。
            </div>
          </section>

          <section class="panel system-panel">
            <div class="panel-title">系统状态</div>
            <div class="system-row" v-for="item in systemStatus" :key="item.name">
              <span>
                <i :class="{ online: item.ok && streamConnected }"></i>
                {{ item.name }}
              </span>
              <b>{{ streamConnected ? item.value : '待机' }}</b>
            </div>
          </section>
        </aside>
      </section>

      <section v-else class="sub-page">
        <div class="sub-page-header">
          <h2>{{ currentMenuTitle }}</h2>
          <p>{{ currentMenuDesc }}</p>
        </div>

        <div class="sub-card-grid">
          <div class="panel sub-card" v-for="card in subCards" :key="card.title">
            <div class="sub-icon">{{ card.icon }}</div>
            <h3>{{ card.title }}</h3>
            <p>{{ card.desc }}</p>
            <button @click="streamConnected ? null : toggleStream">
              {{ streamConnected ? '查看详情' : '接入演示视频' }}
            </button>
          </div>
        </div>

        <div class="panel sub-table">
          <div class="panel-title">{{ currentMenuTitle }}模块数据</div>
          <table>
            <thead>
              <tr>
                <th>时间</th>
                <th>模块</th>
                <th>状态</th>
                <th>说明</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="streamConnected" v-for="row in subRows" :key="row.time + row.module">
                <td>{{ row.time }}</td>
                <td>{{ row.module }}</td>
                <td :class="row.levelClass">{{ row.status }}</td>
                <td>{{ row.desc }}</td>
                <td>查看｜导出</td>
              </tr>
              <tr v-if="!streamConnected">
                <td colspan="5" class="empty-table">暂无实时数据。当前页面已可点击，后续可接入后端接口。</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

const activeMenu = ref('home')
const activeTab = ref('enhance')
const streamConnected = ref(false)
const detectEnabled = ref(true)
const alertEnabled = ref(true)
const voiceEnabled = ref(false)
const recording = ref(false)
const deviceLinked = ref(true)

const currentTime = ref('')
const currentDate = ref('')
const runningSeconds = ref(0)
let timer = null

const menus = [
  { key: 'home', label: '首页概览', icon: '⌂' },
  { key: 'monitor', label: '实时监控', icon: '◎', children: true },
  { key: 'events', label: '事件管理', icon: '▣', children: true },
  { key: 'playback', label: '事件回放', icon: '◴', children: true },
  { key: 'statistics', label: '数据统计', icon: '◷', children: true },
  { key: 'devices', label: '设备管理', icon: '▤', children: true },
  { key: 'zones', label: '区域管理', icon: '◎', children: true },
  { key: 'rules', label: '规则管理', icon: '◇', children: true },
  { key: 'linkage', label: '联动控制', icon: '⚙', children: true },
  { key: 'docs', label: '帮助文档', icon: '❔', children: true },
  { key: 'users', label: '用户管理', icon: '♙' }
]

const modeTabs = [
  { key: 'realtime', label: '实时画面' },
  { key: 'enhance', label: '增强画面' },
  { key: 'detect', label: '目标检测' },
  { key: 'risk', label: '风险区域' },
  { key: 'map', label: '地图联动' }
]

const riskEvents = [
  {
    id: 1,
    type: '车人共现风险',
    level: '高风险',
    levelClass: 'high',
    time: '22:35:48',
    location: '坡道入口',
    device: 'AIoT-Edge-001'
  },
  {
    id: 2,
    type: '强光干扰风险',
    level: '中风险',
    levelClass: 'mid',
    time: '22:34:15',
    location: '城市道路',
    device: 'AIoT-Edge-001'
  },
  {
    id: 3,
    type: '弱光小目标风险',
    level: '中风险',
    levelClass: 'mid',
    time: '22:32:56',
    location: '乡村道路',
    device: 'AIoT-Edge-002'
  },
  {
    id: 4,
    type: '盲区接近风险',
    level: '高风险',
    levelClass: 'high',
    time: '22:30:21',
    location: '地下车库',
    device: 'AIoT-Edge-001'
  },
  {
    id: 5,
    type: '危险区域入侵',
    level: '高风险',
    levelClass: 'high',
    time: '22:28:03',
    location: '施工通道',
    device: 'AIoT-Edge-003'
  }
]

const timelineEvents = [
  { time: '00:15', type: '弱光小目标风险', level: '中风险', levelClass: 'mid' },
  { time: '00:35', type: '强光干扰风险', level: '中风险', levelClass: 'mid' },
  { time: '00:55', type: '盲区接近风险', level: '高风险', levelClass: 'high' },
  { time: '01:20', type: '车人共现风险', level: '高风险', levelClass: 'high' },
  { time: '01:45', type: '危险区域入侵', level: '高风险', levelClass: 'high' }
]

const systemStatus = [
  { name: '图像增强', value: '正常', ok: true },
  { name: '网络状态', value: '延迟：28ms', ok: true },
  { name: '边缘计算', value: 'AIoT-Edge-001', ok: true },
  { name: '存储状态', value: '256GB / 512GB', ok: true },
  { name: 'MySQL事件库', value: '待接入', ok: false },
  { name: '报警设备', value: '蜂鸣器｜警示灯', ok: true },
  { name: '补光灯控制', value: '亮度：60%', ok: true },
  { name: '语音播报', value: '开启', ok: true }
]

const pageMap = {
  monitor: {
    title: '实时监控',
    desc: '用于接入摄像头或视频文件，显示暗光增强前后画面、目标检测框和实时风险结果。'
  },
  events: {
    title: '事件管理',
    desc: '用于管理五类风险事件，包括车人共现、弱光小目标、强光干扰、盲区接近和危险区域入侵。'
  },
  playback: {
    title: '事件回放',
    desc: '用于查看风险发生时的截图、短视频片段、时间戳和事件详情。'
  },
  statistics: {
    title: '数据统计',
    desc: '用于统计事件数量、风险等级分布、误报率、延迟和设备运行趋势。'
  },
  devices: {
    title: '设备管理',
    desc: '用于管理边缘计算设备、摄像头、ESP32、警示灯、蜂鸣器和补光设备。'
  },
  zones: {
    title: '区域管理',
    desc: '用于配置ROI风险区域、禁入区域、盲区边界和监控场景。'
  },
  rules: {
    title: '规则管理',
    desc: '用于配置风险触发阈值、目标置信度、持续帧数和联动策略。'
  },
  linkage: {
    title: '联动控制',
    desc: '用于管理MQTT、WebSocket、HTTP推送、声光报警和AIoT联动闭环。'
  },
  docs: {
    title: '帮助文档',
    desc: '用于展示系统说明、部署流程、接口说明和比赛答辩材料。'
  },
  users: {
    title: '用户管理',
    desc: '用于管理管理员、运维人员、查看权限和日志权限。'
  }
}

const subCards = [
  {
    icon: '🎥',
    title: '视频流接入',
    desc: '支持摄像头、MP4文件和离线演示视频。'
  },
  {
    icon: '🧠',
    title: '智能识别',
    desc: '暗光增强后进入目标检测与事件规则判断。'
  },
  {
    icon: '🚨',
    title: '风险告警',
    desc: '高风险事件触发声光提示和平台预警。'
  },
  {
    icon: '🔗',
    title: 'AIoT联动',
    desc: '边缘端输出事件JSON，联动ESP32设备。'
  }
]

const subRows = [
  {
    time: '22:35:48',
    module: '风险识别',
    status: '高风险',
    levelClass: 'high',
    desc: '检测到车人共现风险，已触发平台预警。'
  },
  {
    time: '22:34:15',
    module: '暗光增强',
    status: '正常',
    levelClass: 'safe',
    desc: '画面亮度提升，对比度增强。'
  },
  {
    time: '22:32:56',
    module: 'AIoT联动',
    status: '已联动',
    levelClass: 'mid',
    desc: '警示灯、蜂鸣器和补光设备进入响应状态。'
  }
]

const totalEvents = computed(() => riskEvents.length ? 32 : 0)
const visibleEvents = computed(() => (streamConnected.value ? riskEvents : []))
const currentRisk = computed(() => (streamConnected.value ? riskEvents[0] : null))
const currentMenuTitle = computed(() => pageMap[activeMenu.value]?.title || '功能模块')
const currentMenuDesc = computed(() => pageMap[activeMenu.value]?.desc || '该模块用于后续系统功能扩展。')
const runningTimeText = computed(() => {
  const h = Math.floor(runningSeconds.value / 3600)
  const m = Math.floor((runningSeconds.value % 3600) / 60)
  const s = runningSeconds.value % 60
  return `${h}小时 ${m}分 ${s}秒`
})

const eventJson = computed(() => {
  const event = currentRisk.value
  if (!event) return '{}'
  return JSON.stringify(
    {
      event_id: 'EVT20260519-00032',
      device_id: event.device,
      device_type: 'car_edge_node',
      risk_type: event.type,
      risk_level: event.level,
      time: `2026-05-19 ${event.time}`,
      location: event.location,
      targets: ['person', 'car'],
      action: ['platform_warning', 'snapshot', 'mqtt_alarm'],
      snapshot_url: '/snapshots/20260519/EVT20260519-00032.jpg'
    },
    null,
    2
  )
})

const emptyJson = `{
  "status": "waiting_stream",
  "message": "未接入视频流，暂无事件JSON"
}`

function toggleStream() {
  streamConnected.value = !streamConnected.value
  if (streamConnected.value) {
    runningSeconds.value = 369
    activeTab.value = 'enhance'
  } else {
    runningSeconds.value = 0
    recording.value = false
  }
}

function updateDateTime() {
  const now = new Date()
  const pad = (n) => String(n).padStart(2, '0')
  currentTime.value = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`
  currentDate.value = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`
  if (streamConnected.value) {
    runningSeconds.value += 1
  }
}

onMounted(() => {
  updateDateTime()
  timer = setInterval(updateDateTime, 1000)
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.nightsight-page {
  min-height: 100vh;
  display: flex;
  background:
    radial-gradient(circle at 18% 12%, rgba(0, 100, 255, 0.22), transparent 28%),
    radial-gradient(circle at 80% 0%, rgba(0, 160, 255, 0.18), transparent 26%),
    #050b18;
  color: #d8e9ff;
  font-family:
    "Microsoft YaHei",
    "PingFang SC",
    Arial,
    sans-serif;
  overflow: hidden;
}

.side-bar {
  width: 148px;
  min-width: 148px;
  height: 100vh;
  padding: 12px 8px;
  background: linear-gradient(180deg, rgba(5, 22, 47, 0.98), rgba(3, 11, 27, 0.98));
  border-right: 1px solid rgba(53, 135, 255, 0.22);
  display: flex;
  flex-direction: column;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 50px;
  padding: 4px 6px 12px;
  border-bottom: 1px solid rgba(61, 139, 255, 0.16);
}

.brand-icon {
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  color: #37a2ff;
  border-radius: 8px;
  background: rgba(44, 128, 255, 0.16);
  box-shadow: inset 0 0 14px rgba(0, 162, 255, 0.25);
}

.brand-title {
  font-size: 13px;
  font-weight: 800;
  color: #eef7ff;
  white-space: nowrap;
}

.brand-subtitle {
  font-size: 10px;
  color: rgba(184, 213, 255, 0.6);
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-top: 12px;
}

.nav-item {
  height: 36px;
  border: 1px solid transparent;
  border-radius: 6px;
  background: transparent;
  color: rgba(216, 233, 255, 0.76);
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 8px;
  cursor: pointer;
  font-size: 13px;
  text-align: left;
}

.nav-item:hover,
.nav-item.active {
  background: linear-gradient(90deg, rgba(18, 89, 198, 0.82), rgba(8, 47, 110, 0.52));
  border-color: rgba(53, 139, 255, 0.38);
  color: #ffffff;
  box-shadow: 0 0 18px rgba(0, 110, 255, 0.2);
}

.nav-icon {
  width: 18px;
  text-align: center;
  color: #80c3ff;
}

.nav-arrow {
  margin-left: auto;
  opacity: 0.6;
}

.side-status {
  margin-top: auto;
  padding: 12px 8px;
  border-radius: 8px;
  background: rgba(5, 24, 52, 0.86);
  border: 1px solid rgba(67, 145, 255, 0.18);
}

.side-status-title {
  font-size: 12px;
  color: #bcd6ff;
  margin-bottom: 8px;
}

.status-ring {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  margin: 8px auto;
  padding: 5px;
  background: conic-gradient(#12e68b, #006bff, #0d2f63, #12e68b);
}

.ring-inner {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: #061224;
  display: grid;
  place-items: center;
  color: #18e890;
  font-weight: 800;
  font-size: 13px;
}

.status-small {
  font-size: 11px;
  color: rgba(198, 220, 255, 0.72);
  line-height: 1.8;
}

.main-layout {
  flex: 1;
  height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.top-header {
  height: 48px;
  padding: 0 14px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(53, 135, 255, 0.22);
  background: rgba(4, 13, 31, 0.78);
  backdrop-filter: blur(12px);
}

.page-title {
  flex: 1;
  text-align: center;
  font-size: 18px;
  font-weight: 800;
  letter-spacing: 0.5px;
  color: #dcecff;
  text-shadow: 0 0 16px rgba(69, 155, 255, 0.35);
}

.top-meta {
  min-width: 310px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: rgba(216, 233, 255, 0.75);
}

.user-badge {
  padding-left: 6px;
  border-left: 1px solid rgba(255, 255, 255, 0.15);
}

.work-area {
  height: calc(100vh - 48px);
  display: grid;
  grid-template-columns: minmax(720px, 1fr) 282px;
  gap: 8px;
  padding: 8px;
  overflow: hidden;
}

.center-area {
  min-width: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.mode-tabs {
  height: 32px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 3px 8px;
  border-radius: 6px;
  background: rgba(4, 16, 38, 0.75);
  border: 1px solid rgba(55, 131, 255, 0.16);
}

.mode-tabs button {
  height: 24px;
  padding: 0 22px;
  border-radius: 5px;
  border: 1px solid transparent;
  background: transparent;
  color: rgba(211, 230, 255, 0.72);
  cursor: pointer;
}

.mode-tabs button.active {
  background: linear-gradient(180deg, rgba(32, 92, 190, 0.88), rgba(11, 42, 96, 0.88));
  border-color: rgba(74, 157, 255, 0.46);
  color: #ffffff;
}

.video-grid {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  height: 292px;
}

.video-card,
.panel {
  border-radius: 7px;
  background: linear-gradient(180deg, rgba(8, 26, 56, 0.93), rgba(3, 15, 35, 0.94));
  border: 1px solid rgba(53, 135, 255, 0.24);
  box-shadow:
    inset 0 0 24px rgba(40, 116, 255, 0.08),
    0 0 18px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

.video-card {
  position: relative;
}

.video-label {
  position: absolute;
  z-index: 5;
  top: 10px;
  left: 10px;
  padding: 5px 9px;
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.56);
  border: 1px solid rgba(255, 255, 255, 0.28);
  font-size: 12px;
  color: #fff;
}

.video-frame {
  height: 100%;
  position: relative;
  overflow: hidden;
  background: #070b12;
}

.road {
  position: absolute;
  inset: 0;
  overflow: hidden;
  background:
    radial-gradient(circle at 20% 35%, rgba(255, 255, 255, 0.18), transparent 3%),
    radial-gradient(circle at 73% 28%, rgba(255, 255, 255, 0.15), transparent 2%),
    linear-gradient(180deg, #090d14 0%, #111722 38%, #0b0f14 39%, #151922 100%);
}

.road::before {
  content: "";
  position: absolute;
  left: 50%;
  bottom: -30%;
  width: 80%;
  height: 90%;
  transform: translateX(-50%) perspective(500px) rotateX(62deg);
  background:
    repeating-linear-gradient(90deg, transparent 0 48%, rgba(255, 255, 255, 0.22) 49% 50%, transparent 51% 100%),
    linear-gradient(90deg, rgba(10, 10, 10, 0.1), rgba(60, 60, 60, 0.18), rgba(10, 10, 10, 0.1));
  clip-path: polygon(44% 0, 56% 0, 100% 100%, 0 100%);
  opacity: 0.8;
}

.road-enhanced {
  filter: brightness(1.45) contrast(1.15);
}

.road-raw {
  filter: brightness(0.58) contrast(0.9);
}

.lane {
  position: absolute;
  bottom: 0;
  height: 210px;
  width: 2px;
  background: linear-gradient(180deg, transparent, rgba(255, 255, 255, 0.7));
  transform-origin: bottom;
}

.lane-left {
  left: 42%;
  transform: rotate(15deg);
}

.lane-right {
  right: 39%;
  transform: rotate(-17deg);
}

.car-light {
  position: absolute;
  width: 26px;
  height: 14px;
  border-radius: 50%;
  background: #fff7d3;
  box-shadow:
    0 0 14px #fff,
    0 0 42px rgba(255, 230, 162, 0.9);
}

.light-a {
  left: 41%;
  top: 54%;
}

.light-b {
  left: 48%;
  top: 52%;
}

.car-light.bright {
  box-shadow:
    0 0 18px #fff,
    0 0 70px rgba(255, 230, 162, 1),
    0 0 110px rgba(124, 183, 255, 0.65);
}

.person-shape {
  position: absolute;
  width: 10px;
  height: 34px;
  border-radius: 10px 10px 4px 4px;
  background: rgba(255, 255, 255, 0.78);
}

.person-raw {
  right: 28%;
  top: 48%;
  opacity: 0.6;
}

.person-detect {
  right: 28%;
  top: 48%;
}

.dark-car {
  position: absolute;
  width: 54px;
  height: 35px;
  border-radius: 8px 8px 4px 4px;
  background: rgba(55, 65, 75, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.25);
}

.raw-car {
  left: 45%;
  top: 54%;
  opacity: 0.5;
}

.detect-car {
  left: 45%;
  top: 54%;
}

.detect-box {
  position: absolute;
  border: 2px solid;
  z-index: 3;
}

.detect-box span {
  position: absolute;
  top: -20px;
  left: -2px;
  padding: 2px 5px;
  color: #fff;
  font-size: 11px;
}

.car-box {
  left: 43.5%;
  top: 46%;
  width: 90px;
  height: 70px;
  border-color: #ff3d3d;
}

.car-box span {
  background: #ff3d3d;
}

.person-box {
  right: 24%;
  top: 40%;
  width: 58px;
  height: 88px;
  border-color: #a95cff;
}

.person-box span {
  background: #a95cff;
}

.video-metric {
  position: absolute;
  left: 10px;
  bottom: 10px;
  padding: 8px 10px;
  background: rgba(2, 8, 18, 0.65);
  border: 1px solid rgba(107, 174, 255, 0.28);
  border-radius: 5px;
  font-size: 11px;
}

.video-metric p {
  margin: 0;
  line-height: 1.6;
}

.empty-video {
  height: 100%;
  display: grid;
  place-content: center;
  text-align: center;
  padding: 30px;
  background:
    linear-gradient(135deg, rgba(5, 18, 40, 0.94), rgba(3, 8, 18, 0.96)),
    repeating-linear-gradient(45deg, rgba(255,255,255,.02) 0 10px, transparent 10px 20px);
}

.empty-icon {
  font-size: 42px;
  margin-bottom: 12px;
  opacity: 0.85;
}

.empty-title {
  font-size: 18px;
  font-weight: 800;
  color: #ecf6ff;
}

.empty-desc {
  margin-top: 8px;
  max-width: 320px;
  font-size: 13px;
  color: rgba(211, 230, 255, 0.68);
  line-height: 1.7;
}

.risk-floating {
  position: absolute;
  right: 12px;
  top: 8px;
  z-index: 10;
  min-width: 210px;
  padding: 10px 14px;
  display: flex;
  gap: 10px;
  border-radius: 6px;
  color: #ff5757;
  background: rgba(72, 0, 0, 0.76);
  border: 1px solid rgba(255, 58, 58, 0.55);
  box-shadow: 0 0 18px rgba(255, 40, 40, 0.28);
}

.risk-floating-icon {
  font-size: 28px;
}

.risk-floating strong {
  display: block;
  font-size: 14px;
}

.risk-floating span {
  display: block;
  margin-top: 3px;
  font-size: 11px;
}

.control-row {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 8px;
}

.control-btn {
  height: 42px;
  border-radius: 7px;
  border: 1px solid rgba(65, 137, 255, 0.38);
  background: linear-gradient(180deg, rgba(11, 42, 88, 0.95), rgba(5, 24, 55, 0.95));
  color: #cfe7ff;
  cursor: pointer;
  position: relative;
  font-weight: 700;
}

.control-btn span {
  margin-right: 8px;
}

.control-btn i {
  position: absolute;
  top: 3px;
  right: 5px;
  font-size: 9px;
  color: #19e38b;
  font-style: normal;
}

.control-btn.primary,
.control-btn.active {
  border-color: rgba(0, 231, 148, 0.5);
  box-shadow: inset 0 0 18px rgba(0, 255, 160, 0.08);
}

.control-btn.danger,
.control-btn.danger.active {
  color: #ff5959;
  border-color: rgba(255, 58, 58, 0.45);
  background: linear-gradient(180deg, rgba(80, 9, 17, 0.95), rgba(41, 8, 16, 0.95));
}

.summary-grid {
  display: grid;
  grid-template-columns: 1.1fr 1.35fr 0.8fr 0.95fr;
  gap: 8px;
  height: 152px;
}

.panel {
  padding: 10px;
}

.panel-title,
.rail-title {
  font-size: 13px;
  color: #cce4ff;
  font-weight: 800;
  margin-bottom: 8px;
}

.card-stat {
  display: grid;
  grid-template-columns: 94px 1fr;
  grid-template-rows: 22px 1fr;
  column-gap: 10px;
}

.card-stat .panel-title {
  grid-column: 1 / 3;
}

.donut {
  width: 84px;
  height: 84px;
  border-radius: 50%;
  background: conic-gradient(#ff4747 0 25%, #ffbc36 25% 47%, #ffd75e 47% 66%, #3396ff 66% 85%, #9466ff 85% 100%);
  display: grid;
  place-items: center;
}

.donut.small {
  width: 78px;
  height: 78px;
  margin: 4px auto;
}

.donut-center {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background: #08142a;
  display: grid;
  place-items: center;
  text-align: center;
}

.donut-center b {
  display: block;
  font-size: 20px;
  line-height: 1;
  color: #ffffff;
}

.donut-center span {
  font-size: 10px;
  color: rgba(211, 230, 255, 0.65);
}

.legend-list p,
.risk-rate-list p {
  margin: 0;
  line-height: 1.7;
  font-size: 11px;
  color: rgba(216, 233, 255, 0.75);
}

.dot,
.risk-pill {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  margin-right: 5px;
}

.red,
.high {
  color: #ff4848;
}

.mid {
  color: #ffbd3d;
}

.safe {
  color: #17e48b;
}

.orange {
  background: #ff8d33;
}

.yellow {
  background: #ffd43b;
}

.blue {
  background: #3ca5ff;
}

.purple {
  background: #9668ff;
}

.dot.red,
.risk-pill.high {
  background: #ff4848;
}

.risk-pill.mid {
  background: #ffbd3d;
}

.risk-pill.low {
  background: #3ca5ff;
}

.line-chart {
  width: 100%;
  height: 98px;
}

.grid-line {
  fill: none;
  stroke: rgba(114, 171, 255, 0.15);
  stroke-width: 1;
}

.risk-line {
  fill: none;
  stroke-width: 3;
}

.red-line {
  stroke: #ff4040;
  filter: drop-shadow(0 0 5px rgba(255, 64, 64, 0.7));
}

.yellow-line {
  stroke: #ffbd3d;
  filter: drop-shadow(0 0 5px rgba(255, 189, 61, 0.6));
}

.chart-axis {
  display: flex;
  justify-content: space-between;
  color: rgba(205, 226, 255, 0.55);
  font-size: 10px;
}

.mini-risk {
  display: grid;
  grid-template-columns: 90px 1fr;
  grid-template-rows: 24px 1fr;
}

.mini-risk .panel-title {
  grid-column: 1 / 3;
}

.iot-map {
  height: 84px;
  position: relative;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  align-content: center;
}

.iot-node {
  height: 25px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  background: rgba(14, 50, 100, 0.85);
  border: 1px solid rgba(85, 160, 255, 0.28);
  font-size: 10px;
  color: rgba(222, 238, 255, 0.76);
}

.iot-node.main {
  background: rgba(16, 94, 202, 0.85);
  color: #fff;
}

.iot-state {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
}

.iot-state .on {
  color: #18e58b;
}

.timeline-panel {
  height: 92px;
}

.timeline {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.timeline::before {
  content: "";
  position: absolute;
  left: 20px;
  right: 20px;
  top: 25px;
  height: 2px;
  background: linear-gradient(90deg, #10e18a, #ffbd3d, #ff4444);
}

.timeline-item {
  position: relative;
  width: 120px;
  padding-top: 22px;
  text-align: center;
  z-index: 2;
}

.timeline-item::before {
  content: "";
  position: absolute;
  top: 21px;
  left: 50%;
  width: 8px;
  height: 8px;
  transform: translateX(-50%);
  border-radius: 50%;
  background: #ffbd3d;
  box-shadow: 0 0 10px #ffbd3d;
}

.timeline-item.high::before {
  background: #ff4747;
  box-shadow: 0 0 10px #ff4747;
}

.timeline-time {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  font-size: 11px;
  color: rgba(217, 235, 255, 0.64);
}

.timeline-item b {
  display: block;
  padding: 5px 8px 2px;
  border-radius: 6px 6px 0 0;
  background: rgba(19, 67, 118, 0.8);
  font-size: 11px;
  color: #e8f4ff;
}

.timeline-item em {
  display: block;
  padding: 0 8px 5px;
  border-radius: 0 0 6px 6px;
  background: rgba(19, 67, 118, 0.8);
  font-size: 11px;
  color: #ffcf4a;
  font-style: normal;
}

.timeline-item.high b,
.timeline-item.high em {
  background: rgba(112, 22, 30, 0.85);
}

.timeline-item.high em {
  color: #ff6969;
}

.bottom-grid {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: 1.2fr 1.25fr 1.65fr;
  gap: 8px;
  overflow: hidden;
}

.rule-content h3 {
  margin: 0 0 6px;
  color: #ff5a5a;
  font-size: 16px;
}

.rule-content p {
  margin: 0;
  color: rgba(218, 235, 255, 0.74);
  line-height: 1.65;
  font-size: 12px;
}

.rule-preview {
  margin-top: 8px;
  display: grid;
  grid-template-columns: 110px 1fr;
  gap: 8px;
}

.mini-video {
  height: 88px;
  position: relative;
  border-radius: 5px;
  background: linear-gradient(180deg, #172233, #0b1018);
  border: 1px solid rgba(90, 160, 255, 0.28);
}

.mini-box {
  position: absolute;
  border: 1px solid;
  font-size: 10px;
  color: #fff;
}

.mini-box.car {
  left: 35px;
  top: 36px;
  width: 38px;
  height: 28px;
  border-color: #ff4444;
}

.mini-box.person {
  right: 16px;
  top: 24px;
  width: 28px;
  height: 45px;
  border-color: #a865ff;
}

.rule-preview ul {
  margin: 0;
  padding-left: 16px;
  color: rgba(216, 233, 255, 0.72);
  font-size: 11px;
  line-height: 1.7;
}

.json-panel pre {
  height: calc(100% - 20px);
  margin: 0;
  overflow: auto;
  color: #55e6a8;
  font-size: 11px;
  line-height: 1.45;
  font-family: Consolas, "Courier New", monospace;
}

.record-panel table,
.sub-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  color: rgba(219, 237, 255, 0.78);
}

.record-panel th,
.record-panel td,
.sub-table th,
.sub-table td {
  padding: 7px 6px;
  border-bottom: 1px solid rgba(82, 145, 255, 0.12);
  text-align: left;
}

.record-panel th,
.sub-table th {
  color: rgba(176, 208, 255, 0.72);
  font-weight: 700;
}

.thumb,
.alert-thumb {
  display: block;
  border-radius: 3px;
  background:
    radial-gradient(circle at 45% 50%, #fff, transparent 8%),
    radial-gradient(circle at 60% 55%, #fff1b7, transparent 12%),
    linear-gradient(180deg, #141d2c, #050913);
}

.thumb {
  width: 34px;
  height: 22px;
}

.right-rail {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow: hidden;
}

.alert-panel {
  flex: 1.2;
  overflow: hidden;
}

.rail-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.rail-title button {
  border: none;
  background: transparent;
  color: #56a8ff;
  cursor: pointer;
  font-size: 12px;
}

.alert-list {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.alert-item {
  height: 55px;
  padding: 6px;
  display: grid;
  grid-template-columns: 52px 1fr 48px;
  gap: 8px;
  align-items: center;
  border-radius: 6px;
  background: rgba(7, 29, 64, 0.86);
  border: 1px solid rgba(68, 144, 255, 0.15);
}

.alert-item.high {
  border-color: rgba(255, 67, 67, 0.32);
}

.alert-thumb {
  height: 42px;
}

.alert-info b {
  display: block;
  color: #ff6060;
  font-size: 12px;
}

.alert-info span,
.alert-info small {
  display: block;
  font-size: 11px;
  color: rgba(218, 235, 255, 0.66);
  line-height: 1.4;
}

.alert-item strong {
  font-size: 12px;
  color: #ff4c4c;
}

.alert-item.mid strong,
.alert-item.mid .alert-info b {
  color: #ffbd3d;
}

.system-panel {
  flex: 0.8;
}

.system-row {
  height: 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: rgba(217, 235, 255, 0.74);
}

.system-row i {
  display: inline-block;
  width: 7px;
  height: 7px;
  margin-right: 6px;
  border-radius: 50%;
  background: #59667a;
}

.system-row i.online {
  background: #19e58a;
  box-shadow: 0 0 8px rgba(25, 229, 138, 0.7);
}

.system-row b {
  font-weight: 700;
  color: #19e58a;
}

.empty-block {
  height: calc(100% - 22px);
  display: grid;
  place-items: center;
  text-align: center;
  padding: 20px;
  color: rgba(212, 230, 255, 0.62);
  font-size: 13px;
  line-height: 1.8;
}

.empty-table {
  text-align: center !important;
  color: rgba(216, 233, 255, 0.5);
}

.sub-page {
  height: calc(100vh - 48px);
  padding: 12px;
  overflow: auto;
}

.sub-page-header {
  height: 112px;
  padding: 22px;
  border-radius: 10px;
  border: 1px solid rgba(66, 147, 255, 0.26);
  background:
    radial-gradient(circle at 12% 40%, rgba(22, 121, 255, 0.28), transparent 32%),
    linear-gradient(180deg, rgba(9, 31, 67, 0.95), rgba(4, 16, 37, 0.95));
  margin-bottom: 12px;
}

.sub-page-header h2 {
  margin: 0 0 10px;
  font-size: 24px;
  color: #ecf6ff;
}

.sub-page-header p {
  margin: 0;
  color: rgba(220, 236, 255, 0.74);
  line-height: 1.6;
}

.sub-card-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.sub-card {
  min-height: 180px;
  padding: 18px;
}

.sub-icon {
  font-size: 32px;
  margin-bottom: 10px;
}

.sub-card h3 {
  margin: 0 0 8px;
  font-size: 17px;
}

.sub-card p {
  color: rgba(216, 233, 255, 0.68);
  line-height: 1.7;
  font-size: 13px;
}

.sub-card button {
  margin-top: 10px;
  height: 32px;
  padding: 0 16px;
  border-radius: 5px;
  border: 1px solid rgba(69, 151, 255, 0.42);
  background: rgba(17, 74, 155, 0.68);
  color: #e8f4ff;
  cursor: pointer;
}

.sub-table {
  margin-top: 12px;
  min-height: 260px;
}

@media (max-width: 1280px) {
  .top-meta {
    min-width: 260px;
    gap: 8px;
  }

  .page-title {
    font-size: 15px;
  }

  .work-area {
    grid-template-columns: 1fr;
    overflow: auto;
  }

  .right-rail {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }

  .main-layout {
    overflow: auto;
  }

  .bottom-grid,
  .summary-grid,
  .sub-card-grid {
    grid-template-columns: 1fr 1fr;
  }

  .video-grid {
    height: 260px;
  }
}
</style>