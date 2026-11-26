// Pulls the newest videos and posts from the sources listed in feed.json and adds them as cards.
// Run: node tools/refresh.mjs   (Node 18+, no installs). The GitHub Action runs it every morning.
import { readFile, writeFile } from "node:fs/promises";

const FILE = new URL("../feed.json", import.meta.url);
const PER_SOURCE = 6;      // newest items taken from each source per run
const KEEP_FRESH = 160;    // most fetched cards kept in the feed

const feed = JSON.parse(await readFile(FILE, "utf8"));
const seeded = feed.cards.filter(c => !c.fetched);
const old = feed.cards.filter(c => c.fetched);
const known = new Set(feed.cards.map(c => c.url));

const ent = s => s.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;|&#x27;|&apos;/g, "'")
  .replace(/&ldquo;|&rdquo;/g, '"').replace(/&lsquo;|&rsquo;/g, "'").replace(/&mdash;/g, "—").replace(/&ndash;/g, "–").replace(/&nbsp;/g, " ")
  .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n)).replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16))).replace(/&amp;/g, "&");
// unescape first (feeds often escape their HTML), then strip tags, then unescape what's left
const decode = s => ent(ent((s || "").replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1")).replace(/<[^>]+>/g, " "))
  .replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
// first real sentence: skip links, sponsor lines and emoji-led promos
const firstSentence = s => (s.split(/(?<=[.!?])\s|\n/).map(x => x.trim())
  .find(x => x.length > 25 && (x.match(/,/g) || []).length < 5 && !/\b(Dr|Mr|Ms|Prof)\.$/.test(x) && !/https?:|sponsor|check out|patreon|sign up|subscribe/i.test(x) && !/^\p{Extended_Pictographic}/u.test(x)) || "");
const tag = (xml, name) => { const m = xml.match(new RegExp(`<${name}[^>]*>([\\s\\S]*?)</${name}>`)); return m ? m[1] : ""; };
const short = (s, n) => s.length > n ? s.slice(0, s.lastIndexOf(" ", n)) + "…" : s;

async function get(url) {
  const r = await fetch(url, { headers: { "user-agent": "GibberFeed/1.0 (personal feed reader)" } });
  if (!r.ok) throw new Error(r.status + " " + url);
  return r.text();
}

const fresh = [];
for (const ch of feed.sources.youtube || []) {
  try {
    const xml = await get(`https://www.youtube.com/feeds/videos.xml?channel_id=${ch.id}`);
    const entries = xml.split("<entry>").slice(1, PER_SOURCE + 1);
    for (const e of entries) {
      const vid = tag(e, "yt:videoId"), url = `https://www.youtube.com/watch?v=${vid}`;
      if (!vid || known.has(url)) continue;
      const raw = tag(e, "media:description").replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1");
      const desc = firstSentence(ent(raw).replace(/<[^>]+>/g, " ")) || "New from " + ch.name;
      fresh.push({ type: "video", topic: ch.topic, title: decode(tag(e, "title")), body: short(desc, 220),
        source: ch.name, url, vid, date: tag(e, "published"), fetched: true });
      known.add(url);
    }
  } catch (err) { console.warn("skip", ch.name, err.message); }
}
for (const src of feed.sources.rss || []) {
  try {
    const xml = await get(src.url);
    const parts = xml.includes("<entry") ? xml.split(/<entry[\s>]/).slice(1) : xml.split(/<item[\s>]/).slice(1);
    for (const e of parts.slice(0, PER_SOURCE)) {
      let url = decode(tag(e, "link"));
      if (!url) { const m = e.match(/<link[^>]*href="([^"]+)"/); url = m ? m[1] : ""; }
      if (!/^https:\/\//.test(url) || known.has(url)) continue;
      const body = decode(tag(e, "description") || tag(e, "summary") || tag(e, "content"));
      fresh.push({ type: "read", topic: src.topic, title: decode(tag(e, "title")), body: short(firstSentence(body) || body.replace(/https?:\S+/g, "").trim() || "New post from " + src.name, 220),
        source: src.name, url, date: tag(e, "pubDate") || tag(e, "updated") || tag(e, "published"), fetched: true });
      known.add(url);
    }
  } catch (err) { console.warn("skip", src.name, err.message); }
}

const stamp = Date.now();
fresh.forEach((c, i) => { c.id = `f${stamp}_${i}`; c.fresh = true; });
old.forEach(c => { delete c.fresh; });
const fetched = [...fresh, ...old].slice(0, KEEP_FRESH);
feed.cards = [...fetched, ...seeded];
feed.updated = new Date().toISOString().slice(0, 10);
await writeFile(FILE, JSON.stringify(feed, null, 1));
console.log(`added ${fresh.length} new cards, ${feed.cards.length} total`);
