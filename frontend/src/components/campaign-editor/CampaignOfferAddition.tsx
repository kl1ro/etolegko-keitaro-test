"use client";

import {
  useMutation,
  useQueryClient,
  type QueryClient,
  type UseMutationResult,
} from "@tanstack/react-query";
import { useState } from "react";
import { toast } from "sonner";

import SearchableSelect from "@/components/SearchableSelect";
import { Button } from "@/components/ui/button";
import {
  addCampaignOffer,
  describeApiRejection,
  type Campaign,
  type Offer,
  type StreamOffer,
} from "@/lib/api";
import { cacheCampaignOffers } from "@/lib/queries";
import { convertNamedRecordToOption } from "@/lib/select-options";

export default function CampaignOfferAddition(
  props: CampaignOfferAdditionProps,
) {
  const state = useCampaignOfferAdditionState(props);

  return (
    <div className="flex flex-col gap-2 sm:flex-row">
      <div className="min-w-0 flex-1">
        <SearchableSelect
          value={state.selectedOfferId.value}
          options={state.offerOptions}
          placeholder="Выберите оффер"
          onValueChange={state.selectedOfferId.set}
        />
      </div>

      <Button
        disabled={!state.selectedOfferId.value || state.addition.isPending}
        onClick={() => tryAddCampaignOffer(state)}
      >
        Добавить
      </Button>
    </div>
  );
}

export interface CampaignOfferAdditionProps {
  campaignId: Campaign["id"];
  campaignOffers: StreamOffer[];
  offers: Offer[];
}

function useCampaignOfferAdditionState(props: CampaignOfferAdditionProps) {
  return {
    campaignId: props.campaignId,
    offerOptions: getOffersOutsideCampaign(props.offers, props).map(
      convertNamedRecordToOption,
    ),
    selectedOfferId: useSelectedOfferId(),
    queryClient: useQueryClient(),
    addition: useMutation({
      mutationFn: (offerId: Offer["id"]) =>
        addCampaignOffer(props.campaignId, offerId),
    }),
  };
}

async function tryAddCampaignOffer(deps: TryAddCampaignOfferDeps) {
  try {
    if (!deps.selectedOfferId.value) return;
    toast.loading("Добавление оффера…", { id: OFFER_ADDITION_TOAST_ID });

    const campaignOffers = await deps.addition.mutateAsync(
      deps.selectedOfferId.value,
    );

    cacheCampaignOffers(campaignOffers, deps);
    deps.selectedOfferId.set(undefined);
    toast.success("Оффер добавлен", { id: OFFER_ADDITION_TOAST_ID });
  } catch (error) {
    console.error(error);
    toast.error("Не удалось добавить оффер", {
      id: OFFER_ADDITION_TOAST_ID,
      description: describeApiRejection(error),
    });
  }
}

const OFFER_ADDITION_TOAST_ID = "offer-addition";

interface TryAddCampaignOfferDeps {
  campaignId: Campaign["id"];
  selectedOfferId: SelectedOfferId;
  queryClient: QueryClient;
  addition: UseMutationResult<StreamOffer[], Error, Offer["id"]>;
}

function getOffersOutsideCampaign(
  offers: Offer[],
  deps: GetOffersOutsideCampaignDeps,
) {
  const campaignOfferIds = new Set(
    deps.campaignOffers.map((campaignOffer) => campaignOffer.offer_id),
  );
  const offersOutsideCampaign = offers.filter(
    (offer) => !campaignOfferIds.has(offer.id),
  );
  return offersOutsideCampaign;
}

interface GetOffersOutsideCampaignDeps {
  campaignOffers: StreamOffer[];
}

function useSelectedOfferId() {
  const [value, set] = useState<Offer["id"]>();
  return { value, set };
}

type SelectedOfferId = ReturnType<typeof useSelectedOfferId>;
