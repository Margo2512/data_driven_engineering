import lxml.html as l
import pandas as pd
import requests
from tqdm import tqdm


def clone(element):
    return l.etree.fromstring(l.etree.tostring(element))


author_list = []
voice_list = []
comments_list = []
new_data2 = []
all_list = []
name_list = []
id_list = []
for page in tqdm(range(1, 50)):
    url = f"https://habr.com/ru/articles/page{page}/"
    r = requests.get(url)
    root = l.fromstring(r.text)
    author_divs = root.xpath(
        "//a[@class='tm-user-info__username'] | //span[@class='tm-article-datetime-published']"
    )
    voice_divs = root.xpath("//span[@class='bookmarks-button__counter']")
    comments_divs = root.xpath(
        "//span[@class='tm-article-comments-counter-link__value']"
    )
    all_divs = root.xpath("//div[@class='tm-article-snippet__stats']")
    name_divs = root.xpath("//h2[@class='tm-title tm-title_h2']")
    id_divs = root.xpath("//article[@class='tm-articles-list__item']")
    for div in id_divs:
        id_list.append([text for text in div.itertext()])
    for div in name_divs:
        name_list.append([text for text in div.itertext()])
    for div in all_divs:
        all_list.append([text for text in div.itertext()])
    for div in author_divs:
        author_list.append([text for text in div.itertext()])
    new_data = []
    for i in range(len(author_list)):
        if (":" or "час" or "вчера") in author_list[i]:
            if not (
                i > 0
                and (
                    ":" not in author_list[i - 1]
                    or "час" in author_list[i - 1]
                    or "вчера" in author_list[i - 1]
                )
            ):
                new_data.append("0")
            new_data.append(author_list[i])
        else:
            new_data.append(author_list[i])
    new_data2 = new_data[::2]
    for div in voice_divs:
        voice = clone(div).xpath("./text()")[0]
        voice_list.append(voice)
    for div in comments_divs:
        comments = clone(div).xpath("./text()")[0].strip()
        comments_list.append(comments)
difficulty_levels = []
reading_times = []
view_counts = []
for item in all_list:
    difficulty = None
    reading_time = None
    view_count = None
    for i in range(len(item)):
        if item[i] == "Уровень сложности":
            difficulty = item[i + 1]
        elif item[i] == "Время на прочтение":
            reading_time = item[i + 1].replace("мин", "").strip()
            value = float(reading_time)
            hours = round(value / 60, 2)
        elif item[i] == "Количество просмотров":
            view_count_str = item[i + 1]
            if "K" in view_count_str:
                view_count = float(view_count_str.replace("K", ""))
            else:
                view_count = float(view_count_str) / 1000.0
    difficulty_levels.append(difficulty)
    reading_times.append(hours)
    view_counts.append(view_count)
data_dict = {
    "Название статьи": name_list,
    "Уровень сложности": difficulty_levels,
    "Время на прочтение (ч.)": reading_times,
    "Количество просмотров (тыс.)": view_counts,
    "Добавить в закладки": voice_list,
}
df = pd.DataFrame(data_dict)
df.to_csv("df_parser.csv", index=False)
print(df.info())
print(df.head())
