import { Suspense } from "react";

import CampaignEditor from "@/components/CampaignEditor";

export default function CampaignPage(props: PageProps<"/campaigns/[id]">) {
  return (
    <Suspense>
      {props.params.then((params) => (
        <CampaignEditor campaignId={Number(params.id)} />
      ))}
    </Suspense>
  );
}
