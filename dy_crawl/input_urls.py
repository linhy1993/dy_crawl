import re

with open("../urls.txt", "r") as file:
    text = file.read().replace("\n", "")
print("[INFO]: Loading text from urls.txt")
urls = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", text)
print(f"[INFO]: There are {len(urls)} urls going to crawl")
