import { useMemo, useRef, useState } from "react";
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



  // Finds the catalog items that belong to the currently opened pc part category.
  const itemsForOpenKey = useMemo<PartItem[]>(() => {
    if (!openKey) return [];

    const file = PART_FILES.find((p) => p.key === openKey)?.file;
    if (!file) return [];

    return catalog[file] ?? [];
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

  function toggleComponent(key: PartKey) {
    const next = openKey === key ? null : key;
    setOpenKey(next);
    setQuery("");
    setIsSuggestOpen(false);

    if (next) {
      window.setTimeout(() => inputRef.current?.focus(), 0);
    }
  }

  function closeComponent() {
    setOpenKey(null);
    setQuery("");
    setIsSuggestOpen(false);
  }

  return {
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
  };
}
