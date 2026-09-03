import re

with open('src/pages/ProblemSolve.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add state variables
state_add = '''  const [isAskingReview, setIsAskingReview] = useState(false);
  const [isAskingExplain, setIsAskingExplain] = useState(false);
  const [isAskingDebug, setIsAskingDebug] = useState(false);'''

content = content.replace('  const [isAskingReview, setIsAskingReview] = useState(false);', state_add)

# Add handler functions
handlers = '''  const handleAskExplain = async () => {
    setIsAskingExplain(true);
    setMentorHint("Generating explanation...");
    try {
      const res = await fetch(http://localhost:8000/problems//explain, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": Bearer  },
        body: JSON.stringify({ language, code }),
      });
      const data = await res.json();
      setMentorHint(data.message);
    } catch (e) {
      setMentorHint("Error contacting AI.");
    }
    setIsAskingExplain(false);
  };

  const handleAskDebug = async () => {
    setIsAskingDebug(true);
    setMentorHint("Debugging code...");
    try {
      const res = await fetch(http://localhost:8000/problems//debug, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": Bearer  },
        body: JSON.stringify({ language, code }),
      });
      const data = await res.json();
      setMentorHint(data.message);
    } catch (e) {
      setMentorHint("Error contacting AI.");
    }
    setIsAskingDebug(false);
  };
'''

content = content.replace('  const handleAskComplexity = async () => {', handlers + '\n  const handleAskComplexity = async () => {')

# Add buttons
buttons = '''                <button 
                  onClick={handleAskExplain}
                  disabled={isAskingExplain}
                  className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-3 py-1.5 rounded font-medium text-sm transition-colors shadow-sm"
                >
                  {isAskingExplain ? "Explaining..." : "Explain Code"}
                </button>
                <button 
                  onClick={handleAskDebug}
                  disabled={isAskingDebug}
                  className="bg-rose-600 hover:bg-rose-700 disabled:opacity-50 text-white px-3 py-1.5 rounded font-medium text-sm transition-colors shadow-sm"
                >
                  {isAskingDebug ? "Debugging..." : "Debug Code"}
                </button>
'''
content = content.replace('              <div className="flex gap-2">', '              <div className="flex gap-2 flex-wrap">\n' + buttons)

with open('src/pages/ProblemSolve.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
