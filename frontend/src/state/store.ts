import { combineReducers, configureStore } from "@reduxjs/toolkit";

import { breakpointReducer } from "@/state/features/breakpoint";

const rootReducer = combineReducers({ breakpoint: breakpointReducer });

export function makeStore() {
  return configureStore({ reducer: rootReducer });
}

export type RootState = ReturnType<typeof rootReducer>;
export type AppStore = ReturnType<typeof makeStore>;
