"""
知识库生成脚本 - 从 Excel 和 PDF markdown 中提取结构化规则数据

用法: python scripts/generate_knowledge.py

该脚本分两部分：
1. 从 Excel 直接提取结构化数据（武技、术法、专长等列表）
2. 清洗 PDF 规则书文本，提取建卡流程和规则关联

输出到 data/knowledge/ 目录下的 JSON 文件。
"""

import json
import re
import sys
from pathlib import Path

import openpyxl

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ORIGIN_DATA = PROJECT_ROOT / "originData"
MARKDOWN_DIR = PROJECT_ROOT / "data" / "markdown"
OUTPUT_DIR = PROJECT_ROOT / "data" / "knowledge"

EXCEL_PATH = ORIGIN_DATA / "狩魂者空白卡正式版V1.4.xlsx"


def load_workbook():
    return openpyxl.load_workbook(str(EXCEL_PATH), data_only=True)


def extract_attributes(wb) -> dict:
    levels = {
        "E": {
            "value": 1, "strength": 0,
            "physique": '习得基础武技"常规攻击"和基础术法"灵迹"，从基础术法"凝爆"和"超感"中选择一个习得',
            "wisdom": "-",
            "spirit": "-",
        },
        "D": {
            "value": 2, "strength": 1,
            "physique": "可以学习普通武技，习得1项自选武技",
            "wisdom": "可以学习普通术法，习得2项自选术法，获得1点技能点",
            "spirit": "获得1项灵能力专精",
        },
        "C": {
            "value": 3, "strength": 1,
            "physique": "习得1项自选武技",
            "wisdom": "习得2项自选术法，获得1点技能点",
            "spirit": "提前获得灵魂武器",
        },
        "B": {
            "value": 4, "strength": 2,
            "physique": "-",
            "wisdom": "获得1点技能点",
            "spirit": "-",
        },
        "A": {
            "value": 5, "strength": 2,
            "physique": "习得1项自选武技",
            "wisdom": "习得2项自选术法，获得1点技能点",
            "spirit": "觉醒额外灵能印记",
        },
        "S": {
            "value": 6, "strength": 3,
            "physique": "-",
            "wisdom": "获得1点技能点",
            "spirit": "-",
        },
        "SS": {
            "value": 7, "strength": 3,
            "physique": "可以学习秘传武技，习得1项自选武技",
            "wisdom": "可以学习秘传术法，习得2项自选术法，获得1点技能点",
            "spirit": "创造新的灵能力标签",
        },
        "SSS": {
            "value": 8, "strength": 4,
            "physique": "-",
            "wisdom": "获得1点技能点",
            "spirit": "-",
        },
        "SSS+": {
            "value": 9, "strength": 4,
            "physique": "习得1项自选武技",
            "wisdom": "习得2项自选术法，获得1点技能点",
            "spirit": "获得1项灵能力专精",
        },
    }

    spirit_growth = [
        {"level": 10, "reward": "获得一项自选专长"},
        {"level": 12, "reward": "获得你的灵魂武器"},
        {"level": 14, "reward": "习得一挡狩魂绝技"},
        {"level": 16, "reward": "获得另一项新的自选专长"},
        {"level": 18, "reward": "习得二挡狩魂绝技"},
    ]

    return {
        "levels": levels,
        "spirit_growth": spirit_growth,
        "attributes": ["体魄", "智慧", "心魂"],
        "derived_stats": {
            "体魄": {"affects": ["武技强度", "生命值上限", "可学武技数量"]},
            "智慧": {"affects": ["术法强度", "可学术法数量", "技能点"]},
            "心魂": {"affects": ["灵能力强度", "灵能印记数量", "灵能力专精"]},
        },
    }


