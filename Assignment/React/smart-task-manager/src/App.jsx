import React, { useState, useEffect, useMemo } from 'react';
import TaskForm from './TaskForm';
import TaskFilters from './TaskFilters';
import TaskList from './TaskList';

export default function App() {
  // Initialize tasks from localStorage or default to an empty array
  const [tasks, setTasks] = useState(() => {
    const savedTasks = localStorage.getItem('smart-tasks');
    return savedTasks ? JSON.parse(savedTasks) : [];
  });

  // UI States
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('All'); // All, Completed, Pending
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Sync tasks to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('smart-tasks', JSON.stringify(tasks));
  }, [tasks]);

  // Core Feature: Add Task
  const addTask = (title, priority) => {
    const newTask = {
      id: crypto.randomUUID(),
      title,
      priority,
      completed: false,
    };
    setTasks((prevTasks) => [newTask, ...prevTasks]);
  };

  // Core Feature: Mark as Completed (Toggle)
  const toggleTaskStatus = (id) => {
    setTasks((prevTasks) =>
      prevTasks.map((task) =>
        task.id === id ? { ...task, completed: !task.completed } : task
      )
    );
  };

  // Core Feature: Delete Task
  const deleteTask = (id) => {
    setTasks((prevTasks) => prevTasks.filter((task) => task.id !== id));
  };

  // Core Features: Search & Filter (Optimized with useMemo)
  const filteredTasks = useMemo(() => {
    return tasks.filter((task) => {
      const matchesSearch = task.title.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesStatus =
        statusFilter === 'All' ||
        (statusFilter === 'Completed' && task.completed) ||
        (statusFilter === 'Pending' && !task.completed);

      return matchesSearch && matchesStatus;
    });
  }, [tasks, searchQuery, statusFilter]);

  // Quick stats for a mini "dashboard" feel
  const stats = useMemo(() => {
    const total = tasks.length;
    const completed = tasks.filter((t) => t.completed).length;
    return { total, completed, pending: total - completed };
  }, [tasks]);

  return (
    <div className={`min-h-screen transition-colors duration-300 ${isDarkMode ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'}`}>
      <div className="max-w-3xl mx-auto px-4 py-8">
        
        {/* Header & Theme Toggle */}
        <header className="flex justify-between items-center mb-8 pb-4 border-b border-gray-200 dark:border-gray-700">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Smart Task Manager</h1>
            <p className="text-sm opacity-70">Organize your workflow efficiently</p>
          </div>
          <button
            onClick={() => setIsDarkMode(!isDarkMode)}
            className="px-4 py-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:opacity-90 font-medium transition"
          >
            {isDarkMode ? '☀️ Light Mode' : '🌙 Dark Mode'}
          </button>
        </header>

        {/* Dashboard Stats */}
        <div className="grid grid-cols-3 gap-4 mb-6 text-center">
          <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
            <span className="block text-xl font-bold">{stats.total}</span>
            <span className="text-xs uppercase opacity-70">Total</span>
          </div>
          <div className="p-3 bg-green-100 dark:bg-green-900/30 rounded-lg">
            <span className="block text-xl font-bold text-green-600 dark:text-green-400">{stats.completed}</span>
            <span className="text-xs uppercase opacity-70">Completed</span>
          </div>
          <div className="p-3 bg-yellow-100 dark:bg-yellow-900/30 rounded-lg">
            <span className="block text-xl font-bold text-yellow-600 dark:text-yellow-400">{stats.pending}</span>
            <span className="text-xs uppercase opacity-70">Pending</span>
          </div>
        </div>

        {/* Task Form Component */}
        <section className="mb-6 p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm">
          <TaskForm onAddTask={addTask} />
        </section>

        {/* Filters and Controls */}
        <section className="mb-6">
          <TaskFilters
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
            statusFilter={statusFilter}
            setStatusFilter={setStatusFilter}
          />
        </section>

        {/* Task List Component */}
        <main>
          <TaskList
            tasks={filteredTasks}
            onToggleStatus={toggleTaskStatus}
            onDeleteTask={deleteTask}
          />
        </main>
        
      </div>
    </div>
  );
}