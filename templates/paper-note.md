---
title: "{{title}}"
authors: []
year:
venue: ""
arxiv: ""
code: ""
date_added: {{date}}
tags: [research/]
status: read
---

# {{title}}

> [!abstract] Quick card — 30 seconds to recover this paper
> - **One-liner**: {{who, with what method, on what task, achieved what}}
> - **Where others got stuck**: {{the specific failure mode of prior art, not "it did not work well"}}
> - **This paper's cut**: {{the single thing it adds}}
> - **Strongest number**: {{metric from X to Y (units), under what condition}}
> - **For me**: {{borrow / adapt / compare-against / unrelated but worth knowing}}
> - **Verdict**: {{real advance | incremental | engineering integration}}

---

## 1. Problem and motivation

{{the clinical / engineering problem, and why now. One paragraph, not a paraphrase of the abstract.}}

---

<!-- Writing note (not rendered): S2 is the first reason this note exists. If it is vague, the paper was not actually read. -->
## 2. Research gap and novelty

### Limitations of prior work
- **{{prior method 1}}** — {{the specific condition under which it fails; quote the paper where it states this}}
- **{{prior method 2}}** — {{same}}

### The exact gap
> Prior {{X}} cannot {{Y}} under {{Z}}; this paper does.

### Novelty claims
| Type | Claim | Genuinely new? |
|---|---|---|
| Architectural | {{structure / sensor / geometry}} | {{yes / partly / repackaged}} |
| Algorithmic | {{loss / estimator / control law}} | |
| Experimental | {{dataset / in-vivo / benchmark}} | |

### Why it stayed open
- {{the technical / data / requirements barrier that kept the gap open — this decides whether it is a real advance or incremental}}

---

## 3. Method

{{high-level pipeline in 1-3 sentences. Draw complex structure in mermaid; do not redraw a paper figure — embed it.}}

```mermaid
flowchart LR
  A[{{input}}] --> B[{{stage}}] --> C[{{output}}]
```

### 3.1 {{Component}}
{{use the paper's own naming}}

### 3.2 {{Component}}

### 3.3 Training / data details

---

## 4. Mathematical foundation

<!-- Writing note: the bar is that you could reconstruct the equation from this section, not just recognise it. -->
### 4.1 {{Equation name}}

{{one line: what this computes}}

$$
{{equation}}
$$

| Symbol | Meaning | Unit / dimension |
|---|---|---|
| $x_k$ | {{...}} | {{m, m/s}} |

**How to read it**: {{which term dominates when; what it reduces to in the limit}}

---

## 5. Experimental setup

| | |
|---|---|
| **Dataset / phantom / model** | {{...}} |
| **Hardware** | {{...}} |
| **Baselines** | {{...}} |
| **Metrics** | {{...}} |
| **Key hyperparameters** | {{...}} |

---

## 6. Key results

**Headline:** {{one sentence, with numbers}}

| Metric | Baseline | Ours | Delta |
|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} |

### 6.1 Ablation — which component is actually doing the work
- {{remove X and see how much it drops}}

---

## 7. Limitations and future work

**Author-stated:**
- {{...}}

**I noticed but the authors did not say:**
- {{a baseline they did not run / a metric that hides the failure mode / phantom validation sold as clinical / n too small}}

**Author-stated future work:**
- {{what they say comes next — this is the field's public roadmap; anything on it is a crowded lane}}

---

<!-- Writing note: S8 is the second reason this note exists. Without it the note is a second-hand abstract. -->
## 8. Synthesis — my take

**Verdict:** {{real advance / incremental / engineering integration — and on which result or ablation}}

**What transfers to my work:**
- *Borrow*: {{a method or trick to reuse as-is}}
- *Adapt*: {{what, and which part must change}}
- *Compare against*: {{a baseline I must now beat or cite}}

**Research openings:**

> [!question] O1 — {{one sentence, phrased as something buildable}}
> - **Why still open**: {{what this paper or the prior art leaves unresolved — point back to S2 or S7}}
> - **First experiment**: {{the smallest thing that would falsify it}}
> - **Feeds**: [[{{topic-slug}}]]

> [!question] O2 — {{...}}
> - **Why still open**: {{...}}
> - **First experiment**: {{...}}
> - **Feeds**: [[{{topic-slug}}]]

<!-- Writing note: two or three sharp openings beat six vague ones. Zero is legitimate — write "no opening worth taking: <why>" rather than manufacturing one. -->

**What I would do differently:** {{the experiment that should have been run / the baseline that should have been included}}

---

## 9. Useful citation sentence

> {{a quotable line}}
>
> — {{full reference}}

---

## 10. Paper figures and attachments

```bash
python ~/.claude/skills/paper-figures/scripts/extract-figures.py \
  {{pdf-path}} <AI_WIKI>/_attachments/paper-figures/{{slug}}
```

| Asset | File | Embedded in | Content |
|---|---|---|---|
| Fig. 1 | `fig1.png` | S1 | {{...}} |

**Extracted but not embedded:** {{...}}

---

## Related links

- [[{{topic-moc}}]] — the mandatory back-link
- [[{{related-paper}}]]
