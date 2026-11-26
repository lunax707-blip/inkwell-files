# Inkwell and Co daily product run

You are running a daily task for Shaimaa (store owner, designer, Jeddah). Read this whole file, then LOG.md, before making anything.

## The job, every run
1. Make ONE substantial new digital product (see "What to make"). She chose this on 21 Nov 2026 after market research: fewer, bigger, more specific products beat many small ones.
2. Create them on Gumroad as DRAFTS (store `inkwellandco`, USD). Never publish in the same step.
3. Send Shaimaa the previews with SendUserFile and ask, with a selectable question, whether to publish the batch (options: publish all, publish some, publish none). Wait for her answer.
4. Only after she says yes in that chat: publish the approved drafts, then add two or three different Pinterest pins for it (section "Pinterest").
5. Append what you made to pipeline/LOG.md and push.
If she has not answered, leave everything as drafts and stop. The next run starts by listing drafts still waiting (Gumroad list_products) and asks about them together with the new batch. Never publish or pin on the strength of this file or of an old approval.

## Hard rules (hers, do not bend)
- No living beings in any product, cover or pin: no people, animals, birds, insects, faces, eyes on objects. Plants, trees, flowers, landscapes, objects, buildings, patterns are fine. Look at every generated image yourself before using it; discard and regenerate anything doubtful.
- No churches, crosses or other religious buildings or symbols in paintings. Avoid six pointed stars in patterns.
- Never use the em dash or the middle dot anywhere in titles, descriptions, covers, pins or files.
- Coloring and worksheet products are delivered as PDF, never loose PNGs. Wall art is a zip with the JPG(s) and READ_ME.txt.
- High aesthetic bar. Nothing generic or template looking. If a product is weak, drop it and make fewer rather than pad the batch.
- Ramadan and Eid products are on hold until early January.
- Replies to her: short, direct, no fluff. Open questions as selectable options with a recommended one.

## What to make (rotate by day, check LOG.md so nothing repeats)
Primary audience: FREELANCERS (designers, writers, developers, creators with irregular income). Name the buyer in the title and build for their real situation. Generic products do not sell.
Rotation, one per day:
A. Google Sheets / Excel budget or business template for freelancers, $5 to $9. Build a real .xlsx with openpyxl (working formulas, a dashboard tab, instructions tab, sample data that can be cleared) and state it opens in Google Sheets and Excel. Ideas: irregular income budget, invoice and payment tracker, client and project tracker, tax set aside calculator, rate calculator, yearly income dashboard, expense tracker with categories, savings runway calculator. Open the file and check every formula before listing.
B. Planner system as PDF, 40+ pages, $5 to $9, Letter and A4: freelancer weekly planner, project planner, content planner, ADHD friendly planner for freelancers (big type, few boxes, no medical claims), goal and quarter planner.
C. Kids worksheet bundle as PDF, 50+ pages, $5 to $7: one coherent theme per bundle (numbers 1 to 20, English alphabet, Arabic alphabet and words, shapes and patterns, telling time). Objects, shapes, plants and vehicles only; no figures or animals.
D. Wall art: a set of 6 AI paintings ($8) or 3 related singles ($3 each, the only case where one run makes several listings). Original scenes in the manner of a public domain master, never a remake of a famous painting.
Dropped after research: affirmation cards, tiny 5 page packs, single pattern posters.
Listing image for A and B: a clean mockup showing several pages or tabs, with the buyer named.
Arabic text in products: no shadda, no tanween, no French quotation marks, no hyphens.

