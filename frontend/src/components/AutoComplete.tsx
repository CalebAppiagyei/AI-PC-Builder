import { PART_FILES } from "../constants";
import type { FormState, PartKey } from "../types";

type Option = {
  label: string;
  value: string;
};

type Props = {
  openKey: PartKey | null;
  form: FormState;
  query: string;
  inputRef: React.RefObject<HTMLInputElement | null>;
  filteredOptions: Option[];
  isSuggestOpen: boolean;
  setQuery: React.Dispatch<React.SetStateAction<string>>;
  setOpenKey: React.Dispatch<React.SetStateAction<PartKey | null>>;
  setIsSuggestOpen: React.Dispatch<React.SetStateAction<boolean>>;
  selectOption: (value: string, label?: string) => void;
  clearSelection: () => void;

}

export default function AutoComplete({ openKey, form, query, inputRef, filteredOptions, isSuggestOpen,
   setQuery, setOpenKey, setIsSuggestOpen, selectOption, clearSelection, }: Props) {

    const openLabel = openKey
    ? PART_FILES.find((p) => p.key === openKey)?.label ?? "Component"
    : "";

    const currentSelection = openKey ? form[openKey] : "";

    return  (
        <>
            {/* Autocomplete panel */}
            {openKey && (
              <div className="dropdownPanel">
                <div className="dropdownPanel__header">
                  <div className="dropdownPanel__title">Select: {openLabel}</div>
                  <div className="dropdownPanel__actions">
                    <button type="button" className="smallBtn" onClick={clearSelection}>
                      Clear
                    </button>
                    <button type="button" className="smallBtn" onClick={() => setOpenKey(null)}>
                      Close
                    </button>
                  </div>
                </div>

                <div className="autoWrap">
                  <input
                    ref={inputRef}
                    className="field__control"
                    placeholder={`Search ${openLabel}...`}
                    value={query}
                    onChange={(e) => {
                      setQuery(e.target.value);
                      setIsSuggestOpen(true);
                    }}
                    onFocus={() => setIsSuggestOpen(true)}
                    onBlur={() => {
                      // allow click selection before closing
                      window.setTimeout(() => setIsSuggestOpen(false), 120);
                    }}
                  />

                  <div className="autoMeta">
                    <span className="muted">
                      Selected: <strong>{currentSelection || "(Any)"}</strong>
                    </span>
                    <span className="muted">
                      {query.trim() ? `Showing up to ${filteredOptions.length} matches` : "Type to search"}
                    </span>
                  </div>

                  {isSuggestOpen && query.trim().length > 0 && (
                    <div className="suggestBox" role="listbox" aria-label="Suggestions">
                      {filteredOptions.length === 0 ? (
                        <div className="suggestEmpty">No matches.</div>
                      ) : (
                        filteredOptions.map((opt) => (
                          <button
                            key={opt.value === opt.label ? opt.value : `${opt.value}__${opt.label}`}
                            type="button"
                            className="suggestItem"
                            onMouseDown={(e) => e.preventDefault()}
                            onClick={() => selectOption(opt.value, opt.label)}
                          >
                            {opt.label}
                          </button>
                        ))
                      )}
                    </div>
                  )}
                </div>

                <div className="dropdownPanel__hint">
                  Tip: results are filtered. Be specific (e.g., “7800X3D”).
                </div>
              </div>
            )}
        </>
    )
}