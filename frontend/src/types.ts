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
  file: string;
};

export type PartKey = (typeof PART_FILES)[number]["key"];
