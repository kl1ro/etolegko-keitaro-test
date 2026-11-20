import type { MotionProps } from "motion/react";

export const FADE_OUT_ANIMATION = {
  exit: { opacity: 0 },
  transition: { duration: 0.3, ease: [0.16, 1, 0.3, 1] },
} satisfies MotionProps;
