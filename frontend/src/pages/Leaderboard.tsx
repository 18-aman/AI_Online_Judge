import { useEffect, useState } from "react";

interface LeaderboardEntry {
  rank: number;
  username: string;
  score: number;
  solved: number;
}

export default function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/leaderboard/")
      .then((res) => res.json())
      .then((data) => {
        setLeaderboard(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="max-w-4xl mx-auto p-6 w-full">
      <h1 className="text-3xl font-bold mb-2">Global Leaderboard</h1>
      <p className="text-gray-400 mb-8">Rankings based on uniquely solved problems (+100 points each).</p>
      
      {loading ? (
        <div className="text-gray-400">Loading rankings...</div>
      ) : (
        <div className="bg-gray-800 rounded-lg shadow-lg border border-gray-700 overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-gray-700 border-b border-gray-600">
              <tr>
                <th className="px-6 py-4 font-semibold text-gray-300 w-24">Rank</th>
                <th className="px-6 py-4 font-semibold text-gray-300">Hacker</th>
                <th className="px-6 py-4 font-semibold text-gray-300 text-right">Problems Solved</th>
                <th className="px-6 py-4 font-semibold text-gray-300 text-right">Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {leaderboard.length === 0 ? (
                <tr>
                  <td colSpan={4} className="px-6 py-8 text-center text-gray-500">
                    No hackers on the board yet! Solve a problem to claim #1.
                  </td>
                </tr>
              ) : (
                leaderboard.map((entry) => (
                  <tr key={entry.username} className="hover:bg-gray-750 transition-colors">
                    <td className="px-6 py-4">
                      <span className={`font-bold ${entry.rank === 1 ? 'text-yellow-400' : entry.rank === 2 ? 'text-gray-300' : entry.rank === 3 ? 'text-orange-400' : 'text-gray-500'}`}>
                        #{entry.rank}
                      </span>
                    </td>
                    <td className="px-6 py-4 font-medium text-blue-400">
                      {entry.username}
                    </td>
                    <td className="px-6 py-4 text-right text-gray-300">
                      {entry.solved}
                    </td>
                    <td className="px-6 py-4 text-right font-bold text-green-400">
                      {entry.score}
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
