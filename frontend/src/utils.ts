import type {PartItem, PartKey} from './types'

// Ensure Json caontains valid parts
export function isPartItem(x: unknown): x is PartItem {
  if (typeof x !== "object" || x === null) return false;
  const rec = x as Record<string, unknown>;
  return typeof rec.name === "string" && rec.name.length > 0;
}
// Convert "$1,500" -> 1500
export function moneyToNumber(raw: string): number | null {
  const cleaned = raw.replace(/[$, ]/g, "");
  if (cleaned.trim() === "") return null;
  const n = Number(cleaned);
  return Number.isFinite(n) && n >= 0 ? n : null;
}
// Load Json file
export async function loadJsonArray(url: string): Promise<PartItem[]> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to load ${url}: ${res.status}`);
  const data: unknown = await res.json();
  if (!Array.isArray(data)) throw new Error(`${url} must be a JSON array`);
  return data.filter(isPartItem);
}
// Conver to lower cases
export function normalize(s: string): string {
  return s.trim().toLowerCase();
}
// Output 50 items
export function filterItems (itemsForOpenKey: PartItem[], openKey: PartKey | null, query: string) {
  if (!openKey) return [];
  const q = normalize(query);
  if (!q) return [];
  // Filter + cap results so we only render a small list
  const out: Array<{ label: string; value: string }> = [];
  for (const item of itemsForOpenKey) {
    if (out.length >= 50) break; // cap to keep UI snappy
    const nomlizedName = normalize(item.name)
    // GPU: search by name OR chipset, and display both
    if (openKey === "gpu") {
      const chipset = normalize(typeof item.chipset === "string" ? item.chipset : "");
      const haystack = `${nomlizedName} ${chipset}`;
      if (haystack.includes(q)) {
        out.push({ 
          label: chipset ? `${item.name} — ${chipset}` : item.name, 
          value: item.name });
      }
      continue;
    }
    // Default: search by name only
    if (nomlizedName.includes(q)) {
      out.push({ label: item.name, value: item.name });
    }
  }
  return out;
}
