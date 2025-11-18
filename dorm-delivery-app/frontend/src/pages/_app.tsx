"use client";
import type { AppProps } from "next/app";
import Head from "next/head";
import { useEffect } from "react";
import { hydrateToken } from "../utils/auth";
import "../styles/globals.css";

export default function MyApp({ Component, pageProps }: AppProps) {
  useEffect(() => {
    hydrateToken();
  }, []);

  return (
    <>
      <Head>
        <title>Campus Delivery</title>
        <meta name="application-name" content="Campus Delivery" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="Campus Delivery" />
        <meta name="theme-color" content="#ffffff" />
        <link rel="manifest" href="/manifest.json" />
        <link rel="icon" href="/icons/icon-192x192.png" />
        <link rel="apple-touch-icon" href="/icons/icon-512x512.png" />
      </Head>
      <Component {...pageProps} />
    </>
  );
}