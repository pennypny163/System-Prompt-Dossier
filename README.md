# System Prompt Dossier · 大模型人格档案

> 把看不见的 system prompt 拆开，看清每个 AI 的真实人格、能力边界与进化史。

本项目对主流大模型的 **system prompt** 进行中文拆解与人格分析，聚焦**复杂企业环境下的 Agent**。区别于单纯收集 prompt 原文，本项目提供：

- **双版本人格画像** —— 面向大学生的科普版 + 面向行业 KA 高层的授课版，用生动的人像比喻
- **八维拆解骨架** —— 基于业界方法论提炼的标准分析框架
- **版本演进时间线 + Prompt Diff** —— 还原每个模型"护栏一步步加上"的政策进化史
- **完整原文阅读入口** —— 每个历史版本的 system prompt 全文可查

---

## 八维拆解骨架

每个模型的拆解都沿用同一套维度，确保结论有据可依、可对比、可复现：

| 维度 | 拆什么 | 理论出处 |
|------|--------|----------|
| **D1 身份 / 人格** | 它把自己当成"谁"？ | COSTAR · Claude's Constitution |
| **D2 指令权限层级** | 冲突时谁说了算？ | OpenAI Model Spec (instruction hierarchy) |
| **D3 安全红线** | 绝对不做的是什么？ | Claude's Constitution (hard constraints) |
| **D4 工具调用规则** | 何时搜索 / 拒绝 / 动手？ | CL4R1T4S (Tool-Use Schema) |
| **D5 商业优先级** | 是否偏向自家产品？ | The Moat is a Config File |
| **D6 运行时干预** | 对话中途会被"插话"吗？ | 实时分类器干预 / anthropic_reminders |
| **D7 跨版本 Diff** | 护栏是怎么一步步加上的？ | CL4R1T4S (Prompt Archaeology) |
| **D8 Token 体量** | 为"安全"付出多少成本？ | CL4R1T4S (context tax) |

核心心智模型（来自 HackerNoon《The Moat is a Config File》）：

> **The system prompt IS the product.**
> LLM 正在变成商品层，产品的差异化几乎全部活在那份看不见的配置里。

---

## 仓库结构

```
.
├── methodology.html              方法论说明页（开篇理论框架）
├── claude-sample.html            Claude 拆解样张（含版本时间线 + 完整 prompt 阅读入口）
├── claude-versions-data.json     Claude 历代版本数据（脚本生成）
├── build_versions.py             从原库读取各版本原文 + 中文分析的构建脚本
├── inject_reader.py              将版本数据注入 HTML 阅读层的脚本
└── system_prompts_leaks/         system prompt 原文素材库（见下方致谢）
```

直接用浏览器打开 `methodology.html` 与 `claude-sample.html` 即可查看。

---

## 致谢与来源

本项目的 prompt 原文素材库 `system_prompts_leaks/` 基于
[**asgeirtj/system_prompts_leaks**](https://github.com/asgeirtj/system_prompts_leaks)
（CC0-1.0 协议），在此致谢。

分析方法论综合自以下公开来源：

- [elder-plinius/CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S) — 泄露 prompt 研究库与"提示词考古"方法论
- The 'Moat' is a Config File — HackerNoon, 2026
- [Claude's Constitution](https://www.anthropic.com/constitution) — Anthropic 官方，CC0 1.0
- OpenAI Model Spec — instruction hierarchy
- COSTAR Framework — Sheila Teo（新加坡首届 GPT-4 Prompt Engineering 赛冠军）
- Constitutional AI: Harmlessness from AI Feedback — Anthropic

---

## 协议

本仓库的拆解分析内容与原文素材均沿用 **CC0-1.0**，可自由使用。
