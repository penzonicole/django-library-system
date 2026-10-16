# 📚 Library Management System — Django

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0%2B-092E20?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-4.0-FF6384?style=for-the-badge&logo=chart.js&logoColor=white)

> **Academic Project** — A full-stack web application built with **Django** for library collection management, strict loan tracking, reservation waitlists, dynamic overdue fine calculations, ORM-driven analytics, and automated email notifications.

---

## 🛠️ 1. Step-by-Step Development Process

The application architecture follows the standard Django **MVT (Model-View-Template)** pattern within the modular `biblioteca_roma` project structure:

### **Phase 1: Project Setup & Relational Data Modeling**
1. **Environment Setup**: Configured virtual environment (`venv`), initialized the main Django project (`biblioteca_roma`), and created the core app (`biblioteca`).
2. **Database Models (`models.py`)**:
   - `Autor` (Author): Author registry.
   - `Livro` (Book): Catalog mapping total copies (`copias_totais`) and available stock on shelves (`copias_disponiveis`).
   - `Membro` (Member): Registered readers and library members.
   - `Emprestimo` (Loan): Links members and books with issue/due dates, statuses (`ATIVO`, `DEVOLVIDO`, `ATRASADO`), and dynamically calculated properties (`esta_atrasado`, `valor_multa`).
   - `Reserva` (Reservation): Priority queue for books currently out of stock.

### **Phase 2: Business Logic & Django ORM Aggregations (`views.py`)**
1. **Advanced Search**: Multi-field dynamic filtering using Django `Q` objects across Title, Author, or ISBN.
2. **Stock Tracking & Loan Limit Enforcement**:
   - Prevents loan checkout if a member already has **3 active loans**.
   - Automatically decrements available copies upon loan checkout and increments stock upon book return.
3. **Waitlist Reservation & Email Notifications**:
   - Displays a "Reserve Book" button when `copias_disponiveis == 0`.
   - Triggers automated emails via `send_mail` when a returned book becomes available for the next member in line.
4. **Analytics & Reports**:
   - Most borrowed books ranking compiled via `.annotate(total_emprestimos=Count('emprestimo'))`.
   - Monthly time-series data aggregation using `TruncMonth` to feed interactive **Chart.js** charts.

### **Phase 3: User Interface & Administration (`templates/` & `admin.py`)**
1. **Customized Django Admin**: Configured `TabularInline` views for inline loan management directly within Member profile pages.
2. **Responsive UI**: Responsive templates built with Bootstrap 5, featuring status badges, alert messages, and modal reservation views.

---

## 🚧 2. Technical Challenges & Applied Solutions

During development and refactoring, several technical challenges emerged and were resolved through architectural decisions:

| Technical Challenge | Root Cause | Implemented Solution |
| :--- | :--- | :--- |
| **Dynamic Fine Calculation** | Storing fine amounts directly in the database creates data inconsistency if returns occur at later dates. | Implemented a `@property` method on the `Emprestimo` model, dynamically calculating `(current_date - due_date) * daily_rate` only for overdue items. |
| **Database Aggregation for Charts** | Grouping loan data by month natively in SQLite for consumption by frontend libraries like Chart.js. | Leveraged Django ORM expressions (`TruncMonth` + `Count('id')`) to format labels and datasets directly into Chart.js-compatible structures. |
| **Queue Notification Logic** | Ensuring only the first waiting member in line is notified when a book copy is returned. | Queried reservations ordered by `data_reserva` filtering for `atendida=False`, updating status flags and triggering `send_mail` within the return view transaction. |
| **Git Repository Configuration** | `.gitignore` was mistakenly created as a directory, causing local SQLite databases and virtualenv files to be tracked initially. | Removed the folder via terminal (`rm -rf .gitignore`), re-created it as a proper file at the project root (`touch .gitignore`), and configured rules to ignore `venv/` and `db.sqlite3`. |

---

## 📱 3. Application Workflow & Screenshots

Below is the step-by-step application flow alongside corresponding interface screenshots:

### **1. Book Catalog & Advanced Search**
> *Real-time search by title, author name, or ISBN, displaying stock availability and popular titles ranking.*

