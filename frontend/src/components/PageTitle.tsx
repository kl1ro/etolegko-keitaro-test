import type { ReactNode } from "react";

export default function PageTitle(props: PageTitleProps) {
  return <h1 className="text-2xl font-semibold tracking-tight md:text-3xl">{props.children}</h1>;
}

export interface PageTitleProps {
  children: ReactNode;
}
