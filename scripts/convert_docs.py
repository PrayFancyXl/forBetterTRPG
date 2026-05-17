"""
文档转换脚本 - 使用 markitdown 将 originData 下的 PDF/Excel 转为 Markdown

用法: python scripts/convert_docs.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "markitdown" / "packages" / "markitdown" / "src"))

from markitdown import MarkItDown

ORIGIN_DATA = PROJECT_ROOT / "originData"
OUTPUT_DIR = PROJECT_ROOT / "data" / "markdown"

FILES_MAP = {
    "core_rules.md": "狩魂者TRPG核心规则-电子版（资源部分二三四章）.pdf",
    "card_tutorial.md": "狩魂者车卡教学v1.pdf",
    "blank_card.md": "狩魂者空白卡正式版V1.4.xlsx",
}


def convert_file(input_path: Path, output_path: Path) -> bool:
    print(f"  转换中: {input_path.name}")
    try:
        md = MarkItDown()
        result = md.convert(str(input_path))
        output_path.write_text(result.markdown, encoding="utf-8")
        size_kb = output_path.stat().st_size / 1024
        print(f"  完成: {output_path.name} ({size_kb:.1f} KB)")
        return True
    except Exception as e:
        print(f"  错误: {e}")
        return False


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"源文件目录: {ORIGIN_DATA}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"待转换文件: {len(FILES_MAP)} 个\n")

    success_count = 0
    for output_name, input_name in FILES_MAP.items():
        input_path = ORIGIN_DATA / input_name
        output_path = OUTPUT_DIR / output_name

        if not input_path.exists():
            print(f"  跳过（文件不存在）: {input_name}")
            continue

        if convert_file(input_path, output_path):
            success_count += 1

    print(f"\n转换完成: {success_count}/{len(FILES_MAP)} 个文件成功")
    return 0 if success_count == len(FILES_MAP) else 1


if __name__ == "__main__":
    sys.exit(main())