def extract_skills() -> dict:
    skills = [
        {"name": "运动", "attribute": "体魄"},
        {"name": "操作", "attribute": "体魄"},
        {"name": "隐秘", "attribute": "智慧"},
        {"name": "调查", "attribute": "智慧"},
        {"name": "洞察", "attribute": "心魂"},
        {"name": "说服", "attribute": "心魂"},
        {"name": "狩魂学识", "attribute": "特殊"},
    ]
    return {
        "skills": skills,
        "rules": {
            "total_points": "由智慧等级决定",
            "max_per_skill": 5,
            "attribute_bonus": "由对应属性等级的属性值决定",
        },
    }


def extract_martial_arts(wb) -> list:
    ws = wb["武技"]
    arts = []
    for row in ws.iter_rows(min_row=3, values_only=True):
        name = row[1]
        if not name or name == "名称" or str(name).strip() == "":
            continue
        cost = row[2] if row[2] else "无"
        target = row[3] if row[3] else ""
        assist = str(row[4]) == "☑" if row[4] else False
        secret = str(row[5]) == "☑" if row[5] else False
        effect = row[6] if row[6] else ""
        flavor = row[7] if row[7] else ""
        arts.append({
            "name": str(name).strip(),
            "cost": str(cost).strip(),
            "target": str(target).strip(),
            "assist": assist,
            "secret": secret,
            "effect": str(effect).strip(),
            "flavor": str(flavor).strip(),
        })
    return arts


def extract_spells(wb) -> list:
    ws = wb["术法"]
    spells = []
    for row in ws.iter_rows(min_row=3, values_only=True):
        name = row[1]
        if not name or name == "名称" or str(name).strip() == "":
            continue
        cost = row[2] if row[2] else "无"
        target = row[3] if row[3] else ""
        category = row[4] if row[4] else ""
        secret = str(row[5]) == "☑" if row[5] else False
        spell_type = row[6] if row[6] else ""
        effect = row[7] if row[7] else ""
        flavor = row[8] if row[8] else ""
        spells.append({
            "name": str(name).strip(),
            "cost": str(cost).strip(),
            "target": str(target).strip(),
            "category": str(category).strip(),
            "secret": secret,
            "type": str(spell_type).strip(),
            "effect": str(effect).strip(),
            "flavor": str(flavor).strip(),
        })
    return spells


def extract_spirit_marks(wb) -> list:
    ws = wb["灵能印记"]
    marks = []
    for row in ws.iter_rows(min_row=3, values_only=True):
        mark_type = row[1]
        desc = row[2]
        if not mark_type or str(mark_type).strip() == "" or mark_type == "印记\n类型":
            continue
        marks.append({
            "type": str(mark_type).strip(),
            "description": str(desc).strip() if desc else "",
        })
    return marks


def extract_feats(wb) -> list:
    ws = wb["专长"]
    feats = []
    for row in ws.iter_rows(min_row=3, values_only=True):
        name = row[1]
        desc = row[2]
        if not name or name == "名称" or str(name).strip() == "":
            continue
        feats.append({
            "name": str(name).strip(),
            "description": str(desc).strip() if desc else "",
        })
    return feats


def extract_ultimates(wb) -> list:
    ws = wb["绝技"]
    ultimates = []
    for row in ws.iter_rows(min_row=3, values_only=True):
        name = row[1]
        if not name or name == "绝技类型" or str(name).strip() == "":
            continue
        soul = row[2] if row[2] else ""
        domain = row[3] if row[3] else ""
        desc = row[4] if row[4] else ""
        effect = row[5] if row[5] else ""
        tier_raw = row[6] if row[6] else ""
        tier = "一挡" if "一" in str(tier_raw) else "二挡" if "二" in str(tier_raw) else ""
        ultimates.append({
            "name": str(name).strip(),
            "soul": str(soul).strip(),
            "domain": str(domain).strip(),
            "description": str(desc).strip(),
            "effect": str(effect).strip(),
            "tier": tier,
        })
    return ultimates


