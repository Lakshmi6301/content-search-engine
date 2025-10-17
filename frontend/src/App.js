import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);

  // fetch suggestions when typing
  useEffect(() => {
    const fetchSuggestions = async () => {
      if (query.length < 2) {
        setSuggestions([]);
        return;
      }
      try {
        const res = await axios.get(`${API_URL}/suggest?q=${query}`);
        setSuggestions(res.data.suggestions || []);
        setShowSuggestions(true);
      } catch (err) {
        console.error("Suggestion error:", err);
      }
    };

    const delay = setTimeout(fetchSuggestions, 300);
    return () => clearTimeout(delay);
  }, [query]);

  // search results
  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setResults([]);
    try {
      const res = await axios.get(`${API_URL}/search?query=${query}`);
      setResults(res.data.results || []);
    } catch (err) {
      console.error("Search error:", err);
    }
    setLoading(false);
    setShowSuggestions(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 flex flex-col items-center py-10">
      <h1 className="text-3xl font-bold mb-8">Content Search Engine</h1>

      <div className="relative w-full max-w-2xl">
        <input
          type="text"
          placeholder="Search..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => setShowSuggestions(true)}
          className="w-full border border-gray-300 rounded-lg p-3 shadow-sm focus:ring-2 focus:ring-blue-400 outline-none"
        />
        <button
          onClick={handleSearch}
          className="absolute right-2 top-2 bg-blue-500 text-white px-4 py-2 rounded-md"
        >
          Search
        </button>

        {/* suggestions dropdown */}
        {showSuggestions && suggestions.length > 0 && (
          <ul className="absolute z-10 bg-white border border-gray-200 rounded-md shadow-md mt-1 w-full max-h-60 overflow-y-auto">
            {suggestions.map((s, i) => (
              <li
                key={i}
                onClick={() => {
                  setQuery(s.title);
                  setShowSuggestions(false);
                  handleSearch();
                }}
                className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
              >
                {s.title}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="mt-10 w-full max-w-3xl">
        {loading && <p>Searching...</p>}
        {!loading && results.length === 0 && <p>No results found.</p>}

        <div className="space-y-5">
          {results.map((r, i) => (
            <div
              key={i}
              className="bg-white rounded-xl p-5 shadow hover:shadow-lg transition"
            >
              <a
                href={r.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xl font-semibold text-blue-600 hover:underline"
              >
                {r.title}
              </a>
              <p className="text-gray-700 mt-2">
                {r.snippet || "No description available."}
              </p>
              <p className="text-sm text-gray-500 mt-1 truncate">{r.link}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
