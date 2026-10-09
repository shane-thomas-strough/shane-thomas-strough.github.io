# Strix field study publication handoff

Status: staged in the local site checkout on branch `research/publication-engine-recon`. Not deployed or merged.

## Site files

- `the-finding-is-not-the-report.html`: publishable article page.
- `_build/strix-workflow-report.md`: canonical editable article source.
- `_build/build_strix_report.py`: deterministic page renderer using the site's existing article CSS.
- `images/strix-workflow-report.png`: share image; `_build/make_strix_card.py` regenerates it.
- `insights.html`: Technical Library entry pointing to the article.
- `sitemap.xml`: article and companion landing URLs.
- `research/strix-workflow-2026/index.html`: companion landing page.
- `research/strix-workflow-2026/`: invented fixtures, instructions, oracle, public ledger, claim map, trace excerpt, SHA256SUMS, and `verify.py` / `check_fixture.py`.
- `research/strix-workflow-2026.zip`: downloadable packet with byte-identical contents.
- `_build/pack_strix_packet.py`: deterministic ZIP builder with an explicit public-file allowlist.
- `_build/strix-next-study-protocol.md`: proposed larger blinded study, not executed and not part of this article's results.
- `_build/check_strix_publication.py`: static page, link, ZIP, sitemap, and publication-boundary checks.

## Rebuild and validation

From the site repo, run `python3 _build/build_strix_report.py`, `python3 _build/make_strix_card.py`, `python3 _build/pack_strix_packet.py`, and `python3 _build/check_strix_publication.py`. From `research/strix-workflow-2026`, run `python3 verify.py` and `python3 check_fixture.py`. If packet files change, rerun the ZIP builder before the site check.

These checks passed on 2026-10-09. A separate AI technical read of the raw traces caught one wording error in the Orca case study; it was corrected in the source and regenerated HTML. That pass found no other material factual or privacy blocker in the evidence it inspected. A browser viewport check could not run because the in-app browser backend was unavailable. The private technical review handoff at `../_tools/strix-benchmark-20261008/PUBLICATION-TECHNICAL-REVIEW.md` records the evidence and review limit.

Do not push this branch into the GitHub Pages publishing branch as part of routine cleanup. Shane decides the publication batch after reading the page and the independent technical review.
