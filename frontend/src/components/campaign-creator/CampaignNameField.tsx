"use client";

import { Controller } from "react-hook-form";

import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import type { CampaignFormState } from "@/lib/campaign-form";

export default function CampaignNameField(props: CampaignNameFieldProps) {
  return (
    <Controller
      control={props.form.control}
      name="name"
      render={(controller) => (
        <Field data-invalid={controller.fieldState.invalid}>
          <FieldLabel htmlFor="campaign-name">Название</FieldLabel>

          <Input
            {...controller.field}
            id="campaign-name"
            autoComplete="off"
            aria-invalid={controller.fieldState.invalid}
          />

          <FieldError errors={[controller.fieldState.error]} />
        </Field>
      )}
    />
  );
}

export interface CampaignNameFieldProps {
  form: CampaignFormState;
}
