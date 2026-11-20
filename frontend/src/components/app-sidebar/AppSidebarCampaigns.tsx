"use client";

import { useSuspenseQuery } from "@tanstack/react-query";
import { usePathname } from "next/navigation";

import AppSidebarLink from "@/components/app-sidebar/AppSidebarLink";
import { SidebarMenu } from "@/components/ui/sidebar";
import type { Campaign } from "@/lib/api";
import { CAMPAIGNS_QUERY } from "@/lib/queries";

export default function AppSidebarCampaigns() {
  const state = useAppSidebarCampaignsState();

  if (!state.campaigns.data.length)
    return (
      <p className="px-2 text-sm text-muted-foreground">Кампаний пока нет</p>
    );

  return (
    <SidebarMenu>
      {state.campaigns.data.map((campaign) => (
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

function useAppSidebarCampaignsState() {
  return {
    campaigns: useSuspenseQuery(CAMPAIGNS_QUERY),
    pathname: usePathname(),
  };
}

function getCampaignHref(campaign: Campaign) {
  return `/campaigns/${campaign.id}`;
}
