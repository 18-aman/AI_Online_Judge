
const fs = require('fs');
let content = fs.readFileSync('src/pages/ProblemSolve.tsx', 'utf-8');
const buttonHtml = '              </button>\n              <button \n                onClick={handleAskReview}\n                disabled={isAskingReview}\n                className=\'bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white px-3 py-1.5 rounded font-medium text-sm transition-colors shadow-sm\'\n              >\n                {isAskingReview ? \'Reviewing...\' : \'Code Review\'}\n              </button>\n              <button \n                onClick={handleAskComplexity}\n                disabled={isAskingComplexity}\n                className=\'bg-teal-600 hover:bg-teal-700 disabled:opacity-50 text-white px-3 py-1.5 rounded font-medium text-sm transition-colors shadow-sm\'\n              >\n                {isAskingComplexity ? \'Analyzing...\' : \'Big-O\'}\n              </button>';
content = content.replace(/(onClick=\{handleAskMentor\}[\s\S]*?<\/button>)/, \\n\);
fs.writeFileSync('src/pages/ProblemSolve.tsx', content, 'utf-8');

