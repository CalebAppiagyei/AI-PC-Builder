import { useEffect, useMemo, useRef, useState } from "react";
import { PART_FILES } from "../constants";
import { filterItems } from "../utils";
import type { FormState, PartCatalog, PartItem, PartKey } from "../types";

// Owns autocomplete sections

type UpdateForm = <K extends keyof FormState>(key: K, value: FormState[K]) => void;

export function usePartAutocomplete(
  catalog: PartCatalog,
  update: UpdateForm
) {

  // Autocomplete input
  const [query, setQuery] = useState(""); 
  // suggestion dropdoem state
  const [isSuggestOpen, setIsSuggestOpen] = useState(false); 
  // track pc category table
  const [openKey, setOpenKey] = useState<PartKey | null>(null); 
  // Autocomplet input focus
  const inputRef = useRef<HTMLInputElement | null>(null); 



  const itemsForOpenKey = useMemo<PartItem[]>(() => {
    if (!openKey) return [];

    const endpoint = PART_FILES.find((p) => p.key === openKey)?.endpoint;
    if (!endpoint) return [];

    return catalog[endpoint] ?? [];
  }, [openKey, catalog]);

  // Apply search filter condition to current category
  const filteredOptions = useMemo(
    () => filterItems(itemsForOpenKey, openKey, query),
    [itemsForOpenKey, openKey, query]
  );

  // Write selected category into the form
  function selectOption(value: string, label?: string) {
    if (!openKey) return;

    update(openKey, value);
    setQuery(label ?? value);
    setIsSuggestOpen(false);
  }

  // Clear current selections
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