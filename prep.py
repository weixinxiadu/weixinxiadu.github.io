import json
import os
import collections
import hashlib

def wxread_url(bookId):
    if not bookId.isdigit():
        print("Cannot process book id: ", bookId)
        return None
    md5 = hashlib.md5(bookId.encode("utf-8")).hexdigest()
    result = md5[:3] + "32" + md5[-2:]
    split_hexes = [
        "%x" % int(bookId[start: start+9])
        for start in range(0, len(bookId), 9)
    ]
    result += "g".join([
        "%02x%s" % (len(hex), hex)
        for hex in split_hexes
    ])
    if len(result) < 20:
        result += md5[:20-len(result)]
    resultHash = hashlib.md5(result.encode("utf-8")).hexdigest()[:3]
    return "https://weread.qq.com/web/appreader/" + result + resultHash

def process_wx_files():
    with open("wxread.jsonlines") as lines:
        metadata = collections.Counter()
        books_split = collections.defaultdict(list)
        for line in lines:
            d = json.loads(line)
            bookInfo = d["bookInfo"]
            category = bookInfo["category"]
            if len(category) > 0:
                metadata[category] += 1
                book = {
                    "bookId": bookInfo["bookId"],
                    "title": bookInfo["title"],
                    "author": bookInfo["author"],
                    "cover": bookInfo["cover"],
                    "bookUrl": wxread_url(bookInfo["bookId"])
                }
                books_split[category].append(book)
        for category, books in books_split.items():
            with open("public/data/{}.json".format(category), "w") as f:
                print(json.dumps(books, ensure_ascii=False), file=f)
        with open("public/data/meta.json", "w") as f:
            f.write(json.dumps(metadata, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    process_wx_files()