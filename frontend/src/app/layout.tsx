import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";
import { LayoutDashboard, MessageSquare, Upload, Activity } from "lucide-react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "RAGScope - Production RAG Platform",
  description: "Enterprise RAG system with telemetry and observability",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} min-h-screen bg-neutral-950 text-neutral-50 flex`}>
        {/* Sidebar */}
        <div className="w-64 border-r border-neutral-800 bg-neutral-900 flex flex-col hidden md:flex">
          <div className="p-6 border-b border-neutral-800">
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
              RAGScope
            </h1>
            <p className="text-xs text-neutral-400 mt-1">Enterprise AI Platform</p>
          </div>
          <nav className="flex-1 p-4 space-y-2">
            <Link href="/" className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-neutral-800 transition-colors text-neutral-300 hover:text-white">
              <Activity className="w-4 h-4" />
              <span>Overview</span>
            </Link>
            <Link href="/chat" className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-neutral-800 transition-colors text-neutral-300 hover:text-white">
              <MessageSquare className="w-4 h-4" />
              <span>RAG Chat</span>
            </Link>
            <Link href="/ingest" className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-neutral-800 transition-colors text-neutral-300 hover:text-white">
              <Upload className="w-4 h-4" />
              <span>Data Ingestion</span>
            </Link>
            <Link href="/dashboard" className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-neutral-800 transition-colors text-neutral-300 hover:text-white">
              <LayoutDashboard className="w-4 h-4" />
              <span>Telemetry Dashboard</span>
            </Link>
          </nav>
          <div className="p-4 border-t border-neutral-800 text-xs text-neutral-500 text-center">
            v1.0.0 Production
          </div>
        </div>
        
        {/* Main Content */}
        <main className="flex-1 flex flex-col h-screen overflow-hidden">
          {children}
        </main>
      </body>
    </html>
  );
}
