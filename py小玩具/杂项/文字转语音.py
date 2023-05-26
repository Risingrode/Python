import pyttsx3

engine = pyttsx3.init()

# engine.say("请叫我长得帅")
# engine.say("轻轻的，我走了，正如我轻轻的来")
with open("../../爬虫/b站爬虫合集/数据解析/三国演义.txt", 'r', encoding="utf-8") as r:
    engine.say(r.read())

engine.runAndWait()
