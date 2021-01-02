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

for item in sorted(items):
    print(source_dir + "/" + item)
    os.mkdir(destination_dir + '/' + item)

    details = os.listdir(source_dir + "/" + item)
    photos = []
    for detail in sorted(details):
        if detail.endswith(".jpg"):
            print(source_dir + "/" + item + "/" + detail)
            copyfile(source_dir + "/" + item + "/" + detail, destination_dir + "/" + item + "/" + detail)
            photos.append(item + "/" + detail)

    if os.path.isfile(source_dir + "/" + item + "/Opis_exports/Opis.txt") and os.path.isfile(source_dir + "/" + item + "/Cena_exports/Cena.txt"):
        with open('item.html.mustache', 'r') as item_html_template:
            with open(destination_dir + '/' + item + '.html', 'w') as item_html:
                with open(source_dir + "/" + item + "/Opis_exports/Opis.txt", 'r') as opis_txt:
                    with open(source_dir + "/" + item + "/Cena_exports/Cena.txt", 'r') as cena_txt:
                        cena = cena_txt.read().strip()
                        html = chevron.render(item_html_template, {
                            'name': item,
                            'price': cena,
                            'description': opis_txt.readlines(),
                            'photos': photos})

                        items_with_details.append({
                            'name': item,
                            'price': cena,
                            'photo': photos[0]
                        })

                        cena_txt.close()
                    opis_txt.close()
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
