import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "DemoBoard",
  description: "Next.js와 shadcn/ui로 만든 게시판 데모 사이트",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="ko"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-background">
        <header className="border-b">
          <div className="mx-auto flex w-full max-w-4xl items-center justify-between px-4 py-4">
            <Link href="/" className="text-xl font-bold tracking-tight">
              DemoBoard
            </Link>
            <nav className="flex items-center gap-4 text-sm text-muted-foreground">
              <Link href="/" className="hover:text-foreground">
                게시판
              </Link>
              <Link href="/write" className="hover:text-foreground">
                글쓰기
              </Link>
            </nav>
          </div>
        </header>
        <main className="mx-auto w-full max-w-4xl flex-1 px-4 py-8">
          {children}
        </main>
        <footer className="border-t py-6 text-center text-xs text-muted-foreground">
          DemoBoard &middot; Next.js + TypeScript + shadcn/ui
        </footer>
      </body>
    </html>
  );
}
