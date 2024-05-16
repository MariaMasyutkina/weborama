from pathlib import Path
from bs4 import BeautifulSoup
from zipfile import ZipFile
import shutil


def get_book_info():

    book_title = ""
    author = list()
    publisher = ""
    year = ""

    file_dir = Path(input("Укажите путь к файлу: "))

    # книга в формате fb2
    if file_dir.suffix == ".fb2":
        with open(file_dir, encoding="utf-8") as fb2_file:
            file = fb2_file.read()
            soup = BeautifulSoup(file, "xml")

            # данные по названию и автору
            title_info = soup.find("title-info")
            if title_info:
                book_title = title_info.find("book-title")
                author_info = title_info.find("author")
                if author_info:
                    author_fn = author_info.find("first-name")

                    if author_fn:
                        author.append(author_fn.contents[0])
                    author_mn = author_info.find("middle-name")
                    if author_mn:
                        author.append(author_mn.contents[0])
                    author_ln = author_info.find("last-name")
                    if author_ln:
                        author.append(author_ln.contents[0])

            # издательство
            publisher_info = soup.find("publish-info")
            if publisher_info:
                publisher = publisher_info.find("publisher")
                year = publisher_info.find("year")

            if not book_title:
                book_title = publisher_info.find("book-name")

    # книга в формате epub
    elif file_dir.suffix == ".epub":

        # распаковка epub как архива
        with ZipFile(file_dir) as epub_zip:
            epub_zip.extractall("epub-zip_" + file_dir.name)

        # получение пути к файлу с данными по книге
        with open(
            "epub-zip_" + file_dir.name + "\\META-INF\\container.xml", encoding="utf-8"
        ) as container_file:
            file = container_file.read()
            soup = BeautifulSoup(file, "xml")
            root_file = soup.find("rootfile")
            cont_file_path = root_file.attrs.get("full-path")

        # чтение файла с данными по книге
        with open(
            "epub-zip_" + file_dir.name + "\\" + cont_file_path, encoding="utf-8"
        ) as content_file:
            file = content_file.read()
            soup = BeautifulSoup(file, "xml")
            book_title = soup.find("dc:title")
            author_name = soup.find("dc:creator")
            if author_name:
                author.append(author_name.contents[0])
            publisher = soup.find("dc:publisher")
            year = soup.find("dc:date")

        # удаление распакованной папки
        shutil.rmtree("epub-zip_" + file_dir.name)

    else:
        print("Выберите файл в формате fb2 или epub")
        return

    # print(
    #     f"Название: {book_title.contents[0] if book_title else ""}"
    #     + f"\nАвтор: {" ".join(author)}"
    #     + f"\nИздательство: {publisher.contents[0] if publisher else ""}"
    #     + f"\nГод: {year.contents[0] if year else ""}"
    # )

    return (
        book_title.contents[0] if book_title else "",
        " ".join(author),
        publisher.contents[0] if publisher else "",
        year.contents[0] if year else "",
    )


try:
    get_book_info()
except UnicodeDecodeError:
    print("Ваш файл не в кодировке utf-8. Выберите другой файл")
