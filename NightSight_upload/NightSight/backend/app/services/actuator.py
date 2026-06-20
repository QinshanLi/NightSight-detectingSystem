"""
声光设备联动。当前默认软件模拟（MQTT_ENABLED=false）：
只记日志、回传状态，不真正驱动硬件——满足“保留接口”要求。
把 MQTT_ENABLED 设 true 即真发指令到 ESP32，无需改其它代码。
"""
import json
from app.core.config import settings

ACTUATOR_NAMES = {
    "led": "LED 警示灯", "buzzer": "蜂鸣器", "voice": "语音广播",
    "fill_light": "自动补光灯", "popup": "前端弹窗", "enhance": "自适应增强", "log": "事件记录",
}


class Actuator:
    def __init__(self):
        self.enabled = settings.MQTT_ENABLED
        self._client = None
        if self.enabled:
            self._connect()

    def _connect(self):
        import paho.mqtt.client as mqtt
        self._client = mqtt.Client()
        self._client.connect(settings.MQTT_HOST, settings.MQTT_PORT, 60)
        self._client.loop_start()

    def trigger(self, actuators: list[str], event_id: int | None = None):
        """对一组联动动作下发指令（或模拟）。返回日志条目列表。"""
        logs = []
        for a in actuators:
            cmd = "flash" if a == "led" else "on"
            if self.enabled and self._client and a in ("led", "buzzer", "voice", "fill_light"):
                payload = json.dumps({"actuator": a, "command": cmd, "event_id": event_id})
                self._client.publish(settings.MQTT_TOPIC_CMD, payload)
                simulated = False
            else:
                simulated = True   # 软件模拟
            logs.append({
                "actuator": a, "name": ACTUATOR_NAMES.get(a, a),
                "command": cmd, "simulated": simulated, "result": "已执行",
            })
        return logs


actuator = Actuator()
