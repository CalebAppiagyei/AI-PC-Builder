import { PART_FILES, PRIMARY_USES } from '../constants';
import type { FormState, PartCatalog, PartKey } from '../types';
import AutoComplete from './AutoComplete';
import Compatibility from './Compatibility';

type Option = {
  label: string;
  value: string;
};

type SelectionsProps = {
  query: string;
  form: FormState;
  compatIssues: string;
  options: Option[];
  isLoading: boolean;
  catalog: PartCatalog;
  openKey: PartKey | null;
  inputRef: React.RefObject<HTMLInputElement | null>;
  buttonLabel: string;
  isSuggestOpen: boolean;
  setOpenKey: React.Dispatch<React.SetStateAction<PartKey | null>>;
  setQuery: React.Dispatch<React.SetStateAction<string>>;
  setIsSuggestOpen: React.Dispatch<React.SetStateAction<boolean>>;
  update: <K extends keyof FormState>(key: K, value: FormState[K]) => void;
  selectOption: (value: string, label?: string) => void;
  clearSelection: () => void;
  onRun: () => void;
};

export default function Selections({ query, form, compatIssues, options, isLoading, catalog, openKey, inputRef, buttonLabel, isSuggestOpen,
   setOpenKey, setQuery, setIsSuggestOpen, update, selectOption, clearSelection, onRun }: SelectionsProps) {
    
  function toggleOpen(key: PartKey) {
    setOpenKey((prev) => {
      const next = prev === key ? null : key;
      return next;
    });
  }

  return (
    <section className='grid'>
      {/* Left column */}
      <div className='panel'>
        <h2 className="panel__title">Selections</h2>
        {/* Component buttons */}
        <div className="componentButtons">
          {PART_FILES.map(({ key, label }) => {
            const selectedName = form[key];
            // For GPU, show "Name — Chipset" on the button (but keep the stored value as the name)
            let displayValue = selectedName;
            if (key === "gpu" && selectedName) {
              const gpuItems = catalog["video-card.json"] ?? [];
              const match = gpuItems.find((it) => it.name === selectedName);
              const chipset = match && typeof match.chipset === "string" ? match.chipset : "";
              if (chipset) displayValue = `${selectedName} — ${chipset}`;
            }
            return (
              <button
                key={key}
                type="button"
                className={openKey === key ? "compBtn compBtn--active" : "compBtn"}
                onClick={() => toggleOpen(key)}
                title={selectedName ? `Selected: ${displayValue}` : "No selection"}
              >
                <span className="compBtn__label">{label}</span>
                <span className="compBtn__value">{displayValue || "(Any)"}</span>
              </button>
            );
          })}
        </div>
        <AutoComplete
          openKey={openKey}
          form={form}
          query={query}
          inputRef={inputRef}
          filteredOptions={options}
          isSuggestOpen={isSuggestOpen}
          setQuery={setQuery}
          setOpenKey={setOpenKey}
          setIsSuggestOpen={setIsSuggestOpen}
          selectOption={selectOption} 
          clearSelection={clearSelection}
        />
        {/* Primary use + Budget */}
        <div className="inlineRow">
          <div className="field">
            <label className="field__label" htmlFor="primaryUse">
              Primary Use
            </label>
            <select
              id="primaryUse"
              className="field__control"
              value={form.primaryUse}
              onChange={(e) => update("primaryUse", e.target.value)}
            >
              {PRIMARY_USES.map((u) => (
                <option key={u} value={u}>
                  {u}
                </option>
              ))}
            </select>
          </div>

          <div className="field">
            <label className="field__label" htmlFor="budget">
              Budget
            </label>
            <input
              id="budget"
              className="field__control"
              placeholder="e.g. 1500"
              value={form.budget}
              onChange={(e) => update("budget", e.target.value)}
            />
          </div>
        </div>

        <div className="actions">
          <button className="primaryBtn" onClick={onRun} disabled={isLoading} type="button">
            {isLoading ? "Working…" : buttonLabel}
          </button>
        </div>
      </div>
      <Compatibility compatIssues={compatIssues} />
    </section>
      
  )
}