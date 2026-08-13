import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata={title:"HME Motors — Seu próximo carro está aqui",description:"Carros seminovos revisados, com procedência e condições que cabem no seu momento."};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="pt-BR"><body>{children}</body></html>}
