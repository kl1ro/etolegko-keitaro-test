import type { NamedRecord } from "@/lib/api";

export interface SelectOption<Value extends SelectOptionValue> {
  value: Value;
  label: string;
  hint: string;
}

export type SelectOptionValue = string | number;

export function convertNamedRecordToOption(
  record: NamedRecord,
): SelectOption<NamedRecord["id"]> {
  return { value: record.id, label: record.name, hint: `#${record.id}` };
}
