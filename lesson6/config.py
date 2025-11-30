# MQTT 監控儀表板設定檔

# MQTT Broker 連線設定
BROKER = "localhost"
PORT = 1883

# MQTT Topics
TOPIC_TEMPERATURE = "客廳/溫度"
TOPIC_HUMIDITY = "客廳/濕度"
TOPIC_LIGHT = "客廳/電燈"

# Excel 儲存設定
EXCEL_FILE = "mqtt_data.xlsx"

# 圖表顯示設定
MAX_DATA_POINTS = 100  # 圖表最多顯示的資料點數量
UPDATE_INTERVAL = 1  # Streamlit 自動更新間隔(秒)
