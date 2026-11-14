# Snapshot validation

Collected on 2026-11-14, from 13:32–13:37 KST (exact timestamps are in catalog.json).

- 712 distinct product URLs from the official Korean ARKET sitemap under `/about-arket/product.*`.
- 585 product details confirmed, including 580 discounted products and 583 products with at least one available size.
- 127 URLs returned unavailable product details. Kept as explicit unavailable entries, without invented price or stock information. Their display names are derived from URL slugs.
- 585 official product thumbnail images cached locally; no failed downloads.
- Product identifiers match their source URLs. Available sizes agree with each recorded size's availability.

Browser checks passed at desktop and 390px mobile viewport widths:

1. Initial pagination and full rendering of all 712 entries.
2. Exact product-number search and empty results.
3. Combined department, in-stock size and discount filtering.
4. Ascending price sort.
5. Unavailable and sold-out status filters.
6. Grid and list views.
7. Official external product links.
8. Mobile layout without horizontal page overflow.
9. Locally cached images load successfully; no JavaScript runtime errors.

The first browser-check attempt tried to click the hidden “show all” control when fewer than 48 results existed. The check was corrected to click it only when visible, then the complete interaction check passed. This was a verification-script issue, not an application change.

The public snapshot is not automatically refreshed. Coupon prices are not calculated. Unavailable detail pages must not be interpreted as confirmed sold-out stock.
