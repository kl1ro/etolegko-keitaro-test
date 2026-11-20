import CampaignTable from "@/components/CampaignTable";
import PageTitle from "@/components/PageTitle";

export default function CampaignsPage() {
  return (
    <div className="flex flex-col gap-6">
      <PageTitle>Кампании</PageTitle>
      <CampaignTable />
    </div>
  );
}
