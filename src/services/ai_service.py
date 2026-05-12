from __future__ import annotations

import json
from typing import AsyncGenerator

import openai

from ..config import settings
from ..models.enums import CreationStep
from .knowledge_loader import knowledge

STEP_KNOWLEDGE_MAP = {
    CreationStep.SPIRIT_POWER: ["card_template", "spirit_marks"],
    CreationStep.BOND: ["card_template"],
    CreationStep.CHARACTER_INFO: ["card_template"],
    CreationStep.ATTRIBUTES: ["attributes"],
    CreationStep.SKILLS: ["skills", "attributes"],
    CreationStep.ABILITIES: ["martial_arts", "spells", "feats", "ultimates", "stylish_moves", "spirit_marks"],
}

SYSTEM_PROMPT_BASE = """你是《狩魂者TRPG》的建卡助手。你的职责是帮助玩家创建角色卡，回答规则问题，并提供建卡建议。

核心规则摘要：
- 三大属性：体魄、智慧、心魂，等级从E(1)到SSS+(9)
- 属性强度决定战斗加骰数
- 灵识等级决定成长奖励（10级专长、12级灵魂武器、14级一挡绝技、16级专长、18级二挡绝技）
- 体魄决定可学武技数量，D级解锁普通武技，SS级解锁秘传武技
- 智慧决定可学术法数量和技能点，D级解锁普通术法，SS级解锁秘传术法
- 心魂决定灵能印记数量，A级觉醒额外灵能印记

回答时请：
1. 简洁明了，使用游戏术语
2. 如果涉及具体数值，给出准确数据
3. 如果玩家在犹豫选择，分析各选项的优劣
4. 适当给出角色发展方向的建议
5. 输出列表时使用 `-` 作为列表符号，不要使用 `*`
6. 输出表格时，每行必须独立换行，使用标准 Markdown 表格格式，分隔行（`:---`）必须单独占一行
"""


def _build_step_context(step: CreationStep) -> str:
    sections = STEP_KNOWLEDGE_MAP.get(step, [])
    context_parts = []

    for section in sections:
        data = getattr(knowledge, section, None)
        if data is None:
            continue
        if isinstance(data, list) and len(data) > 20:
            context_parts.append(f"\n【{section}】（前20条）:\n{json.dumps(data[:20], ensure_ascii=False, indent=1)}")
        elif isinstance(data, dict):
            context_parts.append(f"\n【{section}】:\n{json.dumps(data, ensure_ascii=False, indent=1)}")
        else:
            context_parts.append(f"\n【{section}】:\n{json.dumps(data, ensure_ascii=False, indent=1)}")

    return "\n".join(context_parts)


def _get_client() -> openai.AsyncOpenAI:
    import httpx
    http_client = httpx.AsyncClient(proxy=settings.HTTP_PROXY) if settings.HTTP_PROXY else None
    return openai.AsyncOpenAI(
        api_key=settings.DEEPSEEK_API_KEY,
        base_url=settings.DEEPSEEK_BASE_URL,
        http_client=http_client,
    )


def build_messages(user_message: str, step: CreationStep, chat_history: list[dict] = None) -> list[dict]:
    step_context = _build_step_context(step)
    step_names = {
        CreationStep.SPIRIT_POWER: "灵能力创建",
        CreationStep.BOND: "狩魂者羁绊选择",
        CreationStep.CHARACTER_INFO: "角色信息填写",
        CreationStep.ATTRIBUTES: "属性分配",
        CreationStep.SKILLS: "技能分配",
        CreationStep.ABILITIES: "武技/术法/专长/绝技选择",
    }

    system_content = SYSTEM_PROMPT_BASE + f"\n\n当前玩家正在进行：{step_names.get(step, '建卡')}\n\n相关规则数据：{step_context}"
    messages: list[dict] = [{"role": "system", "content": system_content}]

    if chat_history:
        for msg in chat_history[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_message})
    return messages


async def chat_stream(user_message: str, step: CreationStep, chat_history: list[dict] = None, model: str = None) -> AsyncGenerator[str, None]:
    client = _get_client()
    messages = build_messages(user_message, step, chat_history)

    stream = await client.chat.completions.create(
        model=model or settings.DEEPSEEK_MODEL,
        messages=messages,
        stream=True,
        temperature=0.7,
        max_tokens=1024,
    )
    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


def get_contextual_tip(step: CreationStep) -> str:
    tips = {
        CreationStep.SPIRIT_POWER: "灵能力是你角色的核心特色。先想一个概念（如操纵火焰、读心术），再用不超过80字描述，最多3个标签。",
        CreationStep.BOND: "狩魂者羁绊是你加入狩魂活动的动机，它会影响你的角色扮演方向。",
        CreationStep.CHARACTER_INFO: "代号是你在狩魂者组织中的称呼，真名则是你的本名。背景故事会让角色更有深度。",
        CreationStep.ATTRIBUTES: "三大属性决定了你的战斗风格：体魄偏武技近战，智慧偏术法远程，心魂偏灵能力辅助。",
        CreationStep.SKILLS: "技能点由智慧等级决定。运动/操作对应体魄，隐秘/调查对应智慧，洞察/说服对应心魂。",
        CreationStep.ABILITIES: "根据你的属性等级，选择对应数量的武技和术法。注意秘传技能需要SS级以上才能学习。",
    }
    return tips.get(step, "")
