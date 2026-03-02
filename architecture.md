# 🧬 Project Chimera: Architecture & Context Blueprint

**Target Audience:** Human Architects, AI Assistants (via explicit read).
**Version:** v1.0 (Phase-3 Filter focus)
**Companion Doc:** See `.cursorrules` for strict coding behaviors and constraints.

---

## 1. 系统哲学 (The System Philosophy)

Project Chimera (PaperMiner) 绝不是一个传统的增删改查 (CRUD) 单体应用。它是一个**外显的认知系统 (Exocortex)**，其核心特征如下：

*   **人类是唯一阀门 (Human as the Only Gate)**：
    系统（LLM）负责产生高维度的噪音过滤（ Reject/Skim/MustRead）和洞察生成。但最终只有**人类**有权将它固化到 Obsidian (The Vault) 中。
*   **状态即位置 (State is Location)**：
    系统中不使用复杂的 SQL 数据库来记录“这篇论文处理到哪了”。文件的物理位置决定了它的状态流转：
    `arxivpdf/` (Inbox) -> `md_papers/` (Processed & Ready for LLM) -> `filtered/` (Archived).
*   **非即时流水线 (Asynchronous Pipeline)**：
    各个模块（爬取、解析、大模型分析）是松散耦合的脚本。MinerU 转换可以今天跑，DeepSeek 分析可以明天跑。系统必须**容忍断点**，随时可重入。

---

## 2. 知识本体论 (The Vault Ontology)

本项目最终对接的是 Obsidian 知识库。我们在 `schema/docs/` 中定义了严格的四层认知节点：

1.  **Knowledge (📄)**: 客观真理、论文原文、冷文本。严禁主观判断。（由系统提取生成）
2.  **Thought (💭)**: 思考、重述、理解模型。允许推翻，通过追加日志记录演化。（Human + AI 辅助）
3.  **Insight (💡)**: 跨域类比、已被验证的底层假设。数量极少。（核心锚点）
4.  **Decision/Action (⚡)**: 基于洞察作出的研究方向或工程决策。

**系统的终极目标是：自动化生成完美的 Knowledge 节点，并辅助构建 Thought 节点。**

---

## 3. 模块映射图 (Module Map)

本项目采用**领域驱动（类 DDD）**的扁平架构。

### 🧊 `src/core/` (不可变内核)
系统的“法律定义”。只包含纯数据结构（Pydantic）。
*   `config.py`: 配置中心。
*   `paper.py`: 贯穿全局的数据实体 (`Paper` class)。
*   `verdict.py`: AI 裁决的结果枚举和分数对象。

### 🦾 `src/io_adapter/` (与现实世界的物理接口)
所有脏活累活都在这里。此层**不作任何业务决策**。
*   `paper2md.py` (MinerU Wrapper): 接受 PDF 路径，扔出 Markdown 路径。屏蔽子进程错误。
*   *(Planned)* `vault_writer.py`: 接受 `Verdict` 对象，渲染为符合 Obsidian Ontology 的 Markdown 文件。

### 🧠 `src/llm_gateway/` (脑机接口)
LLM 不是管道，它是工具。
*   `prompt_manager.py`: 管理和组装基于 Jinja2 (`prompts/`) 的提示词树。
*   *(Planned)* `llm_client.py`: 封装各种提供商 (DeepSeek/Gemini)，统一输入字符串，严格输出清洗后的 Pydantic 模型。

### ⚖️ `src/decision/` (逻辑引擎)
连接 Core、Gateway 和 IO 的桥梁。
*   包含如 `filter_engine.py` 等判断逻辑：“如果得分 < 5，移动到垃圾箱”。

### 🎬 `src/workflows/` (编排与剧本)
提供给 CLI 或外部调用的入口。
*   `batch_filter.py`: "运行整个 Pipeline" 的最高层抽象。串联所有的 Adapter 和 Engine。

---

## 4. 废弃地带 (The Graveyard)

### 🗑️ `src/utils/`
*当前状态：包含旧时代的混沌代码（`pdf2md.py`, `prompt.py`）。*
**迁移指令**：此目录下的代码没有架构意识。任何触碰此目录的行为，都应该伴随着将逻辑解耦并上推至 `io_adapter` 或 `llm_gateway` 的重构过程。最终目标是销毁该目录。
