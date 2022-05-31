import argparse
import csv
import os
import sys
import requests
from constants import *


def process_command(args):
    """Метод выборает команду на обработку в зависимости от входящих аргументов"""

    if args.posts:
        show_posts(args.domain)
    if args.comments:
        show_comments(args.domain)
    if args.description:
        show_description(args.domain)


def show_posts(domain):
    """Метод находит топ-10 постов по количеству лайков на основе 100 последних постов,
        записывает результат в форме [место / количество лайков / текст поста] в файл output.txt

        Parameters
        ----------
        domain: str
            короткое имя группы ВК

        Raises
        ------
        ConnectionError
            При ошибке подключения
        KeyError
            При ошибке обращения к словарю
    """

    try:
        data = get_posts(domain)
        min_value = 0
        bottom_post = None
        top_likes_list = []
        for post in data:
            likes = post["likes"]["count"]
            if likes > min_value and len(top_likes_list) == 10:
                top_likes_list.remove(bottom_post)
                min_value, bottom_post = append_item_and_sort(top_likes_list, post)
            elif len(top_likes_list) < 10:
                min_value, bottom_post = append_item_and_sort(top_likes_list, post)
        top_likes_list.reverse()

        with open(output, "w", encoding="UTF-8") as f:
            a_pen = csv.writer(f, delimiter="|")
            a_pen.writerow(p_result_states)
            place = 1
            for post in top_likes_list:
                a_pen.writerow((place, post["likes"]["count"], post["text"]))
                if place != 10:
                    a_pen.writerow(sep)
                place += 1

    except requests.exceptions.ConnectionError:
        sys.exit("Проверьте подключение к интернету.")
    except KeyError:
        sys.exit("Проверьте правильность введенных параметров.")


def show_comments(domain):
    """Метод находит топ-10 комментариев по количеству лайков на основе 100 последних постов,
        записывает результат в форме [место / количество лайков / текст комментария] в файл output.txt

        Parameters
        ----------
        domain: str
            короткое имя группы ВК

        Raises
        ------
        ConnectionError
            При ошибке подключения
        KeyError
            При ошибке обращения к словарю
    """

    try:
        data = get_posts(domain)
        min_value = 0
        bottom_comment = None
        top_comments_list = []
        for post in data:
            comments = get_comments(post["id"], post["owner_id"], post["comments"]["count"])
            for comment in comments:
                try:
                    likes = comment["likes"]["count"]
                except KeyError:
                    likes = 0
                if likes > min_value and len(top_comments_list) == 10:
                    top_comments_list.remove(bottom_comment)
                    min_value, bottom_comment = append_item_and_sort(top_comments_list, comment)
                elif len(top_comments_list) < 10:
                    min_value, bottom_comment = append_item_and_sort(top_comments_list, comment)
        top_comments_list.reverse()
        with open(output, "w", encoding="UTF-8") as f:
            a_pen = csv.writer(f, delimiter="|")
            a_pen.writerow(c_result_states)
            place = 1
            for comment in top_comments_list:
                a_pen.writerow((place, comment["likes"]["count"], comment["text"]))
                if place != 10:
                    a_pen.writerow(sep)
                place += 1
    except requests.exceptions.ConnectionError:
        sys.exit("Проверьте подключение к интернету.")
    except KeyError:
        sys.exit("Проверьте правильность введенных параметров.")


def show_description(domain):
    """Метод находит описание группы ВК, записывает результат в файл output.txt

        Parameters
        ----------
        domain: str
            короткое имя группы ВК

        Raises
        ------
        ConnectionError
            При ошибке подключения
        KeyError
            При ошибке обращения к словарю
    """

    try:
        response = requests.get(request_pattern + "groups.getById", params={
            "access_token": token,
            "v": version,
            "group_id": domain,
            "fields": "description"
        })
        response = response.json()["response"][0]["description"]
        with open(output, "w", encoding="UTF-8") as f:
            a_pen = csv.writer(f, delimiter=":")
            a_pen.writerow((d_result_states + domain, response))

    except requests.exceptions.ConnectionError:
        sys.exit("Проверьте подключение к интернету.")
    except KeyError:
        sys.exit("Проверьте правильность введенных параметров.")


def append_item_and_sort(my_list, item):
    """Метод добавляет переданный элемент item в словарь my_list, а затем сортирует элементы по количеству лайков

    Parameters
    ----------
    my_list: []
        список постов/комментариев
    item: пост/комментарий, представленный словарем
        элемент на добавление в список

    Returns
    ----------
    min_value: int
        минимальное количество лайков среди всех элементов в итоговом списке
    bottom_item: dict
        минимальный по количеству лайков элемент в итоговом списке
    """

    my_list.append(item)
    my_list.sort(key=lambda x: x["likes"]["count"])
    min_value = my_list[0]["likes"]["count"]
    bottom_item = my_list[0]
    return min_value, bottom_item


def get_posts(domain):
    """Метод получения 100 постов со стены группы ВК

        Parameters
        ----------
        domain: str
            короткое имя группы ВК

        Returns
        ----------
        result: json
            json объект, содержащий 100 постов
    """
    response = requests.get(request_pattern + "wall.get",
                            params={"access_token": token,
                                    "v": version,
                                    "domain": domain,
                                    "count": count})
    return response.json()["response"]["items"]


def get_comments(post_id, owner_id, comments_count):
    """Метод получения комментариев из указанного поста со стены группы ВК

        Parameters
        ----------
        post_id: int
            id поста
        owner_id: int
            id группы ВК
        comments_count: int
            количество комментариев, которые нужно вернуть

        Returns
        ----------
        result: json
            json объект, содержащий comments_count комментариев
    """

    response = requests.get(request_pattern + "wall.getComments",
                            params={
                                "access_token": token,
                                "v": version,
                                "post_id": post_id,
                                "owner_id": owner_id,
                                "need_likes": 1,
                                "count": comments_count
                            })
    return response.json()["response"]["items"]


def main():
    """Метод определяет обрабатывает входящие аргументы. При отсутствии параметров -p/-c/-d завершает работу скрипта

        Raises
        ------
        Exception
            При ошибке, вознишкей в методе process_command()
    """
    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(usage=f'{script_name} [OPTIONS] DOMAIN')
    parser.add_argument(
        '-p', "--posts", dest="posts", action='store_true', help="Отображает топ-10 постов по количеству лайков"
    )
    parser.add_argument(
        '-c', "--comments", dest="comments", action='store_true',
        help="Отображает топ-10 комментариев по количеству лайков"
    )
    parser.add_argument(
        '-d', "--description", dest="description", action='store_true', help="Отображает описание сообщества"
    )
    parser.add_argument('domain', help="Короткий адрес сообщества")
    args = parser.parse_args()

    if not (args.posts or args.comments or args.description):
        sys.exit(unexpected_input)

    try:
        process_command(args)
    except Exception as e:
        sys.exit(e)


if __name__ == '__main__':
    main()
