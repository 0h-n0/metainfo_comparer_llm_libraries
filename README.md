# Comparing how to treat meta-meta information in LLM libraries

This script downloads two Japanese books and creates two vector stores. These vector stores contain the descriptions of the books. Both libraries are capable of storing information from the vector stores and processing queries with an Agent (LLM > Action flow). I'm interested in finding out if they can handle meta-meta information, such as, "how many vector stores are registered?" and similar queries.


## Result

Both libries can't handle meta-meta information. They can only handle descriptions(meta information) of the books. I find the llama_index don't support exception handling (don't throw a specific exception when it can't find the answer). It's a bit difficult to debug. langchain is better in this regard.


### llama_index error when the tool can't find the answer

```shell
File ".venv/lib/python3.11/site-packages/dataclasses_json/core.py", line 137, in _decode_dataclass
    kvs = {decode_names.get(k, k): v for k, v in kvs.items()}
                                                 ^^^^
```

### langhchain error when the tool can't find the answer

```shell
File ".venv/lib/python3.11/site-packages/langchain/agents/mrkl/output_parser.py", line 27, in parse
    raise OutputParserException(
langchain.schema.OutputParserException: Could not parse LLM output: `I don't know`
```

## Setup
if you don't have `rye` which is one of Python package manager, you need to install it.

```
$ curl -sSf https://rye-up.com/get | bash
$ echo 'source "$HOME/.rye/env"' >> ~/.bashrc
```

create virualenv
```
$ rye sync
```

## Runs

```
$ rye run python examples/langchain_run.py
Q:  いくつの本を登録しましたか？ # How many books did you register?
A: >>> Could not parse LLM output: `I don't know`
Q:  私の個人主義 の内容を箇条書きで教えてください。 # Please tell me the contents of "私の個人主義" in a list.
A: >>>  私の個人主義の内容は以下の通りです。
1. 個人の自由と独立性を重視する。
2. 自己決定と自己責任を大切にする。
3. 個人の成長と発展を目指す。
4. 社会や他人に依存しない生き方を志向する。
5. 理性と倫理を基盤に行動する。
6. 個人の価値観や意見を尊重し、多様性を認める。
7. 国家主義や集団主義に対抗する立場を取るが、無益な対立を避ける。
8. 個人主義は時に孤独を伴うが、それを受け入れる。
9. 自分の人生において、自分が主役であることを認識する。

これらは、個人主義の一般的な内容を箇条書きにしたものです。ただし、個人主義は人それぞれ異なる解釈や価値観が存在するため、これらのポイントがすべての個人主義者に当てはまるわけではありません。
Q:  斜陽の内容を箇条書きで教えてください。 # Please tell me the contents of "斜陽" in a list.
A: >>>  斜陽の内容を箇条書きで説明することはできませんが、提供されたテキストから抽出できる情報は以下の通りです。

1. 雨が止んで風が吹き始める。
2. 午後3時になる。
3. 一級酒（六合）の配給を受け取りに行く予定。
4. ラム酒の瓶を二本持っていく。
5. 手紙を胸ポケットに入れる。
6. 弟にはお酒を飲ませない。
7. かず子が毎晩コップでお酒を飲む。
8. 林の奥に製材所から来た板が積んである。
9. 将校が白い歯を出して笑う。
10. 板の上で昼寝をする提案がある。
11. 小さい文庫本が上衣のポケットから出される。
12. 冬の日が庭の芝生に当たっている。
13. 庭には梅の木や蜜柑畑がある。
14. 松林の向こうに海が見える。
15. 蛇が庭に現れる。

これらの情報は、斜陽の全体的な内容を説明するものではありませんが、提供されたテキストから抽出できる情報です。
Q:  坊ちゃんの内容を箇条書きで教えてください。 # Please tell me the contents of "坊ちゃん" in a list.
A: >>>  I don't know
```


```
$ rye run python examples/llamaindex_run.py
Q:  いくつの本を登録しましたか？ # How many books did you register?

いくつの本を登録しましたか？ 
答え：不明 # Answer: unknown
Q:  私の個人主義 の内容を箇条書きで教えてください。 # Please tell me the contents of "私の個人主義" in a list.

1. 自分の考えや意見を尊重する
2. 他人の考えや意見を尊重する
3. 自分の行動を自分で決める
4. 自分の行動に責任を持つ
5. 自分の価値観を大切にする
Q:  斜陽の内容を箇条書きで教えてください。 # Please tell me the contents of "斜陽" in a list.

1. 雨が上がり、風が吹き出したことを伝える。
2. 三時であることを伝える。
3. 一級酒（六合）の配給を貰いに行くことを伝える。
4. ラム酒の瓶を二本、袋に入れ、胸のポケットに手紙を入れ、村に出かけることを伝える。
5. 弟に飲ませないことを伝える。
6. 毎晩、コップで一ぱいずつ飲むことを伝える。
7. 師匠さんが軽井沢の別荘へいらしたことを伝える。
8. 師匠さんが伊豆の温泉へ仕事に来た途中で立ち寄ったことを伝える。
9. 芸術家は、おいくつになっても、子供みたいな気ままな事をするものらしいことを伝える。
Q:  坊ちゃんの内容を箇条書きで教えてください。# Please tell me the contents of "坊ちゃん" in a list.
'str' object has no attribute 'items' # <<< 
```