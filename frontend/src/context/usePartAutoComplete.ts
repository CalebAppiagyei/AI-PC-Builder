import { useEffect, useMemo, useRef, useState } from "react";
import { PART_FILES } from "../constants";
import { filterItems } from "../utils";
import type { FormState, PartCatalog, PartItem, PartKey } from "../types";

type UpdateForm = <K extends keyof FormState>(key: K, value: FormState[K]) => void;

export function usePartAutocomplete(
  catalog: PartCatalog,
  update: UpdateForm
) {
  const [query, setQuery] = useState("");
  const [isSuggestOpen, setIsSuggestOpen] = useState(false);
  const [openKey, setOpenKey] = useState<PartKey | null>(null);

  const inputRef = useRef<HTMLInputElement | null>(null);

  const itemsForOpenKey = useMemo<PartItem[]>(() => {
    if (!openKey) return [];

    const file = PART_FILES.find((p) => p.key === openKey)?.file;
    if (!file) return [];

    return catalog[file] ?? [];
  }, [openKey, catalog]);

  const filteredOptions = useMemo(
    () => filterItems(itemsForOpenKey, openKey, query),
    [itemsForOpenKey, openKey, query]
  );

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

  return {
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
  };
}