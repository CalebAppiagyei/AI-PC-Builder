import { useState, useEffect } from "react"
import type { PartCatalog } from "../types"
import { PART_FILES } from "../constants";
import { loadJsonArray } from "../utils";
import { API_BASE_URL } from "../constants";

// add isLoading for seperate loading state in the future sprint.
// replaced compatIssues that used to display catalog loading error with text message in the console log.
export function useCatalog() {
    const [catalog, setCatalog] = useState<PartCatalog>({})
    const [isLoading, setIsLoading] = useState(true)

    useEffect (() => {
        let cancelled = false;
        setIsLoading(true);

        async function loadAll() {
        try {
            const entries = await Promise.all(
            PART_FILES.map(async ({ endpoint }) => {
                const items = await loadJsonArray(`${API_BASE_URL}/parts/${endpoint}`);
                return [endpoint, items] as const;
            })
            );

            if (cancelled) return;

            const next: PartCatalog = {};
            for (const [endpoint, items] of entries) next[endpoint] = items;
            setCatalog(next);
        } catch (err) {
            console.error(err);
            console.log("Error loading database, check your connection.")
        } finally {
            if (!cancelled) setIsLoading(false);
        }
        }

        loadAll();
        return () => {
            cancelled = true;
        };
    }, [])

    return {catalog, isLoading}
}