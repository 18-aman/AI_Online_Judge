import json

code = r'''import React, { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { useAuth } from '../contexts/AuthContext';

interface Problem {
  id: string;
  title: string;
  difficulty: string;
}

export default function Admin() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [selectedProblem, setSelectedProblem] = useState<string>("");
  const [language, setLanguage] = useState("python");
  const [referenceCode, setReferenceCode] = useState("");
  const [inputs, setInputs] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  // Custom checker states
  const [hasCustomChecker, setHasCustomChecker] = useState(false);
  const [checkerCode, setCheckerCode] = useState("def check(input_data: str, user_output: str) -> bool:\n    # Write your logic here\n    # Return True if the user\'s output is correct\n    return False\n");
  const [isSavingChecker, setIsSavingChecker] = useState(false);
  
  const [activeTab, setActiveTab] = useState<'create' | 'testcases'>('create');
  const [newTitle, setNewTitle] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const [newDifficulty, setNewDifficulty] = useState("EASY");
  const [newTopics, setNewTopics] = useState("");
  const [newTimeLimit, setNewTimeLimit] = useState(1.0);
  const [newMemoryLimit, setNewMemoryLimit] = useState(256);
  const [isCreating, setIsCreating] = useState(false);
  
  const { token } = useAuth();

  const fetchProblems = async () => {
    try {
      const res = await fetch('http://localhost:8000/problems/', { headers: { 'Authorization': Bearer  } });
      const data = await res.json();
      setProblems(data);
      if(data.length > 0 && !selectedProblem) {
        handleProblemChange(data[0].id, data);
      }
    } catch(err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchProblems();
  }, [token]);

  const handleCreateProblem = async () => {
    setIsCreating(true);
    try {
        const response = await fetch(http://localhost:8000/admin/problems/, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': Bearer 
            },
            body: JSON.stringify({
                title: newTitle,
                description: newDescription,
                difficulty: newDifficulty,
                topics: newTopics,
                time_limit: newTimeLimit,
                memory_limit: newMemoryLimit
            })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Failed to create problem");
        alert("Problem created successfully! Now you can generate its testcases.");
        
        // Refresh problems
        const pRes = await fetch('http://localhost:8000/problems/', { headers: { 'Authorization': Bearer  } });
        const pData = await pRes.json();
        setProblems(pData);
        
        // Reset form & go to testcases
        setNewTitle(""); setNewDescription(""); setNewTopics("");
        setActiveTab('testcases');
        handleProblemChange(data.id, pData);
    } catch(err: any) {
        alert(err.message);
    } finally {
        setIsCreating(false);
    }
  };

  const handleProblemChange = (id: string, problemList = problems) => {
    setSelectedProblem(id);
    const p = problemList.find((x: any) => x.id === id);
    if (p) {
      setHasCustomChecker((p as any).has_custom_checker || false);
      if ((p as any).checker_code) {
        setCheckerCode((p as any).checker_code);
      } else {
        setCheckerCode("def check(input_data: str, user_output: str) -> bool:\n    # Write your logic here\n    # Return True if the user\'s output is correct\n    return False\n");
      }
    }
  };

  const handleGenerate = async () => {
    if (!selectedProblem) return;
    setIsGenerating(true);
    setResult(null);
    const sanitizedInputs = inputs.replace(/\r/g, '');
    const inputList = sanitizedInputs.split('\n\n').filter(i => i.trim() !== '');

    try {
      const response = await fetch(http://localhost:8000/admin/problems//generate-testcases, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': Bearer 
        },
        body: JSON.stringify({
          reference_code: referenceCode,
          language,
          inputs: inputList
        })
      });
      
      const data = await response.json();
      if (!response.ok) {
        setResult({ type: 'error', message: data.detail || 'Failed to generate test cases.' });
      } else {
        setResult({ type: 'success', message: data.message, cases: data.cases });
      }
    } catch (err: any) {
      setResult({ type: 'error', message: err.message });
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSaveChecker = async () => {
    if (!selectedProblem) return;
    setIsSavingChecker(true);
    try {
      const response = await fetch(http://localhost:8000/admin/problems//checker, {
        method: 'PUT',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': Bearer 
        },
        body: JSON.stringify({
          has_custom_checker: hasCustomChecker,
          checker_code: checkerCode
        })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Failed to save checker');
      alert('Custom checker settings saved successfully!');
    } catch (err: any) {
      alert(Error saving checker: );
    } finally {
      setIsSavingChecker(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-64px)] overflow-hidden bg-[#1e1e1e] text-gray-200">
      <div className="bg-gray-800 border-b border-gray-700 flex px-6 py-3 space-x-4">
        <button 
          onClick={() => setActiveTab('create')}
          className={px-4 py-2 rounded font-bold transition-colors }
        >
          Create New Problem
        </button>
        <button 
          onClick={() => setActiveTab('testcases')}
          className={px-4 py-2 rounded font-bold transition-colors }
        >
          Test Case & Checker Engine
        </button>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {activeTab === 'create' ? (
          <div className="w-full max-w-3xl mx-auto p-8 overflow-y-auto">
            <h2 className="text-2xl font-bold mb-6 text-purple-400">Create New Problem</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold mb-1">Title</label>
                <input value={newTitle} onChange={e => setNewTitle(e.target.value)} className="w-full bg-gray-800 border border-gray-700 rounded p-2 focus:outline-none focus:border-purple-500" placeholder="e.g. Reverse Linked List" />
              </div>
              <div className="flex space-x-4">
                <div className="w-1/3">
                  <label className="block text-sm font-semibold mb-1">Difficulty</label>
                  <select value={newDifficulty} onChange={e => setNewDifficulty(e.target.value)} className="w-full bg-gray-800 border border-gray-700 rounded p-2 focus:outline-none focus:border-purple-500">
                    <option value="EASY">EASY</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="HARD">HARD</option>
                  </select>
                </div>
                <div className="w-1/3">
                  <label className="block text-sm font-semibold mb-1">Time Limit (s)</label>
                  <input type="number" step="0.1" value={newTimeLimit} onChange={e => setNewTimeLimit(parseFloat(e.target.value))} className="w-full bg-gray-800 border border-gray-700 rounded p-2 focus:outline-none focus:border-purple-500" />
                </div>
                <div className="w-1/3">
                  <label className="block text-sm font-semibold mb-1">Memory Limit (MB)</label>
                  <input type="number" value={newMemoryLimit} onChange={e => setNewMemoryLimit(parseInt(e.target.value))} className="w-full bg-gray-800 border border-gray-700 rounded p-2 focus:outline-none focus:border-purple-500" />
                </div>
              </div>
              <div>
                <label className="block text-sm font-semibold mb-1">Topics (comma separated)</label>
                <input value={newTopics} onChange={e => setNewTopics(e.target.value)} className="w-full bg-gray-800 border border-gray-700 rounded p-2 focus:outline-none focus:border-purple-500" placeholder="e.g. Array, Two Pointers, Math" />
              </div>
              <div>
                <label className="block text-sm font-semibold mb-1">Description (Markdown Supported)</label>
                <textarea value={newDescription} onChange={e => setNewDescription(e.target.value)} className="w-full h-64 bg-gray-800 border border-gray-700 rounded p-3 font-mono text-sm focus:outline-none focus:border-purple-500" placeholder="Write problem description here..."></textarea>
              </div>
              <button 
                onClick={handleCreateProblem}
                disabled={isCreating || !newTitle.trim() || !newDescription.trim()}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 rounded disabled:opacity-50 transition-colors"
              >
                {isCreating ? 'Creating...' : 'Create Problem'}
              </button>
            </div>
          </div>
        ) : (
          <>
            <div className="w-1/2 p-6 overflow-y-auto border-r border-gray-800">
              <h2 className="text-2xl font-bold mb-6 text-purple-400">Reference Solution Engine</h2>
              <p className="text-gray-400 mb-6 text-sm">
                Write a perfect reference solution. The system will automatically calculate the expected outputs for your test cases and save them as hidden test cases.
              </p>

              <div className="mb-4">
                <label className="block text-sm font-semibold mb-2">Target Problem</label>
                <select 
                  className="w-full bg-gray-800 border border-gray-700 rounded p-2 focus:outline-none focus:border-purple-500"
                  value={selectedProblem}
                  onChange={e => handleProblemChange(e.target.value)}
                >
                  {problems.map(p => (
                    <option key={p.id} value={p.id}>{p.title} ({p.difficulty})</option>
                  ))}
                </select>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-semibold mb-2">Raw Input Data (Separate cases by double blank line)</label>
                <textarea 
                  className="w-full h-48 bg-gray-800 border border-gray-700 rounded p-3 font-mono text-sm focus:outline-none focus:border-purple-500"
                  placeholder={"[2,7,11,15]\n9\n\n[3,2,4]\n6"}
                  value={inputs}
                  onChange={e => setInputs(e.target.value)}
                ></textarea>
              </div>
              
              <button 
                onClick={handleGenerate}
                disabled={isGenerating || !selectedProblem || !referenceCode.trim() || !inputs.trim()}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 rounded disabled:opacity-50 transition-colors"
              >
                {isGenerating ? 'Evaluating & Saving...' : 
                 !selectedProblem ? 'Error: No Problem Selected (Refresh Page)' :
                 !inputs.trim() ? 'Enter Inputs to Generate' :
                 !referenceCode.trim() ? 'Enter Reference Code to Generate' :
                 'Generate Hidden Test Cases'}
              </button>

              {result && (
                <div className={mt-6 p-4 rounded border }>
                  <p className="font-bold">{result.type === 'error' ? 'Error' : 'Success'}</p>
                  <p className="text-sm mt-1">{result.message}</p>
                  
                  {result.cases && (
                    <div className="mt-4 space-y-3">
                      {result.cases.map((c: any, i: number) => (
                        <div key={i} className="bg-gray-900 p-3 rounded border border-gray-700 text-xs font-mono">
                          <div className="text-gray-500 mb-1">Input:</div>
                          <div className="mb-2 whitespace-pre-wrap">{c.input}</div>
                          <div className="text-gray-500 mb-1">Generated Output:</div>
                          <div className="text-purple-400 whitespace-pre-wrap">{c.generated_output}</div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
            
            <div className="w-1/2 flex flex-col">
              <div className={hasCustomChecker ? "h-1/2 flex flex-col border-b border-gray-800" : "flex-1 flex flex-col"}>
                <div className="bg-gray-800 px-4 py-2 flex items-center justify-between border-b border-gray-700">
                  <span className="font-semibold text-gray-300">Reference Solution</span>
                  <select 
                    value={language}
                    onChange={e => setLanguage(e.target.value)}
                    className="bg-gray-700 text-gray-200 border-none rounded px-2 py-1 text-sm focus:outline-none"
                  >
                    <option value="python">Python</option>
                    <option value="cpp">C++</option>
                    <option value="java">Java</option>
                  </select>
                </div>
                <div className="flex-1 relative">
                  <Editor
                    height="100%"
                    language={language}
                    theme="vs-dark"
                    value={referenceCode}
                    onChange={(val) => setReferenceCode(val || "")}
                    options={{ minimap: { enabled: false }, fontSize: 14, padding: { top: 16 } }}
                  />
                </div>
              </div>

              <div className="bg-gray-800 px-4 py-3 flex items-center justify-between border-b border-gray-700">
                <label className="flex items-center cursor-pointer text-sm font-semibold">
                  <input 
                    type="checkbox" 
                    checked={hasCustomChecker}
                    onChange={e => setHasCustomChecker(e.target.checked)}
                    className="mr-2 rounded bg-gray-700 border-gray-600 text-purple-600 focus:ring-purple-500" 
                  />
                  Use Custom Checker (Special Judge)
                </label>
                <button 
                  onClick={handleSaveChecker}
                  disabled={isSavingChecker}
                  className="bg-purple-600 hover:bg-purple-700 text-white px-3 py-1 text-xs font-bold rounded"
                >
                  {isSavingChecker ? "Saving..." : "Save Settings"}
                </button>
              </div>

              {hasCustomChecker && (
                <div className="flex-1 flex flex-col">
                   <div className="bg-[#1e1e1e] px-4 py-2 text-xs text-gray-400 border-b border-gray-800 font-mono">
                     Language: Python | Must define: def check(input_data: str, user_output: str) -> bool:
                   </div>
                   <div className="flex-1 relative">
                     <Editor
                       height="100%"
                       language="python"
                       theme="vs-dark"
                       value={checkerCode}
                       onChange={(val) => setCheckerCode(val || "")}
                       options={{ minimap: { enabled: false }, fontSize: 14, padding: { top: 16 } }}
                     />
                   </div>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
'''
with open('src/pages/Admin.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
