"use client";

import { PlusIcon } from "lucide-react";
import { usePathname } from "next/navigation";
import { Suspense } from "react";
import { ErrorBoundary } from "react-error-boundary";

import AppSidebarCampaigns from "@/components/app-sidebar/AppSidebarCampaigns";
import AppSidebarLink from "@/components/app-sidebar/AppSidebarLink";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
} from "@/components/ui/sidebar";

export default function AppSidebar() {
  return (
    <Sidebar>
      <SidebarHeader className="h-14 justify-center border-b px-4 font-semibold text-foreground">
        Keitaro
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarMenu>
            <Suspense fallback={<NewCampaignLink />}>
              <ActiveNewCampaignLink />
            </Suspense>
          </SidebarMenu>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel>Кампании</SidebarGroupLabel>

          <ErrorBoundary fallback={<CampaignsLoadError />}>
            <AppSidebarCampaigns />
          </ErrorBoundary>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}

function NewCampaignLink(props: NewCampaignLinkProps) {
  return (
    <AppSidebarLink href={NEW_CAMPAIGN_HREF} isActive={props.isActive}>
      <PlusIcon />
      <span>Новая кампания</span>
    </AppSidebarLink>
  );
}

interface NewCampaignLinkProps {
  isActive?: boolean;
}

const NEW_CAMPAIGN_HREF = "/campaigns/new";

function ActiveNewCampaignLink() {
  const state = useActiveNewCampaignLinkState();
  return <NewCampaignLink isActive={state.isActive} />;
}

function CampaignsLoadError() {
  return (
    <p className="px-2 text-sm text-muted-foreground">
      Не удалось загрузить кампании
    </p>
  );
}

function useActiveNewCampaignLinkState() {
  return {
    isActive: usePathname() === NEW_CAMPAIGN_HREF,
  };
}
