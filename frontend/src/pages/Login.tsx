import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function Login() {
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      if (isRegistering) {
        // Register User
        const res = await fetch('http://localhost:8000/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, username, password })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Registration failed');
        
        setSuccess('Registration successful! You can now log in.');
        setIsRegistering(false);
        setPassword('');
      } else {
        // Login User
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const res = await fetch('http://localhost:8000/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: formData.toString()
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Login failed');
        
        login(data.access_token, data.role);
        navigate(data.role === 'ADMIN' ? '/admin' : '/');
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="flex h-[calc(100vh-64px)] items-center justify-center bg-[#1e1e1e] text-white">
      <div className="bg-gray-800 p-8 rounded-lg shadow-xl w-96 border border-gray-700">
        <h2 className="text-2xl font-bold mb-6 text-center text-purple-500">
          {isRegistering ? 'Create Account' : 'Sign In'}
        </h2>
        {error && <div className="bg-red-500/20 text-red-500 p-3 rounded mb-4 text-sm">{error}</div>}
        {success && <div className="bg-green-500/20 text-green-500 p-3 rounded mb-4 text-sm">{success}</div>}
        
        <form onSubmit={handleAuth} className="space-y-4">
          {isRegistering && (
            <div>
              <label className="block text-sm text-gray-400 mb-1">Username</label>
              <input 
                type="text" 
                value={username}
                onChange={e => setUsername(e.target.value)}
                className="w-full bg-gray-700 rounded p-2 focus:ring-2 focus:ring-purple-500 focus:outline-none"
                placeholder="coding_ninja"
                required={isRegistering} 
              />
            </div>
          )}
          <div>
            <label className="block text-sm text-gray-400 mb-1">Email</label>
            <input 
              type="email" 
              value={email}
              onChange={e => setEmail(e.target.value)}
              className="w-full bg-gray-700 rounded p-2 focus:ring-2 focus:ring-purple-500 focus:outline-none"
              placeholder="user@example.com"
              required 
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Password</label>
            <input 
              type="password" 
              value={password}
              onChange={e => setPassword(e.target.value)}
              className="w-full bg-gray-700 rounded p-2 focus:ring-2 focus:ring-purple-500 focus:outline-none"
              placeholder="••••••••"
              required 
            />
          </div>
          <button type="submit" className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded transition-colors mt-6">
            {isRegistering ? 'Sign Up' : 'Login'}
          </button>
        </form>

        <div className="mt-4 text-center">
          <button 
            onClick={() => { setIsRegistering(!isRegistering); setError(''); setSuccess(''); }}
            className="text-sm text-purple-400 hover:text-purple-300"
          >
            {isRegistering ? 'Already have an account? Sign in' : 'Need an account? Sign up'}
          </button>
        </div>

        {!isRegistering && (
          <div className="mt-6 border-t border-gray-700 pt-6">
            <p className="text-center text-sm text-gray-400 mb-4">Quick Demo Access</p>
            <div className="flex gap-3">
              <button 
                onClick={() => { setEmail('admin@example.com'); setPassword('admin123'); }}
                className="flex-1 bg-gray-700 hover:bg-gray-600 text-sm text-white py-2 rounded transition-colors"
              >
                Fill Admin
              </button>
              <button 
                onClick={() => { setEmail('user@example.com'); setPassword('user123'); }}
                className="flex-1 bg-gray-700 hover:bg-gray-600 text-sm text-white py-2 rounded transition-colors"
              >
                Fill User
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
