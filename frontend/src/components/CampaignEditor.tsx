"use client";

import { useQuery, type UseQueryResult } from "@tanstack/react-query";

import CampaignOfferAddition from "@/components/campaign-editor/CampaignOfferAddition";
import CampaignOfferTable from "@/components/campaign-editor/CampaignOfferTable";
import PageTitle from "@/components/PageTitle";
import QueryError from "@/components/QueryError";
import { Skeleton } from "@/components/ui/skeleton";
import type { Campaign } from "@/lib/api";
import {
  CAMPAIGNS_QUERY,
  getCampaignOffersQuery,
  OFFERS_QUERY,
} from "@/lib/queries";

export default function CampaignEditor(props: CampaignEditorProps) {
  const state = useCampaignEditorState(props);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-1">
        <PageTitle>{getCampaignTitle(props.campaignId, state)}</PageTitle>
        <p className="text-sm text-muted-foreground">ID {props.campaignId}</p>
      </div>

      <section className="flex flex-col gap-4">
        <h2 className="text-lg font-medium">Офферы</h2>

        {state.campaignOffers.isPending && <Skeleton className="h-40 w-full" />}

        {state.campaignOffers.isError && (
          <QueryError
            message="Не удалось загрузить офферы кампании"
            error={state.campaignOffers.error}
          />
        )}

        {state.campaignOffers.isSuccess && (
          <>
            <CampaignOfferTable
              campaignId={props.campaignId}
              campaignOffers={state.campaignOffers.data}
              offers={state.offers.data ?? []}
            />

            <CampaignOfferAddition
              campaignId={props.campaignId}
              campaignOffers={state.campaignOffers.data}
              offers={state.offers.data ?? []}
            />
          </>
        )}
      </section>
    </div>
  );
}

export interface CampaignEditorProps {
  campaignId: Campaign["id"];
}

function useCampaignEditorState(props: CampaignEditorProps) {
  return {
    campaigns: useQuery(CAMPAIGNS_QUERY),
    offers: useQuery(OFFERS_QUERY),
    campaignOffers: useQuery(getCampaignOffersQuery(props.campaignId)),
  };
}

function getCampaignTitle(
  campaignId: Campaign["id"],
  deps: GetCampaignTitleDeps,
) {
  const campaign = deps.campaigns.data?.find(
    (candidate) => candidate.id === campaignId,
  );
  return campaign?.name ?? `Кампания #${campaignId}`;
}

interface GetCampaignTitleDeps {
  campaigns: UseQueryResult<Campaign[]>;
}
