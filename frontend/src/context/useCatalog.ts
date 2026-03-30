import { useState, useEffect } from "react"
import type { PartCatalog } from "../types"
import { PART_FILES } from "../constants";
import { loadJsonArray } from "../utils";

// add isLoading for seperate loading state in the future sprint.
// replaced compatIssues that used to display catalog loading error with text message in the console log.
export function useCatalog() {
    const [catalog, setCatalog] = useState<PartCatalog>({})

    useEffect (() => {
        let cancelled = false;

        async function loadAll() {
        try {
            const entries = await Promise.all(
            PART_FILES.map(async ({ file }) => {
                const items = await loadJsonArray(`/data/${file}`);
                return [file, items] as const;
            })
            );

            if (cancelled) return;

            const next: PartCatalog = {};
            for (const [file, items] of entries) next[file] = items;
            setCatalog(next);
        } catch (err) {
            console.error(err);
            console.log("Error loading local JSON files. Make sure they exist in /public/data and are valid arrays.")
        }
        }

        loadAll();
        return () => {
            cancelled = true;
        };
    }, [])

    return {catalog}
}