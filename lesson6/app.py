"""
MQTT 監控儀表板 - Streamlit 應用程式
顯示電燈狀態、溫度和濕度的即時監控介面
"""
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import time
import config
from mqtt_client import MQTTClient
from data_storage import DataStorage


# 頁面設定
st.set_page_config(
    page_title="MQTT 監控儀表板",
    page_icon="🏠",
    layout="wide"
)


@st.cache_resource
def get_data_storage():
    """獲取資料儲存實例(使用 Streamlit 快取確保單例)"""
    print("[初始化] 建立資料儲存實例")
    return DataStorage()


@st.cache_resource
def get_mqtt_client():
    """獲取 MQTT 客戶端實例(使用 Streamlit 快取確保單例)"""
    print("[初始化] 建立 MQTT 客戶端實例")
    
    # 獲取資料儲存實例
    storage = get_data_storage()
    
    def on_message(topic, value, timestamp):
        """MQTT 訊息接收回調函數"""
        storage.add_record(topic, value, timestamp)
        print(f"[MQTT→儲存] {topic} = {value} (總筆數: {len(storage.data)})")
        
        # 每 10 筆資料自動儲存一次
        if len(storage.data) % 10 == 0:
            storage.save_to_excel()
    
    client = MQTTClient(on_message)
    if client.connect():
        client.start_loop()
        print("[MQTT] 連線成功並開始監聽")
        return client
    else:
        print("[MQTT] 連線失敗")
        return None


def create_line_chart(data, title, y_label, color):
    """建立折線圖"""
    if data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="等待資料中...",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20, color="gray")
        )
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data['時間戳記'],
            y=data['數值'],
            mode='lines+markers',
            name=title,
            line=dict(color=color, width=2),
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title="時間",
        yaxis_title=y_label,
        height=400,
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig


# 獲取單例實例
mqtt_client = get_mqtt_client()
data_storage = get_data_storage()

# 主介面
st.title("🏠 MQTT 監控儀表板")
st.markdown("---")

# 連線狀態
col_status1, col_status2 = st.columns([3, 1])
with col_status1:
    if mqtt_client is not None:
        st.success(f"✅ 已連線到 MQTT Broker: {config.BROKER}:{config.PORT}")
    else:
        st.error(f"❌ 無法連線到 MQTT Broker: {config.BROKER}:{config.PORT}")

with col_status2:
    if st.button("🔄 重新載入"):
        st.rerun()

st.markdown("---")

# 第一排:電燈狀態
st.subheader("💡 電燈狀態")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    light_status = data_storage.get_recent_value(config.TOPIC_LIGHT)
    if light_status is None:
        st.info("等待電燈狀態資料...")
    elif str(light_status).lower() in ['1', 'on', 'true', '開']:
        st.success("### 🟢 電燈已開啟")
    else:
        st.warning("### 🔴 電燈已關閉")

st.markdown("---")

# 第二排:溫度和濕度
col_temp, col_humid = st.columns(2)

with col_temp:
    st.subheader("🌡️ 客廳溫度")
    
    # 顯示當前溫度
    current_temp = data_storage.get_recent_value(config.TOPIC_TEMPERATURE)
    if current_temp is not None:
        st.metric(label="當前溫度", value=f"{current_temp} °C")
    else:
        st.info("等待溫度資料...")
    
    # 溫度圖表
    temp_data = data_storage.get_data_by_topic(config.TOPIC_TEMPERATURE)
    if not temp_data.empty and len(temp_data) > config.MAX_DATA_POINTS:
        temp_data = temp_data.tail(config.MAX_DATA_POINTS)
    
    temp_chart = create_line_chart(temp_data, "溫度趨勢", "溫度 (°C)", "#FF6B6B")
    st.plotly_chart(temp_chart, width='stretch')

with col_humid:
    st.subheader("💧 客廳濕度")
    
    # 顯示當前濕度
    current_humid = data_storage.get_recent_value(config.TOPIC_HUMIDITY)
    if current_humid is not None:
        st.metric(label="當前濕度", value=f"{current_humid} %")
    else:
        st.info("等待濕度資料...")
    
    # 濕度圖表
    humid_data = data_storage.get_data_by_topic(config.TOPIC_HUMIDITY)
    if not humid_data.empty and len(humid_data) > config.MAX_DATA_POINTS:
        humid_data = humid_data.tail(config.MAX_DATA_POINTS)
    
    humid_chart = create_line_chart(humid_data, "濕度趨勢", "濕度 (%)", "#4ECDC4")
    st.plotly_chart(humid_chart, width='stretch')

st.markdown("---")

# 資料統計
st.subheader("📊 資料統計")
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    total_records = len(data_storage.data)
    st.metric(label="總資料筆數", value=total_records)

with col_stat2:
    st.metric(label="Excel 檔案", value=config.EXCEL_FILE)

with col_stat3:
    if total_records > 0:
        last_record_time = data_storage.data[-1]['時間戳記']
        if isinstance(last_record_time, str):
            last_time_str = last_record_time
        else:
            last_time_str = last_record_time.strftime("%H:%M:%S")
        st.metric(label="最後更新", value=last_time_str)
    else:
        st.metric(label="最後更新", value="--")

with col_stat4:
    if st.button("💾 立即儲存"):
        if data_storage.save_to_excel():
            st.success("資料已儲存!")

# 自動重新整理
time.sleep(config.UPDATE_INTERVAL)
st.rerun()
