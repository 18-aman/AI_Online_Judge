import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

interface Problem {
  id: string;
  title: string;
  difficulty: "EASY" | "MEDIUM" | "HARD";
  user_status?: "SOLVED" | "ATTEMPTED" | "TODO";
  topics?: { id: string, name: string }[];
}

export default function ProblemList() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [activeTopic, setActiveTopic] = useState<string>("All");
  const [loading, setLoading] = useState(true);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const { token } = useAuth();

  useEffect(() => {
    fetch("http://localhost:8000/recommendations/", {
      headers: { "Authorization": `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => setRecommendations(data || []))
      .catch(console.error);
      
    fetch("http://localhost:8000/problems/", {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then((res) => res.json())
      .then((data) => {
        setProblems(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [token]);

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "EASY": return "text-green-400";
      case "MEDIUM": return "text-yellow-400";
      case "HARD": return "text-red-400";
      default: return "text-gray-400";
    }
  };

  const renderStatus = (status?: string) => {
    if (status === "SOLVED") {
      return <span className="text-green-500 font-bold text-xl" title="Solved">✅</span>;
    }
    if (status === "ATTEMPTED") {
      return <span className="text-yellow-500 font-bold text-xl" title="Attempted">🔄</span>;
    }
    return <span className="text-gray-500">-</span>;
  };

  const allTopics = Array.from(new Set(problems.flatMap(p => p.topics?.map(t => t.name) || []))).sort();

  const filteredProblems = problems.filter((prob) => {
    const matchesSearch = prob.title.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesTopic = activeTopic === "All" || (prob.topics?.some(t => t.name === activeTopic));
    return matchesSearch && matchesTopic;
  });

  return (
    <div className="max-w-6xl mx-auto p-6 w-full flex-1 flex flex-col">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Problems</h1>
        <div className="relative w-72">
          <input
            type="text"
            placeholder="Search problems..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-gray-800 border border-gray-700 text-gray-200 rounded-full py-2 px-4 pl-10 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
          />
          <svg className="w-4 h-4 text-gray-400 absolute left-4 top-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
        </div>
      </div>
      
      {recommendations.length > 0 && (
        <div className="mb-8 p-6 bg-gradient-to-r from-purple-900 to-indigo-900 rounded-lg shadow-lg border border-purple-500/30">
          <h2 className="text-xl font-bold mb-4 flex items-center"><span className="mr-2">✨</span> AI Recommended For You</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {recommendations.map(rec => (
              <Link to={`/problems/${rec.id}`} key={rec.id} className="block p-4 bg-gray-900/50 hover:bg-gray-800 rounded border border-gray-700 hover:border-purple-500 transition-all">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-bold text-blue-400">{rec.title}</h3>
                  <span className={`text-xs font-bold px-2 py-1 rounded bg-gray-800 ${rec.difficulty === "EASY" ? "text-green-400" : rec.difficulty === "MEDIUM" ? "text-yellow-400" : "text-red-400"}`}>{rec.difficulty}</span>
                </div>
                <div className="text-xs text-gray-400">
                  Growth Match: <span className="font-mono text-purple-400">{rec.match_score}%</span>
                  <br />
                  <span className="text-[10px] text-gray-500">Est. Success: {rec.win_probability}%</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Topics Filter */}
      {!loading && allTopics.length > 0 && (
        <div className="mb-6 flex flex-wrap gap-2">
          <button
            onClick={() => setActiveTopic("All")}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${activeTopic === "All" ? "bg-purple-600 text-white" : "bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-gray-200"}`}
          >
            All Topics
          </button>
          {allTopics.map(topic => (
            <button
              key={topic}
              onClick={() => setActiveTopic(topic)}
              className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${activeTopic === topic ? "bg-purple-600 text-white" : "bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-gray-200"}`}
            >
              {topic}
            </button>
          ))}
        </div>
      )}

      {loading ? (
        <div className="text-gray-400 text-center py-12">Loading problems...</div>
      ) : (
        <div className="bg-gray-800 rounded-lg shadow-lg border border-gray-700 overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-gray-700 border-b border-gray-600">
              <tr>
                <th className="px-6 py-4 font-semibold text-gray-300">Status</th>
                <th className="px-6 py-4 font-semibold text-gray-300">Title</th>
                <th className="px-6 py-4 font-semibold text-gray-300">Difficulty</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {filteredProblems.length === 0 ? (
                <tr>
                  <td colSpan={3} className="px-6 py-8 text-center text-gray-500">
                    {searchQuery ? "No problems found matching your search." : "No problems found."}
                  </td>
                </tr>
              ) : (
                filteredProblems.map((prob) => (
                  <tr key={prob.id} className="hover:bg-gray-750 transition-colors">
                    <td className="px-6 py-4">
                      {renderStatus(prob.user_status)}
                    </td>
                    <td className="px-6 py-4">
                      <Link 
                        to={`/problems/${prob.id}`}
                        className="text-blue-400 hover:text-blue-300 font-medium block mb-1"
                      >
                        {prob.title}
                      </Link>
                      <div className="flex flex-wrap gap-1">
                        {prob.topics?.map(t => (
                          <span key={t.id} className="text-[10px] bg-gray-700 text-gray-300 px-1.5 py-0.5 rounded">
                            {t.name}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className={`px-6 py-4 font-medium ${getDifficultyColor(prob.difficulty)}`}>
                      {prob.difficulty}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}





