# 来源标注规范

每个模型版本的数据必须能追溯到原始 prompt 文本。版本分析允许有作者解读，但事实判断、原文摘录、行号和版本 diff 必须能回到来源文件。

## 必填字段

每个 `data/*.json` 的版本对象必须包含 `source` 字段：

```json
{
  "source": {
    "source_repo": "asgeirtj/system_prompts_leaks",
    "source_path": "OpenAI/gpt-5.5-thinking.md",
    "source_commit": "678e7fadee889f036400a478acbf3c8a1d16980f",
    "quoted_lines": [
      {
        "label": "identity_and_date",
        "start": 1,
        "end": 6
      }
    ],
    "license": "CC0 1.0 Universal",
    "analysis_author_note": "全文来自本地克隆的 asgeirtj/system_prompts_leaks；中文拆解为本仓库作者基于原文的分析。"
  }
}
```

## 字段说明

| 字段 | 含义 | 要求 |
|------|------|------|
| `source_repo` | 原始 prompt 来源仓库 | 使用 `owner/repo`，不要只写项目名 |
| `source_path` | 原始 prompt 在来源仓库中的路径 | 必须精确到文件 |
| `source_commit` | 来源仓库 commit SHA | 必须固定版本，避免上游文件变动导致引用漂移 |
| `quoted_lines` | 页面摘录、分析或 diff 使用的原文行号 | 使用 1-based 行号；每个摘录单独列一项 |
| `license` | 来源素材许可证 | 写明上游许可证，例如 `CC0 1.0 Universal` |
| `analysis_author_note` | 分析说明 | 区分原文事实与本仓库作者解读 |

## 页面摘录绑定

模型页中的每个证据摘录块必须使用 `data-source-label` 绑定到 `quoted_lines.label`：

```html
<div class="quote" data-source-label="identity_and_date">
  ...
</div>
```

`scripts/validate.py` 会检查：

- 每个 `.quote` 都必须有 `data-source-label`。
- `data-source-label` 必须存在于该模型 `data/*.json` 的 `source.quoted_lines[].label` 中。
- 对应 `quoted_lines` 的 `start` / `end` 不能越界。

## 当前来源状态

| 数据文件 | 版本数 | 来源状态 | 说明 |
|----------|--------|----------|------|
| `data/claude.json` | 7 | **混合固定** | 来源为 Anthropic Official 四个版本、Claude Product 长 prompt（Opus 4.8、Fable 5）与 Claude Code Fable 5 |
| `data/gpt.json` | 2 | **已固定** | 来源为 `OpenAI/gpt-5.5-thinking.md`、`OpenAI/gpt-5.5-instant.md` |
| `data/gemini.json` | 2 | **已固定** | 来源为 `Google/gemini-3-flash.md`、`Google/gemini-workspace.md` |
| `data/cursor.json` | 1 | **已固定** | 来源为 `Cursor/cursor.md` |
| `data/devin.json` | 1 | **已固定** | 来源为 `Misc/devin-cli.md` |
| `data/grok.json` | 11 | **已固定** | 来源为 xAI Grok 全系列：Grok 3/4/4.1 beta/4.2/4.3 beta/API/Build/personas/account/expert/post safety |
| `data/copilot.json` | 5 | **已固定** | 来源为 Microsoft/GitHub Copilot 五个表面：GitHub、VS Code、CLI、Word、macOS App |

已固定来源来自：

```text
source_repo: asgeirtj/system_prompts_leaks
baseline source_commit: 678e7fadee889f036400a478acbf3c8a1d16980f
Claude Fable 5 source_commit: 28639e67c6774477aa32b9ef1995bae2c74c40f6
Grok / Microsoft Copilot source_commit: 28639e67c6774477aa32b9ef1995bae2c74c40f6
license: CC0 1.0 Universal
```

## 已固定来源明细

| 模型 | 版本 | `source_path` | `quoted_lines` 数量 |
|------|------|---------------|----------------------|
| Claude | Sonnet 3.7 | `Anthropic/Official/2025-02-24-claude-sonnet-3.7.md` | 5 |
| Claude | Sonnet 4 | `Anthropic/Official/2025-05-22-claude-sonnet-4.md` | 6 |
| Claude | Sonnet 4.5 | `Anthropic/Official/2025-09-29-claude-sonnet-4.5.md` | 6 |
| Claude | Sonnet 4.6 | `Anthropic/Official/2026-02-17-claude-sonnet-4.6.md` | 6 |
| Claude | Opus 4.8 | `Anthropic/claude-opus-4.8.md` | 8 |
| Claude | Fable 5 | `Anthropic/claude-fable-5.md` | 9 |
| Claude Code | Fable 5 | `Anthropic/Claude Code/claude-code-2.1.172-fable-5.md` | 6 |
| GPT | 5.5 Thinking | `OpenAI/gpt-5.5-thinking.md` | 5 |
| GPT | 5.5 Instant | `OpenAI/gpt-5.5-instant.md` | 4 |
| Gemini | 3 Flash | `Google/gemini-3-flash.md` | 4 |
| Gemini | Workspace | `Google/gemini-workspace.md` | 4 |
| Cursor | IDE Agent | `Cursor/cursor.md` | 5 |
| Devin | CLI | `Misc/devin-cli.md` | 5 |
| Grok | Grok 3 | `xAI/grok-3.md` | 4 |
| Grok | Grok 4 | `xAI/grok-4.md` | 4 |
| Grok | Grok 4.1 Beta | `xAI/grok-4.1-beta.md` | 4 |
| Grok | Grok 4.2 | `xAI/grok-4.2.md` | 5 |
| Grok | Grok 4.3 Beta | `xAI/grok-4.3-beta.md` | 6 |
| Grok | API | `xAI/grok-api.md` | 3 |
| Grok | Build | `xAI/grok-build.md` | 5 |
| Grok | Personas | `xAI/grok-personas.md` | 4 |
| Grok | Account | `xAI/grok-account.md` | 4 |
| Grok | Expert | `xAI/grok-expert.md` | 4 |
| Grok | Post Safety | `xAI/grok.com-post-new-safety-instructions.md` | 4 |
| Microsoft Copilot | GitHub Copilot | `Microsoft/github-copilot.md` | 5 |
| Microsoft Copilot | VS Code Copilot Agent | `Microsoft/vscode-copilot-agent.md` | 5 |
| Microsoft Copilot | Copilot CLI | `Microsoft/copilot-cli.md` | 5 |
| Microsoft Copilot | Copilot in Word | `Microsoft/copilot-in-microsoft-word.md` | 5 |
| Microsoft Copilot | macOS App | `Microsoft/copilot-macos-app.md` | 5 |

## 发布前检查

发布模型页面前必须确认：

- 没有 `TODO`、`unknown`、`unverified` 留在 `source.source_path` 或 `source.source_commit`。
- 页面中每个英文摘录都必须通过 `data-source-label` 绑定到 `quoted_lines` 中的对应项。
- 版本 diff 的依据能追溯到两个明确的 `source_commit` 或同一来源仓库中的两个明确文件。
- 如果使用第三方仓库素材，README 和页面脚注必须说明来源与许可证。
- 作者观点必须写在分析字段中，不能伪装成原文事实。
- `words`、`lines` 统计应和 `prompt` 原文实际内容保持一致。

## 后续维护

新增模型或版本时，先补 `data/*.json` 的来源字段，再生成页面。若上游素材库更新，请新建版本记录并固定新的 commit，不要直接覆盖已经发布的来源指针。
