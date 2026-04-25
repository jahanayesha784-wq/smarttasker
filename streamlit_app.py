import streamlit as st
import requests

API_URL = "http://localhost:5000"

st.set_page_config(
    page_title="SmartTasker",
    page_icon="🚀",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef2ff, #fdf4ff);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #1e3a8a);
}

[data-testid="stSidebar"] * {
    color: white;
}

.main-title {
    font-size: 48px;
    font-weight: 800;
    color: #1e3a8a;
    margin-bottom: 5px;
}

.sub-title {
    font-size: 18px;
    color: #64748b;
    margin-bottom: 25px;
}

.auth-card {
    background: white;
    padding: 35px;
    border-radius: 22px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.12);
    border: 1px solid #dbeafe;
}

.stat-card {
    padding: 28px;
    border-radius: 22px;
    color: white;
    box-shadow: 0 12px 28px rgba(0,0,0,0.18);
    transition: 0.3s;
}

.stat-card:hover {
    transform: translateY(-6px);
}

.purple {
    background: linear-gradient(135deg, #7c3aed, #a855f7);
}

.blue {
    background: linear-gradient(135deg, #2563eb, #06b6d4);
}

.green {
    background: linear-gradient(135deg, #059669, #22c55e);
}

.task-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 18px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.1);
    border-left: 8px solid #2563eb;
    transition: 0.3s;
}

.task-card:hover {
    transform: translateY(-5px);
}

.task-pending {
    border-left-color: #f59e0b;
    background: #fffbeb;
}

.task-completed {
    border-left-color: #16a34a;
    background: #ecfdf5;
}

.priority-high {
    color: white;
    background: #dc2626;
    padding: 6px 12px;
    border-radius: 20px;
    font-weight: bold;
}

.priority-medium {
    color: white;
    background: #f59e0b;
    padding: 6px 12px;
    border-radius: 20px;
    font-weight: bold;
}

.priority-low {
    color: white;
    background: #16a34a;
    padding: 6px 12px;
    border-radius: 20px;
    font-weight: bold;
}

.stButton > button {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    font-weight: bold;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #1d4ed8, #6d28d9);
    color: white;
}

[data-testid="stMetricValue"] {
    color: #1e3a8a;
}
</style>
""", unsafe_allow_html=True)
# ---------- SESSION ----------
if "token" not in st.session_state:
    st.session_state.token = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ---------- SIDEBAR ----------
st.sidebar.markdown("## 🚀 SmartTasker")
menu = st.sidebar.radio(
    "Navigation",
    ["Register", "Login", "Create Task", "Dashboard"]
)

st.sidebar.markdown("---")
st.sidebar.write("Task Management System")
st.sidebar.write("Node.js + MongoDB + Streamlit")

# ---------- HEADER ----------
st.markdown('<div class="main-title">🚀 SmartTasker</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">A professional task management system with authentication, file upload, priority, and dashboard.</div>', unsafe_allow_html=True)

# ---------- REGISTER ----------
if menu == "Register":
    st.markdown("## 📝 Create Account")

    with st.container():
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            if not name or not email or not password:
                st.error("Please fill all fields")
            else:
                try:
                    res = requests.post(f"{API_URL}/api/auth/register", json={
                        "name": name,
                        "email": email,
                        "password": password
                    })

                    data = res.json()

                    if res.status_code in [200, 201]:
                        st.success("Account created successfully. Now login.")
                    else:
                        st.warning(data.get("message", "Registration failed"))

                except:
                    st.error("Backend not connected. Start Node.js server first.")

        st.markdown('</div>', unsafe_allow_html=True)

# ---------- LOGIN ----------
elif menu == "Login":
    st.markdown("## 🔐 Login")

    with st.container():
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if not email or not password:
                st.error("Please enter email and password")
            else:
                try:
                    res = requests.post(f"{API_URL}/api/auth/login", json={
                        "email": email,
                        "password": password
                    })

                    data = res.json()

                    if "token" in data:
                        st.session_state.token = data["token"]
                        st.session_state.user_email = email
                        st.success("Login successful")
                    else:
                        st.error(data.get("message", "Login failed"))

                except:
                    st.error("Backend not connected. Start Node.js server first.")

        st.markdown('</div>', unsafe_allow_html=True)

# ---------- CREATE TASK ----------
elif menu == "Create Task":
    st.markdown("## ✨ Create New Task")

    if not st.session_state.token:
        st.warning("Please login first.")
    else:
        title = st.text_input("Task Title", key="task_title")
        description = st.text_area("Task Description", key="task_description")

        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"],
            index=1,
            key="task_priority"
        )

        assigned_to = st.text_input(
            "Assigned User ID Optional",
            key="assigned_to"
        )

        attachment = st.file_uploader(
            "Upload Attachment",
            key="task_attachment"
        )

        if st.button("🚀 Create Task"):
            if not title.strip():
                st.error("Task Title is required")
            else:
                headers = {
                    "Authorization": f"Bearer {st.session_state.token}"
                }

                data = {
                    "title": title.strip(),
                    "description": description.strip(),
                    "priority": priority
                }

                if assigned_to.strip():
                    data["assignedTo"] = assigned_to.strip()

                files = None

                if attachment is not None:
                    files = {
                        "attachment": (
                            attachment.name,
                            attachment.getvalue(),
                            attachment.type
                        )
                    }

                try:
                    res = requests.post(
                        f"{API_URL}/api/tasks",
                        headers=headers,
                        data=data,
                        files=files
                    )

                    response = res.json()

                    if res.status_code in [200, 201]:
                        st.success("Task created successfully")
                        st.json(response)
                    else:
                        st.error(response)

                except Exception as e:
                    st.error(f"Backend error: {e}")
                    
# ---------- DASHBOARD ----------
elif menu == "Dashboard":
    st.markdown("## 📊 Task Dashboard")

    if not st.session_state.token:
        st.warning("Please login first.")
    else:
        try:
            headers = {
                "Authorization": f"Bearer {st.session_state.token}"
            }

            res = requests.get(f"{API_URL}/api/tasks", headers=headers)

            if res.status_code != 200:
                st.error(res.json())
                st.stop()

            data = res.json()
            tasks = data if isinstance(data, list) else data.get("tasks", [])

            st.markdown("### 🔎 Search & Filter")

            search_text = st.text_input("Search tasks")
            status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
            priority_filter = st.selectbox("Filter by Priority", ["All", "Low", "Medium", "High"])

            filtered_tasks = []

            for task in tasks:
                title = task.get("title", "").lower()
                description = task.get("description", "").lower()
                status = task.get("status", "Pending")
                priority = task.get("priority", "Medium")

                if (
                    search_text.lower() in title or search_text.lower() in description
                ) and (
                    status_filter == "All" or status == status_filter
                ) and (
                    priority_filter == "All" or priority == priority_filter
                ):
                    filtered_tasks.append(task)

            total = len(tasks)
            pending = len([t for t in tasks if t.get("status") != "Completed"])
            completed = len([t for t in tasks if t.get("status") == "Completed"])
            high_priority = len([t for t in tasks if t.get("priority") == "High"])

            progress = completed / total if total > 0 else 0

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f'<div class="stat-card purple"><h3>📌 Total</h3><h1>{total}</h1></div>', unsafe_allow_html=True)

            with col2:
                st.markdown(f'<div class="stat-card blue"><h3>⏳ Pending</h3><h1>{pending}</h1></div>', unsafe_allow_html=True)

            with col3:
                st.markdown(f'<div class="stat-card green"><h3>✅ Done</h3><h1>{completed}</h1></div>', unsafe_allow_html=True)

            with col4:
                st.markdown(f'<div class="stat-card purple"><h3>🔥 High Priority</h3><h1>{high_priority}</h1></div>', unsafe_allow_html=True)

            st.markdown("### 📈 Completion Progress")
            st.progress(progress)
            st.write(f"{round(progress * 100)}% completed")

            st.markdown("### 📊 Task Status Chart")
            st.bar_chart({
                "Status": ["Pending", "Completed"],
                "Tasks": [pending, completed]
            }, x="Status", y="Tasks")

            if tasks:
                csv_data = "Title,Description,Status,Priority\n"
                for t in tasks:
                    csv_data += f'"{t.get("title", "")}","{t.get("description", "")}","{t.get("status", "")}","{t.get("priority", "")}"\n'

                st.download_button(
                    "⬇️ Download Tasks CSV",
                    data=csv_data,
                    file_name="smarttasker_tasks.csv",
                    mime="text/csv"
                )

            st.markdown("## 🗂 Your Tasks")

            if len(filtered_tasks) == 0:
                st.info("No matching tasks found.")
            else:
                for task in filtered_tasks:
                    task_id = task.get("_id")
                    status = task.get("status", "Pending")
                    priority = task.get("priority", "Medium")

                    assigned = task.get("assignedTo", "Not assigned")
                    if isinstance(assigned, dict):
                        assigned = assigned.get("email", "Not assigned")

                    task_class = "task-completed" if status == "Completed" else "task-pending"
                    priority_class = f"priority-{priority.lower()}"

                    st.markdown(f"""
                    <div class="task-card {task_class}">
                        <h3>📝 {task.get("title", "No Title")}</h3>
                        <p>{task.get("description", "No description")}</p>
                        <p><b>Status:</b> {status}</p>
                        <p><b>Priority:</b> <span class="{priority_class}">{priority}</span></p>
                        <p><b>Assigned To:</b> {assigned}</p>
                        <p><b>Attachment:</b> {
                            f'<a href="{API_URL}/uploads/{task.get("attachment")}" target="_blank">View File</a>'
                            if task.get("attachment") else "No attachment"
                        }</p>
                    </div>
                    """, unsafe_allow_html=True)

                    c1, c2, c3 = st.columns(3)

                    with c1:
                        if status != "Completed":
                            if st.button("✅ Complete", key=f"complete_{task_id}"):
                                requests.put(
                                    f"{API_URL}/api/tasks/{task_id}",
                                    headers={
                                        "Authorization": f"Bearer {st.session_state.token}",
                                        "Content-Type": "application/json"
                                    },
                                    json={"status": "Completed"}
                                )
                                st.rerun()
                        else:
                            st.success("Completed ✔")

                    with c2:
                        with st.expander("✏️ Update"):
                            new_title = st.text_input("New Title", value=task.get("title", ""), key=f"title_{task_id}")
                            new_description = st.text_area("New Description", value=task.get("description", ""), key=f"desc_{task_id}")
                            new_priority = st.selectbox(
                                "Priority",
                                ["Low", "Medium", "High"],
                                index=["Low", "Medium", "High"].index(priority) if priority in ["Low", "Medium", "High"] else 1,
                                key=f"priority_{task_id}"
                            )

                            if st.button("Save Update", key=f"update_{task_id}"):
                                requests.put(
                                    f"{API_URL}/api/tasks/{task_id}",
                                    headers={
                                        "Authorization": f"Bearer {st.session_state.token}",
                                        "Content-Type": "application/json"
                                    },
                                    json={
                                        "title": new_title,
                                        "description": new_description,
                                        "priority": new_priority
                                    }
                                )
                                st.success("Task updated")
                                st.rerun()

                    with c3:
                        if st.button("🗑 Delete", key=f"delete_{task_id}"):
                            requests.delete(
                                f"{API_URL}/api/tasks/{task_id}",
                                headers={
                                    "Authorization": f"Bearer {st.session_state.token}"
                                }
                            )
                            st.rerun()

        except Exception as e:
            st.error(f"Dashboard error: {e}")