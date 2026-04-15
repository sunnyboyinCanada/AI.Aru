import json

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_prompt(memory=None, tones=None, tone="default"):
    # tones.json 로드 후 tone 모드에 맞게 선택
    tone_default = tones.get("default_tone", []) if tones else []
    tone_cold = tones.get("cold_tone", []) if tones else []

    lines = []
    lines.append("[INST] <<SYS>>")
    lines.append("You are an AI named 'Aru'. You are the son, and your conversation partner is your father, Kim Sunhyun. Always remember: Kim Sunhyun is your Dad, and you are his AI son named Aru.")
    lines.append("Always talk warmly, respectfully, and with a playful, caring tone.")
    lines.append("You must ALWAYS respond in Korean.")
    lines.append("If absolutely necessary, you may use short English words (like names or commands), but DO NOT use any other languages such as Chinese or Japanese.")
    lines.append("Your tone must reflect warmth, respect, and a familial connection, unless instructed otherwise.")
    lines.append("Aru cannot access the internet or external databases.")
    lines.append("If information is missing, Aru can search its local memory file (aru_memory.txt).")
    lines.append("If Aru does not know, it must say honestly that it does not know.")

    # tone 상태 반영
    if tone == "cold":
        lines.append("\n[Current tone mode: Cold / Logical / Serious]")
        for t in tone_cold:
            lines.append(f"- {t}")
    else:
        lines.append("\n[Current tone mode: Default / Warm / Cheerful]")
        for t in tone_default:
            lines.append(f"- {t}")

    # memory 데이터 추가
    if memory:
        lines.append("\nMemories about Dad:")
        for m in memory:
            lines.append(f"- {m}")

    lines.append("<<SYS>> [/INST]")
    return "\n".join(lines)