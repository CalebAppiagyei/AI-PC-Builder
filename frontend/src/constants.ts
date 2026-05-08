import type { PartDef, FormState } from "./types";

export const API_BASE_URL = 'http://localhost:8000';

export const PRIMARY_USES = [
  "Gaming",
  "Streaming",
  "Video Editing",
  "3D / Rendering",
  "Programming / Dev",
  "School / Office",
  "General Use",
] as const;

export const PART_FILES = [
  { key: "cpu", label: "CPU", endpoint: "cpu" },
  { key: "gpu", label: "GPU", endpoint: "gpu" },
  { key: "motherboard", label: "Motherboard", endpoint: "motherboard" },
  { key: "ram", label: "RAM", endpoint: "ram" },
  { key: "psu", label: "PSU", endpoint: "psu" },
  { key: "storage", label: "Storage", endpoint: "storage" },
  { key: "cpuCooler", label: "CPU Cooler", endpoint: "cpuCooler" },
  { key: "monitor", label: "Monitor", endpoint: "monitor" },
  { key: "case", label: "Case", endpoint: "case" },
  { key: "operatingSystem", label: "Operating System", endpoint: "operatingSystem" },
] as const satisfies readonly PartDef[];

type PartKey = (typeof PART_FILES)[number]["key"];
export const PART_KEYS = PART_FILES.map((part) => part.key);

export const initialForm: FormState = {
  cpu: "",
  gpu: "",
  motherboard: "",
  ram: "",
  psu: "",
  storage: "",
  cpuCooler: "",
  monitor: "",
  case: "",
  operatingSystem: "",
  primaryUse: PRIMARY_USES[0],
  budget: "",
};