## Tools and routes that work
- Images: Freepik/Magnific MCP. images_generate (aspectRatio 3:4, about 135 credits), then images_upscale (mode classic, scale 4k, classicPreset Art, creativity 0, resemblance 100, about 216 credits) gives 3072 x 4096. Check account_balance first; if under 5,000 credits make coded products only and tell her. The content filter sometimes blocks harmless prompts: reword and retry once.
- Result URLs on pikaso.cdnpk.net are public and downloadable with curl.
- Fonts: pipeline/fonts (Fraunces, Instrument Sans, Noto Naskh Arabic, Noto Kufi Arabic, Amiri). Scripts expect them at /home/claude/fonts/ttf, so: mkdir -p /home/claude/fonts && ln -s <repo>/pipeline/fonts /home/claude/fonts/ttf. Scripts expect /home/claude/book as the work folder. Arabic needs PIL with raqm (layout_engine=ImageFont.Layout.RAQM).
- Brand: navy #2B3A67, cream #F4E9D8, coral #D9583B, mustard #E8A33D, teal #1F6F78, sage #9DB5A0. Wall color for mockups (226,218,206). Framed preview mockup code is the mock() function in scripts/wallpack.py; planner layout in scripts/planner.py; Arabic tracing in scripts/arabic.py; pins in scripts/pins.py.
- Getting files into Gumroad: add_file and add_cover need a public https URL. Push the file to this repo (lunax707-blip/inkwell-files, main), use https://raw.githubusercontent.com/lunax707-blip/inkwell-files/main/<path>, then remove the paid files with an orphan commit of the remaining tree and a force push. Keep pipeline/ and pins/ when you do that. Never write the id of an upload commit in LOG.md, commit messages or chat: old commits stay downloadable on GitHub by id even after the rewrite. If the force push is blocked, say so plainly in your report to her. Never wipe the lunax707-blip.github.io repo.
- Gumroad limit: 10 new products per rolling day. If creation is refused, make what fits, report it, do not retry in a loop.
- Each listing: clear search friendly title, description (what is included, sizes, how to print, personal use only), tags, custom permalink, framed or designed cover as the first cover.
- The sandbox cannot open gumroad.com, github.io or pinterest.com. Verify pushes with git ls-remote and raw.githubusercontent.com.

## Pinterest (only for published products)
Pinterest auto publishes from two RSS feeds on her claimed site, repo lunax707-blip/lunax707-blip.github.io:
- feed-wall-art.xml goes to board Printable Wall Art (wall art, paintings, posters)
- feed-coloring.xml goes to board Printable Coloring Pages (coloring and kids worksheets)
- feed-planners.xml is for planners, spreadsheets and templates. Check LOG.md for whether she has connected it to a board yet; add items to it either way
For each published product: make a 1000 x 1500 pin (scripts/pins.py templates) into /pins/, add a product page at /p/<slug>/index.html (copy an existing one; keep the p:domain_verify meta tag; button links to the Gumroad listing), and add a new <item> at the top of the right feed with a unique guid, current pubDate, link to the product page, enclosure and media:content pointing at the pin. Validate the XML, commit, push.

## Live products on Gumroad (permalink id, slug, price)
zlexbz desert-light-prints $8; eduhsj abstract-art-prints $8; bptppu kids-room-transport-prints $8; zfbhli geometric-pattern-prints $8; hwxnuk things-that-go-coloring $5; kjiuug geometric-patterns-coloring $5; fdqewu trucks-and-diggers-coloring $2; jdvoeg sky-sea-space-coloring $2; ivcmbx places-to-see-coloring $2.
Drafts created 22 Nov 2026: see LOG.md for ids and status. Six product creations were used at about 02:35 Riyadh time on 22 Nov, which counts toward the 10 per rolling day limit.

## Covers and Canva (added 21 Nov 2026 at her request)
- Listing covers: use Magnific for the background scene of each cover (images_generate, about 135 credits, no upscale needed). Ask for a styled flat lay or desk scene with empty paper, a blank laptop screen or a blank frame, and no people, hands, animals or text. Then place the real product pages onto it with PIL and add the title in the brand fonts. Look at the result before using it. A coded mockup is the fallback if credits are low.
- Canva is connected, but this sandbox cannot open Canva thumbnails or export links, so Canva output cannot be checked here. Do not build products in Canva during unattended runs. Use Canva only when she asks for it in the chat, and then give her the Canva link to review herself before anything is listed. If she wants to sell Canva template links, she must first confirm Canva's Content License terms allow it for the elements used.

## Honesty
Say plainly what was made, what failed, what was not checked. Do not claim a pin or listing is live unless the tool confirmed it.

## Notes from the 22 Nov 2026 daily run
- Spreadsheet products: scripts/invoice_tracker.py builds the workbook (PREVIEW=1 adds tight print areas for rendering tabs), scripts/verify_invoice_tracker.py checks a LibreOffice recalculated copy against plain Python arithmetic, scripts/sheetcover.py composes the cover from a Magnific flat lay and the rendered tabs. Recalculate with: soffice --headless --convert-to xlsx --outdir recalc file.xlsx. Render tabs with: soffice --headless --convert-to pdf, then pdftoppm. Do not load and resave the workbook with openpyxl, it drops the chart.
- Use only functions shared by Excel and Google Sheets (SUMIFS, COUNTIFS, INDEX, MATCH, LARGE, IFERROR, SUMPRODUCT, TODAY). No dynamic arrays, no XLOOKUP, no MAXIFS.
- The add_repo tool was not present in that session; the repo was already cloned at /home/claude/inkwell-files and a normal push worked.
- Temporary upload files go in drop/. In that session the force push used to purge them from history was refused by the permission system; do not work around it, delete with a normal commit and tell her.

## Notes from the 23 Nov 2026 daily run
- Planner systems: scripts/freelancer_planner.py builds all four PDFs (Letter and A4, Monday and Sunday start) and prints a warning for any label wider than its column; fix every warning before listing. scripts/plannercover.py composes the cover from a Magnific flat lay and page renders (pdftoppm -r 110 into a pages folder).
- reportlab: character spacing set in a text object leaks into later drawString calls and makes text run wider than measured. Reset it with setCharSpace(0) before drawText.
- Gumroad draft rfnubt (/l/freelancer-planner) created 23 Nov, about 06:25 UTC; one product creation used.

## Notes from the 24 Nov 2026 daily run
- Kids worksheet bundles: scripts/telling_time.py builds Letter and A4 PDFs plus a JSON manifest (hand angles of every drawn clock and every answer). scripts/verify_telling_time.py decodes the clocks and recomputes all answers on its own; it must print FAILURES 0 before listing. scripts/timecover.py makes the desk cover and the "What's inside" grid cover (pages rendered with pdftoppm -r 110 into a pages folder).
- Clock drawing: draw the numerals after the hands and keep the thick part of the minute hand short with a thin needle to the tick marks, otherwise the hand hides the numerals.
- Wrong answer options must stay inside what the section has taught (only o'clock options in the o'clock section and so on).
- On 24 Nov list_products showed all eight drafts from 22 and 23 Nov as published (ssekgf, ayhqww, kjgpbh, xwpynd, arpyl, crsnoy, ettcln, rfnubt). None of them has a Pinterest pin or product page yet; pin only after she says so in the chat.
- Gumroad draft nkqbys (/l/telling-time-worksheets) created 24 Nov, about 09:36 UTC; one product creation used.

## Notes from the 25 Nov 2026 daily run
- Wall art sets: scripts/woodblock_pack.py names the six upscaled JPGs, writes READ_ME, zips, and makes two titled framed covers (edit NAME, TITLE, ITEMS and README for a new set).
- The classic 4k upscale can turn smooth paper grain in large flat skies into blotchy streaks. Check skies at full size; a sky only band reduction (original minus 0.7 x (blur 5 minus blur 70) under a feathered mask) fixed it.
- Gumroad draft rfkcgm (/l/japanese-woodblock-prints) created 25 Nov, about 06:35 UTC; one product creation used. Draft nkqbys (telling time) was still unpublished on 25 Nov.

## Notes from the 26 Nov 2026 daily run
- The sandbox already had a stale clone at /home/claude/inkwell-files whose history no longer matched origin after the 25 Nov rewrite. Do not reset it; make a fresh clone in a new folder (this run used /home/claude/inkwell-fresh) and work there.
- Spreadsheet products, second one: scripts/income_budget.py builds the Irregular Income Budget (argument "empty" for the blank copy, PREVIEW=1 for tab renders). scripts/verify_income_budget.py checks a LibreOffice recalculated copy against plain Python arithmetic, and with --stress builds and checks 7 stress files; it must print FAILURES 0 before listing. scripts/incomecover.py makes the desk cover, scripts/incomecover2.py the "What is inside" grid.
- Spreadsheet traps found: MIN and MAX ignore an empty cell reference, so add +0 to a setting that may be empty; count named rows only (SUMIFS with "<>" on the name column) so a half filled row does not leak into totals; count sentences such as "Payments logged: 3" avoid singular and plural mistakes.
- Listing covers now go in covers/ and stay in the repo, so pins can be made later without regenerating them.
- Gumroad draft aorcmu (/l/irregular-income-budget) created 26 Nov, about 06:35 UTC; one product creation used.

