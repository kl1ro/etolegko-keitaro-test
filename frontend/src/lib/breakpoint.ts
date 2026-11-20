export type Breakpoint = "mobile" | "desktop";

export function getCurrentBreakpoint(): Breakpoint {
  return getMobileMediaQuery().matches ? "mobile" : "desktop";
}

export function getMobileMediaQuery() {
  return window.matchMedia(MOBILE_MEDIA_QUERY);
}

const MOBILE_MAX_WIDTH = 767;
const MOBILE_MEDIA_QUERY = `(max-width: ${MOBILE_MAX_WIDTH}px)`;
