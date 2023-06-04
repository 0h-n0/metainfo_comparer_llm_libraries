import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from llama_index import GPTVectorStoreIndex, StorageContext, Document
from llama_index.langchain_helpers.text_splitter import TokenTextSplitter
from llama_index.vector_stores import QdrantVectorStore
from llama_index.tools import QueryEngineTool
from llama_index.query_engine import RouterQueryEngine
import qdrant_client


class BookInfo(BaseModel):
    content_url: str
    description: str    

class AozoraContent(BaseModel):
    title: str
    author: str
    text: str


def download_text(url: str) -> AozoraContent:
    r = requests.get(url)
    r.encoding = 'Shift_JIS'
    soup = BeautifulSoup(r.text.encode('utf-8'), "html.parser")
    text = soup.find("div", {"class": "main_text"})
    title = soup.find('h1', class_='title')
    author = soup.find('h2', class_='author')
    return AozoraContent(**{"title": title.text, "author": author.text, "text": text.text})


def create_query_tool(content: AozoraContent, description: str):
    client = qdrant_client.QdrantClient(location=":memory:")
    storage_context = StorageContext.from_defaults(
        vector_store=QdrantVectorStore(client=client, collection_name="test")
    )
    text_splitter = TokenTextSplitter(chunk_size=300, chunk_overlap=50)
    texts = text_splitter.split_text(content.text)
    documents = [Document(t) for t in texts]
    index = GPTVectorStoreIndex.from_documents(documents, storage_context=storage_context)
    info_description = ("aouther: " + content.author +"\n" + 
                        "title: " + content.title + "\n" + 
                        "description: " + description)    
    tool = QueryEngineTool.from_defaults(
        query_engine=index.as_query_engine(),
        description=info_description
    )
    return tool


if __name__ == "__main__":
    kojin_info = BookInfo(
        content_url="https://www.aozora.gr.jp/cards/000148/files/772_33100.html",
        description="明治期の文学者、夏目漱石の講演筆記。初出は「孤蝶馬場勝弥氏立候補後援現代文集」［実業之世界社、1915（大正4）年］。本文のはじめに「1914（大正3）年11月25日学習院輔仁会にて述」とある。将来権力と金力を手にするはずの学習院の学生を前に、漱石は「自己本位」という立脚地を得た経歴から、「個人主義」について、自己の個性の発展を望むなら他人の個性も尊重し、自己の権力や金力を使うならそれに伴う義務や責任を重んじなければならないと説く。"
    )
    syayo_info = BookInfo(
        content_url="https://www.aozora.gr.jp/cards/000035/files/1565_8559.html",
        description="破滅への衝動を持ちながらも“恋と革命のため”生きようとするかず子、麻薬中毒で破滅してゆく直治、最後の貴婦人である母、戦後に生きる己れ自身を戯画化した流行作家上原。没落貴族の家庭を舞台に、真の革命のためにはもっと美しい滅亡が必要なのだという悲壮な心情を、四人四様の滅びの姿のうちに描く。昭和22年に発表され、“斜陽族”という言葉を生んだ太宰文学の代表作。"
    )

    kojin_content = download_text(kojin_info.content_url)    
    kojin_tool = create_query_tool(kojin_content, kojin_info.description)
    syayo_content = download_text(syayo_info.content_url)
    syayo_tool = create_query_tool(syayo_content, syayo_info.description)

    query_engine = RouterQueryEngine.from_defaults(
        query_engine_tools=[kojin_tool, syayo_tool]
    )
    
    def ask(input):
        print("Q: ", input)
        try: 
            out = query_engine.query(input)        
            print(out)
        except Exception as e:
            print(e)
    ask("いくつの本を登録しましたか？") # How many books did you register?
    ask("私の個人主義 の内容を箇条書きで教えてください。") # Please tell me the contents of "私の個人主義"(watashi no kojinsyugi) in a list.
    ask("斜陽の内容を箇条書きで教えてください。") # Please tell me the contents of "斜陽"(syaho) in a list.
    ask("坊ちゃんの内容を箇条書きで教えてください。") # Please tell me the contents of "坊ちゃん"(botyan) in a list.