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
  { key: "cpu", label: "CPU", file: "cpu.json" },
  { key: "gpu", label: "GPU", file: "video-card.json" },
  { key: "motherboard", label: "Motherboard", file: "motherboard.json" },
  { key: "ram", label: "RAM", file: "memory.json" },
  { key: "psu", label: "PSU", file: "power-supply.json" },
  { key: "storage", label: "Storage", file: "internal-hard-drive.json" },
  { key: "cpuCooler", label: "CPU Cooler", file: "cpu-cooler.json" },
  { key: "monitor", label: "Monitor", file: "monitor.json" },
  { key: "case", label: "Case", file: "case.json" },
  { key: "operatingSystem", label: "Operating System", file: "os.json" },
] as const satisfies readonly PartDef[];

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
