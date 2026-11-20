"use client";

import { CheckIcon, ChevronsUpDownIcon } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  getOptionSearchText,
  type SelectOption,
  type SelectOptionValue,
} from "@/lib/select-options";
import { cn } from "@/lib/utils";

export default function SearchableMultiSelect<Value extends SelectOptionValue>(
  props: SearchableMultiSelectProps<Value>,
) {
  const state = useSearchableMultiSelectState(props);

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          id={props.id}
          variant="outline"
          role="combobox"
          aria-invalid={props.invalid}
          disabled={props.disabled}
          className="h-auto min-h-9 w-full justify-between font-normal"
        >
          <SelectedOptionTags
            options={state.selectedOptions}
            placeholder={props.placeholder}
          />

          <ChevronsUpDownIcon className="opacity-50" />
        </Button>
      </PopoverTrigger>

      <PopoverContent
        align="start"
        className="w-(--radix-popover-trigger-width) p-0"
      >
        <Command>
          <CommandInput placeholder="Поиск…" />

          <CommandList>
            <CommandEmpty>
              {props.emptyText ?? "Ничего не найдено"}
            </CommandEmpty>

            <CommandGroup>
              {props.options.map((option) => (
                <CommandItem
                  key={option.value}
                  value={getOptionSearchText(option)}
                  onSelect={() => toggleOption(option, state)}
                >
                  <CheckIcon
                    className={cn(
                      "opacity-0",
                      isOptionSelected(option, state) && "opacity-100",
                    )}
                  />
                  <span className="truncate">{option.label}</span>
                  <span className="ml-auto text-xs text-muted-foreground">
                    {option.hint}
                  </span>
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}

export interface SearchableMultiSelectProps<Value extends SelectOptionValue> {
  id?: string;
  values: Value[];
  options: SelectOption<Value>[];
  placeholder: string;
  emptyText?: string;
  invalid?: boolean;
  disabled?: boolean;
  onValuesChange: (values: Value[]) => void;
}

function useSearchableMultiSelectState<Value extends SelectOptionValue>(
  props: SearchableMultiSelectProps<Value>,
) {
  return {
    values: props.values,
    selectedOptions: findSelectedOptions(props.values, props),
    onValuesChange: props.onValuesChange,
  };
}

function SelectedOptionTags<Value extends SelectOptionValue>(
  props: SelectedOptionTagsProps<Value>,
) {
  if (!props.options.length)
    return <span className="text-muted-foreground">{props.placeholder}</span>;

  return (
    <span className="flex flex-wrap gap-1">
      {props.options.map((option) => (
        <span
          key={option.value}
          className="rounded-sm bg-secondary px-1.5 py-0.5 text-xs text-secondary-foreground"
        >
          {option.label}
        </span>
      ))}
    </span>
  );
}

interface SelectedOptionTagsProps<Value extends SelectOptionValue> {
  options: SelectOption<Value>[];
  placeholder: string;
}

function toggleOption<Value extends SelectOptionValue>(
  option: SelectOption<Value>,
  deps: ToggleOptionDeps<Value>,
) {
  const values = getValuesWithToggledValue(deps.values, option.value);
  deps.onValuesChange(values);
}

interface ToggleOptionDeps<Value extends SelectOptionValue> {
  values: Value[];
  onValuesChange: (values: Value[]) => void;
}

function isOptionSelected<Value extends SelectOptionValue>(
  option: SelectOption<Value>,
  deps: IsOptionSelectedDeps<Value>,
) {
  return deps.values.includes(option.value);
}

interface IsOptionSelectedDeps<Value extends SelectOptionValue> {
  values: Value[];
}

function findSelectedOptions<Value extends SelectOptionValue>(
  values: Value[],
  deps: FindSelectedOptionsDeps<Value>,
): SelectOption<Value>[] {
  const selectedOptions = deps.options.filter((option) =>
    values.includes(option.value),
  );

  return selectedOptions;
}

interface FindSelectedOptionsDeps<Value extends SelectOptionValue> {
  options: SelectOption<Value>[];
}

function getValuesWithToggledValue<Value extends SelectOptionValue>(
  values: Value[],
  value: Value,
): Value[] {
  if (values.includes(value))
    return values.filter((candidate) => candidate !== value);

  return [...values, value];
}
