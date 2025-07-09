# data-masking-service


Сервис предназначен для маскирования данных. В данный момент маскируются следующие сущности: 
- ИНН
- ФИО
- Телефон
- Почта

Логика работы основана на регулярных выражениях и словарях, загружаемых из S3 при старте сервиса.
# Инструкция по установке

- Перейти в папку `app`
- Создать файл `.env` со следующим содержимым:
```dotenv
MASKER_TYPE=presidio
MASKER_CONFIG_PATH=configs/analyzer.yaml

# s3 credentials
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_ENDPOINTURL=
```  

- Собрать и запустить приложение `docker-compose up --build` 

# API

###  1. **`/mask`** (POST)
- **Request body**:
```json
{
  "input": {
    "key1": "Меня зовут Владимир!",
    "key2": "Привет, Владимир!",
    "key3": "Мой телефон:",
    "key4": "89071511756",
    "key5": "Ваш телефон 89071511756 получен!"
  }
}
```
- **Response**:
```json
{
  "metadata": {
    "<PHONE_NUMBER_0>": "89071511756",
    "<NAME_0>": "Владимир"
  },
  "output": {
    "key1": "Меня зовут <NAME_0>!",
    "key2": "Привет, <NAME_0>!",
    "key3": "Пополните баланс моего телефона:",
    "key4": "<PHONE_NUMBER_0>",
    "key5": "Ваш телефон <PHONE_NUMBER_0> получен!"
  }
}
```
### 2. **`/demask`** (POST)
- **Request body**:
```json
{
  "metadata": {
    "<PHONE_NUMBER_0>": "89071511756",
    "<NAME_0>": "Владимир"
  },
  "input": {
    "anotherKey1": "<NAME_0>, баланс вашего телефона <PHONE_NUMBER_0> успешно пополнен!"
  }
}
```
- **Response**:
```json
{
  "output": {
    "anotherKey1": "Владимир, баланс вашего телефона 89071511756 успешно пополнен!"
  }
}
```
