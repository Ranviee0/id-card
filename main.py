""" Python version 3.11.5
    ไฟล์หลัก อ่านข้อมูลบัตรประชาชน ThaiCIDHelper 
    วรเพชร  เรืองพรวิสุทธิ์
    09/01/2567
"""

import sys
from ThaiCIDHelper  import *
from DataThaiCID    import *

# สร้าง Instance Class ThaiCIDHelper
reader = ThaiCIDHelper(APDU_SELECT,APDU_THAI_CARD)

# Connect SMC
connection, status = reader.connectReader(0)

if status:
    data = reader.readData()
    print("📄 Thai Description Text:")
    print(data["thaiText"])
    
    print("\n🧾 JSON Text:")
    print(data["jsonText"])
    
    print("\n🔑 JSON as Dictionary:")
    print(data["jsonData"])  # You can also access specific fields: data["jsonData"]["fname"]
else:
    print(f'❌ Error: {reader.lastError}')
    sys.exit(1)