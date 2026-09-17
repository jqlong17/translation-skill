# Linguistics Translation Reference

## Reference scope

Use this file when translating linguistics, cognitive-science, psychology, psycholinguistics, grammar, syntax, semantics, or language-processing books into Chinese.

- Source language: usually English, but the principles also apply to other source languages.
- Target language: Simplified Chinese.
- Intended register: readable university-level textbook prose; precise, direct, mildly conversational when the source allows.
- Argumentative sensitivity: preserve the author's evidential strength and critical tone without intensifying either.
- Evidence sensitivity: examples, judgments, formulas, diagrams, glosses, acceptability markers, and notation often carry the argument. Preserve them unless the user explicitly asks otherwise or the surrounding text clearly treats them as ordinary prose.

Translate prose, headings, captions, notes, and navigational text. Preserve research examples and image assets during the first pass.

## Initial glossary

These are defaults, not context-free substitutions. Record justified exceptions in the book glossary.

| English | Chinese |
|---|---|
| syntax | 句法 |
| grammar | 语法 |
| cognitive approach | 认知取向 |
| dependency grammar | 依存语法 |
| dependency | 依存关系；依存项（按语境） |
| head | 中心词 |
| dependent | 依存项 |
| constituent / constituency | 成分／成分关系 |
| phrase structure grammar | 短语结构语法 |
| construction grammar | 构式语法 |
| combinatory categorial grammar | 组合范畴语法 |
| X-bar phrase structure | X-bar 短语结构 |
| transformation-based theory | 基于转换的理论 |
| acceptability | 可接受性 |
| acceptability judgment task | 可接受性判断任务 |
| grammaticality | 合语法性 |
| corpus analysis | 语料库分析 |
| morphology | 形态学 |
| morpheme | 语素 |
| phoneme | 音位 |
| lexicon | 词库 |
| core lexicon | 核心词库 |
| communal lexicon | 社群词库 |
| idiolect | 个人方言 |
| discourse structure | 话语结构 |
| compositionality | 组合性 |
| part of speech | 词类 |
| determiner | 限定词 |
| article | 冠词 |
| subordinator | 从属词 |
| complementizer | 标句词 |
| category feature | 范畴特征 |
| unification | 合一 |
| argument | 论元 |
| modifier | 修饰语 |
| complement clause | 补语从句 |
| passive construction | 被动构式 |
| coordination | 并列结构 |
| lexical ambiguity | 词汇歧义 |
| syntactic ambiguity | 句法歧义 |
| long-distance dependency | 长距离依存关系 |
| dependency locality | 依存局部性 |
| dependency length | 依存距离 |
| dependency length minimization | 依存距离最小化 |
| locality bias | 局部性偏好 |
| on-line effect | 在线加工效应 |
| nested structure | 嵌套结构 |
| distance metric | 距离度量 |
| harmonic word order | 和谐语序 |
| crossed dependencies | 交叉依存关系 |
| syntactic island | 句法岛 |
| learnability | 可学习性 |
| language network | 语言网络 |
| language processing | 语言加工 |
| language production | 语言产出 |
| language comprehension | 语言理解 |
| noisy channel | 噪声信道 |
| noisy-channel processing | 噪声信道加工 |
| rational inference | 理性推断 |
| surprisal | 惊奇度 |
| resource-rational | 资源理性 |
| lossy context | 有损语境 |
| resource-rational lossy-context surprisal | 资源理性有损语境惊奇度 |
| large language model (LLM) | 大语言模型（LLM） |

## Decisions that require context

Do not resolve these by global search-and-replace:

- `representation`: use `表征` for mental/linguistic representations; use `表示` for notation or display.
- `structure`: usually `结构`; distinguish syntactic, dependency, conceptual, and information structure.
- `category`: usually `范畴`; use `类别` for ordinary classification.
- `reference`: use `指称` in semantics and `引用／参考文献` in publishing contexts.
- `processing`: usually `加工` in psycholinguistics, not `处理`.
- `production`: use `语言产出` for speaking/writing processes, not generic `生产`.
- `comprehender`: prefer `理解者`; avoid inventing a rigid technical label when `听者／读者` is contextually intended.
- `locality`: use `局部性` for the theoretical construct, not `本地性`.
- `legalese`: use `法律文体` or `法律语言` according to whether style or domain language is intended.
- `claim`: distinguish `主张`, `断言`, and `论点` by force and role.

## Handling examples

### Keep English only

Keep the source unchanged when the passage tests:

- word order;
- attachment or scope ambiguity;
- morphology or agreement;
- head-dependent relationships;
- extraction or island effects;
- acceptability contrasts;
- lexical choice or frequency;
- noisy-channel edits;
- prosody tied to English form.

Translate the surrounding explanation. If needed, add a short Chinese semantic gloss after the example, clearly marked `（大意：……）`.

### Keep English plus Chinese

Use both when semantic content matters to the argument but the Chinese wording is not itself evidence. Place Chinese after the complete English example; never insert Chinese words into a tested English string.

### Translate normally

Translate ordinary illustrative prose that is not treated as linguistic data. When uncertain, keep the English and flag the item for review.

## Figures, tables, notes, and equations

- Preserve image-based trees and equations exactly in the first translated EPUB.
- Translate captions and prose references such as “figure 3.2” consistently as `图 3.2`.
- Preserve symbolic node labels unless the prose explicitly defines localized equivalents.
- Translate textual tables cell by cell while preserving row/column relationships.
- Keep footnote/endnote IDs and backlinks unchanged.
- Preserve equation numbering, variables, operators, and MathML structure.

## Review checklist for each chapter

1. Compare heading hierarchy and paragraph count with the source.
2. Check every linguistic example and acceptability marker.
3. Check all figure/table/note references.
4. Verify glossary terms and ambiguous-term decisions.
5. Read the Chinese alone for coherence.
6. Back-check claims containing negation, quantification, comparison, causality, or criticism.
7. Record unresolved items instead of guessing.
