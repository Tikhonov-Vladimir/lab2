import csv
import requests
from bs4 import BeautifulSoup

dialog = {
    'greeting': ['Здравствуйте! Давайте подберем вам анимэ!'],
    'questions': ['Какой жанр вас интересует? \
Пожалуйста, пишите на английском! \
Если данный параметр вам не важен, ведите Enter.',
                  'Какая минимальная оценка? \
Если у вас вещественное число, пишите его через точку. \
Если данный параметр вам не важен, ведите Enter.',
                  'Какое минимальное количество отзывов должно быть? \
Если данный параметр вам не важен, ведите Enter.',
                  'Каких предупреждений не должно быть? \
Пожалуйста, пишите на английском!. \
Если данный параметр вам не важен, ведите Enter.',
                  'Какой формат анимэ вас устроит? \
Пожалуйста, пишите на английском! \
Если данный параметр вам не важен, ведите Enter.',
                  'Какое минимальное количество эпизодов? \
Если данный параметр вам не важен, ведите Enter.',
                  'Анимэ должно быть закончено? \
Введите True или False. \
Если данный параметр вам не важен, ведите Enter.',
                  'Какой год начала съемки анимэ вас интересует? \
Если данный параметр вам не важен, ведите Enter.',
                  'Какой год окончания съемки анимэ вас интересует? \
Если данный параметр вам не важен, ведите Enter.',
                  'Какой сезон съемки анимэ вам нужен? \
Пожалуйста, пишите на английском! \
Если данный параметр вам не важен, ведите Enter.',
                  'Какая студия вас интересует? \
Если данный параметр вам не важен, ведите Enter.'
                  ]
}
question = [
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
]
answer_equal = {
    'Type': '',
    'Finished': '',
    'StartYear': '',
    'EndYear': '',
    'Studios': ''
}
answer_more = {
    'Rating Score': '',
    'Number Votes': '',
    'Episodes': ''
}
answer_in = {
    'Tags': '',
    'Season': ''
}
answer_not_in = {
    'Content Warning': ''
}
answers = [answer_in, answer_not_in, answer_more, answer_equal]


def run_dialog():
    print(dialog['greeting'][0])
    questions = dialog['questions']
    for k in range(len(questions)):
        ans = input(questions[k])
        for an in answers:
            if question[k] in an:
                an[question[k]] = ans


run_dialog()
answer = []
with open('anime.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        good = True
        for i in answer_equal:
            if answer_equal[i] != row[i] and answer_equal[i] != '':
                good = False
        for i in answer_more:
            if answer_more[i] != '':
                if row[i] == 'Unknown':
                    good = False
                elif float(answer_more[i]) > float(row[i]):
                    good = False
        for i in answer_in:
            for j in answer_in[i].split():
                if not (j in row[i]):
                    good = False
        for i in answer_not_in:
            for j in answer_not_in[i].split():
                if j in row[i]:
                    good = False
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
