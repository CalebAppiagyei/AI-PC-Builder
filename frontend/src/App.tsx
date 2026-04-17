import { useState, useRef, useMemo,useEffect } from "react";

import { useCatalog } from "./context/useCatalog";
import { useCompatibility } from "./context/useCompatibility";
import { useAI } from "./context/useAI";

import type { Mode,FormState, PartKey, PartItem} from "./types"
import { moneyToNumber, filterItems } from "./utils";
import { initialForm, PART_FILES } from "./constants";

import Selections from "./components/Selections";
import AIOutput from "./components/AIOutput";
import ModeSelect from "./components/ModeSelect"

import "./styles.css";

export default function App() {
  const { catalog } = useCatalog()
  const [query, setQuery] = useState("");
  const [mode, setMode] = useState<Mode>("full");
  const [isLoading, setIsLoading] = useState(false);
  const [form, setForm] = useState<FormState>(initialForm);
  const [isSuggestOpen, setIsSuggestOpen] = useState(false);
  const [openKey, setOpenKey] = useState<PartKey | null>(null);
  
  const inputRef = useRef<HTMLInputElement | null>(null);
  const buttonLabel = mode === "full" ? "Generate Build" : "Recommend Upgrade";

  // useCallback to avoid frequent request?
  function buildSelectedPayload(budgetOverride?: number) {
    const effectiveBudget = budgetOverride ?? moneyToNumber(form.budget) ?? 0;
    return {
      CPU: form.cpu || "(any)",
      "Video Card (GPU)": form.gpu || "(any)",
      Motherboard: form.motherboard || "(any)",
      "Memory (RAM)": form.ram || "(any)",
      "Power Supply (PSU)": form.psu || "(any)",
      Storage: form.storage || "(any)",
      "CPU Cooler": form.cpuCooler || "(any)",
      Monitor: form.monitor || "(any)",
      Case: form.case || "(any)",
      "Operating System": form.operatingSystem || "(any)",
      "_use_case": form.primaryUse,
      Budget: `$${effectiveBudget.toFixed(2)}`,
      Mode: mode === "full" ? "Full PC build" : "Upgrade recommendation",
    };
  }

  const { compatIssues, setCompatIssues } = useCompatibility( form, buildSelectedPayload, isLoading, mode );
  const { aiOutput, onRun } = useAI( setIsLoading, setCompatIssues, buildSelectedPayload, )

  const itemsForOpenKey = useMemo<PartItem[]>(() => {
      if (!openKey) return [];
      const file = PART_FILES.find((p) => p.key === openKey)?.file;
      if (!file) return [];
      return catalog[file] ?? [];
    }, [openKey, catalog]);

  // bugs?
  const filteredOptions = useMemo(() => filterItems(itemsForOpenKey, openKey, query), [itemsForOpenKey, openKey, query])

  function update<K extends keyof FormState>(key: K, value: FormState[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  function selectOption(value: string, label?: string) {
    if (!openKey) return;
    update(openKey, value);
    setQuery(label ?? value);
    setIsSuggestOpen(false);
  }

  function clearSelection() {
    if (!openKey) return;
    update(openKey, "");
    setQuery("");
    setIsSuggestOpen(false);
    inputRef.current?.focus();
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
          options={filteredOptions}
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
          onRun={() => onRun(form)}/>
        <AIOutput aiOutput={aiOutput}/>
      </main> 
    </div>
  )
}