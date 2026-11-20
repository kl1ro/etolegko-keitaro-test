"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import {
  useQuery,
  useQueryClient,
  type QueryClient,
} from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import CampaignCountryField from "@/components/campaign-creator/CampaignCountryField";
import CampaignLookupField from "@/components/campaign-creator/CampaignLookupField";
import CampaignNameField from "@/components/campaign-creator/CampaignNameField";
import { Button } from "@/components/ui/button";
import { FieldGroup } from "@/components/ui/field";
import {
  createCampaign,
  describeApiRejection,
  type Campaign,
  type CampaignForm,
} from "@/lib/api";
import {
  CAMPAIGN_FORM_SCHEMA,
  type CampaignFormValues,
} from "@/lib/campaign-form";
import {
  CAMPAIGN_GROUPS_QUERY,
  CAMPAIGNS_QUERY,
  DOMAINS_QUERY,
  OFFERS_QUERY,
  TRAFFIC_SOURCES_QUERY,
} from "@/lib/queries";

export default function CampaignCreator() {
  const state = useCampaignCreatorState();

  return (
    <form
      noValidate
      onSubmit={state.form.handleSubmit((form) =>
        tryCreateCampaign(form, state),
      )}
      className="flex w-full max-w-xl flex-col gap-6"
    >
      <FieldGroup>
        <CampaignNameField form={state.form} />
        <CampaignCountryField form={state.form} />

        <CampaignLookupField
          form={state.form}
          name="offer_id"
          label="Оффер"
          placeholder="Выберите оффер"
          query={state.offers}
        />

        <CampaignLookupField
          form={state.form}
          name="domain_id"
          label="Домен"
          placeholder="Выберите домен"
          query={state.domains}
        />

        <CampaignLookupField
          form={state.form}
          name="group_id"
          label="Группа"
          placeholder="Выберите группу"
          query={state.campaignGroups}
        />

        <CampaignLookupField
          form={state.form}
          name="traffic_source_id"
          label="Источник трафика"
          placeholder="Выберите источник трафика"
          query={state.trafficSources}
        />
      </FieldGroup>

      <Button
        type="submit"
        disabled={state.form.formState.isSubmitting}
        className="self-start"
      >
        Создать кампанию
      </Button>
    </form>
  );
}

function useCampaignCreatorState() {
  return {
    form: useForm<CampaignFormValues, unknown, CampaignForm>({
      resolver: zodResolver(CAMPAIGN_FORM_SCHEMA),
      defaultValues: { name: "", countries: [] },
    }),

    offers: useQuery(OFFERS_QUERY),
    domains: useQuery(DOMAINS_QUERY),
    campaignGroups: useQuery(CAMPAIGN_GROUPS_QUERY),
    trafficSources: useQuery(TRAFFIC_SOURCES_QUERY),
    queryClient: useQueryClient(),
    router: useRouter(),
  };
}

async function tryCreateCampaign(
  form: CampaignForm,
  deps: TryCreateCampaignDeps,
) {
  try {
    toast.loading("Создание кампании…", { id: CAMPAIGN_CREATION_TOAST_ID });
    const campaign = await createCampaign(form);
    await refreshCampaignList(deps);
    openCampaignEditor(campaign, deps);
    toast.success("Кампания создана", { id: CAMPAIGN_CREATION_TOAST_ID });
  } catch (error) {
    console.error(error);
    toast.error("Не удалось создать кампанию", {
      id: CAMPAIGN_CREATION_TOAST_ID,
      description: describeApiRejection(error),
    });
  }
}

const CAMPAIGN_CREATION_TOAST_ID = "campaign-creation";

interface TryCreateCampaignDeps {
  queryClient: QueryClient;
  router: ReturnType<typeof useRouter>;
}

async function refreshCampaignList(deps: RefreshCampaignListDeps) {
  await deps.queryClient.invalidateQueries({
    queryKey: CAMPAIGNS_QUERY.queryKey,
  });
}

interface RefreshCampaignListDeps {
  queryClient: QueryClient;
}

function openCampaignEditor(campaign: Campaign, deps: OpenCampaignEditorDeps) {
  deps.router.push(`/campaigns/${campaign.id}`);
}

interface OpenCampaignEditorDeps {
  router: ReturnType<typeof useRouter>;
}
