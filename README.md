# 📚 Library Management System (Django)

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=flat&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat&logo=bootstrap&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-4.0-FF6384?style=flat&logo=chart.js&logoColor=white)

A feature-rich, full-stack **Library Management System** built with **Django**. The platform automates book loan tracking, member management, late return penalties, queue reservation systems, and real-time analytical dashboards.

---

## ✨ Key Features & Business Logic

- 📖 **Catalog & Inventory Management**: Track books, authors, total copies, and real-time available stock.
- 🔄 **Loan & Return Lifecycle**: Automated stock adjustment upon book dispatch and return.
- 💰 **Automated Late Fine Calculation**: Dynamic assessment of overdue fines based on daily rates calculated via Django model properties.
- 📌 **Reservation Queue System**: Enables members to join a waitlist when book stock reaches zero.
- 🔢 **Concurrent Loan Limits**: Enforces a strict limit (maximum 3 active loans per member) to ensure fair inventory distribution.
- 📧 **Automated Email Notifications**: Built-in `send_mail` integration to notify members on checkout and when reserved titles become available.
- 📊 **Analytics Dashboard**: Dynamic monthly metrics rendered using **Chart.js** and Django ORM aggregation (`TruncMonth`, `annotate`, `Count`).
- 🛠️ **Custom Django Admin**: Configured with `TabularInline` for embedded loan management inside member profiles.

---

## 📂 Project Architecture

```text
biblioteca_roma/
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
├── config/                  # Django Settings & URL Routing
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── biblioteca/              # Main Application App
    ├── migrations/
    ├── templates/
    │   └── biblioteca/
    │       ├── lista_livros.html
    │       ├── meus_emprestimos.html
    │       └── dashboard.html
    ├── models.py            # Author, Book, Member, Loan & Reservation models
    ├── admin.py             # Tailored Admin interface & TabularInlines
    ├── views.py             # Business rules, queries & ORM aggregations
    └── urls.py              # Application routes