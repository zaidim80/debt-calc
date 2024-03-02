# Калькулятор задолженности

Клиент-серверное приложение для хранения информации о долгах в форме кредита:

- Список долгов/кредитов
- История платежей
- Расчет предстоящих платежей

## Платформа

FastAPI + Vue.js

## Структура данных

```mermaid
erDiagram
    Debt ||--|{ Payment : debt_id
    Payment }|--|| User : author_email
    Debt {
        string name
        int size
        date start
        float percent
    }
    User {
        string email
        string name
        bool admin
    }
    Payment {
        date date
        int amount
    }
```
