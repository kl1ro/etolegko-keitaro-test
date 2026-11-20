import type { Metadata } from "next";
import { Inter } from "next/font/google";

import AppQueryClientProvider from "@/components/AppQueryClientProvider";
import AppSidebar from "@/components/AppSidebar";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { Toaster } from "@/components/ui/sonner";
import { cn } from "@/lib/utils";
import StoreProvider from "@/state/StoreProvider";
import "./globals.css";

export const metadata: Metadata = {
  title: "Кампании Keitaro",
  description: "Создание и редактирование кампаний Keitaro",
};

export default function RootLayout(props: LayoutProps<"/">) {
  return (
    <html lang="ru" className={cn("dark font-sans", INTER_FONT.variable)}>
      <body>
        <StoreProvider>
          <AppQueryClientProvider>
            <SidebarProvider>
              <AppSidebar />

              <SidebarInset className="min-w-0">
                <header className="sticky top-0 z-10 flex h-14 shrink-0 items-center border-b bg-background px-4">
                  <SidebarTrigger className="cursor-pointer" />
                </header>

                <div className="flex flex-1 flex-col p-4 md:p-8">
                  {props.children}
                </div>
              </SidebarInset>
            </SidebarProvider>
          </AppQueryClientProvider>
        </StoreProvider>

        <Toaster theme="dark" />
      </body>
    </html>
  );
}

const INTER_FONT = Inter({
  subsets: ["latin", "cyrillic"],
  variable: "--font-sans",
});
