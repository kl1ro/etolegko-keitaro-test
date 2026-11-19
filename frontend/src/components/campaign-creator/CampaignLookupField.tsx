"use client";

import type { UseQueryResult } from "@tanstack/react-query";
import { Controller } from "react-hook-form";

import SearchableSelect from "@/components/SearchableSelect";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import type { NamedRecord } from "@/lib/api";
import type { CampaignFormLookupName, CampaignFormState } from "@/lib/campaign-form";
import { convertNamedRecordToOption } from "@/lib/select-options";

export default function CampaignLookupField(props: CampaignLookupFieldProps) {
  const options = props.query.data?.map(convertNamedRecordToOption) ?? [];
  const id = `campaign-${props.name}`;

  return (
    <Controller
      control={props.form.control}
      name={props.name}
      render={(controller) => (
        <Field data-invalid={controller.fieldState.invalid}>
          <FieldLabel htmlFor={id}>{props.label}</FieldLabel>

          <SearchableSelect
            id={id}
            value={controller.field.value}
            options={options}
            placeholder={props.query.isPending ? "Загрузка…" : props.placeholder}
            emptyText={props.query.isError ? "Не удалось загрузить список" : undefined}
            invalid={controller.fieldState.invalid}
            disabled={props.query.isPending}
            onValueChange={controller.field.onChange}
          />

          <FieldError errors={[controller.fieldState.error]} />
        </Field>
      )}
    />
  );
}

export interface CampaignLookupFieldProps {
  form: CampaignFormState;
  name: CampaignFormLookupName;
  label: string;
  placeholder: string;
  query: UseQueryResult<NamedRecord[]>;
}
