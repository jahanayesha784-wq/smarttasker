const API_URL = "http://localhost:5000";

let token = localStorage.getItem("token") || "";

function showMessage(msg) {
  const message = document.getElementById("message");
  if (message) {
    message.innerText = msg;
  } else {
    alert(msg);
  }
}

async function registerUser() {
  const name = document.getElementById("regName").value.trim();
  const email = document.getElementById("regEmail").value.trim();
  const password = document.getElementById("regPassword").value.trim();

  if (!name || !email || !password) {
    showMessage("Please fill all fields");
    return;
  }

  try {
    const res = await fetch(`${API_URL}/api/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ name, email, password })
    });

    const data = await res.json();

    if (res.ok) {
      showMessage("Registration successful. Redirecting to login...");
      setTimeout(() => {
        window.location.href = "login.html";
      }, 1000);
    } else {
      showMessage(data.message || "Registration failed");
    }
  } catch (error) {
    showMessage("Backend not connected. Start server first.");
  }
}

async function loginUser() {
  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value.trim();

  if (!email || !password) {
    showMessage("Please enter email and password");
    return;
  }

  try {
    const res = await fetch(`${API_URL}/api/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (data.token) {
      localStorage.setItem("token", data.token);
      showMessage("Login successful");

      setTimeout(() => {
        window.location.href = "dashboard.html";
      }, 800);
    } else {
      showMessage(data.message || "Login failed");
    }
  } catch (error) {
    showMessage("Backend not connected. Start server first.");
  }
}

async function createTask() {
  token = localStorage.getItem("token");

  if (!token) {
    showMessage("Please login first");
    return;
  }

  const title = document.getElementById("taskTitle").value.trim();
  const description = document.getElementById("taskDescription").value.trim();
  const assignedTo = document.getElementById("assignedTo").value.trim();
  const priority = document.getElementById("priority").value;
  const attachment = document.getElementById("attachment").files[0];

  if (!title) {
    showMessage("Task title is required");
    return;
  }

  const formData = new FormData();
  formData.append("title", title);
  formData.append("description", description);
  formData.append("priority", priority);

  if (assignedTo) {
    formData.append("assignedTo", assignedTo);
  }

  if (attachment) {
    formData.append("attachment", attachment);
  }

  try {
    const res = await fetch(`${API_URL}/api/tasks`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`
      },
      body: formData
    });

    const data = await res.json();

    if (res.ok) {
      showMessage("Task created successfully");
      setTimeout(() => {
        window.location.href = "dashboard.html";
      }, 1000);
    } else {
      showMessage(data.message || data.error || "Task creation failed");
    }
  } catch (error) {
    showMessage("Backend not connected. Start server first.");
  }
}

async function getTasks() {
  token = localStorage.getItem("token");

  if (!token) {
    alert("Please login first");
    window.location.href = "login.html";
    return;
  }

  try {
    const res = await fetch(`${API_URL}/api/tasks`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    const data = await res.json();
    const tasks = data.tasks || data;

    const pendingList = document.getElementById("pendingList");
    const completedList = document.getElementById("completedList");

    if (!pendingList || !completedList) return;

    pendingList.innerHTML = "";
    completedList.innerHTML = "";

    let total = 0;
    let pending = 0;
    let completed = 0;

    tasks.forEach((task) => {
      total++;

      const isCompleted = task.status === "Completed";

      if (isCompleted) {
        completed++;
      } else {
        pending++;
      }

      const div = document.createElement("div");
      div.className = `task ${isCompleted ? "completed" : "pending"} priority-${(task.priority || "Medium").toLowerCase()}`;
      div.draggable = true;
      div.ondragstart = (event) => dragTask(event, task._id);

      div.innerHTML = `
        <div class="task-top">
          <h3>${task.title}</h3>
          <span class="priority-badge priority-${(task.priority || "Medium").toLowerCase()}">
            ${task.priority || "Medium"}
          </span>
        </div>

        <p>${task.description || "No description"}</p>

        <span class="badge ${isCompleted ? "badge-completed" : "badge-pending"}">
          ${task.status}
        </span>

        <p><b>👤 Assigned To:</b> ${
          task.assignedTo ? task.assignedTo.email || task.assignedTo : "Not assigned"
        }</p>

        <p><b>📎 Attachment:</b> ${
          task.attachment
            ? `<a class="file-link" href="${API_URL}/uploads/${task.attachment}" target="_blank">View File</a>`
            : "No attachment"
        }</p>

        <div class="task-actions">
          ${
            !isCompleted
              ? `<button class="complete-btn" onclick="completeTask('${task._id}')">✅ Complete</button>`
              : `<button class="complete-btn" disabled>✔ Done</button>`
          }

          <button class="edit-btn" onclick="editTask('${task._id}', '${escapeText(task.title)}', '${escapeText(task.description || "")}', '${task.priority || "Medium"}')">
            ✏️ Edit
          </button>

          <button class="delete-btn" onclick="deleteTask('${task._id}')">
            🗑 Delete
          </button>
        </div>
      `;

      if (isCompleted) {
        completedList.appendChild(div);
      } else {
        pendingList.appendChild(div);
      }
    });

    document.getElementById("totalTasks").innerText = total;
    document.getElementById("pendingTasks").innerText = pending;
    document.getElementById("completedTasks").innerText = completed;
  } catch (error) {
    alert("Backend not connected. Start server first.");
  }
}

function escapeText(text) {
  return String(text).replace(/'/g, "\\'");
}

async function completeTask(id) {
  await updateTaskStatus(id, "Completed");
}

function allowDrop(event) {
  event.preventDefault();
}

function dragTask(event, id) {
  event.dataTransfer.setData("taskId", id);
}

async function dropTask(event, status) {
  event.preventDefault();

  const taskId = event.dataTransfer.getData("taskId");

  if (!taskId) return;

  await updateTaskStatus(taskId, status);
}

async function updateTaskStatus(id, status) {
  token = localStorage.getItem("token");

  try {
    const res = await fetch(`${API_URL}/api/tasks/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ status })
    });

    if (res.ok) {
      getTasks();
    } else {
      alert("Task update failed");
    }
  } catch (error) {
    alert("Backend not connected.");
  }
}

async function editTask(id, oldTitle, oldDescription, oldPriority) {
  const newTitle = prompt("Enter new title:", oldTitle);
  if (!newTitle) return;

  const newDescription = prompt("Enter new description:", oldDescription);
  const newPriority = prompt("Enter priority: Low, Medium, High", oldPriority || "Medium");

  token = localStorage.getItem("token");

  try {
    const res = await fetch(`${API_URL}/api/tasks/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        title: newTitle,
        description: newDescription,
        priority: newPriority || "Medium"
      })
    });

    if (res.ok) {
      getTasks();
    } else {
      alert("Task edit failed");
    }
  } catch (error) {
    alert("Backend not connected.");
  }
}

async function deleteTask(id) {
  const confirmDelete = confirm("Are you sure you want to delete this task?");
  if (!confirmDelete) return;

  token = localStorage.getItem("token");

  try {
    const res = await fetch(`${API_URL}/api/tasks/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (res.ok) {
      getTasks();
    } else {
      alert("Task delete failed");
    }
  } catch (error) {
    alert("Backend not connected.");
  }
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "login.html";
}

if (window.location.pathname.includes("dashboard.html")) {
  getTasks();
}