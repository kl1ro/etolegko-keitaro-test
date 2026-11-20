"use client";

import { ListIcon, PlusIcon, type LucideIcon } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Suspense } from "react";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar";

export default function AppSidebar() {
  return (
    <Sidebar>
      <SidebarHeader className="h-14 justify-center border-b px-4 font-semibold text-foreground">
        Keitaro
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <Suspense fallback={<AppSidebarMenu />}>
            <ActiveAppSidebarMenu />
          </Suspense>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}

function AppSidebarMenu(props: AppSidebarMenuProps) {
  const state = useAppSidebarMenuState();

  return (
    <SidebarMenu>
      {APP_SIDEBAR_LINKS_FROM_SHALLOWEST.map((link) => (
        <SidebarMenuItem key={link.href}>
          <SidebarMenuButton asChild isActive={link === props.activeLink}>
            <Link
              href={link.href}
              onClick={() => state.sidebar.setOpenMobile(false)}
            >
              <link.icon />
              <span>{link.label}</span>
            </Link>
          </SidebarMenuButton>
        </SidebarMenuItem>
      ))}
    </SidebarMenu>
  );
}

interface AppSidebarMenuProps {
  activeLink?: AppSidebarLink;
}

function ActiveAppSidebarMenu() {
  const state = useActiveAppSidebarMenuState();
  return <AppSidebarMenu activeLink={state.activeLink} />;
}

function useAppSidebarMenuState() {
  return {
    sidebar: useSidebar(),
  };
}

function useActiveAppSidebarMenuState() {
  return {
    activeLink: findActiveAppSidebarLink(usePathname()),
  };
}

function findActiveAppSidebarLink(
  pathname: string,
): AppSidebarLink | undefined {
  return APP_SIDEBAR_LINKS_FROM_SHALLOWEST.findLast((link) =>
    isPathInsideLink(pathname, link),
  );
}

function isPathInsideLink(pathname: string, link: AppSidebarLink) {
  return pathname === link.href || pathname.startsWith(`${link.href}/`);
}

interface AppSidebarLink {
  href: string;
  label: string;
  icon: LucideIcon;
}

const APP_SIDEBAR_LINKS_FROM_SHALLOWEST: AppSidebarLink[] = [
  { href: "/campaigns", label: "Кампании", icon: ListIcon },
  { href: "/campaigns/new", label: "Новая кампания", icon: PlusIcon },
];
