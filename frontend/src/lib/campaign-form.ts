import type { UseFormReturn } from "react-hook-form";
import { z } from "zod";

import type { CampaignForm } from "@/lib/api";

export const CAMPAIGN_FORM_SCHEMA = z.object({
  name: z.string().trim().min(1, "Введите название"),
  country: z.string({ error: "Выберите страну" }),
  offer_id: z.number({ error: "Выберите оффер" }),
  domain_id: z.number({ error: "Выберите домен" }),
  group_id: z.number({ error: "Выберите группу" }),
  traffic_source_id: z.number({ error: "Выберите источник трафика" }),
}) satisfies z.ZodType<CampaignForm>;

export type CampaignFormValues = z.input<typeof CAMPAIGN_FORM_SCHEMA>;
export type CampaignFormState = UseFormReturn<
  CampaignFormValues,
  unknown,
  CampaignForm
>;
export type CampaignFormLookupName = Exclude<
  keyof CampaignForm,
  "name" | "country"
>;
