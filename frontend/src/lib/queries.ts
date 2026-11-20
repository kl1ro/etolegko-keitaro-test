import { queryOptions, type QueryClient } from "@tanstack/react-query";

import {
  loadCampaignGroups,
  loadCampaignOffers,
  loadCampaigns,
  loadDomains,
  loadOffers,
  loadTrafficSources,
  type Campaign,
  type StreamOffer,
} from "@/lib/api";

export const CAMPAIGNS_QUERY = queryOptions({
  queryKey: ["campaigns"],
  queryFn: loadCampaigns,
});
export const OFFERS_QUERY = queryOptions({
  queryKey: ["offers"],
  queryFn: loadOffers,
});
export const DOMAINS_QUERY = queryOptions({
  queryKey: ["domains"],
  queryFn: loadDomains,
});
export const CAMPAIGN_GROUPS_QUERY = queryOptions({
  queryKey: ["campaign-groups"],
  queryFn: loadCampaignGroups,
});
export const TRAFFIC_SOURCES_QUERY = queryOptions({
  queryKey: ["traffic-sources"],
  queryFn: loadTrafficSources,
});

export function getCampaignOffersQuery(campaignId: Campaign["id"]) {
  return queryOptions({
    queryKey: ["campaigns", campaignId, "offers"],
    queryFn: () => loadCampaignOffers(campaignId),
  });
}

export function cacheCampaignOffers(
  campaignOffers: StreamOffer[],
  deps: CacheCampaignOffersDeps,
) {
  deps.queryClient.setQueryData(
    getCampaignOffersQuery(deps.campaignId).queryKey,
    campaignOffers,
  );
}

export interface CacheCampaignOffersDeps {
  campaignId: Campaign["id"];
  queryClient: QueryClient;
}
