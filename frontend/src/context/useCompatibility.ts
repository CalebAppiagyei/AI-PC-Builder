import type { SelectedPayload } from "../types";
import { useState, useEffect } from "react";
import { API_BASE_URL } from "../constants";


export function useCompatibility( 
    hasSelectedPart: boolean, 
    selectedPayload: SelectedPayload, 
    isLoading: boolean, 
) {
    const [compatIssues, setCompatIssues] = useState(
        "Compatibility issues will appear here after you select a component."
    );

    useEffect (() => {
        if (isLoading) return;

        if (!hasSelectedPart) {
            setCompatIssues("Compatibility issues will appear here after you select a component.");
            return;
        }

        const controller = new AbortController();
        const timeoutId = window.setTimeout(async () => {
            try {
                setCompatIssues("Checking compatibility…");

                const res = await fetch(`${API_BASE_URL}/compatibility`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ selected: selectedPayload }),
                    signal: controller.signal,
                });

                if (!res.ok) {
                    const text = await res.text();
                    throw new Error(`Server error ${res.status}: ${text}`);
                }

                const data = (await res.json()) as { compat_issues?: string };
                setCompatIssues(data.compat_issues || "No compatibility issues detected.");

            } catch (err: unknown) {

                if (controller.signal.aborted) return;
                const message = err instanceof Error ? err.message : String(err);
                setCompatIssues(`Error: ${message}`);

            }
        }, 250);

        return () => {
            window.clearTimeout(timeoutId);
            controller.abort();
        };
    }, [hasSelectedPart, selectedPayload, isLoading])

    return { compatIssues, setCompatIssues}
}