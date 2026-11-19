LATEST UPDATE

Removed More photos and Figures & results sections. Added the heading
What I use above the skills globe.

CURRENT PAGE — CONCISE COPY AND LARGER TYPE

Removed filler headings, About/background content, tool categories, and
visible globe instructions and controls. The 17-tool globe retains drag
and keyboard interaction. Base text is 24px desktop and 22px mobile.
Hands-on sessions now shows workshop-ros.webp; the previous hands-on
photo is in More photos. Existing image treatments are retained.
Static asset/link checks and globe interaction checks passed.
Browser rendering is unavailable in this environment. Saved locally.

CURRENT TOOLKIT — SOFTWARE TOOLS AND MATCHING ICONS

LiDAR and IMU integration were removed from the tool globe and category
list. C++ remains a single entry. Git, Docker, and Blender were added at
the user's request. The globe now contains 17 tools.

All tool icons use a consistent charcoal/teal palette, retaining their
original silhouettes and tonal detail. Globe tiles use the same palette
across all categories. Recoloring: python3 scripts/theme_tool_icons.py.
Brand-icon provenance and MIT license remain in assets/icons/tools/.

Inventory, icon colors, local assets, and globe interactions verified.
Changes are saved locally; not published.

TOOL GLOBE ICONS

All 16 tools have local SVG icons in the globe, selected-tool panel, and
category list. Main software logos come from Devicon (MIT); palette-adjusted
ROS/Unity marks and the ROS 2 badge are documented in assets/icons/tools/
sources.json. Other icons are custom technical illustrations rather than
official brand marks. The license is included alongside the icons.

No external icon CDN is required. Accessible tool names and keyboard/pointer
controls remain intact. All icon paths, SVG markup, and globe interaction
checks pass. Browser rendering remains unavailable in this environment.

INTERACTIVE WHAT I USE GLOBE

The toolkit now opens with a rotating 3D tool globe in the existing dark
and teal theme. Drag with a mouse or touch, select a tool for its context,
pause rotation, or reset the view. Arrow keys rotate the focused globe;
Space pauses/resumes and Home resets it. All 16 tools are sourced from the
same HTML category list, which remains available below the globe and is
expanded when JavaScript is unavailable.

Automatic rotation pauses on hover/focus, starts paused for reduced-motion
users, and stops offscreen or in hidden tabs. No external libraries or
network assets are required. Implementation: assets/tool-globe.js.
Validation: node scripts/test_tool_globe.cjs. Geometry and interaction-state
checks pass, including drag/click separation and motion controls. Browser
rendering remains unverified because Chrome is blocked in this environment.
Changes remain local; no publication performed.

READABILITY AND TOOLS UPDATE

Body text is now 18px, with larger navigation, controls, project descriptions,
publication details, and labels. The menu collapses below 1201px to make
room for the larger navigation. Layouts adjust for tablets and phones.

The visible What I use section under Consultancy groups Pejman's tools into
robotics/perception, programming/learning, and simulation/design. The grouped
capabilities idea is inspired by https://www.hugotamm.com/; tool names are
supported by the supplied CV and existing CERN/PJM project content.
No personal claims, projects, or proficiency ratings from Hugo were copied.

JavaScript syntax, document links/anchors, IDs, content preservation, and
release files checked. Browser rendering could not be checked: Chrome is
blocked by the environment's socket permissions. Changes remain local.

ACTIVE PORTRAIT — MONOCHROME WITH RESTORED CHARCOAL TEXTURE

The opening section loads assets/images/pejman-hero-original-textured-zoomed-raised-135.webp.
The current monochrome portrait is uniformly reduced to 82% of its prior
size, centered horizontally and raised 135 pixels above the bottom alignment.
The lower torso fades into the texture; the face remains above the text.
Background texture is sampled from the earlier pejman-hero-restored.png
and applied only to the border-connected dark background. No image
generation or face retouching was used. The WebP is lossless.
Rebuild: python3 scripts/add_hero_background_texture.py --zoom 0.82 --lift 135
Preview: output/portraits/latest-portrait-textured-hero-zoomed-raised-135.png.
This update is local; it has not been published to GitHub.

HISTORICAL NOTES (superseded where they describe the active portrait)

CURRENT HERO — RESTORED APPROVED PORTRAIT

The opening portrait is again assets/images/pejman-hero-v7.png, the earlier
approved dark portrait with short side-combed hair and straight glasses.
The event-photo experiments remain saved separately. No new generation.

