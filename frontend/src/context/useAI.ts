import { useState } from "react";
import { moneyToNumber } from "../utils";
import type { FormState, SelectedPayload } from "../types";
import { API_BASE_URL } from "../constants";


export function useAI (
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>,
  setCompatIssues: React.Dispatch<React.SetStateAction<string>>,
  selectedPayload: SelectedPayload, 
) {
    const [aiOutput, setAiOutput] = useState("AI output will appear here after you run.");
    async function onRun(form: FormState) {
      setIsLoading(true);
      setCompatIssues("Running…");
      setAiOutput("Running…");

      try {
        const budget = moneyToNumber(form.budget);
        if (budget === null) {
          setCompatIssues("Please enter a valid budget (example: 1500).");
          setAiOutput("—");
          return;
        }

        const selected = selectedPayload;

        const res = await fetch(`${API_BASE_URL}/stream`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ selected })
        });

        if (!res.ok || !res.body) {
          const text = await res.text();
          throw new Error(`Server error ${res.status}: ${text}`);
        }

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";
        let aiAccum = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, {stream: true});
          const lines = buffer.split("\n");
          buffer = lines.pop() ?? "";

          for (const line of lines) {
            if (!line.startsWith("data: ")) continue;
            const payload = line.slice(6).trim();
            try {
              const msg = JSON.parse(payload) as { type: string; text?: string };
              if (msg.type === "compat" && msg.text) {
                setCompatIssues(msg.text);
              } else if (msg.type === "token" && msg.text) {
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

  return { aiOutput, onRun}
}