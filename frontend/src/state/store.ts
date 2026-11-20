import { configureStore } from "@reduxjs/toolkit";

import { breakpointReducer } from "@/state/features/breakpoint";

export function createAppStore() {
  return configureStore({ reducer: { breakpoint: breakpointReducer } });
}

export type AppStore = ReturnType<typeof createAppStore>;
export type RootState = ReturnType<AppStore["getState"]>;
