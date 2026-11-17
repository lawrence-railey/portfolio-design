# Lawrence Railey — Third Style Portfolio

A six-world portfolio with a shared white LR identity, technical typography, and landscape-led pages.

The header reads "UI/UX + AI Tech + Creative." Navigation stays fixed while scrolling, contracts from 100px to 76px on desktop (82px to 68px on phones), and uses each destination world's colored underline with a subtle upward-fading gradient on hover, focus, and the active page. Each item has horizontal padding; Contact uses the same treatment in neutral gray and white. Compact pages retain header clearance, section links allow room for the fixed bar, and reduced-motion preferences disable the transition.

## Preview

From this directory, run `python -m http.server 4173 --bind 127.0.0.1`, then open `http://127.0.0.1:4173`.

## Public source repository

The repository includes the website pages, source scripts, content, PHP contact endpoint, vendored mailer, and image/video assets. Private mailer configuration, environment files, private keys, temporary work, caches, and generated deployment ZIPs are excluded by `.gitignore`. `contact-config.example.php` is a safe setup template with an empty password; keep real credentials outside the repository and web root. The static preview above does not execute PHP or send contact messages.

## Pages

| Page | File | Landscape |
| --- | --- | --- |
| Home | `index.html` | Earth |
| Work History | `work-history.html` | Mars |
| UI/UX Portfolio | `portfolio.html` | Ocean |
| Creative AI Portfolio | `creative-ai.html` | Purple |
| Other Work | `other-work.html` | Yellow |
| Contact | `contact.html` | White/gray city |

Nine product, systems, architecture, and marketing case studies sit under UI/UX. The main portfolio uses logo cards ordered Cox, Fullpath, BagsID, LoanAI, Healthesystems & Jurne, and Earlier Work. Earlier Work has a layered preview with The Melting Pot in front, Kennards Hire behind it, and Reeves Import Motorcars beneath. Catalina, Strike Electric, and Kennards Hire case studies are accessible from Earlier Work. The Creative AI archive contains 78 images, including five book covers and 23 additional Cyber Byzantium images, with category filters and a keyboard-accessible image viewer. Other Work includes published fiction, works in progress, music, audio, and video production, with a dedicated Florida Regime branding showcase. Case studies use compact carousels with a vertical thumbnail rail on desktop and a horizontal rail on mobile. Logos introduce their relevant sections, and key live-site links use secondary buttons. The homepage emphasizes UX architecture, UI design and development, and applied AI, with brand-based featured cards. The contact page uses the city hero with a compact form on the left, neutral white/gray accents, secondary LinkedIn and résumé links, and a primary Send message button. Direct email, phone, and address details sit below the hero. The SMTP contact form is live and verified against the destination inbox.

## Editing

- `scripts/build.py` generates the pages. Edit hero messaging and page layout here.
- `content/portfolio.json` holds the imported case studies, career history, artwork selection, writing, and music content.
- `style.css`, `diagrams.css`, and `app.js` contain shared styling and behavior.
- `assets/brand/lr-monogram.svg` is the selected white LR emblem in a broken circular frame. The favicon uses the same mark.
- `assets/worlds-4k` holds the approved, manually edited originals. These are never modified by the page build.
- `assets/worlds-web` holds compressed, responsive copies for the site.
- `assets/worlds-video` holds the silent 3840 × 2160 hero videos. The responsive images remain as loading, error, reduced-motion, and data-saving fallbacks.
- Michroma supplies the extended geometric headings; Rajdhani supplies navigation and technical labels. Fonts load from Google Fonts, with Eurostile and system fallbacks.

Run `python scripts/build.py` to rebuild, `python scripts/validate.py` to check local references, and `node --check app.js` to check JavaScript syntax.

Hero motion starts only when the hero is visible and the visitor's motion/data preferences allow it. There is no on-page pause control. A lightweight responsive still stays visible until playback begins. Unsupported playback, blocked autoplay, media errors, or five seconds of buffering switch to the original 4K PNG; the lightweight still remains painted until the PNG finishes loading. Reduced motion, data saving, and 2G connections use the still automatically. Scrolling away or hiding the tab pauses playback and suspends the loading deadline.

