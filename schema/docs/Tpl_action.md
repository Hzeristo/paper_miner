---
type: decision
id: "{{date:YYYYMMDDHHmm}}"
title: "{{DECISION_ACTION_VERB}} {{TARGET}}"
date: "{{date:YYYY-MM-DD}}"
outcome: "{{OUTCOME: Pending/Success/Failure/Pivot}}"
tags: [decision, strategy, "{{PROJECT_TAG}}"]

graph_edges:
  based_on: []      # 对应正文的 Based On (Insight)
  triggered_by: []  # 对应正文的 Triggered By (Thought/Knowledge)
  impacts: []       # 对应正文的 Impacts (Project)
---

# 🎬 Decision: {{DECISION_ACTION_VERB}} {{TARGET}}

> **Status**: executed / planned / pivoted
> **Owner**: User (The Architect)

---

## 1. The Snapshot (Context)
> **Context**: <INSTRUCTION: Describe the situation.>
> **Constraints**: <INSTRUCTION: Time/Budget/Compute limits.>

---

## 2. The Path Not Taken (Counterfactuals)
*   ❌ **I rejected**: {{OPTION_B}}
    *   **Reason**: <INSTRUCTION: Why?>
*   ❌ **I rejected**: {{OPTION_C}}
    *   **Reason**: ...

---

## 3. The Commitment (Collapse)
> **I have decided to**: {{SELECTED_ACTION}}

**The "Why" (Causality Anchor)**:
*   **Rationale**: <INSTRUCTION: Connect Insight to Constraint.>

---

## 4. Prediction (Bayesian Bet)
*   **Success Metric**: <INSTRUCTION: How do I know I was right?>
*   **Risk Acceptance**: <INSTRUCTION: I accept the risk that...>

---

## 5. Graph Topology (Edges)
⚠️ *Sync this section with YAML.*

- **Based On (Insight)**:
  - [[Insight/...]]

- **Triggered By (Thought/Knowledge)**:
  - [[Thought/...]]


---
*Signed by: User*
