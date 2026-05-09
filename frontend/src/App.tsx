import { useState, useMemo } from "react";

import { useCatalog } from "./context/useCatalog";
import { useCompatibility } from "./context/useCompatibility";
import { useAI } from "./context/useAI";
import { usePartAutocomplete } from "./context/usePartAutoComplete";
import { usePartForm } from "./context/usePartForm"

import type { Mode } from "./types"
import { buildSelectedPayload, moneyToNumber } from "./utils";
import { PART_KEYS } from "./constants";

import Selections from "./components/Selections";
import AIOutput from "./components/AIOutput";
import ModeSelect from "./components/ModeSelect"

import "./styles.css";

export default function App() {
  const { catalog } = useCatalog()
  const { form, update }  = usePartForm();

  const [mode, setMode] = useState<Mode>("full");
  const [isLoading, setIsLoading] = useState(false);
  

  const {
    query,
    setQuery,
    isSuggestOpen,
    setIsSuggestOpen,
    openKey,
    inputRef,
    filteredOptions,
    toggleComponent,
    closeComponent,
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
          setQuery={setQuery}
          setIsSuggestOpen={setIsSuggestOpen}
          update={update}
          toggleComponent={toggleComponent}
          closeComponent={closeComponent}
          selectOption={selectOption}
          clearSelection={clearSelection}
          onRun={() => onRun(selectedPayload, moneyToNumber(form.budget))}/>
        <AIOutput aiOutput={aiOutput}/>
      </main> 
    </div>
  )
}
