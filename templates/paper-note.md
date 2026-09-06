---
title: "{{title}}"
authors: []
year:
venue: ""
arxiv: ""
doi: ""
code: ""
date_added: {{date}}
tags: [research/]
status: read
subarea: ""          # sub-area letter in the owning hub ("C, D" if it spans two); blank if unfiled
tagline: ""          # one-line placement, <=40 chars; feeds the hub's S0.5 paper map
---

# {{title}}

> [!abstract] Quick card
> - **Problem being solved**: {{the specific task and conditions. Not "improves performance"}}
> - **Why existing methods fall short**: {{the concrete failure point of prior work — under what condition, and how it fails}}
> - **What this paper does**: {{plain-language description of the method: what goes in, what is computed, what comes out. After this line the reader should know what the paper actually does}}
> - **Main result**: {{key metric X to Y (units), on what data / under what condition, compared against whom}}
> - **Conclusion**: {{real advance / incremental improvement / engineering integration — on the evidence of which specific result}}
> - **Use to me**: {{borrow as-is / needs adaptation / use as a baseline / unrelated but worth knowing}}

---

<!-- Writing note (not rendered): S0 answers "what does this paper actually do". Write it for someone who knows the field basics but has not read this paper. No jargon dumping; explain each proper noun on first use. If you cannot write this section, you have not understood the paper yet — stop and reread. -->
## 0. What this paper does, in plain language

{{3-5 sentences, in this order: the situation they face, what they built, why it works, what they got.}}

---

## 1. Problem and motivation

{{the clinical / engineering problem, and why now. One paragraph, not a paraphrase of the abstract. S0 covers "what they did"; this covers "why it is worth doing".}}

---

<!-- Writing note: S2 is the first reason this note exists. Generic prose here means the paper was not actually read. -->
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

### Why the gap stayed open
- {{the technical, data, or requirements barrier that blocked prior work — this decides whether it is a real advance or incremental}}

---

## 3. Method

{{high-level pipeline in 1-3 sentences. Draw complex structure in mermaid; embed a paper figure rather than redrawing it.}}

```mermaid
flowchart LR
  A[{{input}}] --> B[{{stage}}] --> C[{{output}}]
```

### 3.1 {{Component}}
{{use the paper's own naming}}

### 3.2 {{Component}}

### 3.3 Training and data details

---

## 4. Mathematical foundation

<!-- Writing note: the bar is that you could reconstruct the equation from this section, not merely recognise it. -->
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

| Metric | Baseline | This paper | Delta |
|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} |

### 6.1 Ablation: which component contributes the performance
- {{remove X and see how much it drops}}

---

## 7. Limitations and future work

**Author-stated limitations:**
- {{...}}

**Problems the authors do not mention, but I believe exist:**
- {{a baseline they did not run / a metric that hides the failure mode / phantom validation sold as a clinical conclusion / sample size too small for the claimed effect}}

**Author-stated future work:**
- {{what they say comes next — the field's public roadmap; anything already on it is a crowded lane}}

---

<!-- Writing note: S8 is the second reason this note exists. Without it the note is a second-hand abstract. -->
## 8. My analysis and judgement

**Conclusion and evidence:** {{real advance / incremental improvement / engineering integration — on which specific result or ablation}}

**What transfers to my work:**
- *Borrow as-is*: {{a method or technique reusable without change}}
- *Needs adaptation*: {{what, and which part must change}}
- *Use as a baseline*: {{what I must now beat or cite}}

**Research opportunities:**

> [!question] O1 — {{one sentence, phrased as something buildable}}
> - **Why it is still unsolved**: {{what this paper or the prior art leaves open — point back to S2 or S7}}
> - **First experiment**: {{the smallest thing that would falsify it}}
> - **Files under topic**: [[{{topic-slug}}]]

> [!question] O2 — {{...}}
> - **Why it is still unsolved**: {{...}}
> - **First experiment**: {{...}}
> - **Files under topic**: [[{{topic-slug}}]]

<!-- Writing note: two or three specific opportunities beat six vague ones. Zero is a legitimate answer — write "no opportunity worth taking: <why>" rather than manufacturing one. -->

**Experiments I think should have been run:** {{the experiment that was missing / the baseline that should have been included}}

---

## 9. Quotable sentence

> {{a directly quotable line}}
>
> — {{full reference}}

---

## 10. Figures and attachments

```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/paper-figures/scripts/extract-figures.py \
  {{pdf-path}} <AI_WIKI>/_attachments/paper-figures/{{slug}}
```

<!-- Writing note: the number of ../ segments depends on this note's depth.
     Research/papers/<topic-slug>/ uses ../../../_attachments/...
     Research/papers/ (root)       uses ../../_attachments/...
     The attachment tree stays flat. After moving a note, fix the prefix or the
     images silently stop rendering. -->


| Asset | File | Embedded in | Content |
|---|---|---|---|
| Fig. 1 | `fig1.png` | S1 | {{...}} |

**Extracted but not embedded:** {{...}}

---

## Related links

- [[{{topic-moc}}]] — required back-link when the note is filed under a topic
- [[{{related-paper}}]]
