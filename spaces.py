import re

english_titles = [
    'Mr', 'Miss', 'Mrs', 'Ms', 'Master', 'Dr', 'Prof', 'Sir', 'Madam',
    'Captain', 'Colonel', 'Major', 'General'
]

thai_titles = [
    # Civilian titles
    'นาย', 'น.ส.', 'นาง', 'นางสาว', 'ดร.', 'ศ.', 'รศ.', 'ผศ.',
    'ด.ช.', 'ด.ญ.', 'เด็กชาย', 'เด็กหญิง',  # Children (under 15)
        
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

def _titles_alternation(titles):
    # Longest first so e.g. 'นางสาว' wins over 'นาง', 'Miss' over 'Mr'
    return "|".join(re.escape(t) for t in sorted(titles, key=len, reverse=True))

# Title may be joined to the name ("ด.ช.นาริน", "MasterNarin") or separated by space/dot.
# Thai also accepts any dotted abbreviation (e.g. ด.ช., น.ส., พล.ต.อ.) even if it's not in the list.
THAI_NAME_RE = re.compile(
    rf"^(?P<title>{_titles_alternation(thai_titles)}|(?:[ก-ฮ]{{1,3}}\.)+)?\s*"
    r"(?P<first>\S+)(?:\s+(?P<last>.+))?$"
)
ENGLISH_NAME_RE = re.compile(
    rf"^(?:(?P<title>{_titles_alternation(english_titles)})\.?\s*)?"
    r"(?P<first>\S+)(?:\s+(?P<last>.+))?$"
)

def _parse_name(fullname: str, pattern, lang: str):
    fullname = " ".join(fullname.split())
    match = pattern.match(fullname)
    if not match:
        return {
            f"title_{lang}": "",
            f"first_name_{lang}": fullname,
            f"last_name_{lang}": "",
            f"full_name_{lang}": fullname
        }
    title = match.group("title") or ""
    first = match.group("first")
    last = match.group("last") or ""
    return {
        f"title_{lang}": title,
        f"first_name_{lang}": first,
        f"last_name_{lang}": last,
        f"full_name_{lang}": " ".join(p for p in (title, first, last) if p)
    }

# Abbreviated titles returned in their full form
THAI_TITLE_EXPANSIONS = {
    'ด.ช.': 'เด็กชาย',
    'ด.ญ.': 'เด็กหญิง',
}

def parse_thai_name(fullname_th: str):
    result = _parse_name(fullname_th, THAI_NAME_RE, "th")
    title = THAI_TITLE_EXPANSIONS.get(result["title_th"])
    if title:
        result["title_th"] = title
        result["full_name_th"] = " ".join(
            p for p in (title, result["first_name_th"], result["last_name_th"]) if p
        )
    return result

def parse_english_name(fullname_en: str):
    return _parse_name(fullname_en, ENGLISH_NAME_RE, "en")