CURRENT HERO — ORIGINAL PHOTO, BACKGROUND REMOVED

assets/images/pejman-original-dark.png uses the original event photo with a
conventional foreground mask, uniform scaling, monochrome treatment and
a charcoal backdrop. Face and expression are not retouched.
Reproducible script: scripts/make_original_hero.py. No image generation.

CURRENT OPENING BACKGROUND

The opening background uses the unedited original event photograph:
assets/images/pejman-original.jpg (byte-identical to the supplied JPEG).
Only CSS cropping and a dark text overlay affect its page presentation.
The latest downloaded scroll fades and consultancy image positioning are
preserved in the working copy. No face composite or glasses edit is used.

CONTENT ORGANIZATION UPDATE

Research project summaries (LiDAR localization, DynaHull, drone trajectory
forecasting, CERN LiDAR dataset) now sit under Research, alongside evidence
and publications. Previous Projects contains applied engineering examples:
CHARMBot teleoperation interface, construction-site monitoring, and
road-scene perception, linked to the existing CERN/PJM source pages.

CHARMBOT BACKGROUND MASK

Previous Projects now uses assets/images/cern/charmbot-cutout.png.
Original photograph retained as charmbot-only.jpg. Reproducible background
mask: python3 scripts/mask_charmbot.py. No image generation used.

CURRENT USER-SELECTED COVERS

Consultancy: image 01, assets/images/workshop-audience.webp
Research: image 08, assets/images/lidar-scans.png
Previous Projects: assets/images/cern/charmbot-only.jpg (robot only)
CHARMBot source: HIP-CERN-Talk-v2/assets/img/p11-001.jpg
CSS-only tone adjustments. No image generation used for this update.

--- Earlier notes ---

CURRENT SECTION IMAGE SELECTION

Consultancy: assets/images/workshop-ros.webp
Research: assets/images/lidar-scans.png
Previous Projects: assets/images/lab-visit.webp
All three replace the earlier selection. CSS-only tonal styling; no image
generation or modifications to originals. Comparison: image-selection.html.

--- Earlier notes ---

LATEST IMAGE SELECTION

The three section covers now use existing content images with CSS-only
monochrome/dark treatments. No image generation was used for this update.
- Consultancy: assets/images/workshop-hands-on.webp
- Research: assets/images/lidar-experiments.png
- Previous Projects: assets/images/robotics-demo.webp
Original files are unchanged; full-color scientific figures remain in the
research evidence gallery. The cover map is labeled as monochrome.
Open image-selection.html for original-versus-styled comparisons.
The approved opening portrait remains pejman-hero-v7.png.

--- Earlier design notes ---

CURRENT DESIGN — November 18, 2026

Local HTML preview: open index.html. No publication was performed.
The portrait uses assets/images/pejman-hero-v7.png.
Three main chapters: Consultancy Services, Research, Previous Projects.
Each opens with a full-width image using a consistent charcoal, white, and
turquoise palette. Supporting content, contact details, publications, real
research figures, biography, and community photos remain available.

Section illustrations (AI-generated concepts, labeled in the page):
- assets/images/consultancy-hero.png
- assets/images/research-hero.png
- assets/images/projects-hero.png
Built-in generation prompts: output/imagegen/section-visual-prompts.json
Pre-redesign source backup: output/backups/scroll-redesign/

Checks: HTML structure, local assets/anchors, image dimensions, JavaScript
syntax and simulated interactions passed. Browser visual QA was unavailable
in this environment. A CSS parser was not installed; only basic CSS source
checks were performed.

--- Previous project notes ---

PEJMAN HABIBIROUDKENAR — PERSONAL ROBOTICS WEBSITE

Open index.html directly in a browser. No installation or build is required.
For local HTTP preview: python3 -m http.server 8080
Then visit http://localhost:8080.

The site uses local images, plain CSS and JavaScript, without external fonts,
analytics, cookies, dependencies, or a backend. Contact opens the visitor's email
application. Publications link to their publisher, DOI, or preprint record.

FILES
index.html                 All page content and search metadata
assets/styles.css          Responsive design
assets/app.js              Mobile navigation and publication filters
assets/images/             Six supplied photographs plus three original research PNGs
assets/documents/           The original supplied CV, available for download
research-sources.json      Research references and editorial notes
scripts/package_site.py    Produces site-release/ and pejman-website.zip
.github/workflows/pages.yml GitHub Pages deployment workflow