<!-- ADD YOUR MAIN CATALOG SCREENSHOT HERE (lista_livros.html) -->
![Library catalog webpage showing book listings with title, author, ISBN search, stock availability, and borrow or reserve options in a clean interface](img//Users/elenescu/Desktop/Screenshot 2026-10-16 alle 17.31.32.png800x400)

- **Workflow**: The search bar evaluates `Q(titulo__icontains=q) | Q(autor__nome__icontains=q)`. When available copies reach 0, the "Borrow" action automatically switches to "Reserve Book".

---

### **2. Loan Limit Validation & Reader History**
> *Loan checkout interface enforcing a maximum threshold of 3 active loans per member.*

<!-- ADD YOUR LOAN HISTORY OR LIMIT WARNING SCREENSHOT HERE -->
![Library catalog page with a blue alert reading O membro Julia já atingiu o limite máximo de 3 empréstimos ativos simultâneos. Four book cards list Quando, Tudo é Rio, Suicidas, and Dias Perfeitos, with authors, ISBNs, total and available copies, and checkout controls. Tudo é Rio has zero available copies and a yellow Reservar Livro button. A search bar, Dashboard and Painel Admin buttons, and a most-borrowed-books report surround the catalog in a clean, neutral interface; the alert clearly communicates the borrowing limit.](/Users/elenescu/Desktop/Screenshot 2026-10-16 alle 17.35.55.png)

- **Workflow**: If a member attempts to check out a 4th book, Django displays a flash error message (`messages.error`). The loan history view presents visual badges (`Active`, `Returned`, or `Overdue`) and displays accrued late fines automatically.

---

### **3. Analytics Dashboard with Chart.js**
> *Administrative dashboard displaying metric cards and monthly loan trend charts.*

<!-- ADD YOUR DASHBOARD SCREENSHOT HERE (dashboard.html) -->
![Library loans dashboard in a clean, light interface. Three summary cards show Total de Livros: 4, Total de Membros: 1, and Total de Empréstimos: 3. Below, a blue monthly loans chart titled Evolução Mensal de Empréstimos shows 3 loans for Oct/2026; a Voltar ao Acervo button appears at the top right. The uncluttered administrative screen has a clear, informative tone.](image.png)
- **Workflow**: Powered by Chart.js consuming ORM monthly aggregated queries (`TruncMonth`), giving administrators a visual overview of library activity over time.

---

### **4. Custom Django Admin Interface**
> *Tailored admin panel featuring embedded loan records inside member detail pages.*

<!-- ADD YOUR DJANGO ADMIN SCREENSHOT HERE -->
![Django administration dashboard in a dark interface. The heading reads Site administration. Sections list Authentication and Authorization, with Groups and Users, and Biblioteca, with Authors, Emprestimos, Livros, Membros, and Reservas; each item has Add and Change links. A Recent actions panel lists Julia borrowing Tudo é Rio and Suicidas, followed by recent entries for Julia, Dias Perfeitos, Suicidas, Raphael Montes, Quando, Tudo é Rio, and Carla Madeira. The top bar reads Django administration and includes Welcome, View site, Change password, and Log out. The organized, utilitarian interface contains no people.](/Users/elenescu/Desktop/Screenshot 2026-10-16 alle 15.25.44.png)

- **Workflow**: Using `EmprestimoInline`, administrators can view and manage borrowing records directly within the member editing interface without switching pages.

---

## 🔧 Local Setup & Installation

```bash
# 1. Clone the repository
git clone [https://github.com/penzonicole/django-library-system.git](https://github.com/penzonicole/django-library-system.git)
cd django-library-system

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create superuser (for Admin panel access)
python manage.py createsuperuser

# 6. Start development server
python manage.py runserver 8001
## 📱 3. Application Workflows & Interface Overview

The system features a responsive, Bootstrap-powered interface designed for both public readers and library administrators. Below is a detailed breakdown of the main application screens and administrative workflows:

---

### **1. Book Catalog & Real-Time Search (`lista_livros.html`)**
The public homepage serves as the primary catalog interface, allowing readers to browse titles and manage stock in real time.

* **Multi-Field Search Bar**: Implements Django ORM `Q` objects (`Q(titulo__icontains=q) | Q(autor__nome__icontains=q) | Q(isbn__icontains=q)`), allowing instant filtering by Book Title, Author Name, or ISBN.
* **Live Stock Status**: Displays total copies versus available copies for checkout.
* **Dynamic Action Buttons**:
  * **"Emprestar" (Checkout)**: Available when stock is greater than zero (`copias_disponiveis > 0`).
  * **"Reservar Livro" (Reserve)**: Dynamically replaces the checkout button when available stock reaches zero (`copias_disponiveis == 0`), placing the user into a priority waitlist queue.
* **Popular Titles Ranking**: An embedded panel listing top-borrowed books powered by Django ORM aggregation: `.annotate(total_loans=Count('emprestimo')).order_by('-total_loans')[:5]`.

---

### **2. Member Loans & Dynamic Fines (`meus_emprestimos.html`)**
A dedicated dashboard for members to track active and past borrowing activity.

* **Loan Limit Enforcement**: Enforces a strict threshold of **maximum 3 active loans** per member. Attempting to check out a 4th title triggers an automated error alert (`messages.error`).
* **Visual Status Badges**:
  * 🟢 **Ativo (Active)**: Currently borrowed within the valid loan period.
  * 🔴 **Atrasado (Overdue)**: Loan period expired without return.
  * ⚪ **Devolvido (Returned)**: Item successfully returned to library inventory.
* **Dynamic Late Fine Calculation**: For overdue items, the table dynamically displays accumulated late penalties calculated at **R$ 2.00 per overdue day** via the `@property def valor_multa(self)` method in the `Emprestimo` model.

---

### **3. Analytics Dashboard & Charts (`dashboard.html`)**
An executive reporting screen designed for library managers to track key performance metrics and trends.

* **Metric Cards**: Quick summary metrics showing total registered members, active loans, pending reservations, and total accrued fines.
* **Chart.js Monthly Trends**: An interactive bar/line chart displaying monthly loan counts, generated using Django ORM date truncation (`TruncMonth('data_emprestimo')`) and count aggregation (`Count('id')`).
* **Inventory Overview**: A visual breakdown comparing total book inventory against currently checked-out copies.

---

### **4. Custom Django Admin Panel (`admin.py`)**
An optimized backend interface tailored for library staff and system administrators.

* **`TabularInline` Member Loans**: Embedded `EmprestimoInline` within the `MembroAdmin` detail view, allowing staff to view, create, or update a member's loan history directly on their profile page without navigating away.
* **Custom List Display & Filters**: Optimized Django Admin list views with custom filters for loan status (`ATIVO`, `DEVOLVIDO`, `ATRASADO`), search bars for author/member lookup, and quick action links.