# System Prompt Dossier · 大模型人格档案

> 把看不见的 system prompt 拆开，看清每个 AI 的真实人格、能力边界与进化史。

本项目对主流大模型和 Agent 产品的 **system prompt** 进行中文拆解与人格分析，聚焦复杂企业环境下的 Agent 行为。区别于单纯收集 prompt 原文，本项目提供：

- **双版本人格画像**：面向大学生的科普版 + 面向行业 KA 高层的授课版。
- **八维拆解骨架**：身份、权限、安全、工具、商业优先级、运行时干预、版本 diff、token 成本。
- **版本时间线 + 原文阅读层**：点击版本卡片查看完整 prompt、来源字段与分析。
- **来源标注规范**：每条版本分析都要求追溯到来源仓库、文件路径、commit 与行号。

当前仓库是**静态展示版**。页面可以直接部署到静态站点；开发态模型页通过 `fetch()` 读取 `data/*.json`，建议使用本地 HTTP 服务查看。

---

## 当前模型页面

| 模型 / 产品 | 开发态页面 | 数据文件 | 发布态单文件 | 来源状态 |
|-------------|------------|----------|--------------|----------|
| Claude | `claude-sample.html` | `data/claude.json` | `dist/claude.html` | 已固定来源路径与 commit；Fable 5 使用最新上游快照 |
| GPT | `gpt.html` | `data/gpt.json` | `dist/gpt.html` | 已固定来源路径与 commit |
| Gemini | `gemini.html` | `data/gemini.json` | `dist/gemini.html` | 已固定来源路径与 commit |
| Cursor | `cursor.html` | `data/cursor.json` | `dist/cursor.html` | 已固定来源路径与 commit |
| Devin | `devin.html` | `data/devin.json` | `dist/devin.html` | 已固定来源路径与 commit |
| Grok | `grok.html` | `data/grok.json` | `dist/grok.html` | 已固定来源路径与 commit |
| Microsoft Copilot | `copilot.html` | `data/copilot.json` | `dist/copilot.html` | 已固定来源路径与 commit |

首页与方法论：

- `index.html`：项目索引页
- `methodology.html`：八维拆解方法论
- `docs/source-annotations.md`：来源标注规范与当前来源状态表

---

## 八维拆解骨架

每个模型的拆解都沿用同一套维度，确保结论有据可依、可对比、可复现：

| 维度 | 拆什么 | 理论出处 |
|------|--------|----------|
| **D1 身份 / 人格** | 它把自己当成“谁”？ | COSTAR · Claude's Constitution |
| **D2 指令权限层级** | 冲突时谁说了算？ | OpenAI Model Spec |
| **D3 安全红线** | 绝对不做的是什么？ | Claude's Constitution |
| **D4 工具调用规则** | 何时搜索 / 拒绝 / 动手？ | CL4R1T4S |
| **D5 商业优先级** | 是否偏向自家产品？ | The Moat is a Config File |
| **D6 运行时干预** | 对话中途会被“插话”吗？ | 实时分类器干预 / anthropic_reminders |
| **D7 跨版本 Diff** | 护栏是怎么一步步加上的？ | Prompt Archaeology |
| **D8 Token 体量** | 为“安全”付出多少成本？ | Context tax |

核心心智模型：

> **The system prompt IS the product.**
> LLM 正在变成商品层，产品差异化很大一部分活在 system prompt 和运行时配置里。

---

## 仓库结构

```text
.
├── README.md
├── LICENSE
├── index.html
├── methodology.html
├── claude-sample.html
├── gpt.html
├── gemini.html
├── cursor.html
├── devin.html
├── grok.html
├── copilot.html
├── data/
│   ├── pages.json
│   ├── claude.json
│   ├── gpt.json
│   ├── gemini.json
│   ├── cursor.json
│   ├── devin.json
│   ├── grok.json
│   └── copilot.json
├── dist/
│   ├── claude.html
│   ├── gpt.html
│   ├── gemini.html
│   ├── cursor.html
│   ├── devin.html
│   ├── grok.html
│   └── copilot.html
├── docs/
│   └── source-annotations.md
├── scripts/
│   ├── build.py
│   ├── build_pages.py
│   └── validate.py
├── templates/
│   └── model.html
└── src/
    ├── reader.js
    ├── site.css
    └── styles.css
```

