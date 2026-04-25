#  SmartTasker – Task Management System

SmartTasker is a full-stack task management system that helps users organize, track, and manage tasks efficiently.  
It supports task creation, assignment, file uploads, authentication, and an interactive dashboard.

The system is built using **Node.js, Express.js, MongoDB, and Streamlit**, and follows modern development practices including **Git version control and CI/CD using GitHub Actions**.

---

#  Live Application

You can access the deployed SmartTasker dashboard here:

 https://smarttasker-xntanq5sbuexs2mlhfed6d.streamlit.app/

The live dashboard allows users to:

- View tasks
- Update tasks
- Delete tasks
- Track task progress
- Monitor statistics

---

#  Features

##  User Authentication
- User Registration
- Secure Login using JWT
- Password hashing using bcrypt
- Protected API routes

##  Task Management
- Create tasks
- Assign tasks to team members
- View tasks
- Update tasks
- Delete tasks
- Mark tasks as completed

##  File Upload
- Upload attachments with tasks
- Files stored in server upload directory
- File information stored in database

##  Dashboard
Interactive Streamlit dashboard displaying:

- Total tasks
- Completed tasks
- Pending tasks
- Task progress

##  CI/CD Integration
GitHub Actions pipeline automatically checks the project when code is pushed to GitHub.

---

#  System Architecture

SmartTasker follows a **three-layer architecture**:

### Client Layer
- Web Browser
- Streamlit Dashboard

### Application Layer
- Node.js Server
- Express.js API
- Controllers
- Middleware

### Data Layer
- MongoDB Database
- File Upload Storage

---

#  System Diagrams

The project includes several UML diagrams:

- System Architecture Diagram
- Database Schema Diagram (ER Diagram)
- Use Case Diagram
- Sequence Diagram
- Activity Diagram

These diagrams explain the system structure, workflows, and interactions between components.

---

#  Database Schema

SmartTasker uses **MongoDB collections**.

## User Collection

| Field | Type |
|------|------|
| _id | ObjectId |
| name | String |
| email | String |
| password | String |
| createdAt | Date |

## Task Collection

| Field | Type |
|------|------|
| _id | ObjectId |
| title | String |
| description | String |
| priority | String |
| status | String |
| assignedTo | ObjectId |
| createdBy | ObjectId |
| attachment | String |
| createdAt | Date |

### Relationships

- One **User creates many Tasks**
- One **User can be assigned many Tasks**

---

#  Technology Stack

## Backend
- Node.js
- Express.js
- MongoDB
- Mongoose
- JWT Authentication
- bcrypt
- Multer (File Upload)

## Frontend
- HTML
- CSS
- JavaScript

## Dashboard
- Streamlit (Python)

## Development Tools
- Git
- GitHub
- VS Code
- MongoDB Compass

## CI/CD
- GitHub Actions

---

#  Project Structure

```
smarttasker
│
├── backend
│   ├── controllers
│   ├── middleware
│   ├── models
│   ├── routes
│   ├── uploads
│   ├── server.js
│   ├── package.json
│
├── frontend
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── create-task.html
│   ├── dashboard.html
│   ├── script.js
│   └── style.css
│
├── streamlit_app.py
├── requirements.txt
├── .github
│   └── workflows
│       └── node-ci.yml
│
└── README.md
```

---

#  CI/CD Pipeline

The project includes a GitHub Actions CI/CD pipeline.

Pipeline tasks include:

- Checkout repository
- Setup Node.js environment
- Install backend dependencies
- Validate backend server
- Setup Python environment
- Validate Streamlit dashboard

Pipeline configuration file:

```
.github/workflows/node-ci.yml
```

---

#  Installation Guide

## 1 Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/smarttasker.git
cd smarttasker
```

---

## 2 Install Backend Dependencies

```bash
cd backend
npm install
```

---

## 3 Run Backend Server

```bash
node server.js
```

Server runs on:

```
http://localhost:5000
```

---

## 4 Run Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

Dashboard runs on:

```
http://localhost:8501
```

---

#  Security Features

SmartTasker implements several security practices:

- JWT Authentication
- Password hashing with bcrypt
- Middleware authorization checks
- Input validation
- Protected API endpoints

---

#  Future Enhancements

Possible improvements for future versions:

- Email notifications
- Task deadlines and reminders
- Role-based access control
- Mobile application
- Kanban board interface
- Cloud deployment
- Advanced analytics dashboard

---

