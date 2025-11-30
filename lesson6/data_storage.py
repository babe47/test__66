"""
資料儲存模組
負責將 MQTT 接收到的資料儲存為 Excel 檔案
"""
import pandas as pd
from datetime import datetime
import os
import config


class DataStorage:
    def __init__(self, filename=None):
        """
        初始化資料儲存
        
        Args:
            filename: Excel 檔案名稱,預設使用 config 中的設定
        """
        self.filename = filename or config.EXCEL_FILE
        self.data = []
        
        # 如果檔案已存在,載入現有資料
        if os.path.exists(self.filename):
            try:
                df = pd.read_excel(self.filename)
                self.data = df.to_dict('records')
                print(f"已載入現有資料,共 {len(self.data)} 筆")
            except Exception as e:
                print(f"載入現有資料失敗: {e}")
    
    def add_record(self, topic, value, timestamp):
        """
        新增一筆記錄
        
        Args:
            topic: MQTT topic
            value: 資料值
            timestamp: 時間戳記
        """
        record = {
            '時間戳記': timestamp,
            '資料類型': topic,
            '數值': value
        }
        self.data.append(record)
    
    def save_to_excel(self):
        """將資料儲存到 Excel 檔案"""
        try:
            if not self.data:
                print("沒有資料可儲存")
                return False
            
            df = pd.DataFrame(self.data)
            df.to_excel(self.filename, index=False, engine='openpyxl')
            print(f"資料已儲存到 {self.filename},共 {len(self.data)} 筆")
            return True
        except Exception as e:
            print(f"儲存資料失敗: {e}")
            return False
    
    def get_data_by_topic(self, topic):
        """
        取得特定 topic 的所有資料
        
        Args:
            topic: MQTT topic
            
        Returns:
            DataFrame 包含該 topic 的所有資料
        """
        df = pd.DataFrame(self.data)
        if df.empty:
            return pd.DataFrame(columns=['時間戳記', '資料類型', '數值'])
        
        filtered = df[df['資料類型'] == topic]
        return filtered
    
    def get_recent_value(self, topic):
        """
        取得特定 topic 的最新數值
        
        Args:
            topic: MQTT topic
            
        Returns:
            最新的數值,如果沒有資料則返回 None
        """
        df = self.get_data_by_topic(topic)
        if df.empty:
            return None
        return df.iloc[-1]['數值']
