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
    Payment ||--|{ PayLog : payment_id
    Payment }|--|| User : author_email
    PayLog }|--|| User : author_email
    Debt }|--|| User : author_email

    Debt {
        int id PK
        string name
        date date
        int amount
        int period
        float rate
        string author_email FK
    }

    User {
        string email PK
        string name
        string password
        bool admin
    }

    Payment {
        int id PK
        int debt_id FK
        datetime date
        string month
        int amount
        string author_email FK
    }

    PayLog {
        int id PK
        int payment_id FK
        datetime date
        int amount
        string author_email FK
    }
```
