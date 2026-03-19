from pydantic import BaseModel

class RFIDScan(BaseModel):
    rfid_uid: str