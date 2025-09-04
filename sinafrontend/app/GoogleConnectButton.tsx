"use client";
import { useEffect } from "react";

export default function GoogleConnectButton() {
  const handleConnect = () => {
    const clientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID!;
    const redirectUri = "http://localhost:3000/api/auth/callback";
    const scope = "https://www.googleapis.com/auth/adwords";
    const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=${scope}&access_type=offline&prompt=consent`;
    window.location.href = authUrl;
  };

  return (
    <button
      onClick={handleConnect}
      className="px-4 py-2 bg-blue-600 text-white rounded-lg"
    >
      Google ile Bağlan
    </button>
  );
}
