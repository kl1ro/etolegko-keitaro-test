"use client";

import { CheckIcon, ChevronsUpDownIcon } from "lucide-react";
import { useState } from "react";

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
import type { SelectOption, SelectOptionValue } from "@/lib/select-options";
import { cn } from "@/lib/utils";

export default function SearchableSelect<Value extends SelectOptionValue>(
  props: SearchableSelectProps<Value>,
) {
  const state = useSearchableSelectState(props);

  return (
    <Popover open={state.open.value} onOpenChange={state.open.set}>
      <PopoverTrigger asChild>
        <Button
          id={props.id}
          variant="outline"
          role="combobox"
          aria-expanded={state.open.value}
          aria-invalid={props.invalid}
          disabled={props.disabled}
          className="w-full justify-between font-normal"
        >
          <span
            className={cn(
              "truncate",
              !state.selectedOption && "text-muted-foreground",
            )}
          >
            {state.selectedOption?.label ?? props.placeholder}
          </span>

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
                  onSelect={() => selectOption(option, state)}
                >
                  <CheckIcon
                    className={cn(
                      "opacity-0",
                      option === state.selectedOption && "opacity-100",
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

export interface SearchableSelectProps<Value extends SelectOptionValue> {
  id?: string;
  value: Value | undefined;
  options: SelectOption<Value>[];
  placeholder: string;
  emptyText?: string;
  invalid?: boolean;
  disabled?: boolean;
  onValueChange: (value: Value) => void;
}

function useSearchableSelectState<Value extends SelectOptionValue>(
  props: SearchableSelectProps<Value>,
) {
  return {
    open: useSearchableSelectOpen(),
    selectedOption: findSelectedOption(props.value, props),
    onValueChange: props.onValueChange,
  };
}

function getOptionSearchText(option: SelectOption<SelectOptionValue>) {
  return `${option.label} ${option.hint}`;
}

function selectOption<Value extends SelectOptionValue>(
  option: SelectOption<Value>,
  deps: SelectOptionDeps<Value>,
) {
  deps.onValueChange(option.value);
  deps.open.set(false);
}

interface SelectOptionDeps<Value extends SelectOptionValue> {
  open: SearchableSelectOpen;
  onValueChange: (value: Value) => void;
}

function useSearchableSelectOpen() {
  const [value, set] = useState(false);
  return { value, set };
}

type SearchableSelectOpen = ReturnType<typeof useSearchableSelectOpen>;

function findSelectedOption<Value extends SelectOptionValue>(
  value: Value | undefined,
  deps: FindSelectedOptionDeps<Value>,
): SelectOption<Value> | undefined {
  return deps.options.find((option) => option.value === value);
}

interface FindSelectedOptionDeps<Value extends SelectOptionValue> {
  options: SelectOption<Value>[];
}
