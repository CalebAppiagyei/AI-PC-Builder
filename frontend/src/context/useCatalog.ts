import { useState, useEffect } from "react"
import type { PartCatalog } from "../types"
import { PART_FILES } from "../constants";
import { loadJsonArray } from "../utils";


export function useCatalog() {
    const [catalog, setCatalog] = useState<PartCatalog>({})
    const [compatIssues, setCompatIssues] = useState(
        "Compatibility issues will appear here after you select a component."
    );

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
            setCompatIssues(
                "Error loading local JSON files. Make sure they exist in /public/data and are valid arrays."
            );
        }
        }

        loadAll();
        return () => {
            cancelled = true;
        };
    }, [])

    return {catalog, compatIssues}
}