`content/hero-video-generations.json` records the Higgsfield inputs and selected revisions. `scripts/finish-ocean-mars-motion.py` applies the latest blue and red corrections. UI/UX retains its quick double flash but now illuminates neighboring cloud forms. Native wave detail stays in forward motion without endpoint texture blending, and fine periodic ripples animate the distant water. The traveler uses a tight silhouette holdout. Mars adds a small helmet gesture that returns to its starting pose and a slightly stronger translucent sandstorm; the body stays planted. Purple retains the approved sideways fog from `scripts/finish-hero-atmosphere.py`. Earth, Purple, Yellow, and City remain byte-for-byte unchanged in this revision. All videos are silent 3840 x 2160 H.264. Ocean runs approximately eight seconds, Purple eight, and Mars four; the other clips retain their approved timing.

`scripts/import-content.py` was used once to import the earlier local portfolios and prepare the web derivatives. Routine edits do not require running it again.

## Verification

Local page, asset, anchor, heading, and JavaScript checks pass. Gallery curation, all five cover entries, image integrity, logo placement, live-site actions, portfolio order, archive links, and layered preview markup were also checked. Earlier browser checks covered the hero, filters, lightbox, and carousel controls. The six-world/contact and Other Work update passes local reference, image integrity, source-hash, form mapping, hero numbering, carousel order, and JavaScript syntax checks. Carousel navigation thumbnails are optimized separately from the full-size originals.

`scripts/expand-gallery.py` imports the earlier AI archive once. `scripts/prepare-case-thumbnails.py` prepares small carousel thumbnails from the current content; rerun it after adding case-study images, then rebuild. Both require Pillow.

`scripts/refresh-portfolio.py` is the one-time curation/import used for the latest gallery and logo changes. It uses the existing Cyber Byzantium site archive and research files on the author's computer; it is not needed for routine builds. All imported images are included locally in this portfolio.

Primary buttons, including Download résumé, use the section accent as a solid fill with dark text. Secondary and outline buttons retain transparent backgrounds and accent-colored borders.

The homepage hero includes a filled teal "View UI/UX portfolio" button beneath its introductory text, linking directly to `portfolio.html#portfolio-items`. The main menu still opens the portfolio hero. Work History places the copper "Download résumé" primary button in the same position beneath its hero copy. UI/UX, Creative AI, and Other Work retain their original bottom-of-hero scroll cues without additional hero buttons. Anchor navigation allows space for the sticky header and respects reduced-motion preferences.

Hover feedback uses short color fades, small card lifts, and restrained section-colored button glows. Links, gallery controls, filters, and keyboard focus share this treatment. Reduced-motion preferences disable transitions and remove the added hover movement.

## Sixth world and production update

All hero counters run from 01 / 06 through 06 / 06. The approved `assets/worlds-4k/city-4k.png` remains untouched; its 1280, 1920, and 3840 pixel WebP copies provide responsive contact backgrounds.

Dawn Nebula uses a dedicated three-column book layout on desktop and tablet, with a single column on narrow phones. Music actions use a primary Listen here button and a spaced secondary Mixcloud button. The Other Work Florida Regime carousel starts with The Cure After Party, ends with the DJ booth, and omits the early homepage screenshot. Video production and voiceover services have their own section, reusing the current BagsID film and narration credit.

The November 12, 2026 gallery refresh replaces 32 existing entries with 31 distinct original images downloaded from the live Cyber Byzantium website. JPEG bytes are preserved without recompression; separate WebP thumbnails are capped at 720 pixels. `content/byzantium-image-sources.json` records the reviewed matches, source URLs, original dimensions, and SHA-256 hashes. Unmatched artwork and gallery order are preserved. `scripts/refresh-byzantium-assets.py` reapplies the reviewed mapping from a downloaded source directory and manifest.

