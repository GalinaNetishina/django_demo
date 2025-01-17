# Тестирование Django-приложения

## Описание

Есть бэкенд простого приложения с курсами и списком студентов. Вся логика для бэкенда уже есть в заготовке, но совершенно нет тестов.

## Что нужно сделать

необходимо написать тесты для текущей логики приложения.

Создали фикстуры:

- для api-client,
- для фабрики курсов,
- для фабрики студентов.

В качестве библиотеки для фабрик используем `model_bakery` (https://github.com/model-bakers/model_bakery).

Добавлены следующие тест-кейсы:

- проверка получения первого курса (retrieve-логика)

- проверка получения списка курсов (list-логика)
  
- проверка фильтрации списка курсов по `id`
  
- проверка фильтрации списка курсов по `name`

- тест успешного создания курса
  
- тест успешного обновления курса
 
- тест успешного удаления курса.

Все тесты явно проверяют код возврата.


Запуск тестов делается через команду:

```
$ pytest
```



## Дополнительные задания (необязательные для выполнения)

### Ограничить число студентов на курсе

 -[ ] Добавить валидацию на максимальное число студентов на курсе (`settings.py`: `MAX_STUDENTS_PER_COURSE`) . 


## Документация по проекту

Для запуска проекта необходимо

Установить зависимости:

```bash
pip install -r requirements-dev.txt
```


