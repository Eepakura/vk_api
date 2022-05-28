Задача 3. Использование API VK.

I. Документация, справка по использованию.

Консольное приложение может:
1. Показать топ-10 постов по количеству лайков 
Использование: python main.py -p {domain}
domain - Короткий адрес сообщества

2. Показать описание сообщества
Использование: python main.py -d {domain}
domain - Короткий адрес сообщества

3. Показать топ-10 комментариев под постами по количеству лайков
Использование: python main.py -c {domain}
domain - Короткий адрес сообщества

4. Показать справку по использованию
Использование: python main.py -h

II. Тестирование (примеры запуска).
Запуск: python main.py -p knife.media
Результат: top_posts_output.txt

Запуск: python main.py -c math_and_physics
Результат: top_comments_output.txt

Запуск: python main.py -d knife.media
Результат: description_output.txt
