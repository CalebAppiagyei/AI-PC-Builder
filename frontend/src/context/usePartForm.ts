
import { useState } from "react";
import type { FormState } from "../types";
import { initialForm } from "../constants";

// Owns Form state for selection section

export function usePartForm() {
  const [form, setForm] = useState<FormState>(initialForm);


//   Update the field on selection form
  function update<K extends keyof FormState>(key: K, value: FormState[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  return {
    form,
    setForm,
    update,
  };
}