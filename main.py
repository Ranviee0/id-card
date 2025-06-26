""" Python version 3.11.5
    ไฟล์หลัก อ่านข้อมูลบัตรประชาชน ThaiCIDHelper 
    วรเพชร  เรืองพรวิสุทธิ์
    09/01/2567
"""

import sys
from ThaiCIDHelper  import *
from DataThaiCID    import *
from fastapi import FastAPI

app = FastAPI()

# สร้าง Instance Class ThaiCIDHelper
reader = ThaiCIDHelper(APDU_SELECT,APDU_THAI_CARD)

# Connect SMC
connection, status = reader.connectReader(0)

# if status:
#     data = reader.readData()
#     print("📄 Thai Description Text:")
#     print(data["thaiText"])
    
#     print("\n🧾 JSON Text:")
#     print(data["jsonText"])
    
#     print("\n🔑 JSON as Dictionary:")
#     print(data["jsonData"])  # You can also access specific fields: data["jsonData"]["fname"]
# else:
#     print(f'❌ Error: {reader.lastError}')
#     sys.exit(1)


@app.get("/read-cid")
def read_citizen_data():
    reader = ThaiCIDHelper()

    if not reader.cardReaderList:
        return {"error": "No card reader found."}

    connection, status = reader.connectReader(0)

    if status and reader.cardReader is not None:
        try:
            data = reader.readData(readPhoto=False)
            return data["jsonData"]
        except Exception as e:
            return {"error": f"Reading failed: {str(e)}"}
    else:
        return {"error": f"Connection failed: {reader.lastError}"}