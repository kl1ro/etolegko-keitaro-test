"use client";

import { Controller } from "react-hook-form";

import SearchableMultiSelect from "@/components/SearchableMultiSelect";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import type { CampaignFormState } from "@/lib/campaign-form";
import { createCountryOptions } from "@/lib/countries";

export default function CampaignCountryField(props: CampaignCountryFieldProps) {
  return (
    <Controller
      control={props.form.control}
      name="countries"
      render={(controller) => (
        <Field data-invalid={controller.fieldState.invalid}>
          <FieldLabel htmlFor="campaign-countries">Страны</FieldLabel>

          <SearchableMultiSelect
            id="campaign-countries"
            values={controller.field.value}
            options={COUNTRY_OPTIONS}
            placeholder="Выберите страны"
            invalid={controller.fieldState.invalid}
            onValuesChange={controller.field.onChange}
          />

          <FieldError errors={[controller.fieldState.error]} />
        </Field>
      )}
    />
  );
}

export interface CampaignCountryFieldProps {
  form: CampaignFormState;
}

const COUNTRY_OPTIONS = createCountryOptions();
