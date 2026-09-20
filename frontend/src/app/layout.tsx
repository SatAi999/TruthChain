import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata = {
  title: "TRUTHCHAIN — Evidence Intelligence Workstation",
  description: "Don't just answer a claim. Investigate it. Enterprise agentic evidence investigation system.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans antialiased">
        <Navbar />
        <main className="flex-1 flex flex-col">{children}</main>
      </body>
    </html>
  );
}
