import { BrowserRouter as Router, Routes, Route, Link, Navigate, useLocation } from "react-router-dom";
import ProblemList from "./pages/ProblemList";
import ProblemSolve from "./pages/ProblemSolve";
import Leaderboard from "./pages/Leaderboard";
import Admin from "./pages/Admin";
import Profile from "./pages/Profile";
import Login from "./pages/Login";
import { AuthProvider, useAuth } from "./contexts/AuthContext";

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { token } = useAuth();
  if (!token) return <Navigate to="/login" replace />;
  return <>{children}</>;
};

const ProtectedAdminRoute = ({ children }: { children: React.ReactNode }) => {
  const { token, isAdmin } = useAuth();
  if (!token) return <Navigate to="/login" replace />;
  if (!isAdmin) return <Navigate to="/" replace />;
  return <>{children}</>;
};

const Navbar = () => {
  const { token, isAdmin, logout } = useAuth();
  
  // Hide navbar entirely if user is not logged in!
  if (!token) return null;

  return (
    <nav className="bg-[#1e1e1e] p-4 shadow-md flex justify-between items-center border-b border-gray-800">
      <Link to="/" className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent hover:opacity-80 transition-opacity">
        AI-Powered Online Judge
      </Link>
      <div className="space-x-6 flex items-center">
        <Link to="/" className="text-gray-400 hover:text-white transition-colors">Problems</Link>
        <Link to="/leaderboard" className="text-gray-400 hover:text-white transition-colors">Leaderboard</Link>
        {!isAdmin && (
          <Link to="/profile" className="text-gray-400 hover:text-white transition-colors">Profile</Link>
        )}
        {isAdmin && (
          <Link to="/admin" className="text-purple-400 font-semibold hover:text-purple-300 transition-colors">Admin</Link>
        )}
        <button onClick={logout} className="text-gray-400 hover:text-red-400 transition-colors">Logout</button>
      </div>
    </nav>
  );
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-[#121212] text-white flex flex-col">
          <Navbar />
          <main className="flex-1 flex flex-col">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/" element={<ProtectedRoute><ProblemList /></ProtectedRoute>} />
              <Route path="/problems/:id" element={<ProtectedRoute><ProblemSolve /></ProtectedRoute>} />
              <Route path="/leaderboard" element={<ProtectedRoute><Leaderboard /></ProtectedRoute>} />
              <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
              <Route path="/admin" element={<ProtectedAdminRoute><Admin /></ProtectedAdminRoute>} />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