GITHUB PAGES
The site uses relative paths, so it supports both a personal GitHub Pages domain
and a project subdirectory. In the destination repository, enable Settings > Pages
> Build and deployment > Source: GitHub Actions. Push these website files and the
workflow to the main branch, or run the workflow manually. The workflow packages
only index.html, .nojekyll and assets/; it does not publish the source CV filename,
info.txt, original pics directory, README, or research notes.

Alternatively, upload the contents of pejman-website.zip to a repository with
GitHub Pages configured to deploy from its root directory on the chosen branch.

This delivery is local and has not been pushed or published to a GitHub account.
Absolute canonical and social image URLs have deliberately not been guessed.
Once the final URL is known, add a canonical link, og:url, and an absolute og:image.

CONTENT
Research records checked 18 November 2026. Publication dates use the journal or
conference record. The supplied CV is retained as provided and may contain older
titles, dates or company branding. The page calls the business PJM Robotics, as
requested in info.txt and shown on the public LinkedIn profile; the CV says PejiTron.
The list is selected robotics research, not a complete bibliography. The 2026
low-light detection paper is explicitly labeled a preprint. Team achievements
are not presented as individual awards. No citation counts, clients, endorsements,
or performance numbers were invented. Research sources are linked beside claims.
The research section uses original point-cloud, scan-pattern and trajectory figures
from Pejman712/Non_Repetetive_LiDAR_Registertion. Source links and the repository
Apache 2.0 license are included; downloaded PNGs are unmodified.

CHECKS
Verified local asset paths, section anchors, image descriptions and unique IDs.
Browser rendering could not be verified in this environment: Chrome was blocked
by the host sandbox (setsockopt: Operation not permitted). A desktop/mobile browser
review of layout, menu, filters and downloads is recommended before public launch.
The supplied PJM Robotics and HIP-CERN presentation URLs were preserved, but could
not be fetched by the available web tool; their availability is unverified.

SCROLLING DESIGN UPDATE
The page opens with the approved full-screen monochrome portrait, then continues
as one document through Research, Publications, About, Workshops and Contact.
On desktop, the large image column stays beside the content and changes as a new
chapter reaches the upper portion of the viewport. The fixed navigation tracks
the current section. Scrolling uses normal browser behavior, without scroll locks.
On screens up to 800px, images appear inline with each chapter. Reduced-motion
preferences disable crossfades and smooth scrolling. Content remains readable
without JavaScript; navigation and external links use ordinary anchors.

assets/images/pejman-hero.png is the AI-restyled monochrome portrait, generated
from the approved concept with the baked-in interface removed. Live HTML provides
the name, role and buttons. Generation prompt: output/imagegen/hero-background-prompt.txt.
Original research images remain unmodified.

Additional checks: JavaScript syntax and a DOM simulation verified forward/backward
section tracking, image selection, active navigation, publication filters, menu
Escape/resize behavior and reading progress. HTML, image sizes and local links
were checked. These checks do not replace visual browser verification.

Portrait update: the site now uses assets/images/pejman-hero-v2.png with a
slightly straighter head and reduced smile. The earlier portrait is retained.
Built-in image generation prompt: output/imagegen/hero-expression-prompt.txt.

Hair grooming update: the current portrait is assets/images/pejman-hero-v3.png.
Previous versions are retained. Built-in image generation prompt:
output/imagegen/hero-hair-prompt.txt.

Current portrait: assets/images/pejman-hero-v4.png, with slightly longer hair
combed uniformly toward the viewer's left. Previous versions retained.
Built-in image generation prompt: output/imagegen/hero-hair-left-prompt.txt.

Current portrait: assets/images/pejman-hero-v5.png with longer left-swept hair.
Previous versions retained. Built-in image generation prompt:
output/imagegen/hero-long-hair-prompt.txt.

Current portrait: assets/images/pejman-hero-v6.png, based on v2 (before hair
edits) with straightened glasses. Earlier versions retained.
Built-in image generation prompt: output/imagegen/hero-glasses-prompt.txt.

Current portrait: assets/images/pejman-hero-v7.png, short hair tidied toward
the viewer's left, retaining straight glasses. Previous versions retained.
Built-in image generation prompt: output/imagegen/hero-side-hair-prompt.txt.
