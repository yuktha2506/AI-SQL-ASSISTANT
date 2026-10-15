import { Copy, Download } from 'lucide-react';

const SQL_KEYWORDS = new Set([
  'SELECT',
  'FROM',
  'WHERE',
  'JOIN',
  'INNER',
  'LEFT',
  'RIGHT',
  'ON',
  'GROUP',
  'BY',
  'ORDER',
  'LIMIT',
  'DESC',
  'ASC',
  'COUNT',
  'AVG',
  'SUM',
  'MIN',
  'MAX',
  'AS',
  'WITH',
  'AND',
  'OR'
]);

function highlightSql(sql) {
  return sql.split(/(\s+|,|\(|\)|;)/).map((token, index) => {
    const upperToken = token.toUpperCase();
    const className = SQL_KEYWORDS.has(upperToken)
      ? 'text-cyan-300'
      : /^\d+(\.\d+)?$/.test(token)
        ? 'text-amber-300'
        : token.startsWith("'") || token.startsWith('"')
          ? 'text-emerald-300'
          : 'text-slate-100';

    return (
      <span key={`${token}-${index}`} className={className}>
        {token}
      </span>
    );
  });
}

export default function SQLViewer({ sql, onCopy, onDownload }) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3 dark:border-slate-800">
        <h2 className="text-sm font-semibold text-slate-700 dark:text-slate-200">Generated SQL</h2>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={onCopy}
            disabled={!sql}
            title="Copy SQL"
            className="rounded-md border border-slate-200 p-2 text-slate-600 transition hover:border-emerald-500 hover:text-emerald-700 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700 dark:text-slate-300"
          >
            <Copy size={16} />
          </button>
          <button
            type="button"
            onClick={onDownload}
            disabled={!sql}
            title="Download SQL"
            className="rounded-md border border-slate-200 p-2 text-slate-600 transition hover:border-emerald-500 hover:text-emerald-700 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700 dark:text-slate-300"
          >
            <Download size={16} />
          </button>
        </div>
      </div>
      <div className="min-h-52 overflow-hidden rounded-b-lg bg-slate-950">
        {sql ? (
          <pre className="min-h-52 overflow-auto p-4 font-mono text-sm leading-6">
            <code>{highlightSql(sql)}</code>
          </pre>
        ) : (
          <div className="flex min-h-52 items-center justify-center px-6 text-center text-sm text-slate-400">
            Generated SQLite query will appear here.
          </div>
        )}
      </div>
    </section>
  );}
