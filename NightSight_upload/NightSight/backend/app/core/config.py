"""集中配置，从环境变量 / .env 读取。"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # 数据库
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "nightsight"
    DB_PASSWORD: str = "change_me"
    DB_NAME: str = "nightsight"

    # 推理
    INFER_MODE: str = "realtime"        # realtime | replay
    MODEL_NAME: str = "EMV-YOLO"        # EMV-YOLO | TGE-YOLO
    WEIGHTS_PATH: str = "weights/emv_yolo.pt"
    DEVICE: str = "cuda"
    CONF_THRES: float = 0.35
    IOU_THRES: float = 0.45
    INPUT_SIZE: int = 608

    # MQTT / ESP32
    MQTT_ENABLED: bool = False
    MQTT_HOST: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_TOPIC_CMD: str = "nightsight/actuator/cmd"

    # replay 源
    REPLAY_VIDEO: str = "data/event_stream_v1.mp4"
    REPLAY_LABELS: str = "data/event_labels.json"

    # 可选：直接给完整连接串，覆盖上面的 MySQL 拼接
    # 演示无 MySQL 时设 DB_URL=sqlite:///./nightsight.db 即可零配置跑起来
    DB_URL: str | None = None

    @property
    def db_url(self) -> str:
        if self.DB_URL:
            return self.DB_URL
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        )


settings = Settings()
