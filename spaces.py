english_titles = [
    'Mr', 'Miss', 'Mrs', 'Ms', 'Dr', 'Prof', 'Sir', 'Madam',
    'Captain', 'Colonel', 'Major', 'General'
]

thai_titles = [
    # Civilian titles
    'นาย', 'น.ส.', 'นาง', 'นางสาว', 'ดร.', 'ศ.', 'รศ.', 'ผศ.',
        
    # Police ranks (from highest to lowest)
    'พล.ต.อ.', 'พล.ต.ท.', 'พล.ต.ต.',  # Police Generals
    'พ.ต.อ.', 'พ.ต.ท.', 'พ.ต.ต.',     # Police Field Officers
    'ร.ต.อ.', 'ร.ต.ท.', 'ร.ต.ต.',     # Police Company Officers
    'ด.ต.', 'จ.ส.ต.', 'ส.ต.อ.', 'ส.ต.ท.', 'ส.ต.ต.',  # Police NCOs
        
    # Army ranks (from highest to lowest)
    'พล.อ.', 'พล.ท.', 'พล.ต.',        # Army Generals
    'พ.อ.', 'พ.ท.', 'พ.ต.',           # Army Field Officers
    'ร.อ.', 'ร.ท.', 'ร.ต.',           # Army Company Officers
    'ส.อ.', 'ส.ท.', 'ส.ต.',           # Army NCOs
    'พล.', 'ทพ.',                     # Army Enlisted
        
    # Navy ranks
    'พล.ร.อ.', 'พล.ร.ท.', 'พล.ร.ต.',  # Navy Admirals
    'น.อ.', 'น.ท.', 'น.ต.',           # Navy Field Officers
    'ร.น.', 'ส.น.', 'พ.น.',           # Navy Company Officers & NCOs
        
    # Air Force ranks
    'พล.อ.อ.', 'พล.อ.ท.', 'พล.อ.ต.',  # Air Force Generals
    'ก.อ.', 'ผ.บ.', 'ส.บ.',          # Air Force Officers
    'น.บ.', 'ส.อ.อ.',                 # Air Force NCOs
        
    # Buddhist monk titles
    'สมเด็จ', 'สมเด็จพระ',             # Supreme Patriarch level
    'หลวงปู่', 'หลวงตา', 'หลวงพ่อ',    # Senior monks
    'พระครู', 'พระอธิการ', 'พระปลัด',   # Administrative monks
    'พระราชาคณะ', 'พระธรรมวิสุทธิ์',    # Royal council monks
    'พระ', 'เณร',                     # General monk titles
        
    # Academic and professional titles
    'ศาสตราจารย์', 'รองศาสตราจารย์', 'ผู้ช่วยศาสตราจารย์',
    'อาจารย์', 'แพทย์', 'ทันตแพทย์', 'เภสัชกร',
    'วิศวกร', 'สถาปนิก', 'นักกฎหมาย',
        
    # Government positions
    'นายกรัฐมนตรี', 'รัฐมนตรี', 'ปลัดกระทรวง',
    'อธิบดี', 'ผู้อำนวยการ', 'หัวหน้า'
]

def parse_thai_name(fullname_th: str):
    for title in sorted(thai_titles, key=len, reverse=True):
        if fullname_th.startswith(title):
            name_without_title = fullname_th[len(title):].strip()
            parts = name_without_title.split(maxsplit=1)
            if len(parts) == 2:
                return {
                    "title_th": title,
                    "first_name_th": parts[0],
                    "last_name_th": parts[1],
                    "full_name_th": f"{title} {parts[0]} {parts[1]}"
                }
            else:
                return {
                    "title_th": title,
                    "first_name_th": name_without_title,
                    "last_name_th": "",
                    "full_name_th": f"{title} {name_without_title}"
                }
    return {
        "title_th": "",
        "first_name_th": fullname_th,
        "last_name_th": "",
        "full_name_th": fullname_th
    }

def parse_english_name(fullname_en: str):
    for title in sorted(english_titles, key=len, reverse=True):
        # Handle with dot, space, or joined directly (e.g., "MissSupharom")
        if fullname_en.startswith(title + ".") or fullname_en.startswith(title + " "):
            name_without_title = fullname_en[len(title):].strip(" .")
        elif fullname_en.startswith(title):
            name_without_title = fullname_en[len(title):].strip()
        else:
            continue

        parts = name_without_title.split(maxsplit=1)
        if len(parts) == 2:
            return {
                "title_en": title,
                "first_name_en": parts[0],
                "last_name_en": parts[1],
                "full_name_en": f"{title} {parts[0]} {parts[1]}"
            }
        else:
            return {
                "title_en": title,
                "first_name_en": name_without_title,
                "last_name_en": "",
                "full_name_en": f"{title} {name_without_title}"
            }

    # fallback
    return {
        "title_en": "",
        "first_name_en": fullname_en,
        "last_name_en": "",
        "full_name_en": fullname_en
    }

