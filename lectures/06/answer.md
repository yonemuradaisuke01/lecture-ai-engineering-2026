# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前： search_glossary
- STEP 2 の [tool call]：glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'Amazon S3 versioning overview'})
- 気づき・疑問：２つに絡む質問をかけたら、toolも2つでてきた。応答4回なのはなぜだろう

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎 
- やったこと：server.tool()(tools.get_lecture_summary)　を追加（mcp_server.pyへ）
- 結果：get_lecture_summary　が追加され、[glossary_get_lecture_summary]
  指定した回（1始まりの整数）の講義の要点を返す。という定義がはいっている。
  
  第２回では何を学びますかに、正しく回答をうけた
  
- 気づき・疑問：
　今回の課題は珍しく特にありませんでした。
- 気づき・疑問：
