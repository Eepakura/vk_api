token = "ca466e4dca466e4dca466e4de1ca3aa534cca46ca466e4da8d69badf37350165835684a"
request_pattern = "https://api.vk.com/method/"
version = 5.92
count = 100
unexpected_input = "Некорректный ввод. Для получения справки используйте параметр -h"
usage_help = "Консольное приложение может:\n" \
             "1. Показать топ-10 постов по количеству лайков\n" \
             "Использование: python main.py -p {domain}" \
             "domain - Короткий адрес сообщества\n" \
             "" \
             "2. Показать описание сообщества\n" \
             "Использование: python main.py -d {domain}\n" \
             "domain - Короткий адрес сообщества\n" \
             "" \
             "3. Показать топ-10 комментариев под постами по количеству лайков\n" \
             "Использование: python main.py -c {domain}\n" \
             "domain - Короткий адрес сообщества\n" \
             "" \
             "4. Показать справку по использованию\n" \
             "Использование: python main.py -h\n"
p_result_states = ("place", "likes", "post")
c_result_states = ("place", "likes", "comment")
d_result_states = "Описание для паблика "

sep = ("------------------------------------------------------------")
output = "output.txt"

