export default function ExplanationBox({ explanation }) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <h2 className="text-sm font-semibold text-slate-700 dark:text-slate-200">Explanation</h2>
      <p className="mt-3 text-sm leading-6 text-slate-600 dark:text-slate-300">
        {explanation || 'A plain-English explanation of the generated SQL will appear here.'}
      </p>
    </section>
  );}
