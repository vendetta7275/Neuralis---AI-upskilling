import React from 'react';

export default function TaskFilters({ searchQuery, setSearchQuery, statusFilter, setStatusFilter }) {
  const options = ['All', 'Pending', 'Completed'];

  return (
    <div className="flex flex-col sm:flex-row gap-4 justify-between items-center bg-white dark:bg-gray-800 p-4 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
      {/* Search Input */}
      <div className="w-full sm:w-72">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="🔍 Search tasks by title..."
          className="w-full px-3 py-2 border rounded-lg bg-transparent border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        />
      </div>

      {/* Filter Tabs */}
      <div className="flex border rounded-lg overflow-hidden border-gray-300 dark:border-gray-600">
        {options.map((option) => (
          <button
            key={option}
            onClick={() => setStatusFilter(option)}
            className={`px-4 py-2 text-sm font-medium transition-colors ${
              statusFilter === option
                ? 'bg-blue-600 text-white'
                : 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-300'
            }`}
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  );
}