"use client";

import { useQuery } from "@tanstack/react-query";
import { AnimatePresence } from "motion/react";
import { usePathname } from "next/navigation";

import AppSidebarLink from "@/components/app-sidebar/AppSidebarLink";
import LoadingOverlay from "@/components/LoadingOverlay";
import { SidebarMenu } from "@/components/ui/sidebar";
import type { Campaign } from "@/lib/api";
import { CAMPAIGNS_QUERY } from "@/lib/queries";
import { cn } from "@/lib/utils";

export default function AppSidebarCampaigns() {
  const state = useAppSidebarCampaignsState();

  return (
    <div className={cn("relative", state.campaigns.isPending && "min-h-24")}>
      {state.campaigns.isSuccess && (
        <CampaignList campaigns={state.campaigns.data} />
      )}

      <AnimatePresence>
        {state.campaigns.isPending && <LoadingOverlay key="loading" />}
      </AnimatePresence>
    </div>
  );
}

function useAppSidebarCampaignsState() {
  return {
    campaigns: useQuery({ ...CAMPAIGNS_QUERY, throwOnError: true }),
  };
}

function CampaignList(props: CampaignListProps) {
  const state = useCampaignListState();

  if (!props.campaigns.length)
    return (
      <p className="px-2 text-sm text-muted-foreground">Кампаний пока нет</p>
    );

  return (
    <SidebarMenu>
      {props.campaigns.map((campaign) => (
        <AppSidebarLink
          key={campaign.id}
          href={getCampaignHref(campaign)}
          isActive={state.pathname === getCampaignHref(campaign)}
        >
          <span>{campaign.name}</span>
        </AppSidebarLink>
      ))}
    </SidebarMenu>
  );
}

interface CampaignListProps {
  campaigns: Campaign[];
}

function useCampaignListState() {
  return {
    pathname: usePathname(),
  };
}

function getCampaignHref(campaign: Campaign) {
  return `/campaigns/${campaign.id}`;
}
