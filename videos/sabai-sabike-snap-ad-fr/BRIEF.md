---
workflow: general-video
flow: automation
storyboard: no
message: "Réserve ton scooter à Phuket sur WhatsApp avant d'arriver — et on te le livre."
destination: snapchat
aspect: 1080x1920
language: fr
audience: "Vacanciers francophones sur le point d'arriver à Phuket"
length: 24.5s
---

## Intent

French version of the Sabai Sabike Snapchat ad. WhatsApp conversation opener
(text only), the fleet (model names only), an animated real map of Phuket that
zooms on a Patong -> Karon delivery, then the WhatsApp booking end card.

## Assets

- assets/fleet/*.jpg — the owner's real fleet photos (cropped, background plate blurred).
- assets/map/phuket-map.json — Phuket coastline from GSHHG full resolution (basemap-data-hires), built by tools/build_map.py. The Patong -> Karon route is an indicative trace over the hill road, not survey data.
- assets/sfx.wav — synthesised SFX, built by tools/build_sfx.py.

## Customizations

- Delivery map scene, Patong -> Karon (owner confirmed delivery anywhere in Phuket is possible).

## Notes

- Removed on request: photo bubble in the chat, captions under the bikes, "real bikes, real photos" collage.
- No prices, insurance or delivery fee claims. No WhatsApp number on screen (Snap CTA links to WhatsApp).
- Keep the bottom ~300px clear for Snapchat's CTA overlay.
