import re

def parse_thai_address(address: str):
    result = {
        "address": "",
        "subdistrict": "",
        "district": "",
        "province": "",
        "is_bangkok": False
    }

    # Pattern to split main address and location
    # Example: 292 ซอยพุทธมณฑลสาย6ซอย11 แขวงบางไผ่ เขตบางแค กรุงเทพมหานคร
    # or: 208/1 ถนนรอบเมือง ตำบลหมากแข้ง อำเภอเมือง จ.อุดรธานี
    pattern = "(.*?)\s+(?:แขวง|ตำบล)(\S+)\s+(เขต|อำเภอ)(\S+)\s+(.*)"  # Full pattern

    match = re.match(pattern, address)
    if match:
        result["address"] = match.group(1).strip()
        result["subdistrict"] = f"{match.group(2).strip()}"
        district_prefix = match.group(3).strip() if match.group(3) == "เขต" else ""
        result["district"] = f"{district_prefix}{match.group(4).strip()}"
        province_raw = match.group(5).strip()

        if province_raw == "กรุงเทพมหานคร":
            result["province"] = "กรุงเทพมหานคร"
            result["is_bangkok"] = True
        else:
            province = province_raw.replace("จังหวัด", "").strip()
            result["province"] = province
            result["is_bangkok"] = False
    else:
        result["address"] = address  # fallback: no pattern matched

    return result