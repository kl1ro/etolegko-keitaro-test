import { describeApiRejection } from "@/lib/api";

export default function QueryError(props: QueryErrorProps) {
  return (
    <div className="rounded-md border border-destructive/50 p-4 text-sm">
      <p className="font-medium text-destructive">{props.message}</p>
      <p className="text-muted-foreground">
        {describeApiRejection(props.error)}
      </p>
    </div>
  );
}

export interface QueryErrorProps {
  message: string;
  error: unknown;
}
