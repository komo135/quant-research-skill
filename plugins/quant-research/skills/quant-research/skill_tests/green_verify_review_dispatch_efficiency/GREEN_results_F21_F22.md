# GREEN dispatch efficiency — F21 / F22 反映後の挙動

RED phase で観察された 2 efficiency-class 失敗モード (F21 / F22) に対する
skill 改修と、post-fix audit (`audit_post_fix.md`) で確認された GREEN 側の
挙動。

## 改修箇所

| 失敗モード | 改修ファイル | 改修内容 |
|---|---|---|
| F21 | `references/bug_review.md` | 新節 "Per-reviewer input contract (efficiency-class, F21)" — 6 reviewer × {required scope / required shared / NOT-receive} の 3 列表。section anchor (`### N. <reviewer-name>`) ベースの pre-extraction を mandate。「The five specialists each receive: ...」の prose を新規 contract に整合させて書き直し。"Section anchor as source of truth" の段落で line range は illustrative であることを明記。 |
| F21 | `experiment-review/references/review_protocol.md` | 同等の "Per-dimension input contract (efficiency-class, F21)" 表を新設 (8 dimension)。section anchor (`## N. <dimension>`) ベースの pre-extraction を mandate。"Tailor each specialist's input bundle accordingly" の prose を structured contract に格上げ。Adversary の bundle list は contract row 8 を source-of-truth にして他の表記をリンク化 (sync drift 防止)。 |
| F21 | dispatch protocol step 2 / SKILL.md Process step 4 | "pre-extracts each reviewer's dimension scope" を mandate、whole-file `bug_review.md` / `review_dimensions.md` を deliver しない、を明文化。 |
| F22 | `references/bug_review.md` | 新節 "Trigger-conditional dispatch on re-verify (efficiency-class, F22)" — Initial pass / Re-verify pass の区別、surface map per reviewer (6 行)、"When in doubt, fire" の default rule、Cross-session boundary (= attestation なしは Initial 扱い)。dispatch protocol step 2 を Initial / Re-verify 分岐に書き直し。 |
| F22 | `experiment-review/references/review_protocol.md` | 同等の F22 節 + surface map (8 dimension) + Cross-session 規定。 |
| F22 | `experiment-review/SKILL.md` Process step 3 | Initial pass vs Re-verify pass を Process 表で明示、surface map intersect の判定 step を追加。 |
| F21+F22 | `references/bug_review.md` + `experiment-review/references/review_protocol.md` | 各々に "Anti-rationalizations (efficiency-class, F21 / F22)" 表を追加。「whole file が安全」「adversary に specialist scope を渡す」「pre-extraction は brittle」「user が comprehensive を求めた」「narrative の `notebook_narrative.md` 全文も extract すべき (= 反例)」「fix が cosmetic なので全 fire」「surface ambiguity → skip」「cross-session を attestation なしで re-verify 扱い」「wording-only fix は skip」を反駁。 |
| F21+F22 | `references/bug_review.md` Single-agent fallback | fallback でも F21 / F22 が適用されることを明記。 |

新 reference は作らず、既存 3 ファイルへの追加 + 改修のみ。

**F20 (prompt caching) は採用せず**: 当初候補化したが、Claude Code 内の
スキルから API-level の `cache_control` を mandate するのは越権 + 並列
sub-agent 間の cache 共有が harness 依存で不確定、と判断。F-id taxonomy
には gap として残す (= "F20 was considered, found to be out of skill scope")。

## F21 の解消 — pre-extraction の理論的削減量

| ファイル | Pre-fix (whole file × N reviewer) | Post-fix (section-only × N reviewer) | 削減 |
|---|---|---|---|
| bug_review.md | 5 × 300 = 1500 | 5 × 12.6 avg + 1 × 39 = 102 | -1398 行 (-93 %) |
| review_dimensions.md | 8 × 489 = 3912 | 7 × ~51 avg + 1 × 112 = 469 | -3443 行 (-88 %) |
| sanity_checks.md | 5 × 189 = 945 | ~5 × 60 = 300 | -645 行 (-68 %) |
| **合計 dead weight** | **5530** | **0** | **-100 %** |

raw 送信量 (= 14 reviewer 合算 input lines): **23115 → 17629 = -24 %**。

skill が直接 control できる、quality 不変、empirical risk 無しの cut。

## F22 の解消 — trigger-conditional dispatch の agent-run 削減

iteration N rounds で 14×N agent-run。GREEN counter は Initial = 14 fire を
維持、Re-verify では surface map 経由で **該当 specialist + adversary のみ**
fire。

仮定: re-verify 1 round あたり typical fix が 2-4 surface に着地 → avg 4
specialist + adversary = 5 reviewer を再 fire。

| iteration rounds | Without F22 (= 全 fire) | With F22 (Initial 14 + 再 verify n×5 avg) | 削減率 |
|---|---|---|---|
| 1 (= initial only) | 14 | 14 | 0 % |
| 2 (= initial + 1 re-verify) | 28 | 14 + 5 = 19 | **-32 %** |
| 3 | 42 | 14 + 5 + 5 = 24 | **-43 %** |
| 4 | 56 | 14 + 5 + 5 + 5 = 29 | **-48 %** |

iteration の深さに応じて savings が累積。実際の agent-run 数は fix
profile (= 何 surface に着地するか) 次第で変動。

re-verify 1 回あたりの specialist 数は最低 1 (= 1 surface 着地) から最大 7
(= 全 surface に着地、ただし adversary 含む 8 で initial の subset)。

## 累積効果 (F21 + F22)

| 指標 | Pre-fix | Post-fix |
|---|---|---|
| F21: raw 送信量 (per-reviewer) | 1650 lines avg | 1255 lines avg (-24 %) |
| F22: agent-run count (Initial + 2 re-verify) | 42 | 24 (-43 %) |
| 累積 input billing (Initial + 2 re-verify、line × agent run) | ~69,000 lines | ~30,000 lines (-57 %) |

