import csv
import requests
from bs4 import BeautifulSoup

print('Здравствуйте! Давайте подберем вам анимэ! Для продолжения введите Enter =)')
start_program = input()
print('Какой жанр вас интересует? Пожалуйста, пишите на английском! Если данный параметр вам не важен, ведите Enter.')
tags = input().split()
print('Какая минимальная оценка? Если у вас вещественное число, пишите его через точку. Если данный параметр вам не важен, ведите Enter.')
Rating = input()
print('Какое минимальное количество отзывов должно быть? Если данный параметр вам не важен, ведите Enter.')
number_of_votes = input()
print('Каких предупреждений не должно быть? Пожалуйста, пишите на английском!. Если данный параметр вам не важен, ведите Enter.')
content_warning = input().split()
print('Какой формат анимэ вас устроит? Пожалуйста, пишите на английском! Если данный параметр вам не важен, ведите Enter.')
form = input()
print('Какое минимальное количество эпизодов? Если данный параметр вам не важен, ведите Enter.')
episodes = input()
print('Анимэ должно быть закончено? Введите True или False. Если данный параметр вам не важен, ведите Enter.')
finish = input()
print('Какой год начала съемки анимэ вас интересует? Если данный параметр вам не важен, ведите Enter.')
start = input()
print('Какой год окончания съемки анимэ вас интересует? Если данный параметр вам не важен, ведите Enter.')
end = input()
print('Какой сезон съемки анимэ вам нужен? Пожалуйста, пишите на английском! Если данный параметр вам не важен, ведите Enter.')
season = input().split()
print('Какая студия вас интересует? Если данный параметр вам не важен, ведите Enter.')
studio = input()

answer = []
with open('anime.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        good = True
        for i in tags:
            if not (i in row['Tags']):
                good = False

        if Rating != '':
            if row['Rating Score'] == 'Unknown':
                good = False
            elif float(Rating) > float(row['Rating Score']):
                good = False

        if number_of_votes != '':
            if row['Number Votes'] == 'Unknown':
                good = False
            elif float(number_of_votes) > float(row['Number Votes']):
                good = False

        for i in content_warning:
            if i in row['Content Warning']:
                good = False

        if form != '':
            if row['Type'] == 'Unknown':
                good = False
            elif form != row['Type']:
                good = False

        if episodes != '':
            if row['Episodes'] == 'Unknown':
                good = False
            elif float(episodes) > float(row['Episodes']):
                good = False

        if finish != '':
            if row['Finished'] == 'Unknown':
                good = False
            elif finish != row['Finished']:
                good = False

        if start != '':
            if row['StartYear'] == 'Unknown':
                good = False
            elif start != row['StartYear']:
                good = False

        if end != '':
            if row['EndYear'] == 'Unknown':
                good = False
            elif end != row['EndYear']:
                good = False

        for i in season:
            if not (i in row['Season']):
                good = False

        if studio != '':
            if row['Studios'] == 'Unknown':
                good = False
            elif studio != row['Studios']:
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
    soup = BeautifulSoup(response.text, 'html.parser')  # BeautifulSoup позволяет преобразовать сложный HTML-документ в объекты Python
    img = requests.get("https://www.anime-planet.com/" + soup.find('img', class_='screenshots')['src'])
    img_file = open(str(i + 1) + '.jpg', 'wb')
    img_file.write(img.content)
    img_file.close()
    f.write(answer[i][2] + ': ' + answer[i][1] + '\n')
for i in range(min(5, len(answer)), len(answer)):
    f.write(answer[i][2] + ': ' + answer[i][1] + '\n')
f.close()

print('---------------------------------------------------------------------------------------------------------------')
print('На этом все. Подходящие вашим запросам анимэ и ссылки на них находятся в файле answer.txt.' + '\n')
print('Анимэ отсортированы в порядке убывания их рейтинга.' + '\n')
print('Для первых 5 анимэ с лучшим рейтингом вы можете посмотреть постеры.' + '\n')
print('Они находятся в файлах 1-5.jpg соответственно.')
