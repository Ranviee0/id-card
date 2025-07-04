""" Python version 3.11.5
    ไฟล์หลัก อ่านข้อมูลบัตรประชาชน ThaiCIDHelper 
    วรเพชร  เรืองพรวิสุทธิ์
    09/01/2567
"""
from fastapi.middleware.cors import CORSMiddleware
import sys
from ThaiCIDHelper  import *
from DataThaiCID    import *
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        raise HTTPException(status_code=404, detail="No card reader found.")

    connection, status = reader.connectReader(0)

    if status and reader.cardReader is not None:
        try:
            data = reader.readData(readPhoto=False)
            return data["jsonData"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Reading failed: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail=f"No card detected or reader connection failed: {reader.lastError}")


@app.get("/read-photo")
def read_citizen_photo():
    reader = ThaiCIDHelper()

    if not reader.cardReaderList:
        raise HTTPException(status_code=404, detail="No card reader found.")

    connection, status = reader.connectReader(0)

    if status and reader.cardReader is not None:
        try:
            # SELECT + TYPE (same as in readData)
            reader.cardReader.transmit(reader.apduSELECT + reader.apduTHCard)

            photo_bytes = []
            for photo_data in APDU_PHOTO:
                apdu = searchAPDUPhoto(photo_data['key'])
                photo_bytes += reader.getPhoto(apdu)

            image_bytes = bytes(photo_bytes)
            return StreamingResponse(io.BytesIO(image_bytes), media_type="image/jpeg")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Photo reading failed: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail=f"No card detected or reader connection failed: {reader.lastError}")