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
  "texts": ["телефон - +79211234556", "имя - иван альбертович парфенов"]
}
```
- **Response**:
```json
[
  {
    "masked_text": "телефон - <PHONE_NUMBER_0>",
    "mask_mapping": {
      "<PHONE_NUMBER_0>": "+79211234556"
    }
  },
  {
    "masked_text": "имя - <NAME_0> <MIDNAME_0> <SURNAME_0>",
    "mask_mapping": {
      "<NAME_0>": "иван",
      "<SURNAME_0>": "парфенов",
      "<MIDNAME_0>": "альбертович"
    }
  }
]
```
