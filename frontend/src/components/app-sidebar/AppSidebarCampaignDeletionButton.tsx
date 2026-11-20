"use client";

import {
  useMutation,
  useQueryClient,
  type QueryClient,
  type UseMutationResult,
} from "@tanstack/react-query";
import { Trash2Icon } from "lucide-react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

import { SidebarMenuAction } from "@/components/ui/sidebar";
import { deleteCampaign, describeApiRejection, type Campaign } from "@/lib/api";
import { CAMPAIGNS_QUERY } from "@/lib/queries";

export default function AppSidebarCampaignDeletionButton(
  props: AppSidebarCampaignDeletionButtonProps,
) {
  const state = useAppSidebarCampaignDeletionButtonState(props);

  return (
    <SidebarMenuAction
      showOnHover
      aria-label="Удалить кампанию"
      disabled={state.deletion.isPending}
      onClick={() => tryDeleteCampaign(state)}
    >
      <Trash2Icon />
    </SidebarMenuAction>
  );
}

export interface AppSidebarCampaignDeletionButtonProps {
  campaign: Campaign;
  isOpen: boolean;
}

function useAppSidebarCampaignDeletionButtonState(
  props: AppSidebarCampaignDeletionButtonProps,
) {
  return {
    campaign: props.campaign,
    isOpen: props.isOpen,
    router: useRouter(),
    queryClient: useQueryClient(),
    deletion: useMutation({ mutationFn: deleteCampaign }),
  };
}

async function tryDeleteCampaign(deps: TryDeleteCampaignDeps) {
  try {
    await deps.deletion.mutateAsync(deps.campaign.id);
    if (deps.isOpen) deps.router.push("/");
    await refreshCampaigns(deps);
  } catch (error) {
    console.error(error);
    toast.error("Не удалось удалить кампанию", {
      description: describeApiRejection(error),
    });
  }
}

interface TryDeleteCampaignDeps {
  campaign: Campaign;
  isOpen: boolean;
  router: ReturnType<typeof useRouter>;
  queryClient: QueryClient;
  deletion: UseMutationResult<undefined, Error, Campaign["id"]>;
}

async function refreshCampaigns(deps: RefreshCampaignsDeps) {
  await deps.queryClient.invalidateQueries({
    queryKey: CAMPAIGNS_QUERY.queryKey,
  });
}

interface RefreshCampaignsDeps {
  queryClient: QueryClient;
}
