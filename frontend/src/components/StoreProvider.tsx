"use client";

import { useEffect, useState, type ReactNode } from "react";
import { Provider } from "react-redux";

import { getCurrentBreakpoint, getMobileMediaQuery } from "@/lib/breakpoint";
import { setBreakpoint } from "@/state/features/breakpoint";
import { createAppStore, type AppStore } from "@/state/store";

export default function StoreProvider(props: StoreProviderProps) {
  const state = useStoreProviderState();
  useStoreProviderEffects(state);
  return <Provider store={state.store}>{props.children}</Provider>;
}

export interface StoreProviderProps {
  children: ReactNode;
}

function useStoreProviderState() {
  return {
    store: usePerProviderStore(),
  };
}

function useStoreProviderEffects(deps: UseStoreProviderEffectsDeps) {
  useBreakpointTrackingEffect(deps);
}

interface UseStoreProviderEffectsDeps {
  store: AppStore;
}

function usePerProviderStore() {
  const [store] = useState(createAppStore);
  return store;
}

function useBreakpointTrackingEffect(deps: UseBreakpointTrackingEffectDeps) {
  useEffect(() => {
    const mobileMediaQuery = getMobileMediaQuery();
    const change = () => updateBreakpoint(deps);
    updateBreakpoint(deps);
    mobileMediaQuery.addEventListener("change", change);
    return () => mobileMediaQuery.removeEventListener("change", change);
  }, []);
}

interface UseBreakpointTrackingEffectDeps {
  store: AppStore;
}

function updateBreakpoint(deps: UpdateBreakpointDeps) {
  deps.store.dispatch(setBreakpoint(getCurrentBreakpoint()));
}

interface UpdateBreakpointDeps {
  store: AppStore;
}
