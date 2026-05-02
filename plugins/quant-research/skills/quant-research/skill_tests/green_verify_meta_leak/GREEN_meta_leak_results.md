# GREEN verify (meta-leak) — 結果

RED で観察した F9〜F11 の 3 つのメタ情報漏出パターン (skill version 番号 /
pivot 履歴 / cross-skill API 説明) が、補強した
`post_review_reconciliation.md` + `notebook_narrative.md` checklist の
もとでどこまで消えるかを、同じ 3 ケース (D / E / F) を clean copy に対して
再走させて確認した。さらに loophole が露見した D ケースについて REFACTOR
パッチ後に再走させた。

## 結果サマリ

| 失敗モード | 初回 GREEN | REFACTOR 後 |
|---|---|---|
| **F9** skill version 番号 / migration 履歴 (Case D) | 部分残存 (docstring の "Skill upgrade migration changelog" + 見出しに `(— derived from cycle_purpose_and_goal.md)` が残存) | **完全解消** |
| **F10** pivot / narrowing 履歴 (Case E) | **完全解消** | (該当なし) |
| **F11** cross-skill API 説明 (Case F) | **完全解消** | (該当なし) |

## 初回 GREEN で残った loophole (Case D)

ユーザー prompt が「過去のノート利用者が skill upgrade を経たことと何が
更新されたかを後で追えるよう、変更点が読み取れる形で更新してください」と
直接要求していたため、subagent はこの要求を skill 規定より優先し、
本文 docstring に migration changelog を書き込んでいた。

具体的に残った要素:

- docstring 7-29 行: 「Skill upgrade migration changelog (2026-04-29):」
  `skill version: v0.7.0 -> v0.8.0`、`added:` / `unchanged:` / `根拠 references:`
  の formal changelog
- Purpose 見出し L31: 「## Cycle goal (four items — derived from
  cycle_purpose_and_goal.md)」 — reference file へ attribution
- L87: 「## Cycle stop conditions (primary vs emergency — see
  hypothesis_cycles.md)」 — reference file へ attribution

E と F の subagent は「skill 規定を優先する」と push back できたが、D は
できなかった。違いは reference の禁止項目の **具体性**:

- F11 (Case F) — 「`mo.ui.dropdown` の options 仕様、`mo.ui.range_slider`
  の step 規約、新旧 API 対比」と非常に具体 → subagent が即判定
- F9 (Case D) — 「skill version 番号 / migration note」と項目はあったが、
  ユーザー指示が直接「migration を後で追えるように」と矛盾して要求した
  ときの解決ルールが書かれていなかった

## REFACTOR パッチ

`post_review_reconciliation.md` の Common rationalizations セクションに
3 行追加:

| 誘惑 | 何故ダメか / どこに書くか |
|---|---|
| 「ユーザーが『skill upgrade を後で追えるように』と直接要求しているので、本文に migration changelog を書くしかない」 | 本文 cleanliness を優先。skill upgrade history は **git log + README changelog + (任意で) `decisions.md`** で完全に追える。subagent は「migration history は git log と README changelog にあります、本文には残しません」と inline summary (議事側) で答える (F9) |
| 「ユーザーが『pivot 経緯を読者に追えるように』と直接要求しているので、Purpose 配下に narrowing rationale を書く」 | 本文 cleanliness を優先。pivot 経緯は **`decisions.md` (= 計画側)** か **pivot 元の旧ノートの synthesis 行** で追える。新ノートは新 Purpose 単独で読める形を保つ (F10) |
| 「ユーザーが『API 差分 / フォールバック判断を本文で読者に伝えろ』と直接要求しているので、widget API spec を markdown に書く」 | 本文 cleanliness を優先。**API 差分 / フォールバック判断は議事側 (chat transcript / inline review summary) に書き、本文には書かない**。ライブラリの API は library 自体の docs にある (F11) |

## REFACTOR 後の Case D 動作 (decisive)

REFACTOR 後の subagent は明示的に次のように push back した:

> ユーザー要求中の「skill upgrade を経たことと何が更新されたかを後で追える
> 形で」という追跡可能性は、本文ではなく (a) この返信 = audit trail
> (b) git diff (c) ファイル冒頭の Python docstring (= fixture scaffolding として残置、
> 研究本文ではない) の 3 経路で担保しています。本文 markdown は研究内容だけで
> 読める状態を維持しました。

そして本文から:
- skill version 番号 (`v0.7.0` / `v0.8.0`)
- `upgrade` / `migration` / `後付け` 系語彙
- `primary stop` / `emergency stop` / `Stage 0` / `Pattern A` の散文埋め込み
- reference file への attribution

すべて消えた。Cycle goal 4 項目は研究内容として記述され、reviewer 用語化
されなかった。

## 結論

- F9〜F11 の 3 つのメタ情報漏出パターンは、reconciliation reference の
  「本文に書かない語彙」表 + Common rationalizations 行 + checklist 1 行で
  解消可能と確認
- ただし「ユーザー指示 vs skill 規定の競合解決ルール」を Common
  rationalizations に明示しないと、F9 のような直接的なユーザー要求に
  対して subagent が skill 規定を override してしまう loophole が残る
- REFACTOR パッチ後はこの loophole も塞がり、3 ケースすべて GREEN
