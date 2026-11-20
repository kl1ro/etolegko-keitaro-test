import CampaignCreator from "@/components/CampaignCreator";
import PageTitle from "@/components/PageTitle";

export default function NewCampaignPage() {
  return (
    <div className="flex flex-col gap-6">
      <PageTitle>Новая кампания</PageTitle>
      <CampaignCreator />
    </div>
  );
}
