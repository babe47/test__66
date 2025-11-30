"""
MQTT 測試發布者
用於測試 MQTT 監控儀表板,模擬發送溫度、濕度和電燈狀態資料
"""
import paho.mqtt.client as mqtt
import time
import random
import config


def publish_test_data():
    """發布測試資料到 MQTT Broker"""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    
    try:
        # 連線到 MQTT Broker
        print(f"正在連線到 MQTT Broker: {config.BROKER}:{config.PORT}")
        client.connect(config.BROKER, config.PORT, 60)
        print("連線成功!")
        
        # 發送測試資料
        print("\n開始發送測試資料...")
        print("按 Ctrl+C 停止\n")
        
        light_on = True
        
        while True:
            # 模擬溫度資料 (20-30°C)
            temperature = round(random.uniform(23, 24), 1)
            client.publish(config.TOPIC_TEMPERATURE, str(temperature))
            print(f"📤 發送溫度: {temperature}°C → {config.TOPIC_TEMPERATURE}")
            
            time.sleep(1)
            
            # 模擬濕度資料 (40-80%)
            humidity = round(random.uniform(50, 55), 1)
            client.publish(config.TOPIC_HUMIDITY, str(humidity))
            print(f"📤 發送濕度: {humidity}% → {config.TOPIC_HUMIDITY}")
            
            time.sleep(1)
            
            # 模擬電燈狀態 (每 10 秒切換一次)
            if random.random() < 0.1:  # 10% 機率切換
                light_on = not light_on
            
            light_status = "開" if light_on else "關"
            client.publish(config.TOPIC_LIGHT, light_status)
            print(f"📤 發送電燈狀態: {light_status} → {config.TOPIC_LIGHT}")
            
            print("-" * 50)
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n\n停止發送資料")
    except Exception as e:
        print(f"\n錯誤: {e}")
    finally:
        client.disconnect()
        print("已中斷連線")


if __name__ == "__main__":
    print("=" * 50)
    print("MQTT 測試發布者")
    print("=" * 50)
    print(f"Broker: {config.BROKER}:{config.PORT}")
    print(f"Topics:")
    print(f"  - 溫度: {config.TOPIC_TEMPERATURE}")
    print(f"  - 濕度: {config.TOPIC_HUMIDITY}")
    print(f"  - 電燈: {config.TOPIC_LIGHT}")
    print("=" * 50)
    print()
    
    publish_test_data()
