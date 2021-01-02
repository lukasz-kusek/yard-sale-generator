import os
from shutil import copyfile, rmtree
import chevron

source_dir = '../yard-sale'
destination_dir = '../yard-sale-html'

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

for item in items:
    print(source_dir + "/" + item)
    os.mkdir(destination_dir + '/' + item)

    details = os.listdir(source_dir + "/" + item)
    photos = []
    for detail in details:
        if detail.endswith(".jpg"):
            print(source_dir + "/" + item + "/" + detail)
            copyfile(source_dir + "/" + item + "/" + detail, destination_dir + "/" + item + "/" + detail)
            photos.append(item + "/" + detail)

    for detail in details:
        if detail == "Opis_exports":
            print(source_dir + "/" + item + "/" + detail)
            with open('item.html.mustache', 'r') as item_html_template:
                with open(destination_dir + '/' + item + '.html', 'w') as item_html:
                    with open(source_dir + "/" + item + "/" + detail + "/Opis.txt", 'r') as opis:
                        html = chevron.render(item_html_template, {'name': item, 'description': opis.readlines(), 'photos': photos})
                        opis.close()
                    item_html.write(html)
                    item_html.close()
                item_html_template.close()

    items_with_details.append({
        'name': item,
        'photo': photos[0]
    })

with open('index.html.mustache', 'r') as index_html_template:
    with open(destination_dir + '/index.html', 'w') as index_html:
        html = chevron.render(index_html_template, {'items': items_with_details})
        index_html.write(html)
        index_html.close()
    index_html_template.close()
