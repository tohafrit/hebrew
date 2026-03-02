import { Outlet } from "react-router-dom";
import { Navbar } from "./navbar";
import { Toaster } from "@/components/ui/toaster";

export function RootLayout() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1 w-full max-w-6xl mx-auto px-4 py-6">
        <Outlet />
      </main>
      <Toaster />
    </div>
  );
}
