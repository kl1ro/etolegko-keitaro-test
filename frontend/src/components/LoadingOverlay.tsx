"use client";

import { motion } from "motion/react";

import { Skeleton } from "@/components/ui/skeleton";
import { FADE_OUT_ANIMATION } from "@/lib/animations";

export default function LoadingOverlay() {
  return (
    <motion.div {...FADE_OUT_ANIMATION} className="absolute inset-0">
      <Skeleton className="size-full" />
    </motion.div>
  );
}