说明：

- `templates/model.html` 是所有模型页共享的 HTML 骨架，包含通用导航、hero、阅读 overlay 和脚本挂载点。
- `data/pages.json` 管理每个模型页的标题、hero 文案、页面内容块、数据文件和输出文件名。
- `src/site.css` 是首页与方法论页共享的视觉系统样式，避免静态入口页继续维护内联 CSS。
- `*.html` 根目录页面是开发态生成物，依赖 `src/styles.css`、`src/reader.js` 和 `data/*.json`。
- `dist/*.html` 是构建后的单文件页面，内嵌 CSS、JS 和对应模型数据，适合离线打开或静态分发。
- `scripts/build.py` 是正式构建入口，会统一生成根目录开发态页面和 `dist/*.html` 发布态页面。
- `scripts/validate.py` 会检查数据统计、来源字段、行号范围、HTML 本地链接和生成物是否过期。

---

## 本地查看

推荐通过本地 HTTP 服务查看开发态页面：

```bash
python3 -m http.server 8000
```

然后访问：

```text
http://localhost:8000/index.html
```

如果不启动 HTTP 服务，请打开 `dist/*.html`。根目录模型页会通过 `fetch()` 读取 `data/*.json`，直接用 `file://` 打开时浏览器可能阻止数据加载。

---

## 构建发布页

生成全部模型的根目录开发态页面和单文件发布页：

```bash
python3 scripts/build.py
```

输出：

```text
claude-sample.html
gpt.html
gemini.html
cursor.html
devin.html
grok.html
copilot.html
dist/claude.html
dist/gpt.html
dist/gemini.html
dist/cursor.html
dist/devin.html
dist/grok.html
dist/copilot.html
```

`scripts/build_pages.py` 是构建实现模块，通常不需要直接调用。

### `dist/` 提交策略

`dist/*.html` 会长期提交到仓库，用作 GitHub Pages / 离线阅读的发布态单文件产物。它们是构建产物，不应手工修改；所有变更应先改 `templates/`、`src/` 或 `data/`，再运行：

```bash
python3 scripts/build.py
```

`scripts/validate.py` 会检查根目录模型页和 `dist/*.html` 是否已经用当前源码重新生成。

---

## 自动校验

发布前运行：

```bash
python3 scripts/validate.py
```

校验内容包括：

- `words` / `lines` 是否和 `prompt` 实际内容一致。
- `source_repo`、`source_path`、`source_commit`、`license` 是否为空或仍含 TODO / 未核对占位。
- `quoted_lines` 是否为空、格式错误或越界。
- 根目录 HTML 与 `dist/*.html` 中的本地 `href` / `src` 是否能解析到真实文件。
- 根目录模型页与 `dist/*.html` 是否和 `templates/model.html`、`data/pages.json`、`data/*.json`、`src/*` 重新构建后的结果一致。

---

## 来源与素材

Claude、GPT、Gemini、Cursor、Devin、Grok、Microsoft Copilot 的真实 prompt 文本来自：

- [asgeirtj/system_prompts_leaks](https://github.com/asgeirtj/system_prompts_leaks)
- 主要固定 commit：`678e7fadee889f036400a478acbf3c8a1d16980f`
- Claude Fable 5 / Claude Code Fable 5 固定 commit：`28639e67c6774477aa32b9ef1995bae2c74c40f6`
- Grok / Microsoft Copilot 固定 commit：`28639e67c6774477aa32b9ef1995bae2c74c40f6`
- 来源许可证：CC0 1.0 Universal

每个模型版本的 `source_path`、`source_commit` 与关键 `quoted_lines` 状态见 `docs/source-annotations.md`。

本地可按需克隆原始素材库：

```bash
git clone https://github.com/asgeirtj/system_prompts_leaks.git
```

本仓库不提交 `system_prompts_leaks/` 或 `.sources/` 原始素材目录；这两个目录已在 `.gitignore` 中忽略。

---

## 协议

本仓库中作者原创的中文拆解、页面结构与展示内容采用 **CC0-1.0** 发布，详见 [`LICENSE`](./LICENSE)。

原始 system prompt 素材来自第三方公开仓库时，请同时遵守对应来源仓库的许可与引用要求。
