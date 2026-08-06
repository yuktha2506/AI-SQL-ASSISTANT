import { Download, History } from 'lucide-react';

export default function QueryHistory({ history, onSelect, onExport }) {
  return (
    <aside className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900 lg:min-h-[calc(100vh-8rem)]">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <History size={18} className="text-emerald-600" />
          <h2 className="text-sm font-semibold text-slate-700 dark:text-slate-200">History</h2>
        </div>
        <button
          type="button"
          onClick={onExport}
          disabled={history.length === 0}
          title="Export history as JSON"
          className="rounded-md border border-slate-200 p-2 text-slate-600 transition hover:border-emerald-500 hover:text-emerald-700 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700 dark:text-slate-300"
        >
          <Download size={16} />
        </button>
      </div>
      <div className="mt-4 space-y-3">
        {history.length === 0 ? (
          <p className="text-sm text-slate-500 dark:text-slate-400">No queries generated yet.</p>
        ) : (
          history.map((item) => (
            <button
              key={item.id}
              type="button"
              onClick={() => onSelect(item)}
              className="w-full rounded-md border border-slate-200 p-3 text-left transition hover:border-emerald-500 dark:border-slate-700"
            >
              <p className="line-clamp-2 text-sm font-medium text-slate-800 dark:text-slate-100">{item.question}</p>
              <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">{item.createdAt}</p>
            </button>
          ))
        )}
      </div>
    </aside>
  );
}
