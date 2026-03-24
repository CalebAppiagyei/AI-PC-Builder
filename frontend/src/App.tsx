import { useState, useRef, useMemo } from "react";

import { useCatalog } from "./context/useCatalog";
import { useCompatibility } from "./context/useCompatibility";
import { useAI } from "./context/useAI";

import type { Mode,FormState, PartKey, PartItem} from "./types"
import { moneyToNumber, filterItems } from "./utils";
import { initialForm, PART_FILES } from "./constants";

import Selections from "./components/Selections";
import Compatibility from "./components/Compatibility"
import AIOutput from "./components/AIOutput";

import "./styles.css";

export default function App() {
  const [mode, setMode] = useState<Mode>("full");
  const { catalog } = useCatalog()
  const [form, setForm] = useState<FormState>(initialForm);
  const [query, setQuery] = useState("");
  const [openKey, setOpenKey] = useState<PartKey | null>(null);
  const [isSuggestOpen, setIsSuggestOpen] = useState(false);
  const inputRef = useRef<HTMLInputElement | null>(null);
  
  const buttonLabel = mode === "full" ? "Generate Build" : "Recommend Upgrade";

  function update<K extends keyof FormState>(key: K, value: FormState[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

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

  const itemsForOpenKey = useMemo<PartItem[]>(() => {
      if (!openKey) return [];
      const file = PART_FILES.find((p) => p.key === openKey)?.file;
      if (!file) return [];
      return catalog[file] ?? [];
    }, [openKey, catalog]);

  // bugs?
  const filtedOptions = useMemo(() => filterItems(itemsForOpenKey, openKey, query), [openKey, query])

  function selectOption(value: string, label?: string) {
    if (!openKey) return;
    update(openKey, value);
    setQuery(label ?? value);
    setIsSuggestOpen(false);
  }

  const { aiOutput, isLoading, onRun } = useAI(buildSelectedPayload)
  const { compatIssues, setCompatIssues } = useCompatibility(
    form,
    buildSelectedPayload,
    isLoading,
    mode,
  );

  return  (
    <div className="page">
      <header className="header">
        <div className="header__title">AI PC Builder</div>
      </header>
      <main className="content">
        <Selections 
          form={form}
          update={update}
          onRun={() => onRun(form, setCompatIssues)}
          isLoading={isLoading}
          query={query}
          setQuery={setQuery}
          options={filtedOptions}
          selectOption={selectOption}
          setOpenKey={setOpenKey}
        />
        <Compatibility compatIssues={compatIssues} />
        <AIOutput aiOutput={aiOutput}/>
      </main> 
    </div>
  )
}