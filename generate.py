import os
from shutil import copyfile, rmtree
import chevron

source_dir = '../yard-sale'
destination_dir = '../yard-sale-html'


def read_price(item_dir):
    if os.path.isfile(item_dir + "/Cena_exports/Cena.txt"):
        with open(item_dir + "/Cena_exports/Cena.txt", 'r') as cena_txt:
            return cena_txt.read().strip()
    return ""


def read_description(item_dir):
    if os.path.isfile(item_dir + "/Opis_exports/Opis.txt"):
        with open(item_dir + "/Opis_exports/Opis.txt", 'r') as opis_txt:
            return opis_txt.readlines()
    return []


if os.path.isdir(destination_dir):
    for content in os.listdir(destination_dir):
        if not content.startswith(".") and os.path.isdir(destination_dir + "/" + content):
            rmtree(destination_dir + "/" + content)
        if content.endswith(".html"):
            os.remove(destination_dir + "/" + content)
else:
    os.mkdir(destination_dir)

items = os.listdir(source_dir)
items_with_details = []

for item in sorted(items):
    print(source_dir + "/" + item)
    os.mkdir(destination_dir + '/' + item)

    details = os.listdir(source_dir + "/" + item)
    photos = []
    for detail in sorted(details):
        if detail.lower().endswith(".jpg"):
            print(source_dir + "/" + item + "/" + detail)
            copyfile(source_dir + "/" + item + "/" + detail, destination_dir + "/" + item + "/" + detail)
            photos.append(item + "/" + detail)

    if len(photos) > 0:
        with open('item.html.mustache', 'r') as item_html_template:
            with open(destination_dir + '/' + item + '.html', 'w') as item_html:
                price = read_price(source_dir + "/" + item)
                description = read_description(source_dir + "/" + item)
                html = chevron.render(item_html_template, {
                    'name': item,
                    'price': price,
                    'description': description,
                    'photos': photos})

                items_with_details.append({
                    'name': item,
                    'price': price,
                    'photo': photos[0]
                })

                item_html.write(html)
                item_html.close()
            item_html_template.close()

with open('index.html.mustache', 'r') as index_html_template:
    with open(destination_dir + '/index.html', 'w') as index_html:
        html = chevron.render(index_html_template, {'items': items_with_details})
        index_html.write(html)
        index_html.close()
    index_html_template.close()

with open('post.html.mustache', 'r') as post_html_template:
    with open(destination_dir + '/post.html', 'w') as post_html:
        html = chevron.render(post_html_template, {'items': items_with_details})
        post_html.write(html)
        post_html.close()
    post_html_template.close()
