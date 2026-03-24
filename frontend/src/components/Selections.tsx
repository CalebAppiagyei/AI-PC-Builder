import { PART_FILES, PRIMARY_USES } from '../constants';

import AutoComplete from '../context/AutoComplete';


export default function Selections(props: any) {
  const { form, update, onRun, isLoading, query, setQuery, options, onSelect } = props;
    
  return (
      <div className='panel'>
        {PART_FILES.map(({ key, label }) => (
          <button key={key} onClick={() => props.setOpenKey(key)}>
            {label}: {form[key] || "(Any)"}
          </button>
        ))}
        <AutoComplete
            query={query}
            setQuery={setQuery}
            options={options}
            onSelect={onSelect} 
        />
        <select
          value={form.primaryUse}
          onChange={e => update("primaryUse", e.target.value)}
        >
          {PRIMARY_USES.map(use => <option key={use}>{use}</option>)}
        </select>

        <input
          value={form.budget}
          onChange={e => update("budget", e.target.value)}
        />

        <button onClick={onRun} disabled={isLoading}>
          Run
        </button>
      </div>
  )
}