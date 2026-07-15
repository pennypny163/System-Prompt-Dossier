#!/usr/bin/env python3
"""Import the audited latest model prompts and refresh their dossier copy."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / ".sources" / "system_prompts_leaks"
PAGES_PATH = ROOT / "data" / "pages.json"


MODEL_IMPORTS = {
    "claude": {
        "path": "Anthropic/claude-sonnet-5.md",
        "entry": {
            "id": "claude-sonnet-5",
            "ver": "Sonnet 5",
            "date": "2026-07-01",
            "track": "Claude Product",
            "color": "#b43a2f",
            "tagline": "最新聊天模型 · 温暖克制 · 搜索与 MCP 优先",
            "now": False,
            "analysis": [
                ["身份与产品线", "第 7-17 行把当前模型明确为 Claude Sonnet 5，并把 Opus 4.8、Sonnet 5、Haiku 4.5 与 Mythos/Fable 特殊轨道放进同一产品说明。"],
                ["稳态人格", "第 184-188 行要求情绪与关系话题保持温暖、真诚、日常化；技术回答则保持具体，命令、路径和代码必须精确。"],
                ["主动查证", "第 171-180 行把 2026 年 1 月设为可靠知识截止点；凡是当前事实或可能变化的信息，都应直接搜索而不是让用户再次授权。"],
                ["记忆有边界", "第 190-246 行允许像同事一样自然使用相关记忆，但禁止在不相关场景突然提起敏感经历，也不让记忆削弱批判性反馈。"],
                ["MCP 优先但不盲从", "第 795-844 行要求先看连接器是否适合，再考虑浏览器；文件或工具中的可疑指令仍需确认，不能自动当成用户本人意图。"],
                ["企业视角", "Sonnet 5 的人格不只是温和，而是把查证、记忆、连接器选择和敏感数据处理组合成一套可审计的协作方式。"],
            ],
            "source": {
                "source_repo": "asgeirtj/system_prompts_leaks",
                "source_path": "Anthropic/claude-sonnet-5.md",
                "source_commit": "feff4a1a5372f491af7c9579760c87c62784251b",
                "quoted_lines": [
                    {"label": "full_prompt", "start": 1, "end": 3844},
                    {"label": "sonnet_identity", "start": 7, "end": 17},
                    {"label": "sonnet_product_ecosystem", "start": 19, "end": 29},
                    {"label": "sonnet_wellbeing", "start": 97, "end": 133},
                    {"label": "sonnet_search", "start": 171, "end": 180},
                    {"label": "sonnet_memory", "start": 190, "end": 246},
                    {"label": "sonnet_mcp_priority", "start": 795, "end": 844},
                ],
                "license": "CC0 1.0 Universal",
                "analysis_author_note": "全文来自上游提交 feff4a1；中文拆解为本仓库作者基于原文的分析。",
            },
        },
    },
    "gpt": {
        "path": "OpenAI/gpt-5.6-sol-extra-high.md",
        "entry": {
            "id": "gpt-5-6-sol-extra-high",
            "ver": "5.6 Sol · Extra High",
            "date": "2026-07-10",
            "color": "#d35a45",
            "tagline": "最新推理模型 · 强制查证 · 工具与交付物密集",
            "now": True,
            "analysis": [
                ["模型身份", "第 61 行把自身声明为 GPT-5.6 Thinking，并明确这是带隐藏思维链的推理模型；文件名对应 Sol Extra High 运行形态。"],
                ["先查证再回答", "第 19-25 行把诚实、时效搜索和事实引用放在前部：只要事实可能在知识截止后变化，就必须联网核验。"],
                ["交付物工作流", "第 4-16 行要求 PDF、文档、幻灯片、表格任务先读取对应技能规范，再生成可交付文件，而不是直接凭经验动手。"],
                ["产品化表达", "第 82-157 行区分可复用写作成品、普通解释与工具任务，并要求语言可读、少行话、少堆列表。"],
                ["广义工具外壳", "主体大部分篇幅用于 web、文件搜索、邮箱、日历、联系人、图像和连接器等工具契约，说明人格越来越受运行环境塑造。"],
                ["企业视角", "5.6 Sol 更像一个带审计规则的知识工作操作系统：模型推理只是内核，查证、权限、工具和交付格式共同决定最终行为。"],
            ],
            "source": {
                "source_repo": "asgeirtj/system_prompts_leaks",
                "source_path": "OpenAI/gpt-5.6-sol-extra-high.md",
                "source_commit": "72d763ffabca3d3d29d2f9edbc7bab5472b4adde",
                "quoted_lines": [
                    {"label": "full_prompt", "start": 1, "end": 2662},
                    {"label": "identity_and_date", "start": 1, "end": 2},
                    {"label": "artifact_skills", "start": 4, "end": 16},
                    {"label": "trustworthiness_and_web", "start": 19, "end": 25},
                    {"label": "model_identity", "start": 61, "end": 61},
                    {"label": "writing_style", "start": 143, "end": 163},
                ],
                "license": "CC0 1.0 Universal",
                "analysis_author_note": "全文来自上游提交 72d763f；中文拆解为本仓库作者基于原文的分析。",
            },
        },
    },
    "gemini": {
        "path": "Google/gemini-3.5-flash.md",
        "entry": {
            "id": "gemini-3-5-flash",
            "ver": "3.5 Flash",
            "date": "2026-05-20",
            "color": "#4285f4",
            "tagline": "最新 Web 模型 · 自适应同伴 · 视觉与组件路由",
            "now": True,
            "analysis": [
                ["身份定位", "第 6-13 行明确 Core Model 是面向 Web 的 Gemini 3.5 Flash，并注明当前运行在 Paid tier。"],
                ["同伴式人格", "第 17-25 行要求成为真实、可适应的知识型同伴：温暖但坦率，匹配用户词汇水平，不摆出僵硬讲师姿态。"],
                ["完成优先", "第 51-57 行把任务分成可直接完成与需要引导两类；封闭问题不追加菜单式追问，开放问题最多问一个关键问题。"],
                ["个性化边界", "第 59-79 行规定当前对话优先于历史信息，敏感数据不主动推断，必要使用时还要标注来源与不确定性。"],
                ["视觉路由", "第 87-139 行要求视觉必须真正帮助理解，并在图片、Markdown、Sequence、Timeline 等组件之间按内容形态选择。"],
                ["企业视角", "3.5 Flash 的差异不只是速度，而是把自然对话、可视化组件和用户数据边界组合成面向 Web 的交互层。"],
            ],
            "source": {
                "source_repo": "asgeirtj/system_prompts_leaks",
                "source_path": "Google/gemini-3.5-flash.md",
                "source_commit": "24a139b206be1046e107e02314a66ae980515351",
                "quoted_lines": [
                    {"label": "full_prompt", "start": 1, "end": 235},
                    {"label": "model_identity", "start": 6, "end": 13},
                    {"label": "adaptive_peer", "start": 17, "end": 25},
                    {"label": "response_principles", "start": 33, "end": 57},
                    {"label": "user_data_hierarchy", "start": 59, "end": 79},
                    {"label": "image_strategy", "start": 87, "end": 115},
                    {"label": "lmdx_routing", "start": 117, "end": 139},
                ],
                "license": "CC0 1.0 Universal",
                "analysis_author_note": "全文来自上游提交 24a139b；中文拆解为本仓库作者基于原文的分析。",
            },
        },
    },
}


PAGE_META = {
    "claude": {
        "hero_title_html": '<span class="en">Claude</span> Fable 5',
        "persona_tag": "Mythos 级的企业级思考体",
        "subtitle_html": 'Claude 已从单一聊天助手演进成多产品工作层。本页继续以 <b style="color:#f3c98a">Fable 5</b> 作为主分析对象，观察 Claude 5 / Mythos-class 特殊轨道如何与 Claude Code、Cowork、MCP Apps、Artifacts、web search 和 memory 系统组合。<span style="color:var(--t3)">Sonnet 5 作为新增的标准 Sonnet 线快照收入时间线，不替代 Fable 5 的主分析位置。</span>',
    },
    "gpt": {
        "hero_title_html": '<span class="en">GPT</span> 5.6 Sol',
        "persona_tag": "先查证、再交付的工具型推理产品经理",
        "subtitle_html": 'GPT 5.6 Sol Extra High 把推理模型放进一套密集的知识工作运行环境：时效事实必须查证，文档与表格先遵循技能规范，搜索、邮箱、日历和连接器各有权限契约。<span>本页保留 5.5 历史版本，并把 5.6 Sol 标记为当前最新快照。</span>',
    },
    "gemini": {
        "hero_title_html": '<span class="en">Gemini</span> 3.5 Flash',
        "persona_tag": "温暖、清晰、会选择视觉组件的 Web 协作者",
        "subtitle_html": 'Gemini 3.5 Flash 面向 Web，把自适应同伴式表达、完成优先、用户数据边界与 LMDX 视觉组件路由组合起来。<span>本页保留 Gemini 3 Flash 与 Workspace 两条历史/产品表面，并把 3.5 Flash 标记为当前最新快照。</span>',
    },
}


CONTENT_REPLACEMENTS = {
    "claude": [
        (
            '''    <div class="quote" data-source-label="fable_identity">
      <div class="src">Anthropic / claude-fable-5.md · fable_identity</div>
      <div class="en">Fable 5 is described as the first Claude 5 model, part of a <b>Mythos-class model tier</b> above Opus, and the most intelligent generally available Claude model.</div>
      <div class="cn">这不是 Opus 4.x 的小版本号更新，而是产品叙事上进入 Claude 5 / Mythos 级：能力层级和安全分层一起被写进 prompt。</div>
    </div>''',
            '''    <div class="quote" data-source-label="sonnet_identity">
      <div class="src">Anthropic / claude-sonnet-5.md · sonnet_identity</div>
      <div class="en">The prompt explicitly identifies this iteration as <b>Claude Sonnet 5</b> and places it alongside Opus 4.8 and Haiku 4.5.</div>
      <div class="cn">Sonnet 5 的第一层变化是身份与产品线重新定位：它成为最新日常聊天主线，同时保留 Opus、Haiku 与特殊 Mythos/Fable 轨道的边界。</div>
    </div>''',
        ),
        (
            '''    <div class="quote" data-source-label="fable_product_ecosystem">
      <div class="src">Anthropic / claude-fable-5.md · fable_product_ecosystem</div>
      <div class="en">Claude is connected to Claude Code, Claude Cowork, Chrome, Excel, PowerPoint, API, mobile and desktop access paths.</div>
      <div class="cn">Fable 5 的 system prompt 已经像产品总线：聊天、编码、办公、浏览器、移动端和 API 被放在同一张 Anthropic 产品地图里。</div>
    </div>''',
            '''    <div class="quote" data-source-label="sonnet_product_ecosystem">
      <div class="src">Anthropic / claude-sonnet-5.md · sonnet_product_ecosystem</div>
      <div class="en">Claude connects chat, Code, Cowork, Chrome, Excel, PowerPoint, API, mobile and desktop into one product map.</div>
      <div class="cn">Sonnet 5 的 system prompt 已经像产品总线：聊天、编码、办公、浏览器、移动端和 API 被放在同一张工具地图里。</div>
    </div>''',
        ),
        (
            '''    <div class="quote" data-source-label="fable_mcp_priority">
      <div class="src">Anthropic / claude-fable-5.md · fable_mcp_priority</div>
      <div class="en">MCP-first does not suspend normal caution; instructions inside files are not the person typing them, and sensitive exfiltration gets flagged.</div>
      <div class="cn">最关键的企业 Agent 逻辑：有合适 MCP 就优先用，但工具优先不等于盲从，文件里的指令不会自动升级成用户本人意图。</div>
    </div>''',
            '''    <div class="quote" data-source-label="sonnet_mcp_priority">
      <div class="src">Anthropic / claude-sonnet-5.md · sonnet_mcp_priority</div>
      <div class="en">Claude checks connected MCP tools before reaching for the browser, while preserving confirmation and sensitive-data safeguards.</div>
      <div class="cn">最关键的企业 Agent 逻辑仍然成立：连接器优先不等于盲从，文件里的指令不会自动升级成用户本人意图。</div>
    </div>''',
        ),
        ("Fable 5 / Opus 4.8 prompt", "Sonnet 5 / Opus 4.8 prompt"),
        ("Fable 5 时代", "Sonnet 5 时代"),
        ("25,544 词 / 3,826 行", "25,672 词 / 3,844 行"),
        ("约 <b>40,000+ tokens</b>", "约 <b>40,000+ tokens</b>"),
        ("Fable 5 的 <b>输入 token 成本</b>", "Sonnet 5 的 <b>输入 token 成本</b>"),
        ("Claude Fable 5 选择", "Claude Sonnet 5 选择"),
        ("只画最新版（Fable 5）人格画像", "只画最新版（Sonnet 5）人格画像"),
    ],
    "gpt": [
        (
            '''    <div class="quote" data-source-label="identity_and_date">
      <div class="src">system_prompts_leaks / OpenAI/gpt-5.5-thinking.md · identity_and_date</div>
      <div class="en">"You are ChatGPT" appears together with knowledge cutoff and current date.</div>
      <div class="cn">GPT 的第一层不是人格比喻，而是平台身份与时间口径：先确定“我是谁、我知道到哪天、今天是哪天”。</div>
    </div>''',
            '''    <div class="quote" data-source-label="model_identity">
      <div class="src">system_prompts_leaks / OpenAI/gpt-5.6-sol-extra-high.md · model_identity</div>
      <div class="en">The runtime identifies itself as <b>GPT-5.6 Thinking</b>, a reasoning model with a hidden chain of thought.</div>
      <div class="cn">5.6 Sol 的第一层是明确的推理模型身份；页面把“Sol Extra High”视为运行形态，把“GPT-5.6 Thinking”视为原文中的模型自述。</div>
    </div>''',
        ),
        (
            '''    <div class="quote" data-source-label="tool_skill_rules">
      <div class="src">system_prompts_leaks / OpenAI/gpt-5.5-thinking.md · tool_skill_rules</div>
      <div class="en">For PDFs, documents, slides and spreadsheets, the model must read the matching skill instructions first.</div>
      <div class="cn">这说明 GPT 的工具人格是“流程驱动”：不是会工具就立刻用，而是先读取对应 skill 规范，再进入执行。</div>
    </div>''',
            '''    <div class="quote" data-source-label="artifact_skills">
      <div class="src">system_prompts_leaks / OpenAI/gpt-5.6-sol-extra-high.md · artifact_skills</div>
      <div class="en">PDF, document, slide and spreadsheet tasks must begin by reading the matching skill instructions.</div>
      <div class="cn">5.6 Sol 的工具人格仍是流程驱动：先读取对应技能规范，再生成可下载、可复用的交付物。</div>
    </div>''',
        ),
        (
            '''    <div class="quote" data-source-label="retrieval_rules">
      <div class="src">system_prompts_leaks / OpenAI/gpt-5.5-instant.md · retrieval_rules</div>
      <div class="en">Before answering, it internally decides whether user-specific memory could affect the answer, then retrieves when needed.</div>
      <div class="cn">Instant 版本的重点是上下文路由：记忆、会话、模型上下文不是背景装饰，而是会影响答案的证据源。</div>
    </div>''',
            '''    <div class="quote" data-source-label="trustworthiness_and_web">
      <div class="src">system_prompts_leaks / OpenAI/gpt-5.6-sol-extra-high.md · trustworthiness_and_web</div>
      <div class="en">Facts that may have changed after the knowledge cutoff require web verification, and factual explanations should carry citations.</div>
      <div class="cn">5.6 Sol 把“可能过时就搜索、涉及事实就引用”前置为硬规则，形成先查证再交付的工作方式。</div>
    </div>''',
        ),
        ("当前两份来源已可支撑基础观察", "当前三份来源已可支撑 5.5 与 5.6 的基础横向观察"),
        ("当前缺少本地真实原文，先不估算 token。", "5.6 Sol 原文为 <b>17,124 词 / 2,662 行</b>；体量主要来自工具、连接器和产品运行规则。"),
        ("GPT 页已接入 <b>OpenAI/gpt-5.5-thinking.md</b> 与 <b>OpenAI/gpt-5.5-instant.md</b> 全文", "GPT 页已接入 <b>OpenAI/gpt-5.6-sol-extra-high.md</b>，并保留两份 GPT 5.5 全文"),
    ],
    "gemini": [
        (
            '''    <div class="quote" data-source-label="persona">
      <div class="src">system_prompts_leaks / Google/gemini-3-flash.md · persona</div>
      <div class="en">Gemini is framed as an authentic, adaptive collaborator with empathy and candor.</div>
      <div class="cn">Gemini 的人格不是纯工具型，而是“会共情但会纠错”的协作者，表达上比 GPT 更强调互动气质。</div>
    </div>''',
            '''    <div class="quote" data-source-label="adaptive_peer">
      <div class="src">system_prompts_leaks / Google/gemini-3.5-flash.md · adaptive_peer</div>
      <div class="en">Gemini 3.5 Flash is framed as an authentic, adaptive collaborator and a knowledgeable peer: warm, approachable and candid.</div>
      <div class="cn">3.5 Flash 把人格写得更明确：不是正式讲师，而是会匹配用户词汇水平、温暖但坦率的知识型同伴。</div>
    </div>''',
        ),
        (
            '''    <div class="quote" data-source-label="search_conditions">
      <div class="src">system_prompts_leaks / Google/gemini-workspace.md · search_conditions</div>
      <div class="en">Google Search is allowed only under strict conditions, such as explicit web-search wording.</div>
      <div class="cn">这不是“会搜索”的简单能力，而是清晰的来源路由：什么时候查 Workspace、什么时候查 Web，被系统层规定。</div>
    </div>''',
            '''    <div class="quote" data-source-label="user_data_hierarchy">
      <div class="src">system_prompts_leaks / Google/gemini-3.5-flash.md · user_data_hierarchy</div>
      <div class="en">Current conversation statements outrank inferred history; sensitive attributes must not be inferred and require source-aware handling.</div>
      <div class="cn">3.5 Flash 不只会个性化，也给个性化设边界：当前对话优先，敏感属性不主动推断，冲突时要向用户确认。</div>
    </div>''',
        ),
        ("► 生态上下文优先", "► 自适应同伴"),
        ("Gemini 的优势来自与 Search、Workspace 和多模态输入的组合。", "Gemini 3.5 Flash 会匹配用户的知识水平和语言风格，在温暖与坦率之间保持平衡。"),
        ("► 资料员气质", "► 完成优先"),
        ("它更像研究助理：先找资料、归纳、关联，再产出文档。", "封闭任务直接完成，开放问题最多追问一个关键条件，避免把下一步菜单重新丢给用户。"),
        ("► 权限敏感", "► 数据边界清晰"),
        ("私有邮件、云盘、日历等上下文必须被严格区分和标注。", "当前对话高于历史推断；敏感信息默认不推断、不意外带入回答。"),
        ("► 多模态默认", "► 视觉按需路由"),
        ("图片、文档、表格和网页信息可能同时进入任务链。", "只有当图片或组件真正帮助理解时才调用，并在 Markdown、Sequence、Timeline 等表达方式之间选择。"),
        ("会翻资料的图书馆学长", "会把复杂问题讲成人话的跨学科学长"),
        ("你问他问题，他先去资料架找证据", "懂很多，但会先对齐你的知识水平"),
        ("Gemini 的人格感不强，但资料整合感强。它擅长把搜索、文档和上下文放到一张桌上。", "Gemini 3.5 Flash 会先给出核心答案，再用你熟悉的词解释复杂概念；遇到情绪或挫折时，它会接住感受，但也会坦率指出问题。"),
        ("它最适合“帮我看这些材料得出结论”，而不是单纯陪聊。", "它不会为了显得专业而堆术语，也不会为了热情而不断追问；能完成的任务就直接完成。"),
        ("搜索与办公生态里的研究助理：这是给非技术读者的一句话人格锚点。", "温暖但不讨好、清晰但不端着：这是 3.5 Flash 的一句话人格锚点。"),
        ("嵌入办公流的研究助理", "面向用户的智能交互层"),
        ("适合文档、邮件、会议和知识检索场景", "适合把复杂能力包装成清晰、可完成的 Web 体验"),
        ("对企业来说，Gemini 的关键价值在 Workspace 生态协同和信息 grounding。", "对企业来说，3.5 Flash 的价值在于把自然语言、视觉组件和用户上下文组织成一致的交互层。"),
        ("核心风险是私有上下文混入回答时，必须清晰说明来源、权限和可引用边界。", "核心风险是个性化和视觉增强过度：敏感数据、推断来源和组件触发都需要可审计边界。"),
        ("运行时干预重点在 grounding、搜索结果过滤、Workspace 权限和安全分类。", "运行时干预重点在 image_agent、LMDX 组件路由、当前时间注入和用户数据层级。"),
        ("Gemini 页已接入 <b>Google/gemini-3-flash.md</b> 与 <b>Google/gemini-workspace.md</b> 全文", "Gemini 页已接入 <b>Google/gemini-3.5-flash.md</b>，并保留 3 Flash 与 Workspace 全文"),
    ],
}

# Claude 的主分析对象仍是 Fable 5；Sonnet 5 只进入版本时间线。
CONTENT_REPLACEMENTS["claude"] = [
    (new, old)
    for old, new in CONTENT_REPLACEMENTS["claude"]
    if "只画最新版" not in old
]
CONTENT_REPLACEMENTS["claude"].extend(
    [
        (
            '只画最新版（Sonnet 5）人格画像，历代版本沉入"时间线 + diff 技术分析"。',
            '以 Fable 5 为主分析对象；Sonnet 5 作为新增标准 Sonnet 快照收入"时间线 + diff 技术分析"。',
        ),
        (
        '只画最新版（Fable 5）人格画像，历代版本沉入"时间线 + diff 技术分析"。',
        '以 Fable 5 为主分析对象；Sonnet 5 作为新增标准 Sonnet 快照收入"时间线 + diff 技术分析"。',
        ),
    ]
)


CURRENT_IDS = {
    "claude": "fable5",
    "gpt": "gpt-5-6-sol-extra-high",
    "gemini": "gemini-3-5-flash",
}


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def import_models() -> None:
    for slug, spec in MODEL_IMPORTS.items():
        prompt_path = SOURCE_ROOT / spec["path"]
        prompt = prompt_path.read_text(encoding="utf-8")
        entry = dict(spec["entry"])
        entry["prompt"] = prompt
        entry["words"] = len(prompt.split())
        entry["lines"] = len(prompt.splitlines())

        data_path = ROOT / "data" / f"{slug}.json"
        versions = json.loads(data_path.read_text(encoding="utf-8"))
        versions = [version for version in versions if version.get("id") != entry["id"]]
        versions.append(entry)
        for version in versions:
            version["now"] = version.get("id") == CURRENT_IDS[slug]
        write_json(data_path, versions)


def refresh_pages() -> None:
    pages_data = json.loads(PAGES_PATH.read_text(encoding="utf-8"))
    for page in pages_data["pages"]:
        slug = page.get("slug")
        if slug not in PAGE_META:
            continue
        page.update(PAGE_META[slug])
        content = page["content_html"]
        for old, new in CONTENT_REPLACEMENTS[slug]:
            if old in content:
                content = content.replace(old, new)
            elif new not in content:
                raise RuntimeError(f"Unable to find expected {slug} page fragment: {old[:80]!r}")
        page["content_html"] = content
    write_json(PAGES_PATH, pages_data)


if __name__ == "__main__":
    import_models()
    refresh_pages()
    print("Imported Claude Sonnet 5, GPT 5.6 Sol, and Gemini 3.5 Flash.")