def extract_stylish_moves(wb) -> dict:
    ws = wb["时髦动作"]
    styles = {}
    current_style = None

    for row in ws.iter_rows(min_row=3, values_only=True):
        style_name = row[1]
        cost = row[2]
        action = row[3]

        if style_name and str(style_name).strip() and str(style_name).strip() != "时髦风格":
            current_style = str(style_name).strip()
            if current_style not in styles:
                styles[current_style] = []

        if current_style and cost and action:
            styles[current_style].append({
                "cost": str(cost).strip(),
                "action": str(action).strip(),
            })

    return styles


def extract_effects(wb) -> list:
    ws = wb["通用效果"]
    effects = []
    for row in ws.iter_rows(min_row=3, values_only=True):
        name = row[1]
        desc = row[2]
        polarity = row[3]
        duration = row[4]
        if not name or name == "效果名称" or str(name).strip() == "":
            continue
        effects.append({
            "name": str(name).strip(),
            "description": str(desc).strip() if desc else "",
            "polarity": str(polarity).strip() if polarity else "",
            "duration": str(duration).strip() if duration else "",
        })
    return effects


def extract_card_template() -> dict:
    return {
        "sections": {
            "basic_info": {
                "fields": ["姓名", "代号", "性别", "年龄", "狩魂羁绊", "业力标签", "背景故事", "外形描述", "经历标签"],
                "required": ["姓名", "代号"],
            },
            "attributes": {
                "fields": ["体魄", "智慧", "心魂"],
                "range": "E-SSS+",
                "derived": ["武技强度", "术法强度", "灵能力强度"],
            },
            "resources": {
                "fields": ["生命值", "灵力值", "时髦值", "道具点上限", "经验值", "灵识"],
                "defaults": {"时髦值": 10, "道具点上限": 3, "经验值": 0},
            },
            "skills": {
                "fields": ["运动", "操作", "隐秘", "调查", "洞察", "说服", "狩魂学识"],
                "components": ["属性附加", "自由分配", "技能等级"],
            },
            "spirit_power": {
                "fields": ["灵能力名称", "灵能力描述"],
                "constraints": {"max_chars": 80, "max_tags": 3},
                "specializations": {"max": 2},
            },
            "spirit_marks": {"max": 4, "fields": ["类型", "对应魂魄"]},
            "soul_weapon": {"fields": ["名称", "类型", "效果"]},
            "ultimates": {
                "tier_1": {"unlock": "灵识14级", "fields": ["名称", "类型", "效果", "绝技描述"]},
                "tier_2": {"unlock": "灵识18级", "fields": ["名称", "类型", "效果", "绝技描述"]},
            },
            "stylish_moves": {"fields": ["时髦风格", "消耗", "动作名和效果"]},
            "feats": {"max": 2, "unlock": ["灵识10级", "灵识16级"]},
            "martial_arts": {"fields": ["名称", "消耗", "目标", "辅助", "秘传", "效果", "风味描述"]},
            "spells": {"fields": ["名称", "消耗", "目标", "类别", "秘传", "类型", "效果", "风味描述"]},
        },
        "creation_steps": [
            "创建灵能力（概念→标签→描述）",
            "选择狩魂者羁绊",
            "构建角色信息（代号、真名、外貌、性格、背景故事）",
            "分配三大属性等级（体魄、智慧、心魂）",
            "分配技能等级",
            "选择武技、术法、专长、灵魂武器、绝技",
        ],
    }


