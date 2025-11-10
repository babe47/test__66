print("Hello, Python!") 

# BMI 計算程式

# 取得使用者輸入
height_cm = float(input("請輸入您的身高（公分）："))
weight_kg = float(input("請輸入您的體重（公斤）："))

# 將身高轉換為公尺
height_m = height_cm / 100

# 計算 BMI
bmi = weight_kg / (height_m ** 2)

# 顯示結果
print(f"您的 BMI 為：{bmi:.2f}")

# 判斷 BMI 所屬範圍
if bmi < 18.5:
    print("體重過輕")
elif 18.5 <= bmi < 24:
    print("正常範圍")
elif 24 <= bmi < 27:
    print("過重")
elif 27 <= bmi < 30:
    print("輕度肥胖")
elif 30 <= bmi < 35:
    print("中度肥胖")
else:
    print("重度肥胖")
