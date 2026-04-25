const Task = require("../models/Task");

// CREATE TASK
exports.createTask = async (req, res) => {
  try {
    console.log("REQ BODY:", req.body);
    console.log("REQ FILE:", req.file);

    const title = req.body?.title;
    const description = req.body?.description || "";
    const priority = req.body?.priority || "Medium";
    const assignedTo = req.body?.assignedTo || null;

    if (!title) {
      return res.status(400).json({
        error: "Task title is required"
      });
    }

    const task = new Task({
      title,
      description,
      priority,
      assignedTo: assignedTo || undefined,
      userId: req.user.id,
      attachment: req.file ? req.file.filename : null
    });

    await task.save();

    res.status(201).json({
      message: "Task created successfully",
      task
    });

  } catch (error) {
    res.status(500).json({
      error: error.message
    });
  }
};

// GET TASKS
exports.getTasks = async (req, res) => {
  try {
    const tasks = await Task.find({
      $or: [
        { userId: req.user.id },
        { assignedTo: req.user.id }
      ]
    })
      .populate("assignedTo", "name email")
      .sort({ createdAt: -1 });

    res.json(tasks);

  } catch (error) {
    res.status(500).json({
      error: error.message
    });
  }
};

// UPDATE TASK
exports.updateTask = async (req, res) => {
  try {
    const task = await Task.findOneAndUpdate(
      {
        _id: req.params.id,
        $or: [
          { userId: req.user.id },
          { assignedTo: req.user.id }
        ]
      },
      req.body,
      { new: true }
    );

    if (!task) {
      return res.status(404).json({
        message: "Task not found"
      });
    }

    res.json({
      message: "Task updated successfully",
      task
    });

  } catch (error) {
    res.status(500).json({
      error: error.message
    });
  }
};

// DELETE TASK
exports.deleteTask = async (req, res) => {
  try {
    const task = await Task.findOneAndDelete({
      _id: req.params.id,
      userId: req.user.id
    });

    if (!task) {
      return res.status(404).json({
        message: "Task not found"
      });
    }

    res.json({
      message: "Task deleted successfully"
    });

  } catch (error) {
    res.status(500).json({
      error: error.message
    });
  }
};