import csv
import requests
from bs4 import BeautifulSoup

p = ' Пожалуйста, пишите на английском!'
e = ' Если данный параметр вам не важен, ведите Enter.'
dialog = {
    'greeting': ['Здравствуйте! Давайте подберем вам анимэ!'],
    'questions': ('Какой жанр вас интересует?' + p + e,
                  'Какая минимальная оценка? Если у вас вещественное число, пишите его через точку.' + e,
                  'Какое минимальное количество отзывов должно быть?' + e,
                  'Каких предупреждений не должно быть?' + p + e,
                  'Какой формат анимэ вас устроит?' + p + e,
                  'Какое минимальное количество эпизодов?' + e,
                  'Анимэ должно быть закончено? Введите True или False.' + e,
                  'Какой год начала съемки анимэ вас интересует?' + e,
                  'Какой год окончания съемки анимэ вас интересует?' + e,
                  'Какой сезон съемки анимэ вам нужен?' + p + e,
                  'Какая студия вас интересует?' + p + e
                  )
}
question = (
    'Tags',
    'Rating Score',
    'Number Votes',
    'Content Warning',
    'Type',
    'Episodes',
    'Finished',
    'StartYear',
    'EndYear',
    'Season',
    'Studios'
)
answer_equal = {
    'Type': '',
    'Finished': '',
    'StartYear': '',
    'EndYear': ''
}
answer_more = {
    'Rating Score': '',
    'Number Votes': '',
    'Episodes': ''
}
answer_in = {
    'Tags': '',
    'Season': '',
    'Studios': ''
}
answer_not_in = {
    'Content Warning': ''
}
answers = [answer_in, answer_not_in, answer_more, answer_equal]


def save_answer(ans, q_type, answers):
    for answer_gr in answers:
        if q_type in answer_gr:
            answer_gr[q_type] = ans


def run_dialog(answers, dialog):
    print(*dialog['greeting'])
    questions = dialog['questions']
    for k in range(len(questions)):
        ans = input(questions[k])
        save_answer(ans, question[k], answers)


def is_equal(answer_in, entry):
    return True if answer_in in ('', entry) else False


def is_more(answer_in, entry):
    if answer_in == '':
        answer_in = float(0)
    if entry == 'Unknown':
        entry = float(0)
    return True if float(answer_in) <= float(entry) else False


def is_in(answer_in, entry):
    return True if answer_in in entry else False


def is_not_in(answer_in, entry):
    return False if answer_in in entry else True


run_dialog(answers, dialog)
answer = []

with open('anime.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        good = True
        for key, val in answer_equal.items():
            good = good and is_equal(val, row[key])

        for key, val in answer_more.items():
            good = good and is_more(val, row[key])

        for key, val in answer_in.items():
            for j in val.split():
                good = good and is_in(j, row[key])

        for key, val in answer_not_in.items():
            for j in val.split():
                good = good and is_not_in(j, row[key])

        if good:
            if row['Rating Score'] == 'Unknown':
                answer.append([float(0), row['Url'], row['Name']])
            else:
                answer.append([float(row['Rating Score']), row['Url'], row['Name']])
answer.sort()
answer.reverse()
f = open('answer.txt', 'w', encoding='utf-8')
for i in range(min(5, len(answer))):
    response = requests.get(answer[i][1])  # отправляем запрос на страницу. answer[i][1] - ссылка на странцу с постером.
    soup = BeautifulSoup(response.text,
                         'html.parser')  # BeautifulSoup позволяет преобразовать сложный HTML-документ в объекты Python
    img = requests.get("https://www.anime-planet.com/" + soup.find('img', class_='screenshots')['src'])
    img_file = open(str(i + 1) + '.jpg', 'wb')
    img_file.write(img.content)
    img_file.close()
    f.write(answer[i][2] + ': ' + answer[i][1] + '\n')
for i in range(min(5, len(answer)), len(answer)):
    f.write(answer[i][2] + ': ' + answer[i][1] + '\n')
f.close()

print('---------------------------------------------------------------------------------------------------------------')
print('На этом все. Подходящие вашим запросам анимэ и ссылки на них находятся в файле answer.txt.\n')
print('Анимэ отсортированы в порядке убывания их рейтинга.\n')
print('Для первых 5 анимэ с лучшим рейтингом вы можете посмотреть постеры.\n')
print('Они находятся в файлах 1-5.jpg соответственно.')
