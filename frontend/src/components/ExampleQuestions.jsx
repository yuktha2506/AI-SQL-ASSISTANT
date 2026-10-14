const examples = [
  'Show top five departments with highest placement percentage',
  'List students with CGPA greater than 9',
  'Show average marks by course',
  'Find departments with placement percentage above 85',
  'List courses offered by Computer Science department'
];

export default function ExampleQuestions({ onSelect }) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
        Example Questions
      </h2>
      <div className="mt-3 flex flex-wrap gap-2">
        {examples.map((question) => (
          <button
            key={question}
            type="button"
            onClick={() => onSelect(question)}
            className="rounded-md border border-slate-200 px-3 py-2 text-left text-sm text-slate-700 transition hover:border-emerald-500 hover:text-emerald-700 dark:border-slate-700 dark:text-slate-200 dark:hover:border-emerald-400 dark:hover:text-emerald-300"
          >
            {question}
          </button>
        ))}
      </div>
    </section>
  );}
