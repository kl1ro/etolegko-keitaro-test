import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

import type { Breakpoint } from "@/lib/breakpoint";

const breakpointSlice = createSlice({
  name: "breakpoint",
  initialState: getInitialBreakpoint,
  reducers: { setBreakpoint: handleBreakpointSet },
  selectors: { selectIsMobile: (breakpoint) => breakpoint === "mobile" },
});

export const breakpointReducer = breakpointSlice.reducer;
export const { setBreakpoint } = breakpointSlice.actions;
export const { selectIsMobile } = breakpointSlice.selectors;

function getInitialBreakpoint(): Breakpoint {
  return "desktop";
}

function handleBreakpointSet(
  _state: Breakpoint,
  action: PayloadAction<Breakpoint>,
) {
  return action.payload;
}
