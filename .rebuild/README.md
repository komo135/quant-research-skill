# quant-research skill rebuild — meta workspace

このディレクトリは **quant-research skill の再構成プロジェクト自体** を管理するメタワークスペース。
スキルの本体は `skills/quant-research/` 以下。このディレクトリはその「rebuild プロジェクト」の charter / decisions / progress / guardrails を保持する。

---

## このディレクトリが存在する理由

agent はコンテキスト断絶 (新セッション / context compaction / 別 agent への引き継ぎ) のたびに、

1. 設計意図を再構築しようとして **元と微妙に違う方向に drift する**
2. 既に決まった事項を **再交渉しようとする**
3. 進捗を確認せずに **既に終わった作業をやり直す**
4. 表面情報だけ読んで **「全体を把握した」と誤認する**

これを防ぐため、すべてのセッション開始時にこのディレクトリの所定ファイルを順に読むことを **必須プロトコル** とする。

---

## セッション開始プロトコル (必読・スキップ禁止)

新セッション / コンテキスト断絶後、次の順で必ず読む:

1. **`GUARDRAILS.md`** — 自分 (agent) がやらかしがちな失敗のリスト。これを最初に読まないと、以下を読みながら同じ失敗を即座に犯す。
2. **`CHARTER.md`** — 何を作るか・なぜ作るか。**frozen**。再交渉禁止。
3. **`DECISIONS.md`** — これまでに決まったこと。append-only。
4. **`PROGRESS.md`** — 現在どこまで終わっているか。
5. (作業に該当する場合のみ) `skills/quant-research/SKILL.md` と関連 reference

このプロトコルを **省略してはいけない**。「短いセッションだから」「以前読んだから」「なんとなく覚えているから」は省略の理由にならない。コンテキストは前のセッションの記憶を保持しないし、人間の記憶と違って agent の "覚えている" は anchor された幻覚である可能性が高い。

---

## セッション終了プロトコル

セッション終了時 (作業中断 / ハンドオフ前) に必ず:

1. `PROGRESS.md` を更新 — 完了したタスクにチェック、新たに発見したタスクを追記
2. `DECISIONS.md` に追記 — このセッションで決まったことがあれば append (frozen 項目は変更不可、open 項目のみ追加)
3. 未解決事項を `PROGRESS.md` の "Next session pickup" セクションに具体的に書く ("〜を続ける" ではなく "〜の `<file:line>` を編集する" レベル)

セッション終了の儀式を怠ると、次セッションは **白紙からの推測** になる。

---

## ディレクトリ構成

```
.rebuild/
├── README.md           # このファイル (entry point + session protocol)
├── CHARTER.md          # frozen 設計意図 + Heilmeier 8 questions for this rebuild
├── DECISIONS.md        # append-only 決定 log
├── PROGRESS.md         # Phase 0-8 トラッカー (mutable)
└── GUARDRAILS.md       # agent 失敗モードと構造的対策
```

---

## このメタワークスペースの不変条件

- `CHARTER.md` は **frozen**。変更は CHARTER 内の "Amendments" セクションに append のみ。本文書き換え禁止。
- `DECISIONS.md` は **append-only**。過去の決定を遡って書き換えてはいけない。撤回する場合も「YYYY-MM-DD: D-N を撤回、理由 X」を append する。
- `GUARDRAILS.md` は agent が **自分の改善のために** append できる。ただし削除は禁止。
- `PROGRESS.md` は mutable。

これらの不変条件は agent が「楽な方向に流す」のを構造で防ぐためにある。違反は drift の最初の兆候。
