# tune-o-matic

A free, 100% client-side guitar tuner and intonation wizard. Runs entirely in
your browser — no accounts, no uploads, no tracking. Audio never leaves your
device.

**Live:** https://intonate.availfind.com/

## What it does

- **Chromatic tuner** — 4-string (bass, mandolin, ukulele), 6-string (12
  tunings incl. drop + open), 7-string, 12-string; A4 reference 432–440 Hz.
- **Intonation wizard** — walks you through tune open string → 12th-fret
  harmonic → fretted note, compares the cent offsets, and tells you which way
  to turn each saddle and roughly how far, iterated until you're within
  tolerance.
- **Analog meter** — raster VU face with a nonlinear scale (±3¢ occupies the
  inner fifth of the sweep), LED strobe ring, 14-segment note display with
  proper ♯/♭ symbols.
- **Guided tutorial** — a simulated, step-by-step walkthrough on the landing
  page. No microphone or audio access required.

## Running it

It's a single HTML file plus assets. Any static file server works:

```
python3 -m http.server 8088
```

Open `http://localhost:8088/`. Note: microphone capture requires a secure
context, so serve over HTTPS (or use localhost) for the tuner to see your
input device.

## Configuration

Tunables live in `config.json` next to `index.html`: sensitivity (input gate +
median filter), tuning tolerances, theme, LED colour, and accidental
preference (`auto` shows E♭/B♭ as flats, other accidentals as sharps). Edits
take effect on the next page load. Per-user overrides for tolerances are
available in the app's Advanced Options panel (localStorage).

## Privacy

Web Audio runs locally; pitch detection (YIN) happens in your browser. No
telemetry, no analytics, no cookies.

## License

MIT