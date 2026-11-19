"use client";

import { QueryCache, QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState, type ReactNode } from "react";

export default function AppQueryClientProvider(props: AppQueryClientProviderProps) {
  const state = useAppQueryClientProviderState();
  return <QueryClientProvider client={state.queryClient}>{props.children}</QueryClientProvider>;
}

export interface AppQueryClientProviderProps {
  children: ReactNode;
}

function useAppQueryClientProviderState() {
  const [queryClient] = useState(createQueryClient);
  return { queryClient };
}

function createQueryClient() {
  return new QueryClient({ queryCache: new QueryCache({ onError: reportQueryError }) });
}

function reportQueryError(error: unknown) {
  console.error(error);
}
