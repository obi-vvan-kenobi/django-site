import requests
import json
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import logging
from os import getenv
import django
import sys
sys.path.append("..")

django.setup()

from books.models import Book, SubCategories, Categories, Authors
from django.utils.text import slugify

logging.basicConfig(filename='../books/logs/Pictures.log', level=logging.WARNING,
                    format="%(asctime)s - %(levelname)s - %(pathname)s: %(lineno)d - %(message)s - %(url)s")

SOURCE_DATA_FILE = getenv('SOURCE_DATA_FILE')


def _parse_book_json(path: str):
    with open(path, 'r', encoding='utf-8') as j:
        json_ = json.load(j)
    return json_


def _check_new_books():
    books = [book['title'] for book in Book.objects.all().values('title')]
    return [book for book in _parse_book_json('../' + SOURCE_DATA_FILE) if
            book['title'] not in books]


def save_book_pic(url, title):
    if url:
        resp = requests.get(url)
        try:
            pic_name = rf'{title.replace("/", "_")}.webp'
            Image.open(BytesIO(resp.content)).convert('RGB').save(
                f'../media/{pic_name}', 'webp')
            return pic_name
        except UnidentifiedImageError as e:
            logging.warning(e, extra={'url': url})


def save_pic_and_parse_to_db():
    for book in _check_new_books():
        title = book.get('title')
        isbn = book.get('isbn')
        page_count = book.get('pageCount', 0)
        publish_date = book.get('publishedDate', {}).get('$date')
        url = book.get('thumbnailUrl')
        short_desc = book.get('shortDescription')
        long_desc = book.get('longDescription')
        status = book.get('status')
        authors = book.get('authors')
        categories = book.get('categories')
        photo_url = save_book_pic(url, title)

        b = Book(title=title, isbn=isbn, page_count=page_count, time_publish=publish_date,
                 thumbnail_url=url, photo_url=photo_url, short_description=short_desc, long_description=long_desc,
                 status=status)

        sub_cats = []
        if categories:
            cat, created = Categories.objects.get_or_create(name=categories[0], slug=slugify(categories[0]))

            if len(categories) > 1:
                for subcat in categories[1:]:
                    if subcat:
                        s_c, created = SubCategories.objects.get_or_create(name=subcat, cat_id=cat.id)
                        sub_cats.append(s_c)
        else:
            no_categories = 'New'
            cat, created = Categories.objects.get_or_create(name=no_categories, slug=slugify(no_categories))

        b.cat_id = cat.id
        b.save()
        if sub_cats:
            b.sub_cat.add(*sub_cats)

        if authors:
            for author in authors:
                a, created = Authors.objects.get_or_create(name=author)
                b.author.add(a)


if __name__ == '__main__':
    save_pic_and_parse_to_db()
