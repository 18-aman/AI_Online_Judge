import re

# App.tsx
with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

if "import Profile" not in content:
    content = content.replace("import Admin from './pages/Admin';", "import Admin from './pages/Admin';\nimport Profile from './pages/Profile';")
    content = content.replace("<Route path=\"/admin\"", "<Route path=\"/profile\" element={<ProtectedRoute><Profile /></ProtectedRoute>} />\n          <Route path=\"/admin\"")
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)

# Navbar.tsx
with open('src/components/Navbar.tsx', 'r', encoding='utf-8') as f:
    nav = f.read()

if "to=\"/profile\"" not in nav:
    nav = nav.replace('to="/admin" className="hover:text-purple-400 transition-colors">Admin Panel</Link>', 'to="/admin" className="hover:text-purple-400 transition-colors">Admin Panel</Link>\n              <Link to="/profile" className="hover:text-purple-400 transition-colors">Profile</Link>')
    with open('src/components/Navbar.tsx', 'w', encoding='utf-8') as f:
        f.write(nav)
