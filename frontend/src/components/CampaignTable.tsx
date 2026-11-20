"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";

import QueryError from "@/components/QueryError";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { CAMPAIGNS_QUERY } from "@/lib/queries";

export default function CampaignTable() {
  const state = useCampaignTableState();
  if (state.campaigns.isPending) return <Skeleton className="h-40 w-full" />;
  if (state.campaigns.isError)
    return (
      <QueryError
        message="Не удалось загрузить кампании"
        error={state.campaigns.error}
      />
    );
  if (!state.campaigns.data.length)
    return <p className="text-sm text-muted-foreground">Кампаний пока нет</p>;

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-24">ID</TableHead>
            <TableHead>Название</TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          {state.campaigns.data.map((campaign) => (
            <TableRow key={campaign.id}>
              <TableCell className="text-muted-foreground">
                {campaign.id}
              </TableCell>

              <TableCell>
                <Link
                  href={`/campaigns/${campaign.id}`}
                  className="font-medium hover:underline"
                >
                  {campaign.name}
                </Link>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

function useCampaignTableState() {
  return {
    campaigns: useQuery(CAMPAIGNS_QUERY),
  };
}
