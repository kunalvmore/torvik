#!/usr/bin/env python3
"""Builds the Torvik website: index.html, privacy/, support/ and 404.html.

Run from the website folder, with your support email in an environment variable:

    TORVIK_SUPPORT_EMAIL="you@yourdomain.com" python3 _src/build.py

Edit the settings below for the domain, App Store link and email form.
The pages are plain HTML; you can also edit them directly, but they are overwritten when you rebuild.
"""
import json
import os

# ---------------------------------------------------------------- settings
SITE_URL = "https://torvik.app"          # your domain, no trailing slash (used for share previews and Google)
APP_STORE_URL = ""                       # e.g. "https://apps.apple.com/app/id1234567890" once the app is live
APP_STORE_ID = ""                        # e.g. "1234567890" (turns on Safari's Smart App Banner)
EMAIL = os.environ.get("TORVIK_SUPPORT_EMAIL", "support@example.com")
NOTIFY_ENDPOINT = ""                     # form URL from an email service (Buttondown, ConvertKit, Formspree…). Empty = opens an email instead.
UPDATED = "24 November 2026"
# -------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITLE = "Torvik: Gym & Home Workout with 3D Form Check"
DESC = ("Get stronger, rep by rep. Torvik is a free iPhone workout app with a 3D coach for every move, "
        "camera form check that counts your reps, and plans for the gym or home.")


def store_badge(p):
    if APP_STORE_URL:
        return (f'<a class="store-badge" href="{APP_STORE_URL}" aria-label="Download Torvik on the App Store">'
                f'<img src="{p}assets/img/app-store-badge.svg" alt="Download on the App Store" width="156" height="52"></a>')
    return ('<span class="store-badge pending" role="note"><span><small>iPhone · iOS 17 or later</small>'
            'Coming soon to the App Store</span></span>')


def head(p, title, desc, path):
    banner = f'<meta name="apple-itunes-app" content="app-id={APP_STORE_ID}">\n' if APP_STORE_ID else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE_URL}{path}">
<meta name="theme-color" content="#0C0F14">
{banner}<link rel="icon" href="{p}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{p}assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="{p}assets/img/apple-touch-icon.png">
<link rel="preload" href="{p}assets/fonts/inter-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<script>document.documentElement.classList.add("js")</script>
<link rel="stylesheet" href="{p}assets/css/style.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Torvik">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE_URL}{path}">
<meta property="og:image" content="{SITE_URL}/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>'''


def header(p, active=""):
    def link(href, label):
        cur = ' aria-current="page"' if label == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    get = APP_STORE_URL or f"{p}#get"
    return f'''
<header class="site-header">
<div class="progress-bar" aria-hidden="true"></div>
<div class="wrap">
<a class="brand" href="{p or './'}"><img src="{p}assets/img/icon-256.webp" alt="" width="34" height="34">Torvik</a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
<nav class="nav" id="nav" aria-label="Main">
{link(f"{p}#features", "Features")}
{link(f"{p}privacy/", "Privacy")}
{link(f"{p}support/", "Support")}
<a class="btn btn-grad" href="{get}">Get the app</a>
</nav>
</div>
</header>
<hr class="gline">'''


def mail(subject=""):
    q = f"?subject={subject}" if subject else ""
    return f"mailto:{EMAIL}{q}"


def footer(p):
    return f'''
<hr class="gline">
<footer class="site-footer">
<div class="wrap">
<div class="foot-left">
<a class="brand" href="{p or './'}"><img src="{p}assets/img/icon-256.webp" alt="" width="26" height="26">Torvik</a>
<span>© 2026 Torvik. All rights reserved. Built rep by rep.</span>
<span class="legal">Torvik and the Torvik icon are trademarks of Torvik. Apple, the Apple logo and iPhone are trademarks of Apple Inc., registered in the U.S. and other countries.</span>
</div>
<nav class="foot-links" aria-label="Footer">
<a href="{p}privacy/">Privacy</a>
<a href="{p}support/">Support</a>
<a href="{mail()}">{EMAIL}</a>
</nav>
</div>
</footer>
<script src="{p}assets/js/main.js" defer></script>
</body>
</html>
'''


