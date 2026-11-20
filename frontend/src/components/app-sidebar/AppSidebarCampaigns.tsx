"use client";

import { useQuery } from "@tanstack/react-query";
import { AnimatePresence } from "motion/react";
import { usePathname } from "next/navigation";

import AppSidebarCampaignDeletionButton from "@/components/app-sidebar/AppSidebarCampaignDeletionButton";
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
        <CampaignLink
          key={campaign.id}
          campaign={campaign}
          isOpen={state.pathname === getCampaignHref(campaign)}
        />
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

function CampaignLink(props: CampaignLinkProps) {
  return (
    <AppSidebarLink
      href={getCampaignHref(props.campaign)}
      isActive={props.isOpen}
      action={<AppSidebarCampaignDeletionButton {...props} />}
    >
      <span>{props.campaign.name}</span>
    </AppSidebarLink>
  );
}

interface CampaignLinkProps {
  campaign: Campaign;
  isOpen: boolean;
}

function getCampaignHref(campaign: Campaign) {
  return `/campaigns/${campaign.id}`;
}
