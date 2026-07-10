import React from 'react';

export default function TaskList({ tasks, onToggleStatus, onDeleteTask }) {
  
  // Helper to color-code priorities cleanly
  const getPriorityBadge = (priority) => {
    switch (priority) {
      case 'High':
        return 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300';
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300';
      case 'Low':
        return 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-xl opacity-60">
        <p className="text-lg font-medium">No tasks found</p>
        <p className="text-sm">Try adding a new task or resetting your filters.</p>
      </div>
    );
  }

  return (
    <ul className="space-y-3">
      {tasks.map((task) => (
        <li
          key={task.id}
          className={`flex items-center justify-between p-4 rounded-xl border transition-all duration-200 bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 shadow-sm ${
            task.completed ? 'opacity-60 bg-gray-50/50 dark:bg-gray-800/50' : ''
          }`}
        >
          <div className="flex items-center gap-4 flex-1 min-w-0">
            {/* Completion Checkbox */}
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => onToggleStatus(task.id)}
              className="w-5 h-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
            />
            
            {/* Title & Badge Layout */}
            <div className="flex flex-col sm:flex-row sm:items-center gap-2 flex-1 min-w-0">
              <span
                className={`text-base font-medium truncate ${
                  task.completed ? 'line-through text-gray-400 dark:text-gray-500' : ''
                }`}
              >
                {task.title}
              </span>
              <span className={`text-xs px-2.5 py-0.5 rounded-full font-semibold w-fit ${getPriorityBadge(task.priority)}`}>
                {task.priority}
              </span>
            </div>
          </div>

          {/* Action Button Section */}
          <div className="flex items-center gap-3 ml-4">
            <span className={`text-xs hidden sm:inline-block font-medium ${task.completed ? 'text-green-500' : 'text-amber-500'}`}>
              {task.completed ? 'Completed' : 'Pending'}
            </span>
            <button
              onClick={() => onDeleteTask(task.id)}
              className="p-1.5 rounded-lg text-gray-400 hover:text-red-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
              title="Delete task"
            >
              🗑️
            </button>
          </div>
        </li>
      ))}
    </ul>
  );
}