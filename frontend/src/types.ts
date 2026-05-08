import { PART_FILES } from "./constants";

export type Mode = "full" | "upgrade";

export type PartItem = {
  name: string;
  [key: string]: unknown;
};

export type PartCatalog = Record<string, PartItem[]>;

export type FormState = {
  cpu: string;
  gpu: string;
  motherboard: string;
  ram: string;
  psu: string;
  storage: string;
  cpuCooler: string;
  monitor: string;
  case: string;
  operatingSystem: string;
  primaryUse: string;
  budget: string;
};

export type PartDef = {
  key: keyof FormState;
  label: string;
  endpoint: string;
};

export type PartKey = (typeof PART_FILES)[number]["key"];

export type SelectedPayload = {
  CPU: string;
  "Video Card (GPU)": string;
  Motherboard: string;
  "Memory (RAM)": string;
  "Power Supply (PSU)": string;
  Storage: string;
  "CPU Cooler": string;
  Monitor: string;
  Case: string;
  "Operating System": string;
  _use_case: string;
  Budget: string;
  Mode: string;
};

export type Option = {
  label: string;
  value: string;
};
