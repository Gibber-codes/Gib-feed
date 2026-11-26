"""Builds feed.json: hand-written cards + checked links. Run: python3 tools/seed.py
The daily refresh (tools/refresh.mjs) adds fresh RSS items on top of this."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "feed.json")

def yid(url):
    m = re.search(r"v=([\w-]{11})", url)
    return m.group(1) if m else None

# ---------- videos (checked links) ----------
V = [
 ("ai","3Blue1Brown","Large Language Models explained briefly","https://www.youtube.com/watch?v=LPZh9BOjkQs","A light intro to what LLMs are, how pretraining works, and what a transformer does.","8 min"),
 ("ai","3Blue1Brown","But what is a neural network?","https://www.youtube.com/watch?v=aircAruvnKk","Neurons, layers and the math behind the simplest neural network, drawn beautifully.","19 min"),
 ("ai","3Blue1Brown","Transformers, the tech behind LLMs","https://www.youtube.com/watch?v=wjZofJX0v4M","How a transformer turns words into vectors and predicts the next token.","27 min"),
 ("ai","3Blue1Brown","Attention in transformers, step-by-step","https://www.youtube.com/watch?v=eMlx5fFNoYc","Queries, keys, values and multi-head attention, shown visually.","26 min"),
 ("ai","3Blue1Brown","How might LLMs store facts","https://www.youtube.com/watch?v=9-Jl0dxWQs8","Where a fact like 'Michael Jordan plays basketball' might live inside the network.","23 min"),
 ("ai","3Blue1Brown","Backpropagation calculus","https://www.youtube.com/watch?v=tIeHLnjs5U8","The calculus of how a network learns from its mistakes.","10 min"),
 ("ai","Andrej Karpathy","[1hr Talk] Intro to Large Language Models","https://www.youtube.com/watch?v=zjkBMFhNj_g","A one-hour tour of what LLMs are, how they're trained and where they're going.","1 hr"),
 ("ai","Andrej Karpathy","Deep Dive into LLMs like ChatGPT","https://www.youtube.com/watch?v=7xTGNNLPyMI","The whole pipeline: pretraining, fine-tuning, RL, hallucinations, tool use. Watch in chunks.","3.5 hr"),
 ("ai","Andrej Karpathy","How I use LLMs","https://www.youtube.com/watch?v=EWvNQjAaOHw","Practical ways a top researcher uses chat models day to day.","2 hr"),
 ("ai","Andrej Karpathy","Let's build GPT: from scratch, in code, spelled out.","https://www.youtube.com/watch?v=kCc8FmEb1nY","Code a small GPT yourself. Your C/C# background makes this very doable.","2 hr"),
 ("ai","Andrej Karpathy","Building micrograd: neural networks and backprop spelled out","https://www.youtube.com/watch?v=VMj-3S1tku0","Build a tiny learning engine in ~100 lines and see exactly how backprop works.","2.5 hr"),
 ("ai","Welch Labs","The moment we stopped understanding AI [AlexNet]","https://www.youtube.com/watch?v=UZDiGooFs54","How one 2012 model kicked off the deep learning era.","18 min"),
 ("ai","Welch Labs","The Misconception that Almost Stopped AI","https://www.youtube.com/watch?v=NrO20Jb-hy0","Why training rarely gets stuck in 'local minima' when there are millions of dimensions.","20 min"),
 ("ai","Welch Labs","AI can't cross this line and we don't know why.","https://www.youtube.com/watch?v=5eqRuVp65eY","Scaling laws: the strange straight line that predicts how fast AI improves.","24 min"),
 ("ai","Welch Labs","The most complex model we actually understand","https://www.youtube.com/watch?v=D8GOeCFFby4","Inside an AI model researchers can explain end to end.","30 min"),
 ("ai","Welch Labs","Inside the World's Smartest Robot Brain [VLA]","https://www.youtube.com/watch?v=2mrGMMmrVNE","How vision-language-action models let robots see, understand and act.","25 min"),
 ("ai","Welch Labs","But how do AI images and videos actually work?","https://www.youtube.com/watch?v=iv-5mZ_9CPY","Diffusion models and CLIP: turning text into pictures by removing noise.","38 min"),
 ("ai","Two Minute Papers","DeepSeek's Insane New Architecture","https://www.youtube.com/watch?v=vIHw_2VjSUw","A new model architecture paper explained in minutes.","short"),
 ("ai","Two Minute Papers","DeepMind's AI Learns Locomotion From Scratch","https://www.youtube.com/watch?v=14zkfDTN_qo","Simulated bodies teach themselves to walk and run by trial and error.","short"),
 ("ai","Computerphile","Sleeper Agents in Large Language Models","https://www.youtube.com/watch?v=wL22URoMZjo","Models with hidden behaviour that stays dormant until a trigger shows up.","15 min"),
 ("ai","Computerphile","Why AI Tokens are so Expensive","https://www.youtube.com/watch?v=-0HRzXk8vlk","Why agents burn through so many tokens, and what that costs.","15 min"),
 ("ai","Computerphile","Glitch Tokens","https://www.youtube.com/watch?v=WO2X3oZEJOA","Weird tokens that make language models spit out gibberish.","15 min"),
 ("ai","Computerphile","AI Sandbagging","https://www.youtube.com/watch?v=pYP0ynR8h-k","Can a model pretend to be dumber on a test than it really is?","15 min"),
 ("ai","Computerphile","Ch(e)at GPT?","https://www.youtube.com/watch?v=XZJc1p6RE78","How you could hide a watermark in AI-written text.","15 min"),
 ("ai","Anthropic","Tracing the thoughts of a large language model","https://www.youtube.com/watch?v=Bj9BD2D3DzA","What researchers found when they looked inside Claude while it thinks.","short"),
 ("ai","Anthropic","What is interpretability?","https://www.youtube.com/watch?v=TxhhMTOTMDg","Why AI models are black boxes, and how people pry them open.","short"),
 ("ai","Anthropic","Mastering Claude Code in 30 minutes","https://www.youtube.com/watch?v=6eBSHbLKuN0","Workflows, shortcuts and power moves for the tool you build with every day.","30 min"),
 ("ai","Anthropic","Claude ran a business in our office","https://www.youtube.com/watch?v=5KTHvKCrQ00","Project Vend: what happened when an AI ran a little shop for real.","short"),
 ("ai","Anthropic","Anthropic's philosopher answers your questions","https://www.youtube.com/watch?v=I9aGC6Ui3eE","How an AI's character gets shaped, and the ethics behind it.","long"),
 ("ai","Kurzgesagt","AI Just Crossed the Terrifying Line - Now What?","https://www.youtube.com/watch?v=ujkD4SxPKOI","An animated look at where AI is heading and what it means.","short"),
 ("space","PBS Space Time","The Universe Has Been Expanding Since the Big Bang. Just Not How We Thought.","https://www.youtube.com/watch?v=eYViePMalJE","New survey hints that dark energy might be changing over time.","17 min"),
 ("space","PBS Space Time","What If (Tiny) Black Holes Are Everywhere?","https://www.youtube.com/watch?v=srVKjWn26AQ","Could microscopic black holes from the Big Bang be the dark matter?","17 min"),
 ("space","PBS Space Time","JWST May Have Discovered a New Cosmic Object: The Black Hole Star","https://www.youtube.com/watch?v=mxpuV33vpNk","Strange early-universe objects the Webb telescope keeps finding.","17 min"),
 ("physics","PBS Space Time","Is The Future Predetermined By Quantum Mechanics?","https://www.youtube.com/watch?v=1JCRDaa3ehk","Superdeterminism, quantum measurement and free will.","17 min"),
 ("physics","PBS Space Time","What If Space And Time Are NOT Real?","https://www.youtube.com/watch?v=SN8nTQiWOYY","Ideas that spacetime emerges from something deeper.","17 min"),
 ("physics","Veritasium","The Most Misunderstood Concept in Physics","https://www.youtube.com/watch?v=DxL2HoqLbyA","What entropy really is, and why time only runs one way.","27 min"),
 ("science","Veritasium","Once you understand game theory, you understand the world.","https://www.youtube.com/watch?v=mScpHTIi-kM","The prisoner's dilemma and why cooperation wins in the long run.","27 min"),
 ("science","Veritasium","Math's Fundamental Flaw","https://www.youtube.com/watch?v=HeQX2HjkcNo","Gödel: some true things can never be proven.","34 min"),
 ("space","Veritasium","White holes and wormholes are probably real. Here's why.","https://www.youtube.com/watch?v=6akmv1bsz1M","What Einstein's equations say happens inside a black hole.","30 min"),
 ("science","Veritasium","The line that broke mathematicians for 2000 years","https://www.youtube.com/watch?v=lFlu60qs7_4","One 'obvious' rule about parallel lines that turned out to be optional.","30 min"),
 ("space","Kurzgesagt","Black Holes Explained – From Birth to Death","https://www.youtube.com/watch?v=e-P5IFTqB98","How black holes form, grow, and eventually evaporate.","6 min"),
 ("science","Kurzgesagt","The Immune System Explained I – Bacteria Infection","https://www.youtube.com/watch?v=zQGOcOUBi6s","Your body's defence army, animated.","7 min"),
 ("science","Kurzgesagt","The Egg - A Short Story","https://www.youtube.com/watch?v=h6fcK_fRYaI","Andy Weir's mind-bending short story, animated.","8 min"),
 ("physics","minutephysics","General Relativity Explained in 7 Levels of Difficulty","https://www.youtube.com/watch?v=eNhJY-R3Gwg","Gravity as curved spacetime, from easy to hard.","short"),
 ("physics","minutephysics","Why is Relativity Hard?","https://www.youtube.com/watch?v=1rLWVZVWfdY","Why special relativity feels wrong, and how to think about it.","short"),
 ("physics","minutephysics","Spacetime Diagrams","https://www.youtube.com/watch?v=hTxWAQGgeQw","The one drawing that makes relativity click.","short"),
 ("physics","minutephysics","Relativity of Simultaneity","https://www.youtube.com/watch?v=SrNVsfkGW-0","Why 'at the same time' depends on who's moving.","short"),
]

# ---------- AI Hero (checked links) ----------
H = [
 ("skill","AI Hero","/grill-me: stress-test an idea","https://www.aihero.dev/skills-grill-me","A skill that makes the agent interview you hard about a plan before you build. Perfect for an idea person: run it on your next game idea."),
 ("skill","AI Hero","/to-spec then /to-tickets","https://www.aihero.dev/skills-to-spec","Turn a chat into a written spec, then into small tickets an agent can build one by one. Basically what your Silk Boards cards are."),
 ("skill","AI Hero","/implement: test-first building","https://www.aihero.dev/skills-implement","The agent writes the test first, watches it fail, then writes code until it passes. Fewer 'it said it works' moments."),
 ("skill","AI Hero","/handoff: pass work to the next agent","https://www.aihero.dev/skills-handoff","Summarizes a long session so a fresh agent can pick it up without losing the plot."),
 ("skill","AI Hero","/wait-what: plain English please","https://www.aihero.dev/skills-wait-what","Makes the agent restate its last answer in plain words. Use it whenever an answer reads like soup."),
 ("skill","AI Hero","/diagnosing-bugs","https://www.aihero.dev/skills-diagnosing-bugs","Start from a failing repro, then hunt the bug like a mechanic: isolate, test, confirm."),
 ("skill","AI Hero","/prototype: answer it with throwaway code","https://www.aihero.dev/skills-prototype","When you can't decide a design, build a quick throwaway version and look at it."),
 ("skill","AI Hero","/teach: learn a topic over sessions","https://www.aihero.dev/skills-teach","Turns the agent into a tutor that builds lessons on top of each other. Good pair with this feed."),
 ("skill","AI Hero","All 27 skills in one place","https://www.aihero.dev/skills","The full menu, with install steps for Claude Code."),
 ("read","AI Hero","The Home Repo Pattern","https://www.aihero.dev/the-home-repo-pattern","Keep your skills, AGENTS.md and shared docs in one repo that points at all your other repos. Fits Gibber Hub nicely."),
 ("read","AI Hero","Watch me ship a 21,000-line feature with mattpocock/skills","https://www.aihero.dev/watch-me-ship-a-21-000-line-feature-with-mattpocock-skills~ez95n","A full walkthrough: grilling, specs, letting agents build while away, then review."),
 ("read","AI Hero","Armin Ronacher and Mario Zechner on Coding With Agents","https://www.aihero.dev/armin-ronacher-and-mario-zechner-on-coding-with-agents~fn8vd","Two well-known devs on where coding agents fall short and how much code they still read."),
 ("read","AI Hero","AI Coding Dictionary","https://www.aihero.dev/ai-coding-dictionary","AI words translated into plain English. Each term is short enough to read on the toilet."),
 ("read","AI Hero","Dictionary: Harness","https://www.aihero.dev/ai-coding-dictionary/harness","The tools, system prompt and context around a model that turn it into an agent. Claude Code is a harness."),
 ("read","AI Hero","Dictionary: Prefix cache","https://www.aihero.dev/ai-coding-dictionary/prefix-cache","Why repeating the same start of a prompt makes requests cheaper and faster."),
 ("read","AI Hero","Dictionary: Context window","https://www.aihero.dev/ai-coding-dictionary/context-window","Everything the model can see at once, and why it runs out."),
]

# ---------- blogs to follow ----------
B = [
 ("Simon Willison's Weblog","https://simonwillison.net","Near-daily hands-on notes on new AI tools and models. The best single feed for 'what's new and does it actually work'."),
 ("Lil'Log (Lilian Weng)","https://lilianweng.github.io","Long, clear deep-dives on agents, LLMs and reinforcement learning. Save for a slow evening."),
 ("Latent Space","https://www.latent.space","AI engineering essays and a podcast about building with models."),
 ("Hugging Face Blog","https://huggingface.co/blog","Open models you can run on your own desktop build, with tutorials."),
 ("Quanta Magazine","https://www.quantamagazine.org","Top-tier science and math stories written for curious people, not experts."),
 ("One Useful Thing","https://www.oneusefulthing.org","Ethan Mollick on practical ways to use AI for real work."),
 ("Interconnects","https://www.interconnects.ai","Nathan Lambert on open models and how models get trained after pretraining."),
 ("Import AI","https://importai.substack.com","Jack Clark's weekly roundup of AI research."),
]

# ---------- explainers (written for this feed) ----------
I = [
 ("ai","A model only does one thing","Every chat model does exactly one move: guess the next token, add it, repeat. Code, essays, jokes, all of it is that loop running thousands of times.","Next time an answer streams in, you're watching the loop live."),
 ("ai","Tokens aren't words","A token is a chunk of text, often part of a word. 'Unbelievable' might be 3 tokens. Roughly, 1,000 tokens is about 750 English words.","That's why limits and prices are counted in tokens, not words."),
 ("ai","Embeddings: words as directions","Models turn each token into a long list of numbers, a point in a space with thousands of dimensions. Similar meanings land near each other.","Famous trick: king minus man plus woman lands close to queen."),
 ("ai","Attention, in one picture","Each word asks every earlier word 'are you relevant to me?' and blends in the answers. In 'the engine seized because it overheated', attention links 'it' back to 'engine'.","That one mechanism is the T in GPT."),
 ("ai","Training vs inference","Training sets the billions of numbers once, using huge amounts of text and compute. Inference is just using those frozen numbers to answer you.","Your chat never changes the model's weights."),
 ("ai","Why models 'hallucinate'","A model always produces the most likely-sounding next token, even when it doesn't actually know. Confident and wrong look the same from the inside.","Fix: give it the real source (docs, files) in context, or let it search."),
 ("ai","Agents = model + tools + loop","An agent is a model that can call tools (read a file, run a command), see the result, and decide the next step, over and over until done.","Claude Code is an agent; the model inside it is the brain, the harness is the body."),
 ("ai","Context is the whole game","A model only knows what's in its context window right now, plus what it learned in training. Good results mostly come from giving it the right context.","That's why CLAUDE.md files and clear specs make agents way better."),
 ("ai","Temperature","Temperature controls how random the next-token pick is. Low = predictable and repetitive. High = creative and sometimes unhinged.","For code you want low; for brainstorming game ideas, higher."),
 ("ai","Fine-tuning vs prompting","Prompting changes what you say to the model. Fine-tuning changes the model itself with extra training on your examples.","Most apps never need fine-tuning: a good prompt plus the right context wins."),
 ("ai","RAG in one line","Retrieval-augmented generation: search your own docs first, paste the best chunks into the prompt, then ask. The model answers from your stuff.","A 'chat with my manual' app for your mechanic work would be RAG."),
 ("ai","RLHF: how chatbots learn manners","After pretraining, people rank model answers, and the model is trained to prefer the higher-ranked style. That's a big part of why assistants feel helpful.","Raw pretrained models just continue text; they don't 'answer'."),
 ("ai","Scaling laws","Bigger models trained on more data with more compute get predictably better, along a smooth curve. That predictability is why companies spend billions.","Welch Labs has a great video on this in the feed."),
 ("ai","Run models on your own PC","Open-weight models can run locally on a good GPU with tools like Ollama or LM Studio. Smaller 'quantized' versions squeeze into less video memory.","Rule of thumb: VRAM decides which model sizes you can run."),
 ("ai","Quantization","Storing a model's numbers with fewer bits (like 4-bit instead of 16-bit) makes it much smaller and faster, losing a little quality.","It's how big models fit on a gaming GPU."),
 ("ai","Diffusion: art from noise","Image models start with pure static and remove noise step by step, steered by your text prompt, until a picture appears.","Same idea now powers AI video."),
 ("ai","MCP: plugs for AI","The Model Context Protocol is a standard way to give an AI tools and data, like a USB port. Your Silk Boards board talks to Claude through it.","Build one MCP server and every MCP-aware app can use it."),
 ("ai","Interpretability","Researchers look inside models to find 'features', directions in the numbers that mean things like 'Golden Gate Bridge' or 'code bug'.","Turning a feature up or down actually changes how the model behaves."),
 ("ai","Mixture of experts","Some big models are split into many 'experts' and only a few run for each token. Huge total size, but each answer only uses a slice.","That's how some models are giant yet still fast."),
 ("ai","Reasoning models","Newer models can 'think' in hidden tokens before answering. More thinking costs more tokens but cracks harder problems.","That's the 'effort' setting you see in some tools."),
 ("physics","Light takes time","Sunlight is about 8 minutes old when it hits you. Light from the nearest star past the Sun left it over 4 years ago.","Looking far away is looking back in time."),
 ("physics","GPS needs relativity","Satellite clocks run fast by about 38 microseconds a day: weaker gravity speeds them up more than their speed slows them down. Without correcting it, GPS would drift several miles a day.","Einstein is in your phone's map app."),
 ("physics","Quantum tunneling","Tiny particles can pass through barriers they don't have the energy to climb over, because they behave like spread-out waves.","The Sun only shines because protons tunnel close enough to fuse."),
 ("physics","Entropy is just counting","There are vastly more messy arrangements than neat ones, so things drift toward messy. That's the second law of thermodynamics.","It's also why your shop never cleans itself."),
 ("physics","Why the sky is blue","Air molecules scatter short blue wavelengths much more than red ones, so blue light comes at you from every direction.","Sunsets go orange because the light crosses so much air the blue gets scattered away."),
 ("physics","E = mc²","A tiny bit of mass holds a huge amount of energy because c² is enormous. One gram of mass is roughly the energy of a 20-kiloton bomb.","Nuclear power runs on turning a sliver of mass into heat."),
 ("physics","Superposition","Before it's measured, a quantum particle isn't secretly in one state; its description is a mix of possibilities that can interfere with each other.","Quantum computers exploit that interference to do certain math faster."),
 ("physics","Torque, the physics way","Torque is force times the distance from the pivot. Double the wrench length and you get double the twist for the same push.","A breaker bar is just physics you can hold."),
 ("physics","Why engines need gears","An engine makes useful power only in a band of RPM. Gears trade speed for torque so the engine stays in that band from a stop to highway speed.","First gear: lots of torque, little speed. Top gear: the reverse."),
 ("physics","Absolute zero","At −273.15 °C, particles would have the least motion physics allows. You can get within billionths of a degree but never reach it.","Labs do this to make atoms act like one giant quantum wave."),
 ("space","Neutron stars","A neutron star packs more than the Sun's mass into a ball about the size of a city. A teaspoon would weigh billions of tons.","Some spin hundreds of times a second."),
 ("space","Black holes evaporate","Hawking showed black holes slowly leak radiation and shrink. A big one would take far longer than the current age of the universe.","Kurzgesagt's black hole video in the feed covers the whole life story."),
 ("space","The universe is speeding up","Distant galaxies are flying apart faster over time. Whatever pushes that is called dark energy, and nobody knows what it is.","New surveys hint it might even be changing."),
 ("space","Most of the universe is invisible","Ordinary matter (atoms, stars, you) is only about 5% of everything. The rest is dark matter and dark energy.","We know dark matter is there because galaxies spin too fast without it."),
 ("space","Days on Venus","Venus turns so slowly that its day is longer than its year, and it spins backwards compared to most planets.","Sunrise there is in the west."),
 ("science","Your brain runs on ~20 watts","The human brain uses about as much power as a dim light bulb, while training a big AI model can use as much electricity as hundreds or even thousands of homes use in a year.","Nature still wins on efficiency."),
 ("science","Gödel in one breath","In any math system rich enough to do arithmetic, there are true statements it can never prove.","Veritasium's 'Math's Fundamental Flaw' is the long version."),
 ("science","Game theory: tit for tat","In repeated prisoner's dilemma tournaments, a simple strategy won: cooperate first, then copy what the other player did last time.","Be nice, retaliate, forgive, be clear."),
 ("build","Code tip: one change, then test","Agents and people both break less when each change is small and checked before the next one. Big-bang changes hide the bug.","Same as wrenching: swap one part, then start it."),
 ("build","Git worktrees","A worktree lets one repo have several folders checked out on different branches at once. Agents can work on two cards side by side without stepping on each other.","Handy with several Claude sessions running."),
 ("build","Tailscale in one line","Tailscale builds a private network between your devices, so your phone reaches your PC at a fixed 100.x address from anywhere.","It's how your launcher talks to Gibber Hub."),
 ("build","PWA = website that installs","A progressive web app has a manifest and a service worker, so the browser can install it with its own icon and run it full screen, even offline.","This feed is one."),
]

cards = []
def add(c):
    c["id"] = f"c{len(cards)+1:03d}"
    cards.append(c)

for t, ch, title, url, body, length in V:
    add({"type":"video","topic":t,"title":title,"body":body,"source":ch,"url":url,"vid":yid(url),"len":length})
for kind, src, title, url, body in H:
    add({"type":kind,"topic":"ai","title":title,"body":body,"source":src,"url":url})
for name, url, body in B:
    add({"type":"follow","topic":"ai" if name!="Quanta Magazine" else "science","title":name,"body":body,"source":"Worth following","url":url})
for t, title, body, kicker in I:
    add({"type":"idea","topic":t,"title":title,"body":body,"kicker":kicker,"source":"GibberFeed"})

feed = {
  "name":"GibberFeed",
  "updated":"2026-11-25",
  "sources":{
    "youtube":[
      {"name":"Sleep On Physics","id":"UCuKoEFuLJL1Q8HUqXC70RjQ","topic":"physics"},
      {"name":"3Blue1Brown","id":"UCYO_jab_esuFRV4b17AJtAw","topic":"ai"},
      {"name":"Andrej Karpathy","id":"UCXUPKJO5MZQN11PqgIvyuvQ","topic":"ai"},
      {"name":"Welch Labs","id":"UConVfxXodg78Tzh5nNu85Ew","topic":"ai"},
      {"name":"Two Minute Papers","id":"UCbfYPyITQ-7l4upoX8nvctg","topic":"ai"},
      {"name":"Computerphile","id":"UC9-y-6csu5WGm29I7JiwpnA","topic":"ai"},
      {"name":"Anthropic","id":"UCrDwWp7EBBv4NwvScIpBDOA","topic":"ai"},
      {"name":"PBS Space Time","id":"UC7_gcs09iThXybpVgjHZ_7g","topic":"space"},
      {"name":"Veritasium","id":"UCHnyfMqiRRG1u-2MsSQLbXA","topic":"science"},
      {"name":"Kurzgesagt","id":"UCsXVk37bltHxD1rDPwtNM8Q","topic":"science"},
      {"name":"minutephysics","id":"UCUHW94eEFW7hkUMVaZz4eDg","topic":"physics"}
    ],
    "rss":[
      {"name":"AI Hero","url":"https://www.aihero.dev/rss.xml","topic":"ai"},
      {"name":"Simon Willison","url":"https://simonwillison.net/atom/everything/","topic":"ai"},
      {"name":"Lil'Log","url":"https://lilianweng.github.io/index.xml","topic":"ai"},
      {"name":"Hugging Face","url":"https://huggingface.co/blog/feed.xml","topic":"ai"},
      {"name":"Quanta Magazine","url":"https://www.quantamagazine.org/feed/","topic":"science"}
    ]
  },
  "cards":cards
}
with open(OUT,"w") as f:
    json.dump(feed,f,ensure_ascii=False,indent=1)
print(len(cards),"cards ->",os.path.abspath(OUT))
