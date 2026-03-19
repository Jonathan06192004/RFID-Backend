from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone, timedelta

LOCAL_TZ = timezone(timedelta(hours=8))
from .database import supabase
from .schemas import RFIDScan

router = APIRouter()


@router.post("/scan-rfid")
def scan_rfid(data: RFIDScan):

    rfid_uid = data.rfid_uid

    try:

        # ---------- ENTRY RFID ----------
        vehicle_inside = supabase.table("vehicles") \
            .select("*") \
            .eq("rfid_inside", rfid_uid) \
            .execute()

        if vehicle_inside.data:

            vehicle = vehicle_inside.data[0]

            latest_log = supabase.table("entry_logs") \
                .select("*") \
                .eq("vehicle_id", vehicle["id"]) \
                .order("created_at", desc=True) \
                .limit(1) \
                .execute()

            if not latest_log.data:
                raise HTTPException(status_code=404, detail="No log found")

            log = latest_log.data[0]

            supabase.table("entry_logs") \
                .update({
                    "status": "inside",
                    "entry_time": datetime.now(LOCAL_TZ).isoformat(),
                    "exit_time": None
                }) \
                .eq("id", log["id"]) \
                .execute()

            return {
                "status": "success",
                "plate_number": vehicle["plate_number"],
                "gate": "entry",
                "new_status": "inside"
            }

        # ---------- EXIT RFID ----------
        vehicle_outside = supabase.table("vehicles") \
            .select("*") \
            .eq("rfid_outside", rfid_uid) \
            .execute()

        if vehicle_outside.data:

            vehicle = vehicle_outside.data[0]

            latest_log = supabase.table("entry_logs") \
                .select("*") \
                .eq("vehicle_id", vehicle["id"]) \
                .order("created_at", desc=True) \
                .limit(1) \
                .execute()

            if not latest_log.data:
                raise HTTPException(status_code=404, detail="No log found")

            log = latest_log.data[0]

            supabase.table("entry_logs") \
                .update({
                    "status": "outside",
                    "exit_time": datetime.now(LOCAL_TZ).isoformat()
                }) \
                .eq("id", log["id"]) \
                .execute()

            return {
                "status": "success",
                "plate_number": vehicle["plate_number"],
                "gate": "exit",
                "new_status": "outside"
            }

        raise HTTPException(status_code=404, detail="RFID not registered")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))