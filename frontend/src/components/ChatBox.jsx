import { Loader2, Sparkles } from 'lucide-react';

export default function ChatBox({ question, setQuestion, onGenerate, loading }) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <label htmlFor="question" className="text-sm font-semibold text-slate-700 dark:text-slate-200">
        Ask a question
      </label>
      <textarea
        id="question"
        value={question}
        onChange={(event) => setQuestion(event.target.value)}
        placeholder="Example: Show top five departments with highest placement percentage"
        className="mt-3 min-h-32 w-full resize-y rounded-md border border-slate-200 bg-slate-50 p-3 text-sm text-slate-900 outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100 dark:focus:ring-emerald-950"
      />
      <div className="mt-4 flex justify-end">
        <button
          type="button"
          onClick={onGenerate}
          disabled={loading}
          className="inline-flex items-center gap-2 rounded-md bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-70"
        >
          {loading ? <Loader2 size={18} className="animate-spin" /> : <Sparkles size={18} />}
          Generate SQL
        </button>
      </div>
    </section>
  );
}
