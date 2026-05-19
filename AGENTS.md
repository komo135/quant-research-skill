# AGENTS.md

このリポジトリでは、明示的な指示がない限り日本語で回答し、ドキュメントも日本語で書く。

## 作業と Git

- 作業は作業ブランチで行う。
- 作業完了時は、変更一式を確認し、コミット、push、必要なら PR 更新まで行う。
- 作業者が自分で触ったかどうかだけを理由に、既存の未コミット変更を放置しない。現在の作業対象としてユーザーが求めている差分はまとめて扱う。
- ただし、明確に無関係な変更や衝突しそうな変更がある場合は、勝手に戻さず、差分を確認してから扱う。

## テスト追加の判断

テストを追加または変更する前に、作業を分類する。

- Behavior / public contract change
- Bug regression
- Characterization / protection test
- Documentation contract
- Release / packaging / cache operation
- Refactor only

新しいリポジトリテストは、将来のバージョンでも守るべき外部から観測可能な契約を保護する場合だけ許可する。

追加してよい例:

- 公開スクリプトの入出力、失敗条件、生成ファイル構造
- テンプレートの必須構造
- 生成されるプロジェクトレイアウト
- CJK 文字混入チェックなど、配布物として機械的に検出できる品質ゲート
- 削除済みコマンドが復活しないことなど、安定した公開面の確認

追加しない例:

- 現在のバージョン番号
- リリースチェックリスト状態
- キャッシュやインストール状態
- PR / push / merge 状態
- 実装パスの好み
- 安定契約ではない文言の有無
- `SKILL.md` の望ましい文章を文字列検索で固定するテスト

スキルの判断力や運用規律を確認したい場合は、リポジトリテストではなく、サブエージェント圧力テストで確認する。

## TDD と圧力テスト

TDD は「先に赤いテストを書くこと」自体が目的ではない。先に、要求、ユーザーから見えるふるまい、観測可能な仕様を明確にする。

スキル文書の改善では、リポジトリテストを濫用しない。特に、文章そのものを固定するための文字列検索テストは避ける。代わりに、失敗しやすい状況をサブエージェントに与え、スキルだけを読ませて期待する判断になるかを確認する。

RED / GREEN / REFACTOR を報告する場合は、何を RED と見なしたかを明示する。

- コードや公開スクリプトの変更: 失敗する自動テストや再現手順を RED とする。
- スキル文書の変更: 圧力シナリオでの逸脱、曖昧さ、合理化を RED とする。
- release / packaging / cache 作業: テスト追加ではなく、検証コマンドと証跡を報告する。

## research-skill 固有の注意

このプラグインは proposition-first の研究ライフサイクルを扱う。

- トップレベルの研究単位は plan ではなく proposition。
- hypothesis plan は、親 proposition と source analysis から導かれた 1 つの derived hypothesis を検証する。
- vague topic から直接 hypothesis / plan に進まない。material absence の場合は material-acquisition task に戻す。
- `under-specified`, `split-needed`, `split`, `closed`, `contradicted` の親から plan を作らない。
- `research-plan-review` と `research-result-analysis` は plan path から独立に再構成する前提を守る。

## プラグインバージョン更新

プラグインの公開プロトコルやライフサイクルを変えた場合は、`.codex-plugin/plugin.json` の `version`, `description`, `interface.longDescription` を確認する。

- protocol / lifecycle の大きな変更は minor version を上げる。
- 説明文は現在の公開挙動を反映する。
- 変更後は JSON 構文チェックと関連テストを実行する。
