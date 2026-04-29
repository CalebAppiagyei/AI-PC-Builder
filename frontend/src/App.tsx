import { useState, useMemo,useEffect } from "react";

import { useCatalog } from "./context/useCatalog";
import { useCompatibility } from "./context/useCompatibility";
import { useAI } from "./context/useAI";
import { usePartAutocomplete } from "./context/usePartAutoComplete";

import type { Mode, FormState } from "./types"
import { buildSelectedPayload, moneyToNumber } from "./utils";
import { initialForm, PART_KEYS } from "./constants";

import Selections from "./components/Selections";
import AIOutput from "./components/AIOutput";
import ModeSelect from "./components/ModeSelect"

import "./styles.css";

export default function App() {
  const { catalog } = useCatalog()
  const [mode, setMode] = useState<Mode>("full");
  const [isLoading, setIsLoading] = useState(false);
  const [form, setForm] = useState<FormState>(initialForm);

  const {
    query,
    setQuery,
    isSuggestOpen,
    setIsSuggestOpen,
    openKey,
    setOpenKey,
    inputRef,
    filteredOptions,
    selectOption,
    clearSelection,
  } = usePartAutocomplete(catalog, update);
  
  const buttonLabel = mode === "full" ? "Generate Build" : "Recommend Upgrade";

  const selectedPayload = useMemo(
    () => buildSelectedPayload(form, mode),
    [form, mode]
  )
  const hasSelectedPart = useMemo(
    () => PART_KEYS.some((key) => form[key].trim() !== ""),
    [form]
  )

  const { compatIssues, setCompatIssues } = useCompatibility( hasSelectedPart, selectedPayload, isLoading);
  const { aiOutput, onRun } = useAI( setIsLoading, setCompatIssues )

  function update<K extends keyof FormState>(key: K, value: FormState[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  // When opening a new component, reset search UI
  useEffect(() => {
    if (!openKey) {
      setQuery("");
      setIsSuggestOpen(false);
      return;
    }
    // set query to current selection (optional). I prefer blank for searching.
    setQuery("");
    setIsSuggestOpen(false);

    // focus input next tick
    setTimeout(() => inputRef.current?.focus(), 0);
  }, [openKey]);


  return  (
    <div className="page">
      <header className="header">
        <div className="header__title">AI PC Builder</div>
      </header>
      <main className="content">
        <ModeSelect 
          mode={mode} 
          setMode={setMode}/>
        <Selections 
          query={query}
          form={form}
          compatIssues={compatIssues}
          filteredOptions={filteredOptions}
          isLoading={isLoading}
          catalog={catalog}
          openKey={openKey}
          inputRef={inputRef}
          buttonLabel={buttonLabel}
          isSuggestOpen={isSuggestOpen}
          setOpenKey={setOpenKey}
          setQuery={setQuery}
          setIsSuggestOpen={setIsSuggestOpen}
          update={update}
          selectOption={selectOption}
          clearSelection={clearSelection}
          onRun={() => onRun(selectedPayload, moneyToNumber(form.budget))}/>
        <AIOutput aiOutput={aiOutput}/>
      </main> 
    </div>
  )
}