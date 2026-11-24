# Torvik website

A static site: three pages, one stylesheet, a tiny script, and no third-party code, cookies or analytics
(which is what the privacy policy promises).

```
index.html            Home
privacy/index.html    Privacy policy  → use https://YOUR-DOMAIN/privacy/ in App Store Connect
support/index.html    Support         → use https://YOUR-DOMAIN/support/ in App Store Connect
404.html              "Page not found"
assets/css/style.css  All styles
assets/js/main.js     Phone menu and the "Notify me" form
assets/fonts/         Inter, served from your own site (no Google Fonts requests)
assets/img/           Icon, favicons, app screenshots (WebP + JPG), link preview image
robots.txt, sitemap.xml, favicon.ico, .nojekyll
_src/build.py         Rebuilds the pages from the settings at the top of the file
```

## 1. Fill in your details and rebuild (2 minutes)

Open `_src/build.py` and check the settings at the top:

| Setting | What to put |
|---|---|
| `SITE_URL` | Your domain, e.g. `https://torvik.app` (used for Google and link previews) |
| `APP_STORE_URL` | Your App Store link, once the app is live. Until then the site shows "Coming soon to the App Store". |
| `APP_STORE_ID` | The number from that link. Turns on Safari's "Open in app" banner. |
| `NOTIFY_ENDPOINT` | Optional. The form URL from an email service (Buttondown, ConvertKit, Formspree…). Empty = the form opens a pre-filled email to you. |

The support email is read from an environment variable, so run the build like this from the `website` folder:

```sh
cd website
TORVIK_SUPPORT_EMAIL="your-support-address" python3 _src/build.py
```

Until you run it, the pages show the placeholder `support@example.com`.

## 2. App Store badge

When `APP_STORE_URL` is set, the site shows Apple's official badge from `assets/img/app-store-badge.svg`.
Download it from Apple Marketing Tools (https://tools.applemarketingtools.com), choose the black badge,
save it as `assets/img/app-store-badge.svg`, and rebuild. Apple requires its official artwork; don't redraw it.
The trademark line in the footer is required by Apple when the badge is used, so keep it.

## 3. Put it online (free)

Pick one:

- **GitHub Pages:** push this folder to a repository (or a `docs/` folder), then Settings › Pages › Deploy from branch.
  Add your domain under "Custom domain". `.nojekyll` is already included.
- **Cloudflare Pages:** Create project › Upload assets › drag this folder in. Add your domain under Custom domains.
- **Netlify:** drag this folder onto app.netlify.com/drop, then add your domain.

All three give you free HTTPS. Links are relative, so the site also works on a sub-path while you test.

## 4. After it's live

- Paste the Privacy and Support URLs into App Store Connect (App Information and the version page).
- Paste a link into WhatsApp or iMessage to check the preview card (`assets/img/og-image.png`).
- Add the site in Google Search Console and submit `sitemap.xml`.

## Updating screenshots

The phone screenshots are `assets/img/screen-*.webp` (and `.jpg` fallbacks), 780 × 1688 px.
Replace them with real screenshots from the app when you have them: same names, same size ratio (390 × 844).
