import { useMemo, useState } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { Moon, Sun } from 'lucide-react';

import ChatBox from '../components/ChatBox.jsx';
import ExampleQuestions from '../components/ExampleQuestions.jsx';
import ExplanationBox from '../components/ExplanationBox.jsx';
import QueryHistory from '../components/QueryHistory.jsx';
import SQLViewer from '../components/SQLViewer.jsx';
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function downloadFile(filename, content, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}

export default function Home() {
  const [darkMode, setDarkMode] = useState(false);
  const [question, setQuestion] = useState('');
  const [sql, setSql] = useState('');
  const [explanation, setExplanation] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const pageClassName = useMemo(() => (darkMode ? 'dark' : ''), [darkMode]);

  async function handleGenerate() {
    if (!question.trim()) {
      toast.error('Please enter a question.');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/generate`, {
        question: question.trim()
      });
      const nextSql = response.data.sql;
      const nextExplanation = response.data.explanation;

      setSql(nextSql);
      setExplanation(nextExplanation);
      setHistory((current) => [
        {
          id: crypto.randomUUID(),
          question: question.trim(),
          sql: nextSql,
          explanation: nextExplanation,
          createdAt: new Date().toLocaleString()
        },
        ...current
      ]);
      toast.success('SQL generated successfully.');
    } catch (error) {
      const message = error.response?.data?.detail || 'Unable to generate SQL.';
      toast.error(message);
    } finally {
      setLoading(false);
    }
  }

  async function handleCopy() {
    if (!sql) return;
    await navigator.clipboard.writeText(sql);
    toast.success('SQL copied.');
  }

  function handleDownloadSql() {
    if (!sql) return;
    downloadFile('generated-query.sql', sql, 'text/sql');
    toast.success('SQL downloaded.');
  }

  function handleExportHistory() {
    downloadFile('query-history.json', JSON.stringify(history, null, 2), 'application/json');
    toast.success('History exported.');
  }

  function handleHistorySelect(item) {
    setQuestion(item.question);
    setSql(item.sql);
    setExplanation(item.explanation);
  }

  return (
    <div className={pageClassName}>
      <main className="min-h-screen bg-slate-50 text-slate-950 transition dark:bg-slate-950 dark:text-slate-50">
        <header className="border-b border-slate-200 bg-white/90 backdrop-blur dark:border-slate-800 dark:bg-slate-950/90">
          <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
            <div>
              <h1 className="text-xl font-bold tracking-tight">AI SQL Assistant</h1>
              <p className="text-sm text-slate-500 dark:text-slate-400">Natural language to safe SQLite queries</p>
            </div>
            <button
              type="button"
              onClick={() => setDarkMode((current) => !current)}
              title="Toggle dark mode"
              className="rounded-md border border-slate-200 p-2 text-slate-700 transition hover:border-emerald-500 hover:text-emerald-700 dark:border-slate-700 dark:text-slate-200"
            >
              {darkMode ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </div>
        </header>

        <div className="mx-auto grid max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[320px_1fr] lg:px-8">
          <QueryHistory history={history} onSelect={handleHistorySelect} onExport={handleExportHistory} />
          <div className="space-y-6">
            <ExampleQuestions onSelect={setQuestion} />
            <ChatBox
              question={question}
              setQuestion={setQuestion}
              onGenerate={handleGenerate}
              loading={loading}
            />
            <div className="grid gap-6 xl:grid-cols-[1.25fr_0.75fr]">
              <SQLViewer sql={sql} onCopy={handleCopy} onDownload={handleDownloadSql} />
              <ExplanationBox explanation={explanation} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
