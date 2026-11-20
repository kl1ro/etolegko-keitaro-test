"use client";

import Link from "next/link";
import type { ReactNode } from "react";

import {
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar";

export default function AppSidebarLink(props: AppSidebarLinkProps) {
  const state = useAppSidebarLinkState();

  return (
    <SidebarMenuItem>
      <SidebarMenuButton asChild isActive={props.isActive}>
        <Link
          href={props.href}
          onClick={() => state.sidebar.setOpenMobile(false)}
        >
          {props.children}
        </Link>
      </SidebarMenuButton>

      {props.action}
    </SidebarMenuItem>
  );
}

export interface AppSidebarLinkProps {
  href: string;
  isActive?: boolean;
  action?: ReactNode;
  children: ReactNode;
}

function useAppSidebarLinkState() {
  return {
    sidebar: useSidebar(),
  };
}