def build_rules_graph() -> dict:
    return {
        "nodes": [
            {"id": "灵识", "type": "resource"},
            {"id": "体魄", "type": "attribute"},
            {"id": "智慧", "type": "attribute"},
            {"id": "心魂", "type": "attribute"},
            {"id": "武技", "type": "ability_pool"},
            {"id": "术法", "type": "ability_pool"},
            {"id": "专长", "type": "ability_pool"},
            {"id": "绝技", "type": "ability_pool"},
            {"id": "灵能印记", "type": "ability_pool"},
            {"id": "灵魂武器", "type": "equipment"},
            {"id": "时髦动作", "type": "ability_pool"},
            {"id": "技能点", "type": "resource"},
        ],
        "edges": [
            {"from": "体魄", "to": "武技", "relation": "unlocks", "condition": "D级可学普通，SS级可学秘传"},
            {"from": "体魄", "to": "武技", "relation": "determines_count", "rule": "等级决定可学武技数量"},
            {"from": "智慧", "to": "术法", "relation": "unlocks", "condition": "D级可学普通，SS级可学秘传"},
            {"from": "智慧", "to": "术法", "relation": "determines_count", "rule": "等级决定可学术法数量"},
            {"from": "智慧", "to": "技能点", "relation": "provides", "rule": "每升一级获得技能点"},
            {"from": "心魂", "to": "灵能印记", "relation": "determines_count", "rule": "等级决定灵能印记数量"},
            {"from": "心魂", "to": "灵能印记", "relation": "unlocks_extra", "condition": "A级觉醒额外灵能印记"},
            {"from": "灵识", "to": "专长", "relation": "unlocks", "condition": "10级第一个，16级第二个"},
            {"from": "灵识", "to": "灵魂武器", "relation": "unlocks", "condition": "12级获得"},
            {"from": "灵识", "to": "绝技", "relation": "unlocks", "condition": "14级一挡，18级二挡"},
            {"from": "体魄", "to": "武技", "relation": "strength", "rule": "属性强度=武技加骰数"},
            {"from": "智慧", "to": "术法", "relation": "strength", "rule": "属性强度=术法加骰数"},
            {"from": "心魂", "to": "灵能印记", "relation": "strength", "rule": "属性强度=灵能力加骰数"},
        ],
    }


def clean_pdf_rules() -> str:
    rules_path = MARKDOWN_DIR / "core_rules.md"
    if not rules_path.exists():
        return ""
    content = rules_path.read_text(encoding="utf-8")
    content = re.sub(r"(熔炼跑团工厂 狩魂者TRPG)+", "", content)
    content = re.sub(r"\n{3,}", "\n\n", content)
    content = content.strip()
    return content


def save_json(data, filename: str):
    output_path = OUTPUT_DIR / filename
    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    size_kb = output_path.stat().st_size / 1024
    print(f"  {filename} ({size_kb:.1f} KB)")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("加载 Excel 工作簿...")
    wb = load_workbook()

    print("\n提取结构化数据:")

    print("  属性系统...")
    attributes = extract_attributes(wb)
    save_json(attributes, "attributes.json")

    print("  技能表...")
    skills = extract_skills()
    save_json(skills, "skills.json")

    print("  武技表...")
    martial_arts = extract_martial_arts(wb)
    save_json(martial_arts, "martial_arts.json")

    print("  术法表...")
    spells = extract_spells(wb)
    save_json(spells, "spells.json")

    print("  灵能印记...")
    spirit_marks = extract_spirit_marks(wb)
    save_json(spirit_marks, "spirit_marks.json")

    print("  专长表...")
    feats = extract_feats(wb)
    save_json(feats, "feats.json")

    print("  绝技表...")
    ultimates = extract_ultimates(wb)
    save_json(ultimates, "ultimates.json")

    print("  时髦动作...")
    stylish_moves = extract_stylish_moves(wb)
    save_json(stylish_moves, "stylish_moves.json")

    print("  通用效果...")
    effects = extract_effects(wb)
    save_json(effects, "effects.json")

    print("  角色卡模板...")
    card_template = extract_card_template()
    save_json(card_template, "card_template.json")

    print("  规则关联图...")
    rules_graph = build_rules_graph()
    save_json(rules_graph, "rules_graph.json")

    print("\n清洗PDF规则书文本...")
    cleaned_rules = clean_pdf_rules()
    if cleaned_rules:
        rules_path = OUTPUT_DIR / "core_rules_cleaned.md"
        rules_path.write_text(cleaned_rules, encoding="utf-8")
        size_kb = rules_path.stat().st_size / 1024
        print(f"  core_rules_cleaned.md ({size_kb:.1f} KB)")
    else:
        print("  跳过（未找到PDF转换结果）")

    print(f"\n知识库生成完成！共 {11} 个文件输出到 {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