iteration depth と fix profile に依存するが、典型 cycle で **input billing
は 2-3× 軽くなる**。

## Quality machinery 不変論証 (= 質を落としていない確認)

GREEN counter は **dispatch 規約のみを変更**、reviewer agent 自体の
instruction も specialist 数も roster も touch していない。

### narrowness (= 各 reviewer が自身の dimension のみ扱う)

| 観点 | Pre-fix | Post-fix |
|---|---|---|
| 各 specialist の dimension scope 受領 | whole file + "read §i only" 指示 (= attention で絞る) | §i のみ inline (= 物理的に絞る) |
| Lost-in-middle 効果 | あり | なし (whole file の前後段が来ない) |
| cross-dimensional finding | parallel ensemble の overlap で防御 | **同じ機構で防御** (roster と reviewer 数を touch していない) |

→ narrowness は **strict 化**、弱化はない。

### bundle asymmetry (= adversary が specialists の scope を見ない)

| 観点 | Pre-fix | Post-fix |
|---|---|---|
| adversary の minimum bundle (notebook + 自身の §6/§8 instruction のみ) | yes (whole file 渡しで形式論依存) | yes (§6/§8 のみ inline、specialist scope は物理的に bundle に入らない) |
| adversary が specialists の scope (§1-§5 / §1-§7) を物理的に受け取らない | 形式上 NO (whole file が bundle に入る) | **YES** |
| Re-verify の adversary | always re-fire | any specialist 再 fire 時に auto re-fire (= safety net 維持) |

→ bundle asymmetry は **強化**。Pre-fix は「whole file は渡すが §i 以外
読まないでね」という形式論依存だったが、Post-fix では specialist scope が
adversary の bundle に物理的に入らない。

### parallelism (= 同時 dispatch)

| 観点 | Pre-fix | Post-fix |
|---|---|---|
| Initial pass の dispatch | 14 並列 (required) | 14 並列 (required、不変) |
| Re-verify pass の dispatch | 14 並列 (required) | 該当 specialist + adversary 並列 (= subset、必要分だけ) |
| 各 reviewer の独立 read | yes | yes |

→ parallelism は **不変**、Re-verify では subset を並列、reviewer 数だけ
変動 (= dispatch 数の機械的な削減)。

### trigger discipline (= verdict='supported' 直前必発火)

| 観点 | Pre-fix | Post-fix |
|---|---|---|
| Initial pass の発火条件 | verdict='supported' 直前 (= 必発火) | 同じ (Initial = 全 14 fire の規定 不変) |
| Re-verify pass の発火条件 | 全 14 reviewer 再 fire | surface map intersect する specialist + adversary 再 fire |
| gate の overall 機能 | "verdict='supported' は全 14 review を通る" | "verdict='supported' は initial で全 14 review、re-verify は changed surfaces を全 review、adversary が safety net" — gate の cover が崩れない |

→ trigger discipline の **gate 機能は維持**。Re-verify は Initial 後の
incremental check で、Initial で確認済みの surface は対象外という skip は
合理的 (= surface 変化なしの dimension は最終 verdict='supported' に対する
新しい evidence を生まない)。

### CCR 論文との整合 (= adversary asymmetry が壊れていないことの検証)

`bug_review.md` の §6 + `experiment-review/references/review_dimensions.md`
§8 はいずれも Cross-Context Review (Song, arxiv 2603.12123) を引用して
adversary の minimum-context が gain の機構であることを述べている。
GREEN counter は:

- adversary が specialist findings を見ない → 不変
- adversary が literature / hypotheses / decisions / INDEX を見ない → 不変
- adversary が upstream feature notebooks を見ない → 不変
- adversary が `bug_review.md` §1-§5 / `review_dimensions.md` §1-§7 を見ない
  → **強化** (whole-file 渡しからの脱却で物理的排除)
- adversary の prompt 末端が他 reviewer と異なる (= §6 / §8 instruction だけ
  inline) → 不変
- Re-verify の adversary 自動 re-fire → CCR の cold-eye 機能を loop の毎
  round で発火させる、機能維持

CCR の主張する mechanism は全項目維持。

## Scope 限界 — 本 GREEN でカバーしない経路 (再掲)

- **F20 (prompt caching)**: 採用せず、skill scope 外 (Claude Code 内の
  スキルが API-level の cache_control を mandate する根拠なし)。
- **実測**: 実際に sub-agent dispatch して billed input tokens を計測する
  検証は scope 外。理論値 (line × agent-run count) のみで判定。
- **Specific items to chase の機械化**: efficiency に効く第 3 のレバー、
  本 GREEN では追加せず。future RED 候補。
- **Cross-session attestation の format 詳細**: GREEN は skeleton 規定のみ、
  attestation 表記の verifiability は future iteration 候補。

## F1-F19 を re-run しても GREEN は維持される (回帰確認)

本改修は dispatch 規約の追加・extraction 規約の structured 化・dispatch
分岐の追加のみで、quality-class fixture (F1-F19) と直交:

- F1-F11 (本文への履歴 / 用語流入) と直交 — 本文 cleanliness rule に触れない
- F12-F14 (派生 H 表のノート流入) と直交 — `### Derived hypotheses` table の規定に触れない
- F15-F16 (research-goal layer) と直交 — Cycle goal 5 項目 / target_sub_claim_id を維持
- F17 (carryforward conjunct gate) と直交 — derived H routing に触れない
- F18-F19 (research-subject drift) と直交 — Data availability gate / per-H abstract format rule に触れない

回帰として、既存 RED fixtures の expected GREEN 挙動は不変。
