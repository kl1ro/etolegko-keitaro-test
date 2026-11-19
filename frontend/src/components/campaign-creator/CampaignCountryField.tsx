"use client";

import { Controller } from "react-hook-form";

import SearchableSelect from "@/components/SearchableSelect";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import type { CampaignFormState } from "@/lib/campaign-form";
import { createCountryOptions } from "@/lib/countries";

export default function CampaignCountryField(props: CampaignCountryFieldProps) {
  return (
    <Controller
      control={props.form.control}
      name="country"
      render={(controller) => (
        <Field data-invalid={controller.fieldState.invalid}>
          <FieldLabel htmlFor="campaign-country">Страна</FieldLabel>

          <SearchableSelect
            id="campaign-country"
            value={controller.field.value}
            options={COUNTRY_OPTIONS}
            placeholder="Выберите страну"
            invalid={controller.fieldState.invalid}
            onValueChange={controller.field.onChange}
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
