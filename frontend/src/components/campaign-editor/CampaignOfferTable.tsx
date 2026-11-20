"use client";

import {
  useMutation,
  useQueryClient,
  type QueryClient,
  type UseMutationResult,
} from "@tanstack/react-query";
import { Trash2Icon } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  describeApiRejection,
  removeCampaignOffer,
  type Campaign,
  type Offer,
  type StreamOffer,
} from "@/lib/api";
import { cacheCampaignOffers } from "@/lib/queries";

export default function CampaignOfferTable(props: CampaignOfferTableProps) {
  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Оффер</TableHead>
            <TableHead className="w-24 text-right">Доля</TableHead>
            <TableHead className="w-12" />
          </TableRow>
        </TableHeader>

        <TableBody>
          {props.campaignOffers.map((campaignOffer) => (
            <CampaignOfferRow
              key={campaignOffer.offer_id}
              campaignId={props.campaignId}
              campaignOffer={campaignOffer}
              offers={props.offers}
            />
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

export interface CampaignOfferTableProps {
  campaignId: Campaign["id"];
  campaignOffers: StreamOffer[];
  offers: Offer[];
}

function CampaignOfferRow(props: CampaignOfferRowProps) {
  const state = useCampaignOfferRowState(props);

  return (
    <TableRow>
      <TableCell>
        <span className="font-medium">
          {getOfferName(props.campaignOffer, props)}
        </span>
        <span className="ml-2 text-xs text-muted-foreground">
          #{props.campaignOffer.offer_id}
        </span>
      </TableCell>

      <TableCell className="text-right tabular-nums">
        {props.campaignOffer.share}%
      </TableCell>

      <TableCell>
        <Button
          variant="ghost"
          size="icon"
          aria-label="Удалить оффер"
          disabled={state.removal.isPending}
          onClick={() => tryRemoveCampaignOffer(state)}
        >
          <Trash2Icon />
        </Button>
      </TableCell>
    </TableRow>
  );
}

interface CampaignOfferRowProps {
  campaignId: Campaign["id"];
  campaignOffer: StreamOffer;
  offers: Offer[];
}

function useCampaignOfferRowState(props: CampaignOfferRowProps) {
  return {
    campaignId: props.campaignId,
    campaignOffer: props.campaignOffer,
    queryClient: useQueryClient(),
    removal: useMutation({
      mutationFn: (offerId: Offer["id"]) =>
        removeCampaignOffer(props.campaignId, offerId),
    }),
  };
}

function getOfferName(campaignOffer: StreamOffer, deps: GetOfferNameDeps) {
  const offer = deps.offers.find(
    (candidate) => candidate.id === campaignOffer.offer_id,
  );
  return offer?.name ?? "Оффер";
}

interface GetOfferNameDeps {
  offers: Offer[];
}

async function tryRemoveCampaignOffer(deps: TryRemoveCampaignOfferDeps) {
  const toastId = getOfferRemovalToastId(deps.campaignOffer);

  try {
    toast.loading("Удаление оффера…", { id: toastId });

    const campaignOffers = await deps.removal.mutateAsync(
      deps.campaignOffer.offer_id,
    );

    cacheCampaignOffers(campaignOffers, deps);
    toast.success("Оффер удалён", { id: toastId });
  } catch (error) {
    console.error(error);
    toast.error("Не удалось удалить оффер", {
      id: toastId,
      description: describeApiRejection(error),
    });
  }
}

interface TryRemoveCampaignOfferDeps {
  campaignId: Campaign["id"];
  campaignOffer: StreamOffer;
  queryClient: QueryClient;
  removal: UseMutationResult<StreamOffer[], Error, Offer["id"]>;
}

function getOfferRemovalToastId(campaignOffer: StreamOffer) {
  return `offer-removal-${campaignOffer.offer_id}`;
}
