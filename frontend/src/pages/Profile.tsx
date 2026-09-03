import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';

export default function Profile() {
  const { token, user } = useAuth();
  const [profileData, setProfileData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch('http://localhost:8000/users/me/profile', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => {
        if (!res.ok) throw new Error("Failed to load profile");
        return res.json();
      })
      .then(data => {
        setProfileData(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [token]);

  if (loading) return <div className="p-8 text-gray-400">Loading profile...</div>;
  if (error) return <div className="p-8 text-red-400">Error: {error}</div>;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-100 mb-8">Coder Profile</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {/* User Stats Card */}
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 col-span-1 shadow-lg">
          <div className="flex items-center space-x-4 mb-6">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-purple-500 to-indigo-500 flex items-center justify-center text-2xl font-bold text-white shadow-inner">
              {profileData.username.charAt(0).toUpperCase()}
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">{profileData.username}</h2>
              <p className="text-sm text-purple-400 uppercase font-bold tracking-wider">{profileData.role}</p>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-900 rounded p-4 border border-gray-800 text-center">
              <p className="text-gray-400 text-xs uppercase mb-1">Attempted</p>
              <p className="text-2xl font-bold text-white">{profileData.stats.attempted}</p>
            </div>
            <div className="bg-gray-900 rounded p-4 border border-gray-800 text-center">
              <p className="text-gray-400 text-xs uppercase mb-1">Solved</p>
              <p className="text-2xl font-bold text-green-400">{profileData.stats.solved}</p>
            </div>
          </div>
        </div>

        {/* Topic Radar Chart */}
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 col-span-2 shadow-lg flex flex-col items-center">
          <h3 className="text-lg font-bold text-gray-200 mb-4 self-start">Skill Analytics</h3>
          {profileData.radarData && profileData.radarData.length > 0 ? (
            <div className="w-full h-64">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={profileData.radarData}>
                  <PolarGrid stroke="#374151" />
                  <PolarAngleAxis dataKey="topic" tick={{ fill: '#9CA3AF', fontSize: 12 }} />
                  <PolarRadiusAxis angle={30} domain={[0, 'dataMax + 2']} tick={false} axisLine={false} />
                  <Radar name="Solved" dataKey="solved" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.5} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="flex items-center justify-center h-full text-gray-500 italic">
              Solve some problems to generate your skill radar!
            </div>
          )}
        </div>
      </div>

      {/* Submission History */}
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 shadow-lg">
        <h3 className="text-lg font-bold text-gray-200 mb-4">Recent Submissions</h3>
        
        {profileData.recentSubmissions && profileData.recentSubmissions.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-gray-900 text-gray-400">
                <tr>
                  <th className="px-4 py-3 rounded-tl">Time</th>
                  <th className="px-4 py-3">Problem</th>
                  <th className="px-4 py-3">Status</th>
                  <th className="px-4 py-3">Runtime</th>
                  <th className="px-4 py-3 rounded-tr">Language</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {profileData.recentSubmissions.map((sub: any) => (
                  <tr key={sub.id} className="hover:bg-gray-700/50 transition-colors">
                    <td className="px-4 py-3 text-gray-400">{new Date(sub.created_at).toLocaleString()}</td>
                    <td className="px-4 py-3 font-medium text-purple-300">{sub.problem_title}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded text-xs font-bold ${
                        sub.verdict === 'Accepted' ? 'bg-green-900/40 text-green-400 border border-green-800' :
                        sub.verdict === 'Wrong Answer' ? 'bg-red-900/40 text-red-400 border border-red-800' :
                        'bg-yellow-900/40 text-yellow-400 border border-yellow-800'
                      }`}>
                        {sub.verdict}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-gray-300">{sub.execution_time_ms ? `${sub.execution_time_ms} ms` : '-'}</td>
                    <td className="px-4 py-3 text-gray-400 capitalize">{sub.language}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-gray-500 italic p-4 text-center border border-dashed border-gray-700 rounded">
            No submissions yet. Go solve some problems!
          </div>
        )}
      </div>
    </div>
  );
}
