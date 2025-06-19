# 🧠 ATS Project – Candidate Tracking System (Django + DRF)

A lightweight Applicant Tracking System (ATS) built using Django REST Framework.  
It helps recruiters manage candidates by providing CRUD operations and a powerful search API.

---

## 🚀 Features

- ✅ Create, update, delete, and list candidate profiles
- ✅ Search candidates by name (with partial word matching & relevancy scoring)
- 🧠 Clean architecture using Service Layer, Abstract Base Classes (SOLID principles)
- 🚀 *Optional*: Elasticsearch integration for typo-tolerant search

---

## 📦 Tech Stack

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Python 3.10+]
- *Optional*: [Elasticsearch 7.17+](https://www.elastic.co/elasticsearch/)

---

## 🛠️ Setup Instructions

### 1. Clone the Project

git clone https://github.com/yourusername/ats_project.git
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
cd ats_project
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate


## 🔌 API Overview

All endpoints are served at: http://localhost:8000/api/candidates/


---

### 📘 1. Create Candidate

- **Method:** `POST`
- **URL:** `/candidates/`

#### 🔸 Request

{
  "name": "Ajay Kumar",
  "age": 28,
  "gender": "M",
  "email": "ajay@example.com",
  "phone_number": "9876543210"
}

#### 🔸 Response

{
  "id": 1,
  "name": "Ajay Kumar",
  "age": 28,
  "gender": "M",
  "email": "ajay@example.com",
  "phone_number": "9876543210"
}


### 📘 2. Search Candidates

- **Method:** `GET`
- **URL:** `/candidates/?q=Ajay Kumar`

#### 🔸 Response

[
  {
    "id": 1,
    "name": "Ajay Kumar",
    "age": 28,
    "gender": "M",
    "email": "ajay@example.com",
    "phone_number": "9876543210"
  },
  {
    "id": 2,
    "name": "Ajay Singh",
    "age": 30,
    "gender": "M",
    "email": "ajay.singh@example.com",
    "phone_number": "9123456789"
  }
]


### 📘 3. Full Update Candidate

- **Method:** `PUT`
- **URL:** `/candidates/`

#### 🔸 Request

{
  "id": 1,
  "name": "Ajay Kumar",
  "age": 28,
  "gender": "M",
  "email": "ajay.1@example.com",
  "phone_number": "9876543211"
}

#### 🔸 Response

{
  "id": 1,
  "name": "Ajay Kumar",
  "age": 28,
  "gender": "M",
  "email": "ajay.1@example.com",
  "phone_number": "9876543211"
}


### 📘 4. Partial Update Candidate

- **Method:** `PATCH`
- **URL:** `/candidates/`

#### 🔸 Request

{
  "id": 1,
  "age": 30
}

#### 🔸 Response

{
  "id": 1,
  "name": "Ajay Kumar",
  "age": 30,
  "gender": "M",
  "email": "ajay@example.com",
  "phone_number": "9876543210"
}

### 📘 5. Delete Candidate

- **Method:** `DELETE`
- **URL:** `/candidates/?id=1`

#### 🔸 Response

204 No Content


### 🔍 Search Example

Example:  
For query `q=Ajay Kumar Yadav`, the result order could be:

- "Ajay Kumar Yadav"  
- "Ajay Kumar"  
- "Ajay Yadav"  
- "Kumar Yadav"

> **Note:** Elasticsearch can be used instead of ORM filters to support typo correction and ranking based on fuzziness.

