export const riskTypeMap = {
  vehicle_person_conflict: '车人共现风险',
  weak_light_small_object: '弱光小目标风险',
  glare_interference: '强光干扰风险',
  blind_spot_approach: '盲区接近风险',
  danger_zone_intrusion: '危险区域入侵'
}

export const mockEvents = [
  { id: 'EVT20250519-00032', time: '22:35:48', risk_type: 'vehicle_person_conflict', risk_name: '车人共现风险', level: 'high', level_name: '高风险', device_id: 'AIoT-Edge-001', location: '城市道路-主干道-东侧', targets: ['person', 'car'], confidence: 0.92, action: ['platform_warning', 'snapshot', 'mqtt_alarm'], snapshot: '/mock/snapshot-1.jpg' },
  { id: 'EVT20250519-00031', time: '22:34:15', risk_type: 'glare_interference', risk_name: '强光干扰风险', level: 'medium', level_name: '中风险', device_id: 'AIoT-Edge-001', location: '城市道路', targets: ['car'], confidence: 0.81, action: ['record', 'robust_detection'], snapshot: '/mock/snapshot-2.jpg' },
  { id: 'EVT20250519-00030', time: '22:32:56', risk_type: 'weak_light_small_object', risk_name: '弱光小目标风险', level: 'medium', level_name: '中风险', device_id: 'AIoT-Edge-002', location: '乡村道路', targets: ['person'], confidence: 0.76, action: ['enhancement_on', 'platform_warning'], snapshot: '/mock/snapshot-3.jpg' },
  { id: 'EVT20250519-00029', time: '22:30:21', risk_type: 'blind_spot_approach', risk_name: '盲区接近风险', level: 'high', level_name: '高风险', device_id: 'AIoT-Edge-001', location: '地下车库', targets: ['car'], confidence: 0.88, action: ['buzzer', 'warning_light'], snapshot: '/mock/snapshot-4.jpg' },
  { id: 'EVT20250519-00028', time: '22:28:03', risk_type: 'danger_zone_intrusion', risk_name: '危险区域入侵', level: 'high', level_name: '高风险', device_id: 'AIoT-Edge-003', location: '施工通道', targets: ['person'], confidence: 0.90, action: ['database_record', 'mqtt_alarm'], snapshot: '/mock/snapshot-5.jpg' }
]

export const mockDevices = [
  { name: '摄像头连接', status: '正常', detail: 'AIoT-Cam-01', online: true },
  { name: '网络状态', status: '正常', detail: '延迟 28ms', online: true },
  { name: '边缘计算模块', status: '正常', detail: 'AIoT-Edge-001', online: true },
  { name: '存储状态', status: '正常', detail: '256GB / 512GB', online: true },
  { name: 'MySQL 事件库', status: '已连接', detail: 'events/logs/devices', online: true },
  { name: '报警设备', status: '正常', detail: '蜂鸣器｜警示灯', online: true },
  { name: '补光灯控制', status: '自动', detail: '亮度 60%', online: true },
  { name: '语音播报', status: '开启', detail: 'TTS module', online: true }
]

export const mockStats = {
  total: 32,
  riskDistribution: [
    { name: '车人共现风险', value: 8 },
    { name: '强光干扰风险', value: 7 },
    { name: '弱光小目标风险', value: 6 },
    { name: '盲区接近风险', value: 6 },
    { name: '危险区域入侵', value: 5 }
  ],
  levelDistribution: [
    { name: '高风险', value: 12 },
    { name: '中风险', value: 14 },
    { name: '低风险', value: 6 }
  ],
  trend: {
    x: ['00:00','02:00','04:00','06:00','08:00','10:00','12:00','14:00','16:00','18:00','20:00','22:00','24:00'],
    high: [0,1,2,4,6,8,7,10,12,11,14,16,13],
    medium: [0,0,1,1,2,4,5,5,7,8,7,10,9],
    low: [0,0,0,1,1,2,2,3,3,4,5,6,5]
  }
}

export const mockTimeline = [
  { start: '00:00', title: '正常行驶', level: '低风险', type: 'low' },
  { start: '00:15', title: '弱光小目标风险', level: '中风险', type: 'medium' },
  { start: '00:35', title: '强光干扰风险', level: '中风险', type: 'medium' },
  { start: '00:55', title: '盲区接近风险', level: '高风险', type: 'high' },
  { start: '01:20', title: '车人共现风险', level: '高风险', type: 'high' },
  { start: '01:45', title: '危险区域入侵', level: '红色告警', type: 'high' },
  { start: '02:10', title: '测试结束', level: '', type: 'end' }
]