## Other Work cleanup

The Cyber Byzantium book and DJ photo use matching, left-aligned 4:3 frames with the complete images contained inside them. The Florida Regime logo uses a compact blue starry-sky-and-palms banner, cropped from the existing FR3 artwork to preserve the complete mark, without a project-page link. Its carousel spans the content container and includes Surviving the Storm in place of Trance 001; The Cure After Party remains first and the booth remains last. Listen here jumps to the embedded player on Other Work. The retired `project-florida.html` page is no longer generated; remove that obsolete file when overlaying this update onto an older deployment.

The contact page omits the invitation to contact again, retaining its normal footer links. LendingTech Systems reads October 2025 — Present. Styles and scripts use content-versioned URLs so updates load without a manual cache clear. The original PNG hero fallbacks must be deployed with the video and WebP assets. Run `node scripts/test-hero-motion.cjs` for playback-fallback behavior checks.


## Contact mailer (live)

The public `contact.html` URL is rendered by `contact/index.cgi` through the root `.htaccess` rule. Python uses a conventional POST, followed by a 303 redirect to a signed confirmation state; no background fetch or PHP execution is involved. The normal city background and layout remain. Successful submissions replace the form with `content/contact-confirmation.html`, retaining LinkedIn and résumé buttons. Refreshing the confirmation does not resend mail. Success means the SMTP server accepted the message, not a delivery receipt.

The CGI reads generated `contact.html` as its base template. Run `python scripts/build.py` after editing the source form. `contact.css` styles the confirmation and is content-versioned. Deploy the root `.htaccess`, `contact/.htaccess`, and `contact/index.cgi` (Unix newlines, permissions 0755), plus contact.html, contact.css, and content/contact-confirmation.html. The legacy PHP endpoint is blocked by site routing. The temporary test URL redirects to contact.html.

Python uses only the standard library. Private configuration and rate-limit state live at `/home2/lawreod5/portfolio-contact/python-mailer/` outside public_html (directory 0700, configuration 0600). `config.json` contains host, port, encryption, username, password, from, to, origin, and a randomly generated signing secret. PORTFOLIO_CONTACT_DIR can override the directory for tests. Never commit or publish real settings. Existing authenticated SMTP settings are reused with TLS certificate verification. Visitor addresses are Reply-To only.

The form validates fields and request origin, uses a signed cookie-bound CSRF token and honeypot, and limits attempts to five per IP per hour and thirty total. Private records contain keyed hashes and send status; uncertain sends remain reserved to prevent duplicates. Confirmation receipts are signed, HttpOnly, Secure, and expire after one hour. `python scripts/test-python-contact.py` checks rendering, escaping, token validation, POST redirects, and confirmation integrity without sending email.

## November 12 layout follow-up

The homepage introduction stacks the eyebrow, heading and supporting copy. Cox, Fullpath and LoanAI show UI examples before their architecture narratives. BagsID shows its website and branding first, then product UI and the design system, then diagrams. Existing images, diagram content and anchor IDs are preserved. `scripts/case_order.py` applies this order during the build.

Hero type follow-up: geometric H1/H2 tracking is slightly open (+0.005em), with hero tracking at +0.01em. Desktop hero headlines increase approximately 7–9% (45px cap; Contact 50px). Mobile headline sizes remain unchanged. Verified at 1920px and 390px without additional headline wraps.

## Production root migration — November 17, 2026

The portfolio is now deployed at `https://lawrencerailey.com/` in `/public_html`. Future deployments target that directory, not `/new-site-2`. Old `/new-site-2/` URLs redirect to their corresponding root paths. The Python form uses `/contact.html` and root-scoped cookies.

The former WordPress files, original root configuration, and compressed SQL export are preserved in `/public_html/archive-wp-old`, which denies public access. The original WordPress database is retained. Unrelated hosted projects and `.well-known` remain in place. The obsolete `new-site` directory was deleted. The emptied `new-site-2` directory is retained; root routing redirects its former URLs.
