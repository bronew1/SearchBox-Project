import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const accessToken = request.cookies.get("accessToken")?.value;

  // Login yapılmamışsa ve kullanıcı dashboard sayfasına gidiyorsa → login'e yönlendir
  if (!accessToken && request.nextUrl.pathname.startsWith("/")) {
    if (
      request.nextUrl.pathname.startsWith("/dashboard") ||
      request.nextUrl.pathname.startsWith("/aboneler") ||
      request.nextUrl.pathname.startsWith("/sepete-eklemeler") ||
      request.nextUrl.pathname.startsWith("/reklamlar") ||
      request.nextUrl.pathname.startsWith("/anlik-kullanici") ||
      request.nextUrl.pathname.startsWith("/widgets") ||
      request.nextUrl.pathname.startsWith("/welcome-template") ||
      request.nextUrl.pathname.startsWith("/campaigns")
    ) {
      return NextResponse.redirect(new URL("/login", request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/dashboard/:path*",
    "/aboneler/:path*",
    "/sepete-eklemeler/:path*",
    "/reklamlar/:path*",
    "/anlik-kullanici/:path*",
    "/widgets/:path*",
    "/welcome-template/:path*",
    "/campaigns/:path*",
  ],
};
