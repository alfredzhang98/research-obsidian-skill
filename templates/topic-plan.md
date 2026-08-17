---
title: "{{TOPIC_TITLE}}"
type: topic-plan
mode: "{{MODE}}"
date_started: "{{DATE}}"
updated: "{{DATE}}"
tags:
  - topic
  - "research/{{AREA_SLUG}}"
status: "{{STATUS}}"
---

# {{TOPIC_TITLE}}

> [!abstract] Quick card
> **Central question:** {{CENTRAL_QUESTION}}
> **Current bet:** {{CURRENT_BET_AND_WHY}}
> **Progress:** {{PROGRESS_SUMMARY}}

<!-- MODE is lightweight or full. Refresh this card whenever the topic plan changes. -->

## 1. Scope and central question

{{SCOPE_SUMMARY}}

**Central question:** {{CENTRAL_QUESTION}}

**In scope:**

- {{IN_SCOPE_ITEM}}

**Out of scope:**

- {{OUT_OF_SCOPE_ITEM}}

<!-- For lightweight mode, a concise direction summary is sufficient; do not invent detailed boundaries. -->

## 2. Sub-questions and sub-areas

| Sub-area | Question | Tag | Status |
|---|---|---|---|
| {{SUB_AREA}} | {{SUB_QUESTION}} | `research/{{SUB_AREA_SLUG}}` | {{STATUS}} |

## 3. Search strategy

{{SEARCH_STATUS_OR_STRATEGY}}

<!-- In lightweight mode, write exactly: No systematic search run yet. In full mode, record only searches that will actually be run. -->

### Queries

- `{{VERBATIM_SEARCH_QUERY}}`

### Sources and seeds

- **Sources or venues:** {{SOURCE_OR_VENUE}}
- **Seed authors or works:** {{SEED_AUTHOR_OR_WORK}}
- **Time window:** {{TIME_WINDOW}}
- **Inclusion criteria:** {{INCLUSION_CRITERIA}}
- **Exclusion criteria:** {{EXCLUSION_CRITERIA}}

## 4. Reading queue

<!-- Keep provenance blocks separate. Remove a block only when it is genuinely empty. -->

### User-supplied

Origin: material supplied directly for this topic.

| Paper | Sub-area | Priority | Status | Note |
|---|---|---|---|---|
| {{PAPER_CITATION}} | {{SUB_AREA}} | {{PRIORITY}} | {{READING_STATUS}} | [[{{PAPER_NOTE_SLUG}}]] |

### From bibliographies

Origin: recommendations found in the bibliography of an already reviewed paper.

| Paper | Recommended by | Sub-area | Priority | Status | Note |
|---|---|---|---|---|---|
| {{PAPER_CITATION}} | [[{{SOURCE_PAPER_NOTE_SLUG}}]] | {{SUB_AREA}} | {{PRIORITY}} | {{READING_STATUS}} | [[{{PAPER_NOTE_SLUG}}]] |

### Search hits

Origin: results from a recorded search query.

**Query:** `{{QUERY_THAT_PRODUCED_THE_HITS}}`

| Paper | Sub-area | Priority | Status | Note |
|---|---|---|---|---|
| {{PAPER_CITATION}} | {{SUB_AREA}} | {{PRIORITY}} | {{READING_STATUS}} | [[{{PAPER_NOTE_SLUG}}]] |

## 5. Synthesis and open questions

### Current synthesis

{{CURRENT_SYNTHESIS_WITH_EVIDENCE_SCOPE}}

### Agreements

- {{POINT_OF_AGREEMENT}} — supported by [[{{SUPPORTING_NOTE_SLUG}}]]

### Contradictions

- {{CONTRADICTION}} — compare [[{{NOTE_A_SLUG}}]] with [[{{NOTE_B_SLUG}}]]

### Open questions

- {{SPECIFIC_OPEN_QUESTION}}

## 6. Linked notes

### {{SUB_AREA}}

- [[{{PAPER_OR_LEARNING_NOTE_SLUG}}]] — {{ONE_LINE_RELEVANCE}}