def phone(p, key, alt, eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'''<div class="phone"><div class="screen"><span class="island" aria-hidden="true"></span>
<picture><source type="image/webp" srcset="{p}assets/img/screen-{key}.webp"><img src="{p}assets/img/screen-{key}.jpg" alt="{alt}" width="390" height="844" {load} decoding="async"></picture>
</div></div>'''


def glow(color, opacity, style):
    return f'<div class="glow" aria-hidden="true" style="{style};background:radial-gradient(circle,rgba({color},{opacity}),rgba({color},0) 65%)"></div>'


BLUE, GREEN = "127,178,254", "53,240,122"


def feature(p, fid, eyebrow, title, body, ticks, key, alt, flip=False, green=False):
    tick_items = "".join(f"<li>{t}</li>" for t in ticks)
    col = GREEN if green else BLUE
    return f'''
<section class="feature{" flip" if flip else ""}" id="{fid}" aria-labelledby="{fid}-title">
<div class="wrap">
<div class="feature-copy reveal">
<div class="eyebrow{" g" if green else ""}">{eyebrow}</div>
<h2 id="{fid}-title">{title}</h2>
<p>{body}</p>
<ul class="ticks">{tick_items}</ul>
</div>
<div class="phone-wrap reveal {"from-left" if flip else "from-right"}" style="--d:.12s">{glow(col, .28, "left:50%;top:50%;width:460px;height:460px;margin:-230px 0 0 -230px")}<div class="parallax">{phone(p, key, alt)}</div></div>
</div>
</section>'''


def home():
    p = ""
    ld = {
        "@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Torvik",
        "alternateName": "Torvik: Gym & Home Workout", "operatingSystem": "iOS 17.0 or later",
        "applicationCategory": "HealthApplication", "description": DESC,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "url": SITE_URL + "/", "image": SITE_URL + "/assets/img/icon-512.png",
    }
    if APP_STORE_URL:
        ld["downloadUrl"] = APP_STORE_URL
    tile = lambda c, path: f'<span class="tile" style="background:rgba({c},.14);color:rgb({c})"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg></span>'
    trust = [
        (GREEN, '<path d="M12 2l3 7h7l-5.5 4 2 7L12 16l-6.5 4 2-7L2 9h7z"/>', "Free, no account", "Download and start. No sign-up, no email, no ads."),
        (BLUE, '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>', "Private by design", "The camera runs on your iPhone. Your workouts live on your iPhone and, if you choose, your own iCloud."),
        ("94,230,200", '<path d="M12 15V3M7 8l5-5 5 5"/><path d="M5 13v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/>', "Your data, your call", "Export every set as a spreadsheet file, or delete your history at any time from Settings."),
    ]
    trust_html = "".join(f'<div class="gcard reveal" style="--d:{i * 0.1:.1f}s"><div class="inner">{tile(c, path)}<h3>{t}</h3><p>{d}</p></div></div>' for i, (c, path, t, d) in enumerate(trust))
    body = f'''
<main id="main">
<section class="hero" aria-labelledby="hero-title">
{glow(BLUE, .30, "right:-10%;top:-10%;width:760px;height:760px")}
<div class="wrap">
<div class="hero-copy">
<div class="pill-row"><span class="pill">FREE ON IPHONE</span><span class="muted" style="font-size:13px">iOS 17 or later</span></div>
<h1 id="hero-title">Get stronger, <span class="grad">rep by rep.</span></h1>
<p class="lede">Your 3D coach shows every move, your camera checks every rep, and your plan tells you what to do next. At the gym or at home, every workout moves you forward.</p>
<div class="cta-row" id="get">{store_badge(p)}<a class="btn btn-ghost" href="#features">See how it works</a></div>
<ul class="checks"><li>Free</li><li>No sign-up</li><li>Your data stays in your iCloud</li></ul>
</div>
<div class="hero-visual">
{glow(GREEN, .22, "left:50%;bottom:-60px;width:460px;height:220px;margin-left:-230px")}
<div class="hero-stage">
<div class="tilt">{phone(p, "today", "The Torvik Today screen: weekly goal and streak, the next workout from your plan with a 3D preview, and a Start workout button", eager=True)}</div>
<span class="float-chip chip-a"><span class="dot"></span>Your plan picks today’s workout</span>
<span class="float-chip chip-b"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7FB2FE" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 8V6a2 2 0 0 1 2-2h2M16 4h2a2 2 0 0 1 2 2v2M20 16v2a2 2 0 0 1-2 2h-2M8 20H6a2 2 0 0 1-2-2v-2"/><circle cx="12" cy="12" r="3"/></svg>Your camera counts reps</span>
</div>
</div>
</div>
</section>
<div id="features">
{feature(p, "coach", "3D coach", "Watch every move before you try it",
         "All 20 exercises have a 3D coach that shows the full movement, slows down the hard part and lights up the muscles that are working.",
         ["A timeline of every phase of the rep, with a cue for each", "Switch camera angles and slow it down to half speed", "Muscles worked and the mistakes to avoid"],
         "exercise", "The exercise screen: a 3D coach doing a push-up, camera angle buttons, the rep timeline and a Start button")}
{feature(p, "form-check", "Camera form check", "Your camera counts reps and checks your form",
         "Prop your iPhone up and train. On 15 exercises the front camera counts your reps, scores your form and shows the one thing to fix.",
         ["Video is analysed on your iPhone and never saved or uploaded", "Tap − or + if it misses a rep", "The 3D demo is one tap away"],
         "form-check", "The form check screen during a lateral raise: one arm raised above shoulder height is marked to fix, with the cue Stop at shoulder height, 7 of 10 reps counted and a form score of 86",
         flip=True, green=True)}
{feature(p, "plans", "Plans", "Know exactly what to do today",
         "Pick a goal and the equipment you have. Follow a ready-made plan, or build your own workout. Torvik guides every set with a rest timer and voice cues.",
         ["Four plans: First Steps, Dumbbell Strength, Bodyweight Basics, Core &amp; Posture", "See which day is next and how far you’ve come", "Build your own workouts in seconds"],
         "plans", "The Plans screen: First Steps at 7 of 12 workouts, with Day B up next")}
{feature(p, "progress", "Progress", "Watch yourself get stronger",
         "Every set is logged for you. See your weekly goal fill up, your streak grow and which muscles still need their turn.",
         ["Weekly goal, time trained and streak", "Sets per muscle group, so nothing gets skipped", "Personal records and strength over time"],
         "progress", "The Progress screen: 2 of 3 workouts this week, time trained, sets done, streak and sets per muscle group",
         flip=True, green=True)}
</div>
<section class="trust" aria-label="Why Torvik">
<div class="wrap"><div class="trust-grid">{trust_html}</div></div>
</section>
<section class="notify" aria-labelledby="notify-title">
<div class="wrap"><div class="gcard reveal"><div class="inner">
<div style="max-width:560px"><div class="eyebrow g">Coming next</div><h2 id="notify-title">More 3D exercises are on the way</h2>
<p>Get one email when the next version is out. Nothing else.</p></div>
<div>
<form class="notify-form" action="{NOTIFY_ENDPOINT or mail()}" method="post" data-endpoint="{NOTIFY_ENDPOINT}" data-mailto="{mail("Notify%20me%20about%20Torvik")}">
<label class="sr-only" for="email">Email address</label>
<input id="email" name="email" type="email" autocomplete="email" placeholder="you@example.com" required>
<button class="btn btn-green" type="submit">Notify me</button>
</form>
<p class="form-note" role="status" aria-live="polite"></p>
</div>
</div></div></div>
</section>
<section class="final" aria-labelledby="final-title">
{glow(BLUE, .28, "left:50%;top:0;width:560px;height:320px;margin-left:-280px")}
{glow(GREEN, .2, "left:50%;bottom:-140px;width:760px;height:300px;margin-left:-380px")}
<div class="wrap">
<img class="app-icon reveal" src="assets/img/icon-256.webp" alt="Torvik app icon" width="120" height="120" loading="lazy">
<h2 id="final-title" class="reveal" style="--d:.1s">Built <span class="grad">rep by rep.</span></h2>
<p class="muted" style="margin:0;font-size:17px">Torvik: Gym &amp; Home Workout. Free on iPhone.</p>
{store_badge(p)}
</div>
</section>
</main>
<script type="application/ld+json">{json.dumps(ld)}</script>'''
    return head(p, TITLE, DESC, "/") + header(p) + body + footer(p)


def doc_page(p, active, path, title, eyebrow, h1, intro, content):
    return head(p, title, intro, path) + header(p, active) + f'''
<main id="main">
<section class="doc-hero" aria-labelledby="page-title">
{glow(BLUE, .22, "right:-120px;top:-160px;width:620px;height:420px")}
{glow(GREEN, .12, "left:-160px;top:40px;width:420px;height:320px")}
<div class="wrap"><div class="doc-col">
<div class="eyebrow">{eyebrow}</div>
<h1 id="page-title">{h1}</h1>
<p class="intro">{intro}</p>
{content}
</div></div>
</section>
</main>''' + footer(p)


def privacy():
    p = "../"
    short = "".join(f"<li>{t}</li>" for t in [
        "No account, no sign-up and no ads.",
        "No analytics or tracking. We don’t collect any data from you.",
        "The camera is used only on your iPhone. Video is never saved or uploaded.",
        "Your workouts are stored on your iPhone and, if you turn on iCloud sync, in your own iCloud account.",
        "You can export or delete your workout data at any time."])
    contact = f'<a href="{mail()}">{EMAIL}</a>'
    content = f'''
<div class="gcard summary reveal"><div class="inner"><h2>The short version</h2><ul class="ticks">{short}</ul></div></div>
<div class="prose">
<h2>Who we are</h2><p>Torvik is an iPhone app for strength training. In this policy “we” means Torvik. You can reach us at {contact}.</p>
<h2>What Torvik stores</h2><p>Torvik stores the information you create in the app: your workouts and sets (exercise, weight, reps, hold times and form scores), workouts you build, your progress in a plan, and your settings such as units, weekly goal and reminder times. This information is stored on your iPhone.</p>
<h2>The camera</h2><p>Camera form check uses the front camera to count your reps and check your form. The video is analysed on your iPhone as you train. It is never recorded, saved or sent anywhere. Only the result, such as the rep count and form score, is kept with your workout. You can turn off camera access at any time in the iPhone Settings app.</p>
<h2>iCloud sync</h2><p>If you turn on iCloud sync in Torvik’s Settings, your workout data is stored in your private iCloud account using Apple’s CloudKit, so it can sync across your devices. We can’t see or access this data. Apple’s privacy policy covers how iCloud stores it. You can turn iCloud sync off at any time.</p>
<h2>Notifications</h2><p>If you turn on workout reminders, Torvik schedules them on your iPhone. They are not sent from a server and we don’t receive any information about them.</p>
<h2>What we don’t do</h2><ul><li>We don’t collect, sell or share personal information.</li><li>We don’t use analytics, advertising or tracking tools.</li><li>We don’t ask for your name, email address, location or health data.</li></ul>
<h2>This website</h2><p>This website has no cookies, analytics or tracking, and its fonts are served from this site. If you use the “Notify me” form, your email address is used only to tell you when a new version is out.</p>
<h2>Exporting and deleting your data</h2><p>In Settings, “Export workouts” creates a spreadsheet file (CSV) of your sets that you can save or share where you choose. “Delete workout data” removes your history, workouts, plan progress and preferences from your iPhone, and optionally from iCloud. Deleting the app also removes the data stored on your iPhone.</p>
<h2>Children</h2><p>Torvik is a general fitness app and is not directed at children under 13. Because we don’t collect any personal information, we don’t knowingly collect information from children.</p>
<h2>Changes to this policy</h2><p>If this policy changes, for example when a future version adds subscriptions, we will update this page and the date at the top before the change takes effect.</p>
<h2>Contact</h2><p>Questions about privacy? Email {contact}.</p>
</div>'''
    return doc_page(p, "Privacy", "/privacy/", "Privacy policy · Torvik", "Privacy policy",
                    'Your training. Your data. <span class="grad">Nobody else’s.</span>',
                    f"Last updated {UPDATED}. Torvik has no accounts, no ads and no tracking. Here’s exactly what the app stores, and what it never does.",
                    content)


def support():
    p = "../"
    faqs = [
        ("How does camera form check work?", "Open an exercise with the camera mark and tap Form check. Prop your iPhone up so your whole body is in view, about 2 metres away. The camera counts reps, scores your form and shows the one thing to fix. If it misses a rep, tap − or +."),
        ("Which exercises have form check?", "15 of the 20 exercises: goblet squat, reverse lunge, split squat, Romanian deadlift, glute bridge, push-up, incline push-up, dumbbell bench press, shoulder press, lateral raise, triceps kickback, single-arm row, bent-over row, biceps curl and plank. They have a camera mark in the Exercises tab."),
        ("Is my camera video saved or uploaded?", f'No. The video is analysed on your iPhone while you train and is never recorded or sent anywhere. Read the <a href="{p}privacy/">privacy policy</a> for details.'),
        ("How do I sync between my devices or move to a new iPhone?", "Turn on iCloud sync in Settings › Your data on each device, signed in with the same Apple Account. Your workouts and plan progress sync through your private iCloud."),
        ("How do I export my workouts?", "Go to Settings › Export workouts, choose the date range and whether to include form scores, then save the CSV file to Files or share it. It opens in Numbers, Excel or Google Sheets."),
        ("How do I start over?", "Go to Settings › Delete workout data. You can save a copy first, and choose whether to also delete from iCloud. This can’t be undone."),
        ("My workout reminders don’t show up.", "Check that reminders are on in Torvik’s Settings, and that notifications are allowed for Torvik in the iPhone Settings app under Notifications."),
        ("Does Torvik cost anything?", "No. Torvik is free, with every feature included. There are no ads and no account."),
    ]
    items = "".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(faqs))
    content = f'''
<div class="card faq reveal">{items}</div>
<div class="help-grid reveal" style="--d:.1s">
<div class="card"><h2>Still need help?</h2><p>Email us and we’ll get back to you. It helps to include your iPhone model and iOS version.</p>
<a class="btn btn-light" href="{mail("Torvik%20support")}">{EMAIL}</a></div>
<div class="card"><h2>Requirements</h2><ul class="ticks"><li>iPhone with iOS 17 or later</li><li>Front camera for form check</li><li>iCloud account for sync (optional)</li></ul></div>
</div>'''
    return doc_page(p, "Support", "/support/", "Support · Torvik", "Support",
                    'Stuck on something? <span class="grad">We’ve got your back.</span>',
                    "Quick answers about form check, syncing and your data, so you can get back to training.",
                    content)


def not_found():
    p = "/"
    return head(p, "Page not found · Torvik", DESC, "/404.html") + header(p) + '''
<main id="main" class="not-found"><div class="wrap">
<div class="eyebrow">404</div>
<h1>That page skipped <span class="grad">leg day.</span></h1>
<p class="muted" style="margin:0;font-size:18px">We couldn’t find what you were looking for.</p>
<a class="btn btn-light" href="/">Back to Torvik</a>
</div></main>''' + footer(p)


def write(rel, html):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    write("index.html", home())
    write("privacy/index.html", privacy())
    write("support/index.html", support())
    write("404.html", not_found())
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE_URL}{u}</loc></url>" for u in ("/", "/privacy/", "/support/"))
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    note = "" if "TORVIK_SUPPORT_EMAIL" in os.environ else "  (support email is a placeholder: set TORVIK_SUPPORT_EMAIL)"
    print("Built index.html, privacy/, support/, 404.html, robots.txt, sitemap.xml" + note)
