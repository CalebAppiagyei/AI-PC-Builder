import { useState } from "react";
import type { SelectedPayload } from "../types";
import { API_BASE_URL } from "../constants";

// Owns AI section's states and Send request to backend


export function useAI (
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>,
  setCompatIssues: React.Dispatch<React.SetStateAction<string>>,
) {
    // Ai response
    const [aiOutput, setAiOutput] = useState("AI output will appear here after you run.");
    
    // Run AI build/upgrade request
    async function onRun(selected: SelectedPayload, budget: number | null) {
      setIsLoading(true);
      setCompatIssues("Running…");
      setAiOutput("Running…");

      try {
        // Early stop when 0/null budget
        if (budget === null) {
          setCompatIssues("Please enter a valid budget (example: 1500).");
          setAiOutput("—");
          return;
        }

        // Setup AI request
        const res = await fetch(`${API_BASE_URL}/stream`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ selected })
        });

        // Model health check
        if (!res.ok || !res.body) {
          const text = await res.text();
          throw new Error(`Server error ${res.status}: ${text}`);
        }

        
        const reader = res.body.getReader();
        const decoder = new TextDecoder();

        // SSE lines between chunks
        let buffer = "";
        // AI response
        let aiAccum = "";


        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, {stream: true});
          const lines = buffer.split("\n");
          buffer = lines.pop() ?? "";

          for (const line of lines) {
            // Ignore unnecesary lines
            if (!line.startsWith("data: ")) continue;
            const payload = line.slice(6).trim();
            try {
              const msg = JSON.parse(payload) as { type: string; text?: string };

              if (msg.type === "compat" && msg.text) {
                // Message to compatibility section
                setCompatIssues(msg.text);
              } else if (msg.type === "token" && msg.text) {
                // Message to AI section
                aiAccum += msg.text;
                setAiOutput(aiAccum);
              }
            } catch (err) {
              console.warn("Failed to parse SSE payload:", payload, err);
              setCompatIssues("Received an invalid response chunk from the server.");
            }
          }
        }
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : String(err);
        setCompatIssues(`Error: ${message}`);
        setAiOutput("Check error message in COMPATIBILITY ISSUES section.");
      } finally {
        setIsLoading(false);
      }
    }

  return { aiOutput, onRun }
}