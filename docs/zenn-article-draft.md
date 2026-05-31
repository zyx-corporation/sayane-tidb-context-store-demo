# RAGは検索して終わりではない：TiDB Cloudで作る監査可能なAIメモリ基盤

## はじめに

RAGを実装するとき、最初に目が向くのは検索精度です。しかし、AIエージェントのメモリ基盤として考えると、検索できることだけでは足りません。

どの文書を取り込んだのか。どのchunkが検索されたのか。どの検索モードで、どの結果が採用されたのか。その結果はあとから検査できるのか。

このデモでは、Sayane Context Store Interface の検証用プロトタイプとして、TiDB Cloudをbackendにした最小のContext Storeを作ります。

## このデモで作るもの

このリポジトリでは、以下を実装します。

- Markdown ingestion
- chunking
- TiDB-backed document/chunk storage
- optional embedding generation
- text search
- vector search
- hybrid search
- retrieval logs
- lightweight RDE-style audit summary

ただし、現時点のvector searchはTiDB native vector indexではありません。embeddingをTiDBにJSONとして保存し、Python側でcosine similarityを計算する中間実装です。

## なぜ中間実装から始めるのか

いきなりTiDB native vector searchへ進むと、記事の焦点がSQL構文やクラスタ機能確認に寄りすぎます。

まずは、RAG/AIメモリ基盤における本質的な構造を小さく確認します。

- text searchは固有名詞や仕様語に強い
- vector searchは意味的な近さに強い
- hybrid searchは明示的なmerge policyが必要
- retrieval logはdebug outputではなく、監査可能性の中核である

この段階で、検索方式の違いとretrieval logの価値を確認できます。

## アーキテクチャ

```text
Markdown files
  -> chunker
  -> embedding provider
  -> TiDB Cloud
  -> text / vector / hybrid search
  -> retrieval logs
  -> lightweight audit summary
```

Sayaneの中核はTiDBではありません。中核はContext Store Interfaceです。

TiDB Cloudは、このデモで利用するbackend adapterです。ここを混同すると、実装上の選択が理論的中心にすり替わってしまいます。

## 実行手順

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
cp .env.example .env
```

TiDB接続情報を `.env` に設定したあと、schemaを初期化します。

```bash
sayane-tidb-demo init
```

まずはembeddingなしでMarkdownを取り込みます。

```bash
sayane-tidb-demo ingest data/sample_docs
sayane-tidb-demo search "TiDB" --mode text
```

embeddingを生成してから、vector / hybrid searchを試します。

```bash
sayane-tidb-demo ingest data/sample_docs --embed
sayane-tidb-demo search "Context Store Interface" --mode vector
sayane-tidb-demo search "enterprise backend" --mode hybrid
```

検索結果はretrieval logとして保存されます。

```bash
sayane-tidb-demo logs
sayane-tidb-demo inspect <retrieval_id>
```

## retrieval logの意味

RAGでは、最終回答だけを見ると、どの文脈が使われたのかが見えなくなります。

このデモでは、検索ごとに以下を保存します。

- query
- mode
- retrieved chunk IDs
- scores
- selected chunk IDs
- lightweight audit summary

これにより、生成後に検索過程を確認できます。

## lightweight RDE-style audit

このデモのauditは、完全なRDE実装ではありません。

ここでは、retrieval resultをあとから検査できるようにするための軽量summaryだけを扱います。

この区別は重要です。軽量auditをfull RDE scoringとして説明してはいけません。

## 現時点の制約

現時点では、vector searchはPython側でcosine similarityを計算しています。

つまり、これはvector-enabledではありますが、TiDB-native vector-indexedではありません。

TiDB Cloud native vector searchへの移行は、Issue #1で追跡します。この変更はschema、retrieval semantics、記事の主張境界を変えるため、別のDelta-M変更として扱います。

## まとめ

RAGは検索して終わりではありません。

AIエージェントのメモリ基盤では、検索結果を保存し、あとから検査できることが重要です。

このデモは、TiDB Cloudをbackendに使いながら、Context Store、retrieval log、lightweight auditをひとつの小さなプロトタイプとして確認するものです。
