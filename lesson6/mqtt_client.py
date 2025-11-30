"""
MQTT 客戶端模組
負責連線到 MQTT Broker 並訂閱指定的 topics
"""
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import config


class MQTTClient:
    def __init__(self, on_message_callback):
        """
        初始化 MQTT 客戶端
        
        Args:
            on_message_callback: 接收到訊息時的回調函數
        """
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.on_message_callback = on_message_callback
        
        # 設定回調函數
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
    def _on_connect(self, client, userdata, flags, rc, properties):
        """當連線到 MQTT Broker 時的回調函數"""
        if rc == 0:
            print(f"成功連線到 MQTT Broker: {config.BROKER}:{config.PORT}")
            # 訂閱所有 topics
            self.client.subscribe(config.TOPIC_TEMPERATURE)
            self.client.subscribe(config.TOPIC_HUMIDITY)
            self.client.subscribe(config.TOPIC_LIGHT)
            print(f"已訂閱 topics: {config.TOPIC_TEMPERATURE}, {config.TOPIC_HUMIDITY}, {config.TOPIC_LIGHT}")
        else:
            print(f"連線失敗,錯誤碼: {rc}")
    
    def _on_message(self, client, userdata, msg):
        """當接收到 MQTT 訊息時的回調函數"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            timestamp = datetime.now()
            
            # 嘗試解析 JSON,如果失敗則使用原始字串
            try:
                value = json.loads(payload)
            except json.JSONDecodeError:
                value = payload
            
            # 呼叫外部回調函數
            if self.on_message_callback:
                self.on_message_callback(topic, value, timestamp)
                
        except Exception as e:
            print(f"處理訊息時發生錯誤: {e}")
    
    def connect(self):
        """連線到 MQTT Broker"""
        try:
            self.client.connect(config.BROKER, config.PORT, 60)
            return True
        except Exception as e:
            print(f"連線失敗: {e}")
            return False
    
    def start_loop(self):
        """開始 MQTT 客戶端的背景執行緒"""
        self.client.loop_start()
    
    def stop_loop(self):
        """停止 MQTT 客戶端的背景執行緒"""
        self.client.loop_stop()
    
    def disconnect(self):
        """中斷與 MQTT Broker 的連線"""
        self.client.disconnect()
