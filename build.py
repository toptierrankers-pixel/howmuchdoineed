#!/usr/bin/env python3
"""
HowMuchDoINeed site generator.
Edit BASE and the CALCS list, then run:  python3 build.py
Emits: <slug>.html for each calculator, index.html, sitemap.xml, robots.txt.
Shared assets (styles.css, engine.js, favicons, logo) live in assets/ and are not touched here.
"""
import json, html

# ---- change this to your real domain (no trailing slash) ----
BASE = "https://howmuchdoineed.toptierrankers.workers.dev"
SITE = "HowMuchDoINeed"
FAVV = "3"
BUILD = "2026-07-26 v8 - 25 calculators + 7 guides"

ANALYTICS_TOKEN = ""  # paste your Cloudflare Web Analytics token here, then rebuild, to enable

def analytics():
    if not ANALYTICS_TOKEN:
        return ""
    return ('\n<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
            'data-cf-beacon=\'{"token": "' + ANALYTICS_TOKEN + '"}\'></script>')
   # favicon cache-buster; bump when the icon changes

MARK = ('<svg class="brandmark" viewBox="0 0 64 64" width="24" height="24" aria-hidden="true">'
    '<rect x="4" y="4" width="56" height="56" rx="13" fill="#16181A"/>'
    '<polygon points="32,14 50,24 32,34 14,24" fill="#F6C463"/>'
    '<polygon points="14,24 32,34 32,50 14,40" fill="#E39A0C"/>'
    '<polygon points="50,24 50,40 32,50 32,34" fill="#A86E05"/></svg>')

# ---------------------------------------------------------------------------
# Calculator content. Each entry is self-contained.
# fields: list of dicts -> rendered inputs. compute: JS function body (uses v, H).
# ---------------------------------------------------------------------------
CALCS = [
 {
  "slug":"gravel","cat":"Aggregates · Landscaping","name":"Gravel",
  "grid":"Driveways, paths & drainage",
  "title":"Gravel Calculator: How Much Gravel Do I Need?",
  "desc":"Free gravel calculator. Enter length, width, and depth to get cubic yards, cubic feet, and tons of gravel needed, with a waste factor built in.",
  "lede":"Work out how much gravel you need for a driveway, path, or drainage bed. Enter the area and depth to get cubic yards, cubic feet, and approximate tonnage.",
  "inputs_heading":"Your measurements",
  "howto":["Gravel is sold by volume (cubic yards) or by weight (tons). Both start from length times width times depth. Because depth is usually in inches, divide it by 12 to convert to feet before multiplying.",
           "The 1.4 figure is the rough density of common gravel, about 1.4 tons per cubic yard. Pea gravel, crushed stone, and road base run slightly heavier or lighter, so confirm the exact density with your supplier before ordering by weight."],
  "formula":"cubic feet = length (ft) × width (ft) × depth (in) ÷ 12\ncubic yards = cubic feet ÷ 27\ntons ≈ cubic yards × 1.4",
  "ex_title":"A 20 ft × 10 ft path, 3 inches deep",
  "ex_steps":["Volume in cubic feet: 20 × 10 × (3 ÷ 12) = <strong>50 ft³</strong>",
              "Convert to cubic yards: 50 ÷ 27 = <strong>1.85 yd³</strong>",
              "Add a 10% waste factor: 1.85 × 1.10 = <strong>2.04 yd³</strong>",
              "Convert to tons: 2.04 × 1.4 = <strong>2.85 tons</strong>"],
  "ex_answer":"Order about 2 cubic yards (about 2.9 tons) of gravel.",
  "table_intro":"How far one cubic yard spreads depends on depth. Typical depths:",
  "table":[["Use","Depth","1 yd³ covers"],
           ["Walking path","2 in","162 sq ft"],
           ["Garden / decorative bed","2-3 in","108-162 sq ft"],
           ["Driveway (top layer)","3-4 in","81-108 sq ft"],
           ["Driveway (full base)","6 in","54 sq ft"]],
  "faqs":[["How many tons are in a cubic yard of gravel?","Roughly 1.4 tons for typical gravel, ranging from about 1.4 to 1.5 depending on stone type, size, and moisture. Crushed stone sits at the heavier end."],
          ["How deep should gravel be?","Two inches suits a light path or decorative bed. A driveway needs more: about 4 inches for a top layer over an existing base, or up to 6 inches for a base built from scratch."],
          ["Why add a waste factor?","Ground is never perfectly flat, gravel compacts as it settles, and some is lost in handling. Adding 5 to 10% means you will not run short partway through the job."],
          ["Should I order by volume or weight?","Suppliers may quote either. Cubic yards describe the space to fill; tons describe what goes on the truck. Order by tonnage, and keep the cubic-yard figure to sanity-check the delivery."]],
  "fields":[["length","Length","ft",20,0.5],["width","Width","ft",10,0.5],["depth","Depth","in",3,0.5],["waste","Waste factor","%",10,1]],
  "compute":"""var f=1+v.waste/100;var cf=v.length*v.width*(v.depth/12)*f;var cy=cf/27,tons=cy*1.4;
return{label:"Gravel needed",value:H.fmt(cy,2),unit:"cubic yards",lines:[{label:"Volume",value:H.fmt(cf,1)+" ft\\u00B3"},{label:"Weight (approx)",value:H.fmt(tons,2)+" tons"},{label:"Includes waste",value:v.waste+"%"}],note:"Tonnage assumes ~1.4 t/yd\\u00B3 for typical gravel. Confirm density with your supplier."};""",
 },
 {
  "slug":"sand","cat":"Aggregates · Landscaping","name":"Sand",
  "grid":"Bedding, fill & paver sand",
  "title":"Sand Calculator: How Much Sand Do I Need?",
  "desc":"Free sand calculator. Enter length, width, and depth to get cubic yards, cubic feet, and tons of sand for bedding, fill, or paver joints.",
  "lede":"Estimate sand for paver bedding, pipe backfill, or a play area. Enter the area and depth to get cubic yards, cubic feet, and approximate tonnage.",
  "inputs_heading":"Your measurements",
  "howto":["Sand is measured by volume, then converted to tons for delivery. Multiply length by width by depth, converting depth from inches to feet, and divide into cubic yards.",
           "Dry sand runs about 1.35 tons per cubic yard. Damp or wet sand weighs noticeably more, so order to the heavier side if it has been rained on."],
  "formula":"cubic feet = length (ft) × width (ft) × depth (in) ÷ 12\ncubic yards = cubic feet ÷ 27\ntons ≈ cubic yards × 1.35",
  "ex_title":"A 10 ft × 10 ft paver base, 1 inch of bedding sand",
  "ex_steps":["Volume in cubic feet: 10 × 10 × (1 ÷ 12) = <strong>8.3 ft³</strong>",
              "Convert to cubic yards: 8.3 ÷ 27 = <strong>0.31 yd³</strong>",
              "Add a 10% waste factor: 0.31 × 1.10 = <strong>0.34 yd³</strong>",
              "Convert to tons: 0.34 × 1.35 = <strong>0.46 tons</strong>"],
  "ex_answer":"Order about a third of a cubic yard of bedding sand.",
  "table_intro":"Common sand depths by job:",
  "table":[["Use","Depth","Notes"],
           ["Paver bedding","1 in","Screeded smooth"],
           ["Under a play set","3-6 in","Cushioning layer"],
           ["Pipe / trench backfill","varies","Follow the spec"],
           ["Leveling course","0.5-1 in","Thin and even"]],
  "faqs":[["How many tons is a cubic yard of sand?","About 1.35 tons dry. Moisture adds weight fast, so damp sand can reach 1.5 tons or more per cubic yard."],
          ["What sand goes under pavers?","A coarse concrete or bedding sand, screeded to about one inch. Fine masonry sand shifts too easily and is not recommended for a bedding layer."],
          ["How much sand for paver joints?","Joint filling uses far less than bedding, usually a bag or two of polymeric sand per 100 square feet depending on joint width."],
          ["Does sand settle?","Yes, especially when it gets wet. Compact bedding sand before laying pavers and expect a small drop over time."]],
  "fields":[["length","Length","ft",10,0.5],["width","Width","ft",10,0.5],["depth","Depth","in",1,0.5],["waste","Waste factor","%",10,1]],
  "compute":"""var f=1+v.waste/100;var cf=v.length*v.width*(v.depth/12)*f;var cy=cf/27,tons=cy*1.35;
return{label:"Sand needed",value:H.fmt(cy,2),unit:"cubic yards",lines:[{label:"Volume",value:H.fmt(cf,1)+" ft\\u00B3"},{label:"Weight (approx)",value:H.fmt(tons,2)+" tons"},{label:"Includes waste",value:v.waste+"%"}],note:"Tonnage assumes ~1.35 t/yd\\u00B3 for dry sand; damp sand weighs more."};""",
 },
 {
  "slug":"crushed-stone","cat":"Aggregates · Landscaping","name":"Crushed Stone",
  "grid":"Base rock & #57 stone",
  "title":"Crushed Stone Calculator: How Much Do I Need?",
  "desc":"Free crushed stone calculator. Enter length, width, and depth to get cubic yards and tons of crushed stone or base rock, with a waste factor built in.",
  "lede":"Estimate crushed stone for a base layer, drainage, or a #57 stone fill. Enter the area and depth to get cubic yards and approximate tonnage.",
  "inputs_heading":"Your measurements",
  "howto":["Crushed stone is priced by volume or by weight. Multiply length by width by depth, convert depth to feet, then divide into cubic yards or tons.",
           "Most crushed stone runs about 1.4 tons per cubic yard. Dense grades like crusher run pack heavier than open, clean stone such as #57, so confirm the product density before ordering."],
  "formula":"cubic feet = length (ft) × width (ft) × depth (in) ÷ 12\ncubic yards = cubic feet ÷ 27\ntons ≈ cubic yards × 1.4",
  "ex_title":"A 24 ft × 12 ft base, 4 inches deep",
  "ex_steps":["Volume in cubic feet: 24 × 12 × (4 ÷ 12) = <strong>96 ft³</strong>",
              "Convert to cubic yards: 96 ÷ 27 = <strong>3.56 yd³</strong>",
              "Add a 10% waste factor: 3.56 × 1.10 = <strong>3.91 yd³</strong>",
              "Convert to tons: 3.91 × 1.4 = <strong>5.48 tons</strong>"],
  "ex_answer":"Order about 4 cubic yards (about 5.5 tons) of crushed stone.",
  "table_intro":"Common grades and where they go:",
  "table":[["Grade","Typical use","Note"],
           ["Crusher run","Compacted base","Packs hard"],
           ["#57 stone","Drainage, driveways","Clean, drains well"],
           ["#411","Driveway top","Base plus fines"],
           ["#8 pea-size","Paths, fill","Small, loose"]],
  "faqs":[["How many tons in a cubic yard of crushed stone?","About 1.4 tons on average. Dense crusher run sits a little higher; clean open stone a little lower."],
          ["What is #57 stone?","A clean, roughly three-quarter-inch stone with the fines screened out. It drains well, which makes it popular for driveways, drains, and pipe bedding."],
          ["How deep for a driveway base?","Plan on 4 inches of compacted base for a residential driveway, more over soft or clay soils. Build it up in layers and compact each one."],
          ["Crusher run or clean stone?","Crusher run compacts into a solid base because it contains fines. Clean stone like #57 stays loose and drains, so it is used where water needs to move through."]],
  "fields":[["length","Length","ft",24,0.5],["width","Width","ft",12,0.5],["depth","Depth","in",4,0.5],["waste","Waste factor","%",10,1]],
  "compute":"""var f=1+v.waste/100;var cf=v.length*v.width*(v.depth/12)*f;var cy=cf/27,tons=cy*1.4;
return{label:"Crushed stone",value:H.fmt(cy,2),unit:"cubic yards",lines:[{label:"Volume",value:H.fmt(cf,1)+" ft\\u00B3"},{label:"Weight (approx)",value:H.fmt(tons,2)+" tons"},{label:"Includes waste",value:v.waste+"%"}],note:"Tonnage assumes ~1.4 t/yd\\u00B3; crusher run packs heavier than clean stone."};""",
 },
 {
  "slug":"paver-base","cat":"Aggregates · Landscaping","name":"Paver Base",
  "grid":"Base + bedding under pavers",
  "title":"Paver Base Calculator: How Much Base & Sand?",
  "desc":"Free paver base calculator. Enter your patio size plus base and bedding depths to get cubic yards of crushed stone base and bedding sand.",
  "lede":"Plan the materials under a paver patio or walkway. Enter the area, base depth, and bedding depth to get cubic yards of base stone and bedding sand.",
  "inputs_heading":"Patio dimensions",
  "howto":["A paver installation is two layers: a compacted crushed-stone base for strength, and a thin bedding sand layer the pavers sit in. Each is area times depth, converted to cubic yards.",
           "A typical patio uses about 4 to 6 inches of base and 1 inch of bedding sand. Heavier loads or soft soil call for a deeper base."],
  "formula":"base yd³ = area (ft²) × base depth (in) ÷ 12 ÷ 27\nsand yd³ = area (ft²) × bedding depth (in) ÷ 12 ÷ 27",
  "ex_title":"A 12 ft × 10 ft patio, 4 in base, 1 in sand",
  "ex_steps":["Area: 12 × 10 = <strong>120 ft²</strong>",
              "Base: 120 × (4 ÷ 12) ÷ 27 = <strong>1.48 yd³</strong>",
              "Bedding sand: 120 × (1 ÷ 12) ÷ 27 = <strong>0.37 yd³</strong>",
              "With 10% waste: base <strong>1.63 yd³</strong>, sand <strong>0.41 yd³</strong>"],
  "ex_answer":"Order about 1.6 yd³ of base stone and half a yard of bedding sand.",
  "table_intro":"Suggested base depth by use:",
  "table":[["Use","Base depth","Bedding"],
           ["Walkway / patio (foot traffic)","4 in","1 in"],
           ["Patio over soft soil","6 in","1 in"],
           ["Driveway (light vehicle)","8-12 in","1 in"],
           ["Firepit / seating pad","4 in","1 in"]],
  "faqs":[["What goes under pavers?","A compacted crushed-stone base for load spreading, then about one inch of coarse bedding sand that the pavers are set into and leveled on."],
          ["How thick should the base be?","Four inches for patios and walkways, six or more over soft soil, and eight to twelve inches for anything carrying vehicle weight."],
          ["How much bedding sand do I need?","Enough for a consistent one-inch screeded layer. More than that lets pavers settle unevenly."],
          ["Do I need to compact the base?","Yes. Compact the base in layers with a plate compactor before spreading bedding sand, or the surface will sink over time."]],
  "fields":[["length","Length","ft",12,0.5],["width","Width","ft",10,0.5],["basedepth","Base depth","in",4,0.5],["sanddepth","Bedding sand depth","in",1,0.5],["waste","Waste factor","%",10,1]],
  "compute":"""var f=1+v.waste/100;var A=v.length*v.width;var baseCy=A*(v.basedepth/12)/27*f;var sandCy=A*(v.sanddepth/12)/27*f;var baseTons=baseCy*1.4;
return{label:"Base material",value:H.fmt(baseCy,2),unit:"cubic yards",lines:[{label:"Bedding sand",value:H.fmt(sandCy,2)+" yd\\u00B3"},{label:"Base weight (approx)",value:H.fmt(baseTons,2)+" tons"},{label:"Includes waste",value:v.waste+"%"}],note:"Base is usually crushed stone at ~1.4 t/yd\\u00B3. Compact it before adding bedding sand."};""",
 },
 {
  "slug":"concrete","cat":"Concrete · Masonry","name":"Concrete",
  "grid":"Slabs, footings & bags",
  "title":"Concrete Calculator: How Much Concrete Do I Need?",
  "desc":"Free concrete calculator for slabs and footings. Enter length, width, and thickness to get cubic yards plus the number of 60 lb and 80 lb bags.",
  "lede":"Estimate concrete for a slab, footing, or pad. Enter the dimensions to get cubic yards for ready-mix, plus how many 60 lb or 80 lb bags you would need mixing by hand.",
  "inputs_heading":"Slab dimensions",
  "howto":["Concrete volume is length times width times thickness. Thickness is entered in inches, so divide by 12 to reach feet, then divide the total by 27 for cubic yards, the unit ready-mix trucks use.",
           "A 60 lb bag yields about 0.45 cubic feet of set concrete; an 80 lb bag yields about 0.60. Bagged mixing only makes sense for small jobs. Past roughly half a cubic yard, ready-mix is cheaper and far less work."],
  "formula":"cubic feet = length (ft) × width (ft) × thickness (in) ÷ 12\ncubic yards = cubic feet ÷ 27\n60 lb bags = cubic feet ÷ 0.45\n80 lb bags = cubic feet ÷ 0.60",
  "ex_title":"A 10 ft × 10 ft slab, 4 inches thick",
  "ex_steps":["Volume in cubic feet: 10 × 10 × (4 ÷ 12) = <strong>33.3 ft³</strong>",
              "Convert to cubic yards: 33.3 ÷ 27 = <strong>1.23 yd³</strong>",
              "Add a 10% waste factor: 1.23 × 1.10 = <strong>1.36 yd³</strong>",
              "In 80 lb bags: 36.7 ÷ 0.60 = <strong>62 bags</strong>"],
  "ex_answer":"Order about 1.4 cubic yards of ready-mix. Bagging this by hand (62 bags) is not worth it.",
  "table_intro":"Bag yields and slab thicknesses:",
  "table":[["Item","Yield","Notes"],
           ["40 lb bag","0.30 ft³","Small repairs"],
           ["60 lb bag","0.45 ft³","Posts, small pads"],
           ["80 lb bag","0.60 ft³","Most common"],
           ["1 cubic yard","27 ft³","About 45 × 80 lb bags"]],
  "faqs":[["How many 80 lb bags make a cubic yard?","About 45, since each yields roughly 0.60 cubic feet and a cubic yard is 27 cubic feet. That is the point where ready-mix delivery wins."],
          ["How thick should a concrete slab be?","Four inches suits patios, walkways, and shed floors. Step up to 5 or 6 inches for driveways and anything carrying vehicle weight."],
          ["Should I order extra?","Yes. Forms flex, subgrade is not perfectly level, and you cannot pause a pour to buy more. A 10% cushion is standard and is included here."],
          ["Bags or ready-mix?","Bags win for posts and small pads under about half a yard. Beyond that, ready-mix is cheaper per yard, saves hours of mixing, and gives one continuous pour."]],
  "fields":[["length","Length","ft",10,0.5],["width","Width","ft",10,0.5],["thickness","Thickness","in",4,0.5],["waste","Waste factor","%",10,1]],
  "compute":"""var f=1+v.waste/100;var cf=v.length*v.width*(v.thickness/12)*f;var cy=cf/27;var b80=H.ceil(cf/0.60),b60=H.ceil(cf/0.45);
return{label:"Concrete needed",value:H.fmt(cy,2),unit:"cubic yards",lines:[{label:"80 lb bags",value:H.fmt(b80,0)},{label:"60 lb bags",value:H.fmt(b60,0)},{label:"Volume",value:H.fmt(cf,1)+" ft\\u00B3"}],note:"Bag counts include waste. Over ~0.5 yd\\u00B3, order ready-mix instead."};""",
 },
 {
  "slug":"topsoil","cat":"Soil · Garden","name":"Topsoil",
  "grid":"Lawns, beds & fill",
  "title":"Topsoil Calculator: How Much Topsoil Do I Need?",
  "desc":"Free topsoil calculator. Enter length, width, and depth to get cubic yards, approximate tons, and the number of 40 lb bags of topsoil needed.",
  "lede":"Estimate topsoil for a new lawn, raised bed, or leveling job. Enter the area and depth to get cubic yards for bulk delivery, approximate tonnage, and 40 lb bag counts.",
  "inputs_heading":"Area measurements",
  "howto":["Topsoil is bought by volume for bulk loads and by the bag for small jobs. Start with length times width times depth, convert depth to feet, then split into cubic yards, tons, or bags.",
           "About 1.1 tons per cubic yard is a working average for screened topsoil. Damp or clay-heavy soil weighs more; a dry, peaty mix weighs less. A 40 lb bag holds roughly 0.75 cubic feet."],
  "formula":"cubic feet = length (ft) × width (ft) × depth (in) ÷ 12\ncubic yards = cubic feet ÷ 27\ntons ≈ cubic yards × 1.1\n40 lb bags = cubic feet ÷ 0.75",
  "ex_title":"A 12 ft × 12 ft lawn area, 2 inches deep",
  "ex_steps":["Volume in cubic feet: 12 × 12 × (2 ÷ 12) = <strong>24 ft³</strong>",
              "Convert to cubic yards: 24 ÷ 27 = <strong>0.89 yd³</strong>",
              "Convert to tons: 0.89 × 1.1 = <strong>0.98 tons</strong>",
              "In 40 lb bags: 24 ÷ 0.75 = <strong>32 bags</strong>"],
  "ex_answer":"Order about 1 cubic yard (about 1 ton). Cheaper than 32 bags for this size.",
  "table_intro":"Depth by use:",
  "table":[["Use","Depth","1 yd³ covers"],
           ["Overseeding / thin dressing","0.5 in","648 sq ft"],
           ["New lawn from seed","2-3 in","108-162 sq ft"],
           ["Raised bed / vegetables","6-12 in","27-54 sq ft"],
           ["Leveling low spots","varies","n/a"]],
  "faqs":[["How many tons is a cubic yard of topsoil?","Around 1.1 tons for screened topsoil, though moisture swings it a lot. Wet or clay-rich soil can hit 1.3 tons or more."],
          ["How deep for a new lawn?","Two to three inches of quality topsoil gives grass seed enough to root into. For raised beds and vegetables, go much deeper: six inches at minimum, more for root crops."],
          ["How many 40 lb bags in a cubic yard?","About 36, since each holds roughly 0.75 cubic feet. Bulk delivery almost always wins beyond a small patch."],
          ["Does topsoil settle?","Yes, especially fresh screened soil. Add a little extra depth and water it in, or expect the level to drop over the first few weeks."]],
  "fields":[["length","Length","ft",12,0.5],["width","Width","ft",12,0.5],["depth","Depth","in",2,0.5],["waste","Extra (settling)","%",5,1]],
  "compute":"""var f=1+v.waste/100;var cf=v.length*v.width*(v.depth/12)*f;var cy=cf/27,tons=cy*1.1,bags=H.ceil(cf/0.75);
return{label:"Topsoil needed",value:H.fmt(cy,2),unit:"cubic yards",lines:[{label:"Weight (approx)",value:H.fmt(tons,2)+" tons"},{label:"40 lb bags",value:H.fmt(bags,0)},{label:"Volume",value:H.fmt(cf,1)+" ft\\u00B3"}],note:"Tonnage assumes ~1.1 t/yd\\u00B3 for screened topsoil; wet soil weighs more."};""",
 },
 {
  "slug":"mulch","cat":"Soil · Garden","name":"Mulch",
  "grid":"Garden beds & bag counts",
  "title":"Mulch Calculator: How Much Mulch Do I Need?",
  "desc":"Free mulch calculator. Enter bed length, width, and depth to get cubic yards and the number of 2 cubic foot bags of mulch you need.",
  "lede":"Find out how much mulch your beds need. Enter the area and depth to get cubic yards for bulk delivery and the number of standard 2 cubic foot bags.",
  "inputs_heading":"Bed measurements",
  "howto":["Mulch is measured by volume. Multiply the bed's length, width, and depth, convert depth from inches to feet, then divide into cubic yards for bulk or 2-cubic-foot bags for the standard bag size.",
           "Bulk mulch by the cubic yard is far cheaper than bags once you need more than about ten bags. One cubic yard equals roughly 13.5 standard bags."],
  "formula":"cubic feet = length (ft) × width (ft) × depth (in) ÷ 12\ncubic yards = cubic feet ÷ 27\nbags = cubic feet ÷ 2",
  "ex_title":"A 15 ft × 8 ft bed, 3 inches deep",
  "ex_steps":["Volume in cubic feet: 15 × 8 × (3 ÷ 12) = <strong>30 ft³</strong>",
              "Convert to cubic yards: 30 ÷ 27 = <strong>1.11 yd³</strong>",
              "In 2 ft³ bags: 30 ÷ 2 = <strong>15 bags</strong>"],
  "ex_answer":"Get about 1 cubic yard of bulk mulch, or 15 bags if buying by the bag.",
  "table_intro":"Depth and coverage:",
  "table":[["Use","Depth","1 yd³ covers"],
           ["Refresh over existing mulch","1 in","324 sq ft"],
           ["Standard flower bed","2-3 in","108-162 sq ft"],
           ["Weed suppression","3-4 in","81-108 sq ft"],
           ["Around trees / shrubs","3 in","108 sq ft"]],
  "faqs":[["How many bags of mulch are in a cubic yard?","About 13.5 standard 2-cubic-foot bags. Past roughly ten bags, bulk delivery usually costs less."],
          ["How deep should mulch be?","Two to three inches suits most beds. Up to four for heavy weed suppression. More than that can starve roots of air and hold too much water."],
          ["How often should I add mulch?","Organic mulch breaks down over a season or two. A yearly one-inch refresh keeps depth and appearance up without over-piling."],
          ["Bags or bulk?","Bags are convenient for small beds. Bulk is cheaper and less packaging for larger jobs. The crossover is around ten bags."]],
  "fields":[["length","Length","ft",15,0.5],["width","Width","ft",8,0.5],["depth","Depth","in",3,0.5],["waste","Extra (settling)","%",5,1]],
  "compute":"""var f=1+v.waste/100;var cf=v.length*v.width*(v.depth/12)*f;var cy=cf/27,bags=H.ceil(cf/2);
return{label:"Mulch needed",value:H.fmt(cy,2),unit:"cubic yards",lines:[{label:"2 ft\\u00B3 bags",value:H.fmt(bags,0)},{label:"Volume",value:H.fmt(cf,1)+" ft\\u00B3"},{label:"Includes extra",value:v.waste+"%"}],note:"Bag count uses standard 2 ft\\u00B3 bags. Bulk is cheaper past ~10 bags."};""",
 },
 {
  "slug":"sod","cat":"Soil · Garden","name":"Sod",
  "grid":"New lawns by pallet",
  "title":"Sod Calculator: How Much Sod Do I Need?",
  "desc":"Free sod calculator. Enter your lawn length and width to get square footage, the number of pallets, and rolls of sod needed, with waste built in.",
  "lede":"Work out how much sod to order for a new lawn. Enter the area and get square footage plus pallet and roll counts, with a cutting allowance built in.",
  "inputs_heading":"Lawn measurements",
  "howto":["Sod is sold by the square foot, bundled into rolls and stacked on pallets. Multiply length by width for the area, then add a small allowance for cuts around edges and curves.",
           "A pallet covers roughly 450 square feet, though this varies by farm from about 400 to 500. A single roll or slab covers around 10 square feet."],
  "formula":"area = length (ft) × width (ft)\npallets = area ÷ 450\nrolls = area ÷ 10",
  "ex_title":"A 20 ft × 15 ft back lawn",
  "ex_steps":["Area: 20 × 15 = <strong>300 ft²</strong>",
              "Add a 5% cutting allowance: 300 × 1.05 = <strong>315 ft²</strong>",
              "Pallets: 315 ÷ 450 = <strong>1 pallet</strong>",
              "Rolls: 315 ÷ 10 = <strong>32 rolls</strong>"],
  "ex_answer":"One pallet covers this lawn with a little to spare.",
  "table_intro":"Rough coverage guide:",
  "table":[["Quantity","Covers","Note"],
           ["1 roll / slab","≈10 ft²","Hand-laid"],
           ["1 pallet","≈450 ft²","Varies by farm"],
           ["500 ft² lawn","≈1.1 pallets","Round up"],
           ["1,000 ft² lawn","≈2.2 pallets","Round up"]],
  "faqs":[["How much does a pallet of sod cover?","Around 450 square feet on average, but it ranges from about 400 to 500 depending on the farm and slab size. Confirm before ordering."],
          ["How much extra sod should I order?","Add about 5% for straight lawns and up to 10% for lots of curves and garden beds, since edge cuts create waste."],
          ["Can I order a partial pallet?","Some suppliers sell sod by the roll for small areas, others only by the pallet. Ask your farm what their minimum is."],
          ["How soon should I lay sod?","As soon as possible after delivery, ideally within a day. Sod is a living product and deteriorates fast while stacked."]],
  "fields":[["length","Length","ft",20,0.5],["width","Width","ft",15,0.5],["waste","Cutting allowance","%",5,1]],
  "compute":"""var f=1+v.waste/100;var area=v.length*v.width*f;var pallets=H.ceil(area/450),rolls=H.ceil(area/10);
return{label:"Sod needed",value:H.fmt(area,0),unit:"sq ft",lines:[{label:"Pallets (~450 ft\\u00B2)",value:H.fmt(pallets,0)},{label:"Rolls (~10 ft\\u00B2)",value:H.fmt(rolls,0)},{label:"Includes allowance",value:v.waste+"%"}],note:"Pallet coverage varies by farm (400-500 ft\\u00B2). Order a little extra for cuts."};""",
 },
 {
  "slug":"paint","cat":"Interior · Finishing","name":"Paint",
  "grid":"Walls & rooms by coverage",
  "title":"Paint Calculator: How Much Paint Do I Need?",
  "desc":"Free paint calculator. Enter your wall area, number of coats, and coverage to get how many gallons of paint to buy for your room or project.",
  "lede":"Work out how many gallons of paint to buy. Enter the wall area you are covering, the number of coats, and the coverage on the can to get a gallon count rounded up for purchase.",
  "inputs_heading":"Project details",
  "howto":["Paint is estimated from the area to cover, multiplied by the number of coats, divided by the coverage rate on the can, usually around 350 square feet per gallon.",
           "If you do not know your wall area, measure the total length around the room and multiply by wall height, then subtract about 20 square feet per door and 15 per window. Enter that figure as your area."],
  "formula":"wall area = perimeter (ft) × height (ft), minus doors & windows\ngallons = wall area × coats ÷ coverage (sq ft/gal)",
  "ex_title":"A room with 400 sq ft of wall, 2 coats",
  "ex_steps":["Area × coats: 400 × 2 = <strong>800 sq ft to cover</strong>",
              "Divide by coverage: 800 ÷ 350 = <strong>2.29 gallons</strong>",
              "Round up to buy: <strong>3 gallons</strong>"],
  "ex_answer":"Buy 3 gallons. The extra covers touch-ups and the odd thin spot.",
  "table_intro":"Coverage by surface:",
  "table":[["Surface / paint","Coverage","Notes"],
           ["Smooth drywall","350-400 ft²/gal","Use 350 to be safe"],
           ["Primer","250-350 ft²/gal","Thinner coverage"],
           ["Textured / rough wall","250-300 ft²/gal","Soaks up more"],
           ["New / bare drywall","n/a","Add a primer coat"]],
  "faqs":[["How much does a gallon of paint cover?","About 350 square feet per coat on smooth walls. Rough or textured surfaces drop to 250 to 300, so use the figure on your specific can."],
          ["How many coats do I need?","Two is standard for even coverage. One can work when repainting a similar color. Big color changes may need two coats over primer."],
          ["Do I subtract doors and windows?","For a tighter estimate, yes: about 20 sq ft per door and 15 per window. For a small room it barely changes the gallon count."],
          ["Should I buy extra?","Rounding up to the next whole gallon usually covers touch-ups, and the same batch guarantees a color match later."]],
  "fields":[["area","Wall area to cover","ft²",400,10],["coats","Number of coats","coats",2,1],["coverage","Coverage per gallon","ft²",350,10]],
  "compute":"""var ta=v.area*v.coats;var ex=v.coverage>0?ta/v.coverage:0;var buy=H.ceil(ex);
return{label:"Paint to buy",value:H.fmt(buy,0),unit:buy===1?"gallon":"gallons",lines:[{label:"Exact need",value:H.fmt(ex,2)+" gal"},{label:"Area \\u00D7 coats",value:H.fmt(ta,0)+" ft\\u00B2"},{label:"Coverage",value:v.coverage+" ft\\u00B2/gal"}],note:"Rounded up to whole gallons. For bare or textured walls, add a primer coat."};""",
 },
 {
  "slug":"drywall","cat":"Interior · Finishing","name":"Drywall",
  "grid":"Sheets, screws & mud",
  "title":"Drywall Calculator: How Many Sheets Do I Need?",
  "desc":"Free drywall calculator. Enter the wall and ceiling area and sheet size to get how many drywall sheets, screws, and compound boxes you need.",
  "lede":"Work out how many drywall sheets your project needs. Enter the total wall and ceiling area and pick a sheet size to get sheets, plus rough screw and joint compound counts.",
  "inputs_heading":"Project details",
  "howto":["Drywall is estimated by dividing the total area to cover by the area of one sheet. A 4 by 8 sheet is 32 square feet; a 4 by 12 sheet is 48. Larger sheets mean fewer joints to tape.",
           "Add a waste factor for cutouts around doors, windows, and outlets. The screw and compound figures here are planning estimates, not exact material takeoffs."],
  "formula":"sheets = total area (ft²) ÷ sheet area (ft²), rounded up\nscrews ≈ sheets × 32\ncompound ≈ 1 box (4.5 gal) per 12 sheets",
  "ex_title":"A room with 640 sq ft of wall and ceiling, 4×8 sheets",
  "ex_steps":["Add a 10% waste factor: 640 × 1.10 = <strong>704 ft²</strong>",
              "Divide by sheet area: 704 ÷ 32 = <strong>22 sheets</strong>",
              "Screws: 22 × 32 = <strong>704 screws</strong>",
              "Compound: 22 ÷ 12 = <strong>2 boxes</strong>"],
  "ex_answer":"Order 22 sheets, a 5 lb box of screws, and 2 boxes of compound.",
  "table_intro":"Sheet sizes and where they fit:",
  "table":[["Sheet","Area","Best for"],
           ["4 × 8","32 ft²","Tight spaces, stairs"],
           ["4 × 12","48 ft²","Long walls, fewer seams"],
           ["Screws","≈32/sheet","1-1/4 in for 1/2 in board"],
           ["Compound","1 box / 12 sheets","4.5 gal ready-mix"]],
  "faqs":[["How many drywall sheets do I need?","Divide the total wall and ceiling area by the sheet area (32 sq ft for 4x8, 48 for 4x12) and round up, then add about 10% for cuts and waste."],
          ["What size drywall should I use?","4 by 8 sheets are easier to handle in tight spots. 4 by 12 sheets cover long walls with fewer seams to tape, but they are heavy and awkward solo."],
          ["How many screws per sheet?","Roughly 32 for a wall sheet on 16-inch studs. Ceilings and closer spacing use more. Buy screws by the pound rather than counting exactly."],
          ["How much joint compound?","A rough rule is one 4.5-gallon box of ready-mix per twelve sheets for taping and finishing, more if you are skim-coating."]],
  "fields":[["area","Wall & ceiling area","ft²",640,10],
            ["sheet","Sheet size",None,32,None,[["4 × 8 (32 ft²)",32],["4 × 12 (48 ft²)",48]]],
            ["waste","Waste factor","%",10,1]],
  "compute":"""var f=1+v.waste/100;var sh=H.ceil(v.area*f/v.sheet);var scr=sh*32,box=H.ceil(sh/12);
return{label:"Drywall sheets",value:H.fmt(sh,0),unit:(v.sheet==32?"4\\u00D78 sheets":"4\\u00D712 sheets"),lines:[{label:"Screws (approx)",value:H.fmt(scr,0)},{label:"Compound boxes",value:H.fmt(box,0)},{label:"Includes waste",value:v.waste+"%"}],note:"Screw and compound figures are rough planning estimates."};""",
 },
 {
  "slug":"flooring","cat":"Interior \u00b7 Finishing","name":"Flooring",
  "grid":"Laminate, vinyl & wood by area",
  "title":"Flooring Calculator: How Much Flooring Do I Need?",
  "desc":"Free flooring calculator for laminate, vinyl plank, and hardwood. Enter room size and box coverage to get square footage and how many boxes to buy.",
  "lede":"Estimate flooring for laminate, vinyl plank, or hardwood. Enter the room size and the coverage printed on the box to get square footage and boxes to buy, with cutting waste built in.",
  "inputs_heading":"Room measurements",
  "howto":["Flooring is sold by the box, each covering a set number of square feet. Multiply room length by width for the area, add a waste factor for cuts and mistakes, then divide by the box coverage.",
           "Allow about 10% waste for straight layouts and up to 15% for diagonal or herringbone patterns and rooms with lots of corners."],
  "formula":"area = length (ft) \u00d7 width (ft)\nboxes = area \u00d7 (1 + waste) \u00f7 coverage per box",
  "ex_title":"A 12 ft \u00d7 14 ft room, 20 ft\u00b2 per box",
  "ex_steps":["Area: 12 \u00d7 14 = <strong>168 ft\u00b2</strong>","Add 10% waste: 168 \u00d7 1.10 = <strong>185 ft\u00b2</strong>","Divide by box coverage: 185 \u00f7 20 = <strong>9.25</strong>","Round up: <strong>10 boxes</strong>"],
  "ex_answer":"Buy 10 boxes to floor the room with cutting waste covered.",
  "table_intro":"Typical waste allowances:",
  "table":[["Layout","Waste","Note"],["Straight / plank","10%","Standard"],["Diagonal","15%","More cuts"],["Herringbone / chevron","15-20%","High offcut"],["Busy room, many corners","15%","Extra cuts"]],
  "faqs":[["How much extra flooring should I buy?","Add about 10% for a standard straight layout, and 15% or more for diagonal and herringbone patterns. Keep a spare box for future repairs."],
          ["How do I find my square footage?","Multiply the room length by its width. For L-shaped rooms, split into rectangles, find each area, and add them together."],
          ["Why does the box coverage matter?","Boxes vary from about 18 to 24 square feet depending on the product. Always divide by the exact coverage on your box, not a guess."],
          ["Should I buy all the flooring at once?","Yes, and check the batch or lot numbers match. Colors can shift slightly between production runs."]],
  "fields":[["length","Length","ft",12,0.5],["width","Width","ft",14,0.5],["coverage","Coverage per box","ft\u00b2",20,1],["waste","Waste factor","%",10,1]],
  "compute":"""var f=1+v.waste/100;var area=v.length*v.width*f;var boxes=H.ceil(area/v.coverage);
return{label:"Flooring needed",value:H.fmt(area,0),unit:"sq ft",lines:[{label:"Boxes",value:H.fmt(boxes,0)},{label:"Coverage/box",value:v.coverage+" ft\u00b2"},{label:"Includes waste",value:v.waste+"%"}],note:"Buy a spare box for repairs and match lot numbers across boxes."};""",
 },
 {
  "slug":"tile","cat":"Interior \u00b7 Finishing","name":"Tile",
  "grid":"Floor & wall tile counts",
  "title":"Tile Calculator: How Many Tiles Do I Need?",
  "desc":"Free tile calculator. Enter the area and your tile size to get how many tiles you need for a floor or wall, with cutting waste included.",
  "lede":"Work out how many tiles you need for a floor or wall. Enter the area and your tile size to get a tile count with cutting waste built in.",
  "inputs_heading":"Area & tile size",
  "howto":["Tile count is the area to cover divided by the area of one tile. Convert your tile dimensions from inches to feet, multiply for the tile area, then divide the wall or floor area by it.",
           "Add about 10% for straight layouts and 15% for diagonal patterns, since cuts around edges and fixtures create waste. Keep spares for future repairs."],
  "formula":"area = length (ft) \u00d7 width (ft)\ntile area = (tile L \u00f7 12) \u00d7 (tile W \u00f7 12)\ntiles = area \u00d7 (1 + waste) \u00f7 tile area",
  "ex_title":"A 100 ft\u00b2 floor with 12 in \u00d7 12 in tiles",
  "ex_steps":["Tile area: (12 \u00f7 12) \u00d7 (12 \u00f7 12) = <strong>1 ft\u00b2</strong>","Add 10% waste: 100 \u00d7 1.10 = <strong>110 ft\u00b2</strong>","Divide by tile area: 110 \u00f7 1 = <strong>110 tiles</strong>"],
  "ex_answer":"Buy 110 tiles, plus a few spares for future repairs.",
  "table_intro":"Common tile sizes and coverage:",
  "table":[["Tile size","Area each","Tiles per 100 ft\u00b2"],["12 \u00d7 12 in","1.00 ft\u00b2","100"],["18 \u00d7 18 in","2.25 ft\u00b2","45"],["24 \u00d7 24 in","4.00 ft\u00b2","25"],["6 \u00d7 24 in plank","1.00 ft\u00b2","100"]],
  "faqs":[["How many tiles do I need?","Divide the area to cover by the area of one tile, then add 10 to 15% for cuts and breakage. Round up to whole tiles."],
          ["How much extra tile should I buy?","About 10% for straight layouts, 15% for diagonal. Buy a little more if the tile may be discontinued, so you have spares for repairs."],
          ["How do I handle a wall with a door or window?","Calculate the full wall area, then subtract the opening area. For small openings many people skip this and let the waste factor absorb it."],
          ["Do larger tiles waste more?","They can, because each cut removes a bigger piece. Large-format and diagonal layouts lean toward the higher end of the waste range."]],
  "fields":[["length","Length","ft",10,0.5],["width","Width","ft",10,0.5],["tilel","Tile length","in",12,0.5],["tilew","Tile width","in",12,0.5],["waste","Waste factor","%",10,1]],
  "compute":"""var f=1+v.waste/100;var area=v.length*v.width;var ta=(v.tilel/12)*(v.tilew/12);var tiles=ta>0?H.ceil(area*f/ta):0;
return{label:"Tiles needed",value:H.fmt(tiles,0),unit:"tiles",lines:[{label:"Area",value:H.fmt(area,0)+" ft\u00b2"},{label:"Tile size",value:v.tilel+"\u00d7"+v.tilew+" in"},{label:"Includes waste",value:v.waste+"%"}],note:"Buy spare tiles for repairs; dye lots can vary between batches."};""",
 },
 {
  "slug":"fence","cat":"Structural \u00b7 Exterior","name":"Fence",
  "grid":"Posts, panels & concrete",
  "title":"Fence Calculator: How Much Fencing Material?",
  "desc":"Free fence calculator. Enter your fence length and post spacing to get the number of posts, panels, rails, and bags of concrete you need.",
  "lede":"Plan the materials for a new fence run. Enter the total length and post spacing to get posts, panels, rails, and concrete bags.",
  "inputs_heading":"Fence run",
  "howto":["A fence run is divided into sections between posts. Divide the total length by the post spacing to get sections, then add one post, because a run of N sections needs N plus one posts.",
           "Each section carries two or three rails, and each post is usually set in about two bags of concrete. Adjust rails per section to match your fence style."],
  "formula":"sections = fence length \u00f7 post spacing (rounded up)\nposts = sections + 1\nrails = sections \u00d7 rails per section\nconcrete bags \u2248 posts \u00d7 2",
  "ex_title":"A 96 ft fence, posts every 8 ft, 3 rails",
  "ex_steps":["Sections: 96 \u00f7 8 = <strong>12 sections</strong>","Posts: 12 + 1 = <strong>13 posts</strong>","Rails: 12 \u00d7 3 = <strong>36 rails</strong>","Concrete: 13 \u00d7 2 = <strong>26 bags</strong>"],
  "ex_answer":"You need 13 posts, 12 panels, 36 rails, and about 26 bags of concrete.",
  "table_intro":"Common spacing and rails:",
  "table":[["Fence type","Post spacing","Rails/section"],["Wood privacy","8 ft","3"],["Wood picket","6-8 ft","2-3"],["Chain link","10 ft","1 top rail"],["Vinyl panel","6-8 ft","per kit"]],
  "faqs":[["How far apart should fence posts be?","Six to eight feet for most wood and vinyl fences, up to ten for chain link. Closer spacing is stronger and handles wind and slopes better."],
          ["How many bags of concrete per post?","About two 50 lb fast-setting bags for a standard post in a properly sized hole. Taller and gate posts need more."],
          ["How many rails per section?","Two for shorter fences, three for privacy fences six feet and taller. Gates and heavy panels may need extra bracing."],
          ["Do I count gate posts separately?","Yes. Gate posts take more load, so set them deeper with extra concrete, and remember a gate opening replaces a panel section."]],
  "fields":[["length","Fence length","ft",96,1],["spacing","Post spacing","ft",8,0.5],["rails","Rails per section","",3,1]],
  "compute":"""var sections=v.spacing>0?H.ceil(v.length/v.spacing):0;var posts=sections+1;var rails=sections*v.rails;var conc=posts*2;
return{label:"Fence sections",value:H.fmt(sections,0),unit:"panels",lines:[{label:"Posts",value:H.fmt(posts,0)},{label:"Rails",value:H.fmt(rails,0)},{label:"Concrete bags (~2/post)",value:H.fmt(conc,0)}],note:"Set gate and corner posts deeper with extra concrete."};""",
 },
 {
  "slug":"roofing","cat":"Structural \u00b7 Exterior","name":"Roofing",
  "grid":"Squares & shingle bundles",
  "title":"Roofing Calculator: How Many Shingles Do I Need?",
  "desc":"Free roofing calculator. Enter your roof area to get roofing squares and how many bundles of shingles you need, with waste included.",
  "lede":"Estimate shingles for a roof. Enter the total roof area, meaning all planes and not the ground footprint, to get roofing squares and bundle counts with waste built in.",
  "inputs_heading":"Roof area",
  "howto":["Roofing is measured in squares, where one square equals 100 square feet of roof surface. Measure each roof plane and add them up, since a pitched roof has more area than the footprint below it.",
           "Most architectural shingles come three bundles to a square. Add about 10% waste for starter courses, hips, ridges, and cutting."],
  "formula":"squares = roof area (ft\u00b2) \u00f7 100\nbundles = squares \u00d7 (1 + waste) \u00d7 bundles per square",
  "ex_title":"An 1,800 ft\u00b2 roof, 3 bundles per square",
  "ex_steps":["Squares: 1,800 \u00f7 100 = <strong>18 squares</strong>","Add 10% waste: 18 \u00d7 1.10 = <strong>19.8 squares</strong>","Bundles: 19.8 \u00d7 3 = <strong>60 bundles</strong>"],
  "ex_answer":"Order about 60 bundles (20 squares) of shingles.",
  "table_intro":"Roof area by pitch (multiply the footprint):",
  "table":[["Pitch","Multiplier","Note"],["Flat / low (2:12)","1.02","Nearly footprint"],["Medium (6:12)","1.12","Common"],["Steep (9:12)","1.25","More area"],["Very steep (12:12)","1.41","Much more"]],
  "faqs":[["What is a roofing square?","One hundred square feet of roof surface. Shingles, underlayment, and labor are all quoted by the square."],
          ["How many bundles in a square?","Three for most architectural shingles. Some heavier or specialty shingles run four bundles per square, so check the wrapper."],
          ["How do I measure roof area?","Measure each roof plane (length times width) and add them together. Do not use the ground footprint, since a pitched roof has more surface than the area below it."],
          ["How much extra should I add?","About 10% for starter strips, ridge caps, hips, valleys, and cut waste. Complex roofs with many valleys need more."]],
  "fields":[["area","Roof area","ft\u00b2",1800,10],["bundles","Bundles per square","",3,1],["waste","Waste factor","%",10,1]],
  "compute":"""var f=1+v.waste/100;var sq=v.area/100*f;var bundles=H.ceil(sq*v.bundles);
return{label:"Shingle bundles",value:H.fmt(bundles,0),unit:"bundles",lines:[{label:"Roofing squares",value:H.fmt(sq,1)},{label:"Bundles/square",value:H.fmt(v.bundles,0)},{label:"Includes waste",value:v.waste+"%"}],note:"Measure actual roof planes, not the ground footprint. Add more for complex roofs."};""",
 },
 {
  "slug":"deck","cat":"Structural \u00b7 Exterior","name":"Deck Boards",
  "grid":"Decking boards by area",
  "title":"Deck Board Calculator: How Many Boards Do I Need?",
  "desc":"Free deck board calculator. Enter your deck size and board dimensions to get how many decking boards you need, with waste included.",
  "lede":"Work out how many decking boards your deck needs. Enter the deck size and board dimensions to get a board count with waste for cuts and gaps.",
  "inputs_heading":"Deck & board size",
  "howto":["Board count is the deck area divided by the coverage of one board. A board covers its width times its length, so convert the board width from inches to feet before multiplying.",
           "Add about 10% for cuts, gaps between boards, and the odd defect. Diagonal decking uses more, so allow 15%."],
  "formula":"deck area = length (ft) \u00d7 width (ft)\nboard coverage = (board width in \u00f7 12) \u00d7 board length (ft)\nboards = deck area \u00d7 (1 + waste) \u00f7 board coverage",
  "ex_title":"A 16 ft \u00d7 12 ft deck, 5.5 in \u00d7 12 ft boards",
  "ex_steps":["Deck area: 16 \u00d7 12 = <strong>192 ft\u00b2</strong>","Board coverage: (5.5 \u00f7 12) \u00d7 12 = <strong>5.5 ft\u00b2</strong>","Add 10% waste: 192 \u00d7 1.10 = <strong>211 ft\u00b2</strong>","Boards: 211 \u00f7 5.5 = <strong>39 boards</strong>"],
  "ex_answer":"Order 39 deck boards, plus fasteners and joist material.",
  "table_intro":"Common decking board coverage (12 ft board):",
  "table":[["Board","Actual width","Covers (12 ft)"],["5/4 \u00d7 6","5.5 in","5.5 ft\u00b2"],["2 \u00d7 6","5.5 in","5.5 ft\u00b2"],["2 \u00d7 4","3.5 in","3.5 ft\u00b2"],["1 \u00d7 6","5.5 in","5.5 ft\u00b2"]],
  "faqs":[["How many deck boards do I need?","Divide the deck area by the coverage of one board (its actual width times its length), then add about 10% for cuts and gaps."],
          ["What is the actual width of a deck board?","A nominal 6-inch board is about 5.5 inches wide. Use the actual width, not the nominal size, for an accurate count."],
          ["Does board length matter?","It affects waste. Choosing board lengths that divide evenly into your deck run means fewer cuts and less offcut waste."],
          ["What about joists and fasteners?","This tool covers decking boards. Joists depend on your framing spacing, and plan on roughly 350 screws or hidden clips per 100 square feet."]],
  "fields":[["length","Deck length","ft",16,0.5],["width","Deck width","ft",12,0.5],["boardwidth","Board width","in",5.5,0.25],["boardlength","Board length","ft",12,0.5],["waste","Waste factor","%",10,1]],
  "compute":"""var f=1+v.waste/100;var area=v.length*v.width;var bc=(v.boardwidth/12)*v.boardlength;var boards=bc>0?H.ceil(area*f/bc):0;
return{label:"Deck boards",value:H.fmt(boards,0),unit:"boards",lines:[{label:"Deck area",value:H.fmt(area,0)+" ft\u00b2"},{label:"Board coverage",value:H.fmt(bc,1)+" ft\u00b2"},{label:"Includes waste",value:v.waste+"%"}],note:"Covers decking boards only. Add joists and ~350 fasteners per 100 ft\u00b2."};""",
 },
 {
  "slug":"pea-gravel","cat":"Aggregates \u00b7 Landscaping","name":"Pea Gravel",
  "grid":"Paths & patios by the yard",
  "title":"Pea Gravel Calculator: How Much Do I Need?",
  "desc":"Free pea gravel calculator. Enter length, width, and depth to get cubic yards and tons of pea gravel for paths, patios, and drainage.",
  "lede":"Estimate pea gravel for a path, patio, or drainage bed. Enter the area and depth to get cubic yards and approximate tonnage.",
  "inputs_heading":"Your measurements",
  "howto":["Pea gravel is measured by volume and often sold by the ton. Multiply length by width by depth, convert depth to feet, and divide into cubic yards or tons.",
           "Pea gravel is rounded and shifts underfoot, so two to three inches is plenty for a path. Use edging to keep it contained."],
  "formula":"cubic feet = length (ft) \u00d7 width (ft) \u00d7 depth (in) \u00f7 12\ncubic yards = cubic feet \u00f7 27\ntons \u2248 cubic yards \u00d7 1.4",
  "ex_title":"A 20 ft \u00d7 4 ft path, 2 inches deep",
  "ex_steps":["Volume: 20 \u00d7 4 \u00d7 (2 \u00f7 12) = <strong>13.3 ft\u00b3</strong>","Cubic yards: 13.3 \u00f7 27 = <strong>0.49 yd\u00b3</strong>","Add 10% waste: 0.49 \u00d7 1.10 = <strong>0.54 yd\u00b3</strong>","Tons: 0.54 \u00d7 1.4 = <strong>0.76 tons</strong>"],
  "ex_answer":"Order about half a cubic yard (roughly 0.8 tons) of pea gravel.",
  "table_intro":"Depth guide:",
  "table":[["Use","Depth","1 yd\u00b3 covers"],["Walking path","2 in","162 sq ft"],["Patio topping","2-3 in","108-162 sq ft"],["Dog run / play area","2 in","162 sq ft"],["Drainage","varies","n/a"]],
  "faqs":[["How deep should pea gravel be?","Two to three inches for paths and patios. Deeper than that feels loose underfoot because the stones are rounded."],
          ["How many tons in a yard of pea gravel?","About 1.4, though rounded pea gravel can run a little lighter. Confirm the density with your supplier before ordering by weight."],
          ["Does pea gravel need edging?","Yes. Because the stones are smooth and round, they migrate easily. Edging keeps a path or patio from spreading into the lawn."],
          ["Can I put pea gravel over dirt?","It lasts longer over a compacted base with landscape fabric underneath, which blocks weeds and stops the stone sinking into the soil."]],
  "fields":[["length","Length","ft",20,0.5],["width","Width","ft",4,0.5],["depth","Depth","in",2,0.5],["waste","Waste factor","%",10,1]],
  "compute":"""var f=1+v.waste/100;var cf=v.length*v.width*(v.depth/12)*f;var cy=cf/27,tons=cy*1.4;
return{label:"Pea gravel",value:H.fmt(cy,2),unit:"cubic yards",lines:[{label:"Volume",value:H.fmt(cf,1)+" ft\u00b3"},{label:"Weight (approx)",value:H.fmt(tons,2)+" tons"},{label:"Includes waste",value:v.waste+"%"}],note:"Pea gravel density varies ~1.25-1.4 t/yd\u00b3; confirm with your supplier."};""",
 },
 {
  "slug":"river-rock","cat":"Aggregates \u00b7 Landscaping","name":"River Rock",
  "grid":"Decorative stone by the yard",
  "title":"River Rock Calculator: How Much Do I Need?",
  "desc":"Free river rock calculator. Enter length, width, and depth to get cubic yards and tons of river rock for beds, borders, and drainage.",
  "lede":"Estimate river rock for a bed, border, or dry creek. Enter the area and depth to get cubic yards and approximate tonnage.",
  "inputs_heading":"Your measurements",
  "howto":["River rock is sold by volume or weight. Multiply length by width by depth, convert depth to feet, then divide into cubic yards or tons.",
           "Larger river rock needs more depth to cover the ground fully. Two inches suits small stone; go three or more for larger cobbles."],
  "formula":"cubic feet = length (ft) \u00d7 width (ft) \u00d7 depth (in) \u00f7 12\ncubic yards = cubic feet \u00f7 27\ntons \u2248 cubic yards \u00d7 1.4",
  "ex_title":"A 12 ft \u00d7 6 ft bed, 3 inches deep",
  "ex_steps":["Volume: 12 \u00d7 6 \u00d7 (3 \u00f7 12) = <strong>18 ft\u00b3</strong>","Cubic yards: 18 \u00f7 27 = <strong>0.67 yd\u00b3</strong>","Add 10% waste: 0.67 \u00d7 1.10 = <strong>0.73 yd\u00b3</strong>","Tons: 0.73 \u00d7 1.4 = <strong>1.03 tons</strong>"],
  "ex_answer":"Order about three-quarters of a cubic yard (about 1 ton).",
  "table_intro":"Depth by stone size:",
  "table":[["Stone size","Depth","Note"],["Small (0.5-1 in)","2 in","Even coverage"],["Medium (1-2 in)","3 in","Common"],["Large (2-4 in)","3-4 in","Fewer gaps"],["Cobble (4 in+)","4 in+","Accent only"]],
  "faqs":[["How deep should river rock be?","About two inches for small stone and three or more for larger rock, so the ground underneath is fully hidden."],
          ["How many tons in a yard of river rock?","Roughly 1.4, varying with stone size and type. Ask your supplier for the density of the specific rock."],
          ["Should I use landscape fabric under river rock?","Yes, in most beds. Fabric blocks weeds and keeps the stone from working down into the soil."],
          ["Is river rock good for drainage?","Very. It does not compact, so water moves through it freely, which is why it is popular for dry creeks and French drains."]],
  "fields":[["length","Length","ft",12,0.5],["width","Width","ft",6,0.5],["depth","Depth","in",3,0.5],["waste","Waste factor","%",10,1]],
  "compute":"""var f=1+v.waste/100;var cf=v.length*v.width*(v.depth/12)*f;var cy=cf/27,tons=cy*1.4;
return{label:"River rock",value:H.fmt(cy,2),unit:"cubic yards",lines:[{label:"Volume",value:H.fmt(cf,1)+" ft\u00b3"},{label:"Weight (approx)",value:H.fmt(tons,2)+" tons"},{label:"Includes waste",value:v.waste+"%"}],note:"Tonnage assumes ~1.4 t/yd\u00b3; larger stone can vary. Confirm with your supplier."};""",
 },
 {
  "slug":"play-sand","cat":"Aggregates \u00b7 Landscaping","name":"Play Sand",
  "grid":"Sandboxes & play areas",
  "title":"Play Sand Calculator: How Much Do I Need?",
  "desc":"Free play sand calculator. Enter your sandbox size and depth to get cubic yards, cubic feet, and how many 50 lb bags of play sand you need.",
  "lede":"Work out how much play sand to fill a sandbox or play area. Enter the size and depth to get cubic feet, cubic yards, and bag counts.",
  "inputs_heading":"Sandbox measurements",
  "howto":["Play sand fills a volume, so multiply length by width by depth and convert depth to feet. Bagged play sand is usually 50 pounds, covering about 0.5 cubic feet each.",
           "For a sandbox, six inches of sand is a good play depth. For a base leveling layer under a paver or pool, one to two inches is enough."],
  "formula":"cubic feet = length (ft) \u00d7 width (ft) \u00d7 depth (in) \u00f7 12\ncubic yards = cubic feet \u00f7 27\n50 lb bags = cubic feet \u00f7 0.5",
  "ex_title":"A 5 ft \u00d7 5 ft sandbox, 6 inches deep",
  "ex_steps":["Volume: 5 \u00d7 5 \u00d7 (6 \u00f7 12) = <strong>12.5 ft\u00b3</strong>","Cubic yards: 12.5 \u00f7 27 = <strong>0.46 yd\u00b3</strong>","In 50 lb bags: 12.5 \u00f7 0.5 = <strong>25 bags</strong>"],
  "ex_answer":"Fill this sandbox with about 25 fifty-pound bags of play sand.",
  "table_intro":"Sand depth by use:",
  "table":[["Use","Depth","Note"],["Sandbox play","6 in","Comfortable depth"],["Under a play set","3-6 in","Cushioning"],["Paver / pool base","1-2 in","Leveling layer"],["Sand table","2-3 in","Small fill"]],
  "faqs":[["How much play sand for a sandbox?","Aim for about six inches of depth. Multiply the box length by width by half a foot to get cubic feet, then divide by 0.5 for the number of 50 pound bags."],
          ["How many bags of play sand do I need?","Each 50 pound bag covers about half a cubic foot. Divide your total cubic feet by 0.5 to get the bag count."],
          ["Is play sand different from regular sand?","Yes. Play sand is washed and screened to remove dust and sharp pieces, which makes it safer and cleaner for children."],
          ["How often should I replace sandbox sand?","Top it up as it scatters, and replace it every year or two, or sooner if it stays damp or gets dirty."]],
  "fields":[["length","Length","ft",5,0.5],["width","Width","ft",5,0.5],["depth","Depth","in",6,0.5],["waste","Waste factor","%",5,1]],
  "compute":"""var f=1+v.waste/100;var cf=v.length*v.width*(v.depth/12)*f;var cy=cf/27,bags=H.ceil(cf/0.5);
return{label:"Play sand",value:H.fmt(cy,2),unit:"cubic yards",lines:[{label:"50 lb bags",value:H.fmt(bags,0)},{label:"Volume",value:H.fmt(cf,1)+" ft\u00b3"},{label:"Includes waste",value:v.waste+"%"}],note:"Each 50 lb bag holds ~0.5 ft\u00b3. Use washed, screened play sand for sandboxes."};""",
 },
 {
  "slug":"asphalt","cat":"Aggregates \u00b7 Landscaping","name":"Asphalt",
  "grid":"Driveways by the ton",
  "title":"Asphalt Calculator: How Much Asphalt Do I Need?",
  "desc":"Free asphalt calculator. Enter your driveway size and thickness to get the tons of hot-mix asphalt needed, with a waste factor built in.",
  "lede":"Estimate hot-mix asphalt for a driveway or lot. Enter the area and compacted thickness to get the tonnage to order, with waste built in.",
  "inputs_heading":"Paving area",
  "howto":["Asphalt is ordered by the ton. Multiply length by width by thickness, convert thickness to feet, then multiply the cubic feet by the mix density (about 148 pounds per cubic foot) and divide by 2,000 for tons.",
           "A residential driveway is usually 2 to 3 inches of compacted asphalt over a stone base. Thicker layers carry heavier loads."],
  "formula":"cubic feet = length (ft) \u00d7 width (ft) \u00d7 thickness (in) \u00f7 12\ntons = cubic feet \u00d7 148 \u00f7 2,000",
  "ex_title":"A 40 ft \u00d7 12 ft driveway, 3 inches thick",
  "ex_steps":["Volume: 40 \u00d7 12 \u00d7 (3 \u00f7 12) = <strong>120 ft\u00b3</strong>","Add 10% waste: 120 \u00d7 1.10 = <strong>132 ft\u00b3</strong>","Tons: 132 \u00d7 148 \u00f7 2,000 = <strong>9.77 tons</strong>"],
  "ex_answer":"Order about 10 tons of hot-mix asphalt.",
  "table_intro":"Compacted thickness by use:",
  "table":[["Use","Thickness","Note"],["Overlay on old asphalt","1.5 in","Resurfacing"],["Residential driveway","2-3 in","Over stone base"],["Parking lot","3-4 in","Light vehicles"],["Heavy traffic","4 in+","Trucks"]],
  "faqs":[["How many tons of asphalt do I need?","Find the volume in cubic feet (area times thickness), multiply by about 148 pounds per cubic foot, and divide by 2,000. Add roughly 10% for compaction and waste."],
          ["How thick should a driveway be?","Two to three inches of compacted hot-mix over a solid stone base for a residential driveway. Go thicker for heavier vehicles."],
          ["How much does asphalt weigh?","Hot-mix asphalt weighs roughly 145 to 150 pounds per cubic foot, or about 2 tons per cubic yard. Density varies by mix."],
          ["Do I need a base under asphalt?","Yes. A compacted crushed-stone base is essential. Asphalt laid straight on soil cracks and fails quickly."]],
  "fields":[["length","Length","ft",40,0.5],["width","Width","ft",12,0.5],["thickness","Thickness","in",3,0.5],["waste","Waste factor","%",10,1]],
  "compute":"""var f=1+v.waste/100;var cf=v.length*v.width*(v.thickness/12)*f;var tons=cf*148/2000;var cy=cf/27;
return{label:"Asphalt needed",value:H.fmt(tons,2),unit:"tons",lines:[{label:"Cubic yards",value:H.fmt(cy,2)+" yd\u00b3"},{label:"Volume",value:H.fmt(cf,1)+" ft\u00b3"},{label:"Includes waste",value:v.waste+"%"}],note:"Hot-mix asphalt ~148 lb/ft\u00b3. Confirm mix density with your supplier."};""",
 },
 {
  "slug":"square-footage","cat":"Tools \u00b7 Converters","name":"Square Footage","nocost":True,
  "grid":"Area for any project",
  "title":"Square Footage Calculator: Find Your Area",
  "desc":"Free square footage calculator. Enter length and width to get area in square feet, square yards, acres, and square meters for any room or lot.",
  "lede":"Find the square footage of a room, wall, lot, or project. Enter length and width to get the area in square feet, plus square yards, acres, and square meters.",
  "inputs_heading":"Measurements",
  "howto":["Square footage is length times width. Measure both sides in feet and multiply. For several identical areas, set the number of areas and the total is multiplied for you.",
           "For rooms that are not simple rectangles, split the space into rectangles, find each area, and add them together."],
  "formula":"area (ft\u00b2) = length (ft) \u00d7 width (ft) \u00d7 number of areas\nsquare yards = ft\u00b2 \u00f7 9      acres = ft\u00b2 \u00f7 43,560",
  "ex_title":"A 20 ft \u00d7 15 ft room",
  "ex_steps":["Multiply the sides: 20 \u00d7 15 = <strong>300 ft\u00b2</strong>","In square yards: 300 \u00f7 9 = <strong>33.3 yd\u00b2</strong>","In square meters: 300 \u00d7 0.0929 = <strong>27.9 m\u00b2</strong>"],
  "ex_answer":"The room is 300 square feet.",
  "table_intro":"Handy area conversions:",
  "table":[["From","To","Convert"],["Square feet","Square yards","divide by 9"],["Square feet","Square meters","multiply by 0.0929"],["Square feet","Acres","divide by 43,560"],["Acres","Square feet","multiply by 43,560"]],
  "faqs":[["How do I calculate square footage?","Measure the length and width in feet and multiply them. The result is the area in square feet. For L-shaped spaces, split into rectangles and add each area."],
          ["How many square feet are in a square yard?","Nine. To convert square feet to square yards, divide by nine. Flooring and some materials are priced by the square yard."],
          ["How do I find the size of a lot in acres?","Divide the square footage by 43,560, the number of square feet in one acre."],
          ["What if my room is not a rectangle?","Break it into rectangles and triangles, calculate each piece, and add them. For a triangle, area is half the base times the height."]],
  "fields":[["length","Length","ft",20,0.5],["width","Width","ft",15,0.5],["quantity","Number of areas","",1,1]],
  "compute":"""var q=v.quantity>0?v.quantity:1;var area=v.length*v.width*q;
return{label:"Total area",value:H.fmt(area,0),unit:"sq ft",lines:[{label:"Square yards",value:H.fmt(area/9,1)},{label:"Acres",value:H.fmt(area/43560,3)},{label:"Square meters",value:H.fmt(area*0.092903,1)}],note:"For odd shapes, split into rectangles and add the areas together."};""",
 },
 {
  "slug":"cubic-yards-to-tons","cat":"Tools \u00b7 Converters","name":"Cubic Yards to Tons","nocost":True,
  "grid":"Convert volume to weight",
  "title":"Cubic Yards to Tons Calculator",
  "desc":"Free cubic yards to tons converter. Enter a volume in cubic yards and pick a material to get the approximate weight in tons and pounds.",
  "lede":"Convert a volume in cubic yards into weight. Enter the cubic yards and choose a material to get the approximate tonnage, using typical densities.",
  "inputs_heading":"Volume & material",
  "howto":["Weight is volume times density. Each material has a typical density in tons per cubic yard, so multiply your cubic yards by that figure to get tons.",
           "These are average densities. Moisture, compaction, and the exact product all shift the real weight, so treat the result as a planning estimate."],
  "formula":"tons = cubic yards \u00d7 density (tons per cubic yard)\npounds = tons \u00d7 2,000",
  "ex_title":"5 cubic yards of gravel",
  "ex_steps":["Gravel density: about <strong>1.4 t/yd\u00b3</strong>","Multiply: 5 \u00d7 1.4 = <strong>7 tons</strong>","In pounds: 7 \u00d7 2,000 = <strong>14,000 lb</strong>"],
  "ex_answer":"5 cubic yards of gravel weighs about 7 tons.",
  "table_intro":"Typical material densities:",
  "table":[["Material","Tons per yd\u00b3","Note"],["Topsoil","1.1","Screened"],["Sand","1.35","Dry"],["Gravel","1.4","Typical"],["Crushed stone","1.4","Varies by grade"],["Concrete","2.03","Cured"],["Asphalt","2.0","Hot mix"]],
  "faqs":[["How do I convert cubic yards to tons?","Multiply the cubic yards by the material density in tons per cubic yard. Gravel is about 1.4, sand about 1.35, topsoil about 1.1."],
          ["Why does the material matter?","Different materials weigh very different amounts for the same volume. A cubic yard of mulch is light; a cubic yard of concrete is heavy."],
          ["Are these weights exact?","No, they are averages. Moisture and compaction change the real weight, so confirm with your supplier when ordering by the ton."],
          ["How many pounds in a ton?","Two thousand pounds in a US short ton, which is the unit most suppliers quote."]],
  "fields":[["cy","Cubic yards","yd\u00b3",1,0.1],["material","Material",None,1.4,None,[["Gravel",1.4],["Sand",1.35],["Crushed stone",1.4],["Topsoil",1.1],["Mulch",0.5],["Concrete",2.03],["Asphalt",2.0]]]],
  "compute":"""var d=parseFloat(v.material)||0;var tons=v.cy*d;var lbs=tons*2000;
return{label:"Weight",value:H.fmt(tons,2),unit:"tons",lines:[{label:"Pounds",value:H.fmt(lbs,0)+" lb"},{label:"Density",value:d+" t/yd\u00b3"},{label:"Cubic yards",value:H.fmt(v.cy,2)}],note:"Densities are typical averages; wet material weighs more."};""",
 },
 {
  "slug":"insulation","cat":"Interior \u00b7 Finishing","name":"Insulation",
  "grid":"Batts by area & coverage",
  "title":"Insulation Calculator: How Much Insulation Do I Need?",
  "desc":"Free insulation calculator. Enter your wall or ceiling area and the coverage per bundle to get how many bundles of batt insulation you need.",
  "lede":"Estimate batt insulation for walls or a ceiling. Enter the area to cover and the coverage printed on the bundle to get how many bundles to buy.",
  "inputs_heading":"Area to insulate",
  "howto":["Batt insulation is sold by the bundle, each covering a set number of square feet at a given R-value. Multiply the wall or ceiling area, add a little for trimming, then divide by the bundle coverage.",
           "Coverage drops as R-value rises, so a bundle of R-30 covers less area than a bundle of R-13. Always divide by the coverage printed on your bundle."],
  "formula":"bundles = area (ft\u00b2) \u00d7 (1 + waste) \u00f7 coverage per bundle",
  "ex_title":"A 500 ft\u00b2 wall, 40 ft\u00b2 per bundle",
  "ex_steps":["Add 5% waste: 500 \u00d7 1.05 = <strong>525 ft\u00b2</strong>","Divide by coverage: 525 \u00f7 40 = <strong>13.1</strong>","Round up: <strong>14 bundles</strong>"],
  "ex_answer":"Buy 14 bundles to insulate the wall.",
  "table_intro":"Typical batt coverage by R-value (check your bundle):",
  "table":[["R-value","Use","Coverage/bundle"],["R-13","2x4 walls","~40 ft\u00b2"],["R-15","2x4 walls","~40 ft\u00b2"],["R-19","2x6 walls","~48 ft\u00b2"],["R-30","Ceilings","~88 ft\u00b2"]],
  "faqs":[["How much insulation do I need?","Measure the wall or ceiling area, then divide by the coverage printed on the bundle for your R-value. Add about 5% for trimming."],
          ["Does R-value change how much I buy?","Yes. Higher R-value batts are thicker and cover less area per bundle, so a bundle of R-30 covers less than a bundle of R-13."],
          ["Do I subtract windows and doors?","For a rough estimate you can, but many people skip it and let the small waste factor absorb the openings."],
          ["Batts or blown-in?","Batts suit open walls and standard joist spacing. Blown-in works better for attics and irregular cavities. This tool estimates batts."]],
  "fields":[["area","Area to cover","ft\u00b2",500,10],["coverage","Coverage per bundle","ft\u00b2",40,1],["waste","Waste factor","%",5,1]],
  "compute":"""var f=1+v.waste/100;var b=H.ceil(v.area*f/v.coverage);
return{label:"Insulation bundles",value:H.fmt(b,0),unit:"bundles",lines:[{label:"Area",value:H.fmt(v.area,0)+" ft\u00b2"},{label:"Coverage/bundle",value:v.coverage+" ft\u00b2"},{label:"Includes waste",value:v.waste+"%"}],note:"Coverage varies by R-value; use the figure printed on your bundle."};""",
 },
 {
  "slug":"wallpaper","cat":"Interior \u00b7 Finishing","name":"Wallpaper",
  "grid":"Rolls by wall area",
  "title":"Wallpaper Calculator: How Many Rolls Do I Need?",
  "desc":"Free wallpaper calculator. Enter your wall perimeter and height to get the wall area and how many rolls of wallpaper you need, with pattern waste included.",
  "lede":"Work out how many rolls of wallpaper you need. Enter the distance around the room and the wall height to get rolls, with extra for pattern matching.",
  "inputs_heading":"Wall measurements",
  "howto":["Wallpaper is estimated from wall area divided by the usable coverage of a roll. Measure the distance around the room and multiply by the wall height, then divide by the roll coverage.",
           "Pattern repeats waste paper at every strip, so add about 15%. Large patterns waste more. Buy all rolls from the same batch for a consistent color."],
  "formula":"wall area = perimeter (ft) \u00d7 height (ft)\nrolls = wall area \u00d7 (1 + waste) \u00f7 coverage per roll",
  "ex_title":"A room 40 ft around, 8 ft high, 25 ft\u00b2 per roll",
  "ex_steps":["Wall area: 40 \u00d7 8 = <strong>320 ft\u00b2</strong>","Add 15% waste: 320 \u00d7 1.15 = <strong>368 ft\u00b2</strong>","Divide by roll coverage: 368 \u00f7 25 = <strong>14.7</strong>","Round up: <strong>15 rolls</strong>"],
  "ex_answer":"Buy 15 single rolls, all from the same batch.",
  "table_intro":"Roll coverage guide:",
  "table":[["Roll type","Roll size","Usable coverage"],["Single roll","~27 ft\u00b2","~25 ft\u00b2"],["Double roll","~56 ft\u00b2","~50 ft\u00b2"],["Euro roll","~29 ft\u00b2","~28 ft\u00b2"],["Pattern repeat","varies","adds waste"]],
  "faqs":[["How many rolls of wallpaper do I need?","Find the wall area (distance around the room times height), add about 15% for pattern matching, and divide by the usable coverage of a roll."],
          ["Why add extra for the pattern?","Matching a repeating pattern means trimming waste from every strip. Larger repeats waste more, so 15% is a safe starting point."],
          ["Should I subtract doors and windows?","For big openings you can subtract them, but the pattern waste often cancels out the saving. When unsure, do not subtract."],
          ["Single roll or double roll?","Wallpaper is often priced as single rolls but sold as double-roll bolts. Calculate in single rolls, then buy the bolt count that covers it."]],
  "fields":[["perimeter","Distance around room","ft",40,0.5],["height","Wall height","ft",8,0.5],["coverage","Coverage per roll","ft\u00b2",25,1],["waste","Waste factor","%",15,1]],
  "compute":"""var f=1+v.waste/100;var area=v.perimeter*v.height;var rolls=H.ceil(area*f/v.coverage);
return{label:"Wallpaper rolls",value:H.fmt(rolls,0),unit:"rolls",lines:[{label:"Wall area",value:H.fmt(area,0)+" ft\u00b2"},{label:"Coverage/roll",value:v.coverage+" ft\u00b2"},{label:"Includes waste",value:v.waste+"%"}],note:"Buy all rolls from one batch so the color matches."};""",
 },
 {
  "slug":"grass-seed","cat":"Soil \u00b7 Garden","name":"Grass Seed",
  "grid":"Seed by lawn area",
  "title":"Grass Seed Calculator: How Much Seed Do I Need?",
  "desc":"Free grass seed calculator. Enter your lawn size and seeding rate to get the pounds of grass seed needed for a new lawn or overseeding.",
  "lede":"Work out how much grass seed to buy. Enter the lawn area and a seeding rate to get the pounds of seed for a new lawn or overseeding.",
  "inputs_heading":"Lawn measurements",
  "howto":["Grass seed is applied at a rate of pounds per 1,000 square feet. Multiply your lawn area, divide by 1,000, and multiply by the seeding rate for your grass type.",
           "New lawns use roughly twice the seed of overseeding an existing lawn. Check the rate on your seed bag, since it varies by species."],
  "formula":"pounds = area (ft\u00b2) \u00f7 1,000 \u00d7 seeding rate (lb per 1,000 ft\u00b2)",
  "ex_title":"A 5,000 ft\u00b2 new lawn at 5 lb per 1,000 ft\u00b2",
  "ex_steps":["Divide area by 1,000: 5,000 \u00f7 1,000 = <strong>5</strong>","Multiply by the rate: 5 \u00d7 5 = <strong>25 lb</strong>"],
  "ex_answer":"Buy about 25 pounds of grass seed for the new lawn.",
  "table_intro":"Typical seeding rates:",
  "table":[["Task","Rate (lb/1,000 ft\u00b2)","Note"],["New lawn (most grasses)","4-6","Full coverage"],["Overseeding","2-3","Thickening"],["Tall fescue","6-8","Heavier seed"],["Bluegrass","2-3","Fine seed"]],
  "faqs":[["How much grass seed do I need?","Divide your lawn area by 1,000, then multiply by the seeding rate on the bag. New lawns use about 4 to 6 pounds per 1,000 square feet."],
          ["How much seed for overseeding?","Roughly half the new-lawn rate, about 2 to 3 pounds per 1,000 square feet, since you are thickening existing grass rather than starting bare."],
          ["Does grass type change the rate?","Yes. Fine seeds like bluegrass need less by weight; larger seeds like tall fescue need more. Always follow the bag rate for your species."],
          ["Can I use too much seed?","Yes. Overseeding heavily makes seedlings compete and can weaken the lawn. Stick close to the recommended rate."]],
  "fields":[["length","Length","ft",100,1],["width","Width","ft",50,1],["rate","Seeding rate","lb/1k ft\u00b2",5,0.5]],
  "compute":"""var area=v.length*v.width;var lbs=area/1000*v.rate;
return{label:"Grass seed",value:H.fmt(lbs,1),unit:"lb",lines:[{label:"Lawn area",value:H.fmt(area,0)+" ft\u00b2"},{label:"Rate",value:v.rate+" lb/1k ft\u00b2"}],note:"New lawns need about double the overseeding rate. Follow your bag."};""",
 },
 {
  "slug":"retaining-wall","cat":"Concrete \u00b7 Masonry","name":"Retaining Wall Block",
  "grid":"Block counts by wall size",
  "title":"Retaining Wall Calculator: How Many Blocks Do I Need?",
  "desc":"Free retaining wall block calculator. Enter your wall length and height and block size to get how many blocks you need, with waste included.",
  "lede":"Work out how many blocks your retaining wall needs. Enter the wall length and height and your block size to get a block count with waste built in.",
  "inputs_heading":"Wall & block size",
  "howto":["Block count is the wall face divided by the face size of one block. Work out blocks per row from the wall length and block length, and the number of rows from the wall height and block height, then multiply.",
           "Add a small waste factor for cuts at ends and corners. Cap blocks and the base course of gravel and leveling sand are extra."],
  "formula":"blocks per row = wall length (in) \u00f7 block length (in)\nrows = wall height (in) \u00f7 block height (in)\nblocks = blocks per row \u00d7 rows \u00d7 (1 + waste)",
  "ex_title":"A 20 ft long, 2 ft high wall, 12 in \u00d7 4 in blocks",
  "ex_steps":["Blocks per row: (20 \u00d7 12) \u00f7 12 = <strong>20</strong>","Rows: (2 \u00d7 12) \u00f7 4 = <strong>6</strong>","Blocks: 20 \u00d7 6 = <strong>120</strong>","Add 5% waste: 120 \u00d7 1.05 = <strong>126 blocks</strong>"],
  "ex_answer":"Order about 126 wall blocks, plus caps and base material.",
  "table_intro":"Common block face sizes:",
  "table":[["Block","Length","Height"],["Standard","12 in","4 in"],["Large","18 in","6 in"],["Small","8 in","4 in"],["Cap block","varies","2-3 in"]],
  "faqs":[["How many retaining wall blocks do I need?","Divide the wall length by the block length for blocks per row, divide the wall height by the block height for rows, then multiply the two and add about 5% waste."],
          ["Do I need a base course?","Yes. The first course sits below grade on compacted gravel and leveling sand. It is the most important row for a straight, stable wall."],
          ["What about cap blocks?","Caps finish the top row and are counted separately, usually one cap per block length along the wall. Add construction adhesive for the caps."],
          ["How high can I build without an engineer?","Many areas allow segmental walls up to about 3 to 4 feet before requiring engineering or a permit. Check local codes before building higher."]],
  "fields":[["length","Wall length","ft",20,0.5],["height","Wall height","ft",2,0.5],["blocklen","Block length","in",12,0.5],["blockheight","Block height","in",4,0.5],["waste","Waste factor","%",5,1]],
  "compute":"""var per=v.blocklen>0?H.ceil(v.length*12/v.blocklen):0;var rows=v.blockheight>0?H.ceil(v.height*12/v.blockheight):0;var blocks=H.ceil(per*rows*(1+v.waste/100));
return{label:"Wall blocks",value:H.fmt(blocks,0),unit:"blocks",lines:[{label:"Rows",value:H.fmt(rows,0)},{label:"Blocks per row",value:H.fmt(per,0)},{label:"Includes waste",value:v.waste+"%"}],note:"Caps and the gravel base course are extra. Check local codes for wall height limits."};""",
 },
]

BY_SLUG = {c["slug"]: c for c in CALCS}

COSTLABEL = {
  "gravel":"Price per cubic yard","sand":"Price per cubic yard","crushed-stone":"Price per cubic yard",
  "paver-base":"Price per cubic yard (base)","concrete":"Price per cubic yard","topsoil":"Price per cubic yard",
  "mulch":"Price per cubic yard","sod":"Price per sq ft","paint":"Price per gallon","drywall":"Price per sheet",
  "flooring":"Price per sq ft","tile":"Price per tile","fence":"Price per section",
  "roofing":"Price per bundle","deck":"Price per board",
  "pea-gravel":"Price per cubic yard","river-rock":"Price per cubic yard","play-sand":"Price per cubic yard","asphalt":"Price per ton",
  "insulation":"Price per bundle","wallpaper":"Price per roll","grass-seed":"Price per lb","retaining-wall":"Price per block",
}

def price_field(c):
    label = COSTLABEL.get(c["slug"], "Price per unit") + " (optional)"
    return ["price", label, "$", "", 0.01]

# ---------------------------------------------------------------------------
def esc(s): return html.escape(s, quote=True)

def fields_js(fields):
    out = []
    for fld in fields:
        fid, label = fld[0], fld[1]
        if len(fld) >= 6 and fld[5]:           # select field
            opts = ",".join('{label:%s,value:%s}' % (json.dumps(o[0]), json.dumps(o[1])) for o in fld[5])
            out.append('{id:%s,label:%s,options:[%s],value:%s}' % (json.dumps(fid), json.dumps(label), opts, json.dumps(fld[3])))
        else:
            unit = fld[2]; val = fld[3]; step = fld[4]
            u = ('unit:%s,' % json.dumps(unit)) if unit else ''
            out.append('{id:%s,label:%s,%svalue:%s,min:0,step:%s}' % (json.dumps(fid), json.dumps(label), u, json.dumps(val), json.dumps(step)))
    return "[\n    " + ",\n    ".join(out) + "\n  ]"

def others_grid(current):
    cur = BY_SLUG.get(current); curcat = cur["cat"] if cur else None
    same = [c for c in CALCS if c["slug"] != current and c["cat"] == curcat]
    rest = [c for c in CALCS if c["slug"] != current and c["cat"] != curcat]
    ordered = (same + rest)[:7]
    cards = ['<a class="tool" href="%s.html"><div class="tname">%s</div><div class="tdesc">%s</div></a>'
             % (c["slug"], esc(c["name"]), esc(c["grid"])) for c in ordered]
    cards.append('<a class="tool" href="index.html"><div class="tname">All tools</div><div class="tdesc">See all %d calculators</div></a>' % len(CALCS))
    return "\n      ".join(cards)

def head_common(title, desc, canonical, og_extra=""):
    return f'''<!-- {SITE} build: {BUILD} -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | {SITE}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{BASE}/assets/og-image.png">{og_extra}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="icon" href="assets/favicon.svg?v={FAVV}" type="image/svg+xml">
<link rel="alternate icon" href="assets/favicon.ico?v={FAVV}" sizes="16x16 32x32 48x48">
<link rel="apple-touch-icon" href="assets/favicon-180.png?v={FAVV}">
<link rel="stylesheet" href="assets/styles.css">{analytics()}'''

TOPBAR = f'''<header class="topbar">
  <div class="wrap">
    <a class="brand" href="index.html">{MARK}{SITE}</a>
    <nav>
      <a href="gravel.html">Aggregates</a>
      <a href="concrete.html">Concrete</a>
      <a href="paint.html">Paint</a>
      <a href="index.html#guides">Guides</a>
      <a href="index.html">All tools</a>
    </nav>
  </div>
</header>'''

def footer():
    links = "".join('<a href="%s.html">%s</a>' % (c["slug"], esc(c["name"])) for c in CALCS)
    return f'''<footer class="site">
  <div class="wrap">
    <div class="fnote">{SITE}: quick, no-nonsense material estimators for job sites and weekend projects. Figures are estimates; confirm quantities with your supplier.</div>
    <nav>{links}</nav>
  </div>
</footer>'''

def calc_page(c):
    canonical = f"{BASE}/{c['slug']}.html"
    # JSON-LD: FAQ + SoftwareApplication
    faq_ld = {"@context":"https://schema.org","@type":"FAQPage",
      "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in c["faqs"]]}
    app_ld = {"@context":"https://schema.org","@type":"WebApplication",
      "name":c["title"],"url":canonical,"applicationCategory":"UtilitiesApplication",
      "operatingSystem":"Any","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},
      "description":c["desc"]}
    ld = ('\n<script type="application/ld+json">%s</script>\n<script type="application/ld+json">%s</script>'
          % (json.dumps(faq_ld), json.dumps(app_ld)))

    steps = "\n        ".join("<li>%s</li>" % s for s in c["ex_steps"])
    thead = "".join("<th>%s</th>" % esc(h) for h in c["table"][0])
    trows = "\n        ".join("<tr>%s</tr>" % "".join("<td>%s</td>" % esc(x) for x in row) for row in c["table"][1:])
    faqs = "\n    ".join(
        '<details><summary>%s</summary>\n      <p>%s</p></details>' % (esc(q), esc(a)) for q,a in c["faqs"])
    howto = "\n    ".join("<p>%s</p>" % p for p in c["howto"])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
{head_common(c["title"], c["desc"], canonical)}{ld}
</head>
<body>

{TOPBAR}

<main class="wrap">

  <div class="pagehead">
    <p class="eyebrow">{esc(c["cat"])}</p>
    <h1>{esc(c["name"])} Calculator</h1>
    <p class="lede">{esc(c["lede"])}</p>
  </div>

  <div class="calc">
    <div class="calc-grid">
      <div class="calc-inputs" id="calc-inputs"><h2>{esc(c["inputs_heading"])}</h2></div>
      <aside class="calc-result" id="calc-result"></aside>
    </div>
  </div>

  {guide_link(c)}

  <section class="block">
    <h2 class="blocktitle"><span class="n">01</span>How to calculate {esc(c["name"].lower())}</h2>
    {howto}
    <div class="formula">{esc(c["formula"])}</div>
  </section>

  <section class="block">
    <h2 class="blocktitle"><span class="n">02</span>Worked example</h2>
    <div class="example">
      <h3>{esc(c["ex_title"])}</h3>
      <ol>
        {steps}
      </ol>
      <div class="answer">{esc(c["ex_answer"])}</div>
    </div>
  </section>

  <section class="block">
    <h2 class="blocktitle"><span class="n">03</span>Reference</h2>
    <p>{esc(c["table_intro"])}</p>
    <table class="ref">
      <thead><tr>{thead}</tr></thead>
      <tbody>
        {trows}
      </tbody>
    </table>
  </section>

  <section class="block faq">
    <h2 class="blocktitle"><span class="n">04</span>Common questions</h2>
    {faqs}
  </section>

  <section class="tools">
    <h2 class="blocktitle">Related calculators</h2>
    <div class="toolgrid">
      {others_grid(c["slug"])}
    </div>
  </section>

</main>

{footer()}

<script src="assets/engine.js"></script>
<script>
window.CALC = {{
  fields: {fields_js(c["fields"] if c.get("nocost") else c["fields"] + [price_field(c)])},
  compute: function (v, H) {{
{c["compute"]}
  }}
}};
</script>
</body>
</html>
'''

def index_page():
    canonical = f"{BASE}/"
    # group cards by category, preserving order
    cats = []
    for c in CALCS:
        if c["cat"] not in [x[0] for x in cats]:
            cats.append((c["cat"], []))
        for x in cats:
            if x[0] == c["cat"]:
                x[1].append(c)
    groups_html = ""
    for cat, items in cats:
        cards = "\n      ".join(
            '<a class="tool" href="%s.html"><div class="tname">%s</div><div class="tdesc">%s</div></a>'
            % (c["slug"], esc(c["name"]), esc(c["grid"])) for c in items)
        groups_html += f'''
    <h2 class="blocktitle" style="font-size:18px;margin-top:26px;">{esc(cat)}</h2>
    <div class="toolgrid">
      {cards}
    </div>'''

    website_ld = {"@context":"https://schema.org","@type":"WebSite","name":SITE,"url":BASE+"/"}
    itemlist_ld = {"@context":"https://schema.org","@type":"ItemList",
      "itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{BASE}/{c['slug']}.html","name":c["name"]+" Calculator"}
                         for i,c in enumerate(CALCS)]}
    ld = ('\n<script type="application/ld+json">%s</script>\n<script type="application/ld+json">%s</script>'
          % (json.dumps(website_ld), json.dumps(itemlist_ld)))

    title = f"{SITE}: Free Construction Material Calculators"
    desc = "Fast, free material calculators for job sites and DIY projects. Estimate gravel, concrete, mulch, topsoil, paint, drywall, sod, and more."
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
{head_common(title, desc, canonical)}{ld}
</head>
<body>

{TOPBAR}

<main class="wrap">

  <div class="home-hero">
    <p class="eyebrow">Material estimators</p>
    <h1>Know exactly how much to order.</h1>
    <p class="lede">Free, no-signup calculators that turn a few measurements into cubic yards, tons, bags, or gallons, with a waste factor built in so you do not run short mid-job.</p>
  </div>

  <section class="tools" style="border-top:none;">{groups_html}
  </section>

{guides_section()}  <section class="block" style="margin-top:20px;">
    <h2 class="blocktitle">Why {SITE}</h2>
    <p>Every calculator here does one thing and does it fast: enter your measurements, read the answer. No accounts, no walls of ads over the tool, no guessing at the math. Each one also shows the formula and a worked example, so you can check the number yourself or run it by hand on site.</p>
    <p>Estimates include a waste factor because real jobs are not tidy: ground is not level, material settles, and some is always lost in handling. The goal is a number you can order from with confidence. Always confirm density and coverage with your supplier for the exact product you are buying.</p>
  </section>

</main>

{footer()}

</body>
</html>
'''

def sitemap():
    urls = [f"{BASE}/"] + [f"{BASE}/{c['slug']}.html" for c in CALCS] + [f"{BASE}/{g['slug']}.html" for g in GUIDES]
    items = "\n".join(
        f"  <url><loc>{u}</loc><changefreq>monthly</changefreq><priority>{'1.0' if u.endswith('/') else '0.8'}</priority></url>"
        for u in urls)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{items}
</urlset>
'''

def robots():
    return f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n"

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Cost guides (article-style pages that link into the calculators)
# ---------------------------------------------------------------------------
GUIDES = [{'slug': 'gravel-driveway-cost',
  'calc_slug': 'gravel',
  'calc_name': 'Gravel',
  'eyebrow': 'Cost guide · Aggregates',
  'name': 'Gravel Driveway Cost',
  'griddesc': 'What a gravel driveway costs',
  'title': 'Gravel Driveway Cost: What You Will Pay',
  'desc': 'What does a gravel driveway cost? A clear breakdown of gravel prices per ton, delivery, installation '
          'per square foot, and how to estimate your own driveway.',
  'h1': 'How Much Does a Gravel Driveway Cost?',
  'lede': 'Gravel is the cheapest way to surface a driveway. Here is what the material, delivery, and '
          'installation typically run, plus how to estimate the tonnage for your own driveway.',
  'glance_label': 'Typical installed driveway',
  'glance_range': '$1,200 to $4,500',
  'glance_note': 'Roughly $1 to $3 per square foot installed. A flat, do-it-yourself job can cost far less, since '
                 'you pay only for material and delivery.',
  'intro': ['A gravel driveway is priced two ways: the loose material by the ton or cubic yard, and the finished '
            'job by the square foot once delivery, base preparation, and labor are included.',
            'As a rough guide, expect about 1 to 3 dollars per square foot for a professionally installed gravel '
            'driveway over a prepared base. A basic material-only refresh that you spread yourself costs a '
            'fraction of that.'],
  'breakdown_intro': 'The main cost pieces for a gravel driveway:',
  'breakdown_table': [['Item', 'Typical range', 'Notes'],
                      ['Gravel material',
                       '$15 to $75 per ton',
                       'Crushed stone low, decorative and pea gravel higher'],
                      ['Delivery', '$50 to $150 per load', 'Depends on distance and truck size'],
                      ['Base / sub-base stone', '$15 to $40 per ton', 'Larger stone under the top layer'],
                      ['Grading and prep', '$1 to $2 per sq ft', 'Excavation, leveling, fabric'],
                      ['Installed, all-in (pro)', '$1 to $3 per sq ft', 'Material, base, labor'],
                      ['DIY, material only', '40 to 60% less', 'You supply the labor']],
  'factors': ['Size is the biggest driver. A long or double-wide driveway needs more tons, and cost scales almost '
              'directly with area and depth.',
              'Gravel type matters. Plain crushed stone and crusher run are cheapest; decorative river rock, pea '
              'gravel, and colored stone cost more per ton.',
              'Depth and layers add up. A durable driveway is built in layers, a coarse base topped with a finer '
              'surface, so it needs more material than a single thin layer.',
              'Site prep can dominate a quote. Excavation, hauling away old material, grading for drainage, and '
              'landscape fabric all add labor and cost.',
              'Delivery distance and region shift the total. Rural sites far from a quarry pay more for hauling, '
              'and prices vary widely by area.'],
  'diy_title': 'DIY or hire a pro?',
  'diy': ['A gravel top-up on a flat, stable driveway is a reasonable do-it-yourself job. You order the tonnage, '
          'have it delivered, and spread and rake it. Your main cost is material and delivery.',
          'Hire a pro when the driveway is new, needs excavation, has drainage problems, or sits on a slope. '
          'Proper grading and a compacted base are what keep gravel from washing out and rutting, and that is '
          'worth paying for on a full build.'],
  'faqs': [['How much does a gravel driveway cost?',
            'Roughly 1 to 3 dollars per square foot installed by a contractor. A material-only DIY refresh costs '
            'much less, since you pay only for the gravel and delivery.'],
           ['Is a gravel driveway cheaper than concrete or asphalt?',
            'Yes, by a wide margin. Gravel is the least expensive driveway surface up front, though it needs '
            'occasional top-ups that concrete and asphalt do not.'],
           ['How much gravel do I need for a driveway?',
            'Multiply length by width by depth to get the volume, then convert to tons. Plan on 4 to 6 inches of '
            'depth for a driveway. The gravel calculator does this for you.'],
           ['How long does a gravel driveway last?',
            'Many years with light upkeep. Expect to add a fresh top layer every few years and to regrade '
            'occasionally to fill ruts and keep drainage working.']]},
 {'slug': 'concrete-slab-cost',
  'calc_slug': 'concrete',
  'calc_name': 'Concrete',
  'eyebrow': 'Cost guide · Concrete',
  'name': 'Concrete Slab Cost',
  'griddesc': 'What a concrete slab costs',
  'title': 'Concrete Slab Cost: Per Square Foot and Per Yard',
  'desc': 'What does a concrete slab cost? Prices per square foot installed, per cubic yard of ready-mix, DIY '
          'versus pro, and how to estimate the concrete for your slab.',
  'h1': 'How Much Does a Concrete Slab Cost?',
  'lede': 'Concrete slab cost comes down to size, thickness, and finish. Here is what ready-mix costs per yard, '
          'what a finished slab runs per square foot, and how to estimate your own pour.',
  'glance_label': 'Installed concrete slab',
  'glance_range': '$4 to $8 per sq ft',
  'glance_note': 'Basic broom-finish slabs sit in this range. Reinforcement, decorative finishes, and small pours '
                 'push it higher. Ready-mix alone is about $120 to $180 per cubic yard.',
  'intro': ['A concrete slab is priced by the square foot once you include material, forming, reinforcement, '
            'labor, and finishing. The concrete itself is sold by the cubic yard as ready-mix, or by the bag for '
            'small pours.',
            'A basic broom-finished slab commonly runs 4 to 8 dollars per square foot installed. Decorative '
            'finishes and heavy reinforcement can push that well above 10.'],
  'breakdown_intro': 'The main cost pieces for a concrete slab:',
  'breakdown_table': [['Item', 'Typical range', 'Notes'],
                      ['Ready-mix concrete', '$120 to $180 per yd³', 'Delivered, before labor'],
                      ['Installed slab (basic)', '$4 to $8 per sq ft', 'Broom finish, standard thickness'],
                      ['Installed slab (finished)', '$8 to $12+ per sq ft', 'Stamped, colored, or polished'],
                      ['80 lb bag (DIY)', '$5 to $8 per bag', 'Small pads and posts only'],
                      ['Reinforcement', '$0.50 to $1.50 per sq ft', 'Wire mesh, rebar, or fiber'],
                      ['Pump truck', '$150 to $250', 'Only if the mixer cannot reach']],
  'factors': ['Thickness sets the volume. A 4 inch slab is standard for patios and floors; driveways and '
              'load-bearing slabs go to 5 or 6 inches and use proportionally more concrete.',
              'Square footage changes the per-foot price. Small slabs cost more per square foot because setup, '
              'delivery, and minimum charges spread over less area.',
              'Finish is a big lever. A plain broom finish is cheapest. Stamped, stained, exposed-aggregate, and '
              'polished finishes add labor and material.',
              'Reinforcement and prep add up. Wire mesh, rebar, a gravel sub-base, and forming all add to a bare '
              'pour, and they are what make a slab last.',
              'Access and region matter. If a mixer cannot reach the site you may need a pump, and local labor '
              'and material rates vary widely.'],
  'diy_title': 'DIY or hire a pro?',
  'diy': ['Bagged concrete is fine for a small pad, footing, or setting posts. Once you are past roughly half a '
          'cubic yard, bags stop making sense and ready-mix is cheaper and faster.',
          'Pouring and finishing a large slab is demanding work with a short time window before the concrete '
          'sets. Forming, screeding, and finishing a smooth, flat slab takes skill, so most people hire a pro for '
          'anything sizable or visible.'],
  'faqs': [['How much does a concrete slab cost?',
            'Most basic slabs run 4 to 8 dollars per square foot installed. Decorative finishes and reinforcement '
            'push the price higher.'],
           ['How much does a yard of concrete cost?',
            'Ready-mix concrete is roughly 120 to 180 dollars per cubic yard delivered, before forming, labor, '
            'and finishing.'],
           ['Is it cheaper to pour concrete yourself?',
            'The material alone is much cheaper than a full installed price, but slabs are labor-intensive and '
            'time-sensitive. DIY saves money only if you have the skill and help.'],
           ['How much concrete do I need?',
            'Multiply length by width by thickness to get the volume in cubic yards. The concrete calculator also '
            'gives you the number of 60 and 80 pound bags.']]},
 {'slug': 'sod-cost',
  'calc_slug': 'sod',
  'calc_name': 'Sod',
  'eyebrow': 'Cost guide · Lawn',
  'name': 'Sod Cost',
  'griddesc': 'What sod costs to buy and install',
  'title': 'Sod Cost: Per Square Foot and Per Pallet',
  'desc': 'What does sod cost? Prices per square foot and per pallet, installation cost, sod versus seed, and how '
          'to estimate how much sod your lawn needs.',
  'h1': 'How Much Does Sod Cost?',
  'lede': 'Sod gives an instant lawn, at a higher price than seed. Here is what sod costs per square foot and per '
          'pallet, what installation adds, and how to estimate your lawn.',
  'glance_label': 'Installed sod lawn',
  'glance_range': '$0.90 to $2.00 per sq ft',
  'glance_note': 'The sod itself is about $0.30 to $0.80 per square foot. The rest is soil prep, delivery, and '
                 'labor. A pallet covers roughly 450 square feet.',
  'intro': ['Sod is priced by the square foot or by the pallet for the grass itself, plus soil preparation and '
            'labor if a crew installs it. A pallet typically covers about 450 square feet.',
            'Laid by a pro over prepared soil, sod commonly runs about 0.90 to 2.00 dollars per square foot '
            'all-in. Buying and laying it yourself costs much less, since labor is the largest part.'],
  'breakdown_intro': 'The main cost pieces for a sod lawn:',
  'breakdown_table': [['Item', 'Typical range', 'Notes'],
                      ['Sod material', '$0.30 to $0.80 per sq ft', 'Varies by grass type and region'],
                      ['Per pallet', '$150 to $450', 'Covers about 450 sq ft'],
                      ['Soil prep and grading', '$0.50 to $1.00 per sq ft', 'Tilling, leveling, amendments'],
                      ['Installation labor', '$0.30 to $0.90 per sq ft', 'Laying and rolling'],
                      ['Old lawn removal', 'adds to the total', 'If replacing existing grass'],
                      ['Delivery', '$50 to $150', 'Per load, by distance']],
  'factors': ['Lawn size drives the pallet count and the labor. Larger lawns cost more overall but often a little '
              'less per square foot.',
              'Grass type changes the material price. Common cool-season and warm-season grasses are affordable; '
              'specialty or drought-tolerant varieties cost more.',
              'Site prep is a real cost. Removing an old lawn, tilling, grading, and adding topsoil all add labor '
              'before a single roll goes down.',
              'Slope and access affect labor. Steep or hard-to-reach yards take longer to prepare and lay.',
              'Season and region matter. Sod is cheapest and establishes best in the growing season, and prices '
              'vary by local farm supply.'],
  'diy_title': 'DIY or hire a pro?',
  'diy': ['Laying sod yourself is achievable on a small, already-level yard. You prepare the soil, order pallets, '
          'and lay and roll the sod, paying mainly for material and delivery.',
          'Hire a pro for large lawns, heavy grading, or old-lawn removal. Even coverage and good soil contact '
          'are what let sod root, and a crew with the right tools gets that done fast before the sod dries out.'],
  'faqs': [['How much does sod cost per square foot?',
            'The sod itself is about 0.30 to 0.80 dollars per square foot. Installed over prepared soil, expect '
            'roughly 0.90 to 2.00 dollars per square foot.'],
           ['How much does a pallet of sod cost?',
            'Usually 150 to 450 dollars, and a pallet covers around 450 square feet, though coverage varies by '
            'farm.'],
           ['Is sod cheaper than seed?',
            'No. Seed costs far less up front. Sod costs more but gives an instant, established lawn with less '
            'risk of washout and weeds.'],
           ['How much sod do I need?',
            'Multiply your lawn length by width for the area, then divide by the pallet coverage. The sod '
            'calculator gives pallets and rolls with a cutting allowance.']]},
 {'slug': 'paver-patio-cost',
  'calc_slug': 'paver-base',
  'calc_name': 'Paver Base',
  'eyebrow': 'Cost guide · Hardscape',
  'name': 'Paver Patio Cost',
  'griddesc': 'What a paver patio costs',
  'title': 'Paver Patio Cost: Price Per Square Foot',
  'desc': 'What does a paver patio cost? Prices per square foot installed and DIY, paver and base material costs, '
          'and how to estimate the base and sand you need.',
  'h1': 'How Much Does a Paver Patio Cost?',
  'lede': 'A paver patio costs more than poured concrete but lasts and looks better. Here is the price per square '
          'foot installed and as a DIY job, plus how to estimate your base materials.',
  'glance_label': 'Installed paver patio',
  'glance_range': '$10 to $25 per sq ft',
  'glance_note': 'Basic pavers over a standard base sit at the low end. Premium or permeable pavers and complex '
                 'patterns run higher. DIY material alone is roughly $3 to $6 per square foot.',
  'intro': ['A paver patio is priced by the square foot, covering the pavers themselves plus the crushed-stone '
            'base, bedding sand, edging, and labor. Material quality and pattern complexity move the number the '
            'most.',
            'Installed by a pro, a basic paver patio commonly runs 10 to 17 dollars per square foot, with premium '
            'and permeable systems pushing toward 25. Doing it yourself cuts out the labor, the largest single '
            'cost.'],
  'breakdown_intro': 'The main cost pieces for a paver patio:',
  'breakdown_table': [['Item', 'Typical range', 'Notes'],
                      ['Pavers', '$2 to $8 per sq ft', 'Concrete low, clay and premium higher'],
                      ['Base stone and sand', '$1 to $3 per sq ft', 'Crushed base plus bedding sand'],
                      ['Installed, basic (pro)', '$10 to $17 per sq ft', 'Standard pavers and base'],
                      ['Installed, premium (pro)',
                       '$17 to $25+ per sq ft',
                       'Clay, permeable, or intricate patterns'],
                      ['Edging and polymeric sand', '$1 to $2 per sq ft', 'Holds the field together'],
                      ['DIY, material only', '$3 to $6 per sq ft', 'You supply the labor']],
  'factors': ['Paver type is the biggest swing. Standard concrete pavers are affordable; clay brick, natural '
              'stone, and permeable pavers cost more per square foot.',
              'Patio size affects the per-foot price. Larger patios spread setup and delivery over more area, so '
              'they often cost a little less per square foot.',
              'Base depth and prep matter. A patio over soft soil needs a deeper compacted base, and excavation '
              'and hauling spoil away add labor.',
              'Pattern complexity adds labor. Herringbone, borders, and curves take longer to cut and lay than a '
              'simple running bond.',
              'Slope, drainage, and access all shift the labor, and prices vary by region.'],
  'diy_title': 'DIY or hire a pro?',
  'diy': ['A small, flat paver patio is a popular do-it-yourself project. The work is excavation, a compacted '
          'base, screeded bedding sand, laying the pavers, and locking them with edging and polymeric sand.',
          'The base is everything. Most failed patios fail because the base was too thin or poorly compacted. '
          'Hire a pro for large patios, poor soil, or anything on a slope, where getting the base and drainage '
          'right is worth the labor cost.'],
  'faqs': [['How much does a paver patio cost?',
            'Roughly 10 to 25 dollars per square foot installed, depending on the paver and the base. A DIY patio '
            'costs much less since labor is the biggest part.'],
           ['Are pavers cheaper than concrete?',
            'Pavers usually cost more up front than a poured concrete slab, but they resist cracking, are easy to '
            'repair, and many people prefer the look.'],
           ['How much base do I need under pavers?',
            'Plan on about 4 to 6 inches of compacted crushed stone plus an inch of bedding sand. The paver base '
            'calculator gives you the cubic yards of each.'],
           ['Can I lay pavers myself?',
            'Yes, on a small flat area. The key is a deep, well-compacted base and a level bedding layer. Rushing '
            'the base is the most common mistake.']]},
 {'slug': 'asphalt-driveway-cost',
  'calc_slug': 'asphalt',
  'calc_name': 'Asphalt',
  'eyebrow': 'Cost guide · Aggregates',
  'name': 'Asphalt Driveway Cost',
  'griddesc': 'What an asphalt driveway costs',
  'title': 'Asphalt Driveway Cost: Price Per Square Foot',
  'desc': 'What does an asphalt driveway cost? Prices per square foot and per ton, new versus resurfacing, and '
          'how to estimate the tons of hot mix you need.',
  'h1': 'How Much Does an Asphalt Driveway Cost?',
  'lede': 'Asphalt sits between gravel and concrete on price and gives a smooth, durable driveway. Here is what '
          'it costs per square foot and per ton, plus how to estimate the tonnage.',
  'glance_label': 'New installed driveway',
  'glance_range': '$3 to $7 per sq ft',
  'glance_note': 'A typical residential driveway runs about $2,000 to $6,000 installed. Resurfacing an existing '
                 'base costs less; a full new build over fresh stone costs more. Hot mix is roughly $100 to $200 '
                 'per ton.',
  'intro': ['An asphalt driveway is priced by the square foot installed, or by the ton for the hot mix itself. '
            'The finished price includes the stone base, the asphalt, and the paving crew.',
            'New asphalt driveways commonly run 3 to 7 dollars per square foot. Resurfacing over a sound existing '
            'base is cheaper, while a full excavation and new base is at the top of the range.'],
  'breakdown_intro': 'The main cost pieces for an asphalt driveway:',
  'breakdown_table': [['Item', 'Typical range', 'Notes'],
                      ['Hot-mix asphalt', '$100 to $200 per ton', 'Material, before labor'],
                      ['Installed, new (pro)', '$3 to $7 per sq ft', 'Base plus paving'],
                      ['Resurfacing / overlay', '$2 to $4 per sq ft', 'Over a sound base'],
                      ['Stone base', '$1 to $2 per sq ft', 'Compacted sub-base'],
                      ['Sealcoating', '$0.15 to $0.25 per sq ft', 'Every few years'],
                      ['Old surface removal', 'adds to the total', 'If replacing']],
  'factors': ['Size and thickness set the tonnage. A thicker mat and a larger driveway both use more hot mix, '
              'which is sold by the ton.',
              'New build or overlay makes a big difference. Paving over a sound existing surface skips excavation '
              'and base work; a full rebuild does not.',
              'The base is critical and costs money. Asphalt needs a compacted stone base to last, and weak soil '
              'means more excavation and stone.',
              'Oil-based material prices swing with the market, so asphalt quotes move more over time than most '
              'materials.',
              'Access, slope, and region all affect crew time and the final number.'],
  'diy_title': 'DIY or hire a pro?',
  'diy': ['Asphalt is not a typical do-it-yourself material. Hot mix arrives very hot and has to be spread and '
          'compacted quickly with the right equipment, so almost all asphalt driveways are installed by a paving '
          'crew.',
          'Where you can save is upkeep. Sealcoating and filling small cracks yourself every few years extends '
          'the life of the driveway and is well within DIY range.'],
  'faqs': [['How much does an asphalt driveway cost?',
            'Usually 3 to 7 dollars per square foot for a new driveway installed, or roughly 2,000 to 6,000 '
            'dollars for an average residential driveway.'],
           ['How much is asphalt per ton?',
            'Hot-mix asphalt is roughly 100 to 200 dollars per ton for the material, before base work and labor. '
            'The price tracks oil markets.'],
           ['Is asphalt cheaper than concrete?',
            'Usually yes. Asphalt typically costs less than a concrete driveway up front, though it needs '
            'sealcoating and has a shorter lifespan.'],
           ['How much asphalt do I need?',
            'Multiply area by thickness for the volume, then convert to tons using the mix density. The asphalt '
            'calculator gives you the tonnage with waste included.']]},
 {'slug': 'topsoil-cost',
  'calc_slug': 'topsoil',
  'calc_name': 'Topsoil',
  'eyebrow': 'Cost guide · Soil',
  'name': 'Topsoil Cost',
  'griddesc': 'What topsoil costs by the yard',
  'title': 'Topsoil Cost: Price Per Yard and Per Bag',
  'desc': 'What does topsoil cost? Bulk prices per cubic yard, bagged prices, delivery, and how to estimate how '
          'much topsoil your project needs.',
  'h1': 'How Much Does Topsoil Cost?',
  'lede': 'Topsoil is cheap in bulk and pricier by the bag. Here is what a cubic yard costs delivered, when bags '
          'make sense, and how to estimate the amount you need.',
  'glance_label': 'Bulk screened topsoil',
  'glance_range': '$12 to $55 per cubic yard',
  'glance_note': 'Plus delivery of about $50 to $150 per load. Premium and compost-blended soils cost more. '
                 'Bagged topsoil is convenient but far more expensive per yard.',
  'intro': ['Topsoil is sold in bulk by the cubic yard and in bags for small jobs. Bulk is far cheaper per yard '
            'once you add up bag prices, but bags are easier to handle for a small bed.',
            'Screened bulk topsoil commonly runs 12 to 55 dollars per cubic yard before delivery, with premium '
            'and compost-amended blends higher. Delivery is usually a flat charge per load.'],
  'breakdown_intro': 'The main cost pieces for topsoil:',
  'breakdown_table': [['Item', 'Typical range', 'Notes'],
                      ['Bulk fill dirt', '$5 to $20 per yd³', 'Unscreened, for filling'],
                      ['Bulk screened topsoil', '$12 to $55 per yd³', 'Common for lawns and beds'],
                      ['Premium / compost blend', '$30 to $70 per yd³', 'Amended garden soil'],
                      ['Bagged topsoil', '$2 to $5 per bag', 'About 0.75 ft³ each'],
                      ['Delivery', '$50 to $150 per load', 'By distance and volume'],
                      ['Spreading (pro)', 'adds labor', 'If you are not doing it']],
  'factors': ['Quality is the main driver. Rough fill dirt is cheapest; screened topsoil costs more; amended '
              'garden and compost blends cost the most.',
              'Quantity changes the unit price. Bulk by the yard is much cheaper than bags once you need more '
              'than a few bags.',
              'Delivery is often a flat fee, so small orders cost a lot per yard once hauling is included.',
              'Region and season shift prices, and demand peaks in spring when everyone is planting.'],
  'diy_title': 'Bulk or bags?',
  'diy': ['For anything larger than a small bed, bulk delivery wins on price. You order the cubic yards, have '
          'them dumped, and move the soil with a wheelbarrow.',
          'Bags make sense only for small top-ups where you want no delivery fee and easy handling. It takes '
          'about 36 of the 0.75 cubic foot bags to equal one bulk cubic yard.'],
  'faqs': [['How much does a yard of topsoil cost?',
            'Bulk screened topsoil is roughly 12 to 55 dollars per cubic yard before delivery. Fill dirt is '
            'cheaper; amended garden blends cost more.'],
           ['How much does bagged topsoil cost?',
            'About 2 to 5 dollars for a bag holding roughly 0.75 cubic feet, which works out far more expensive '
            'per yard than bulk.'],
           ['How many bags in a cubic yard?',
            'About 36 of the common 0.75 cubic foot bags. That is why bulk delivery wins for larger jobs.'],
           ['How much topsoil do I need?',
            'Multiply length by width by depth, then convert to cubic yards. The topsoil calculator also gives '
            'tons and bag counts.']]},
 {'slug': 'mulch-cost',
  'calc_slug': 'mulch',
  'calc_name': 'Mulch',
  'eyebrow': 'Cost guide · Garden',
  'name': 'Mulch Cost',
  'griddesc': 'What mulch costs by the yard',
  'title': 'Mulch Cost: Price Per Yard and Per Bag',
  'desc': 'What does mulch cost? Bulk prices per cubic yard, bagged prices, dyed and premium options, and how to '
          'estimate how much mulch your beds need.',
  'h1': 'How Much Does Mulch Cost?',
  'lede': 'Mulch is inexpensive in bulk and handy by the bag. Here is what a cubic yard costs, how dyed and '
          'premium types compare, and how to estimate your beds.',
  'glance_label': 'Bulk hardwood mulch',
  'glance_range': '$20 to $50 per cubic yard',
  'glance_note': 'Plus delivery of about $50 to $150 per load. Dyed, cedar, and premium mulches cost more. Bagged '
                 'mulch runs about $2 to $5 for a 2 cubic foot bag.',
  'intro': ['Mulch is sold in bulk by the cubic yard and in 2 cubic foot bags. Bulk is cheaper per yard, while '
            'bags are easy to carry and store for small beds.',
            'Standard bulk hardwood mulch commonly runs 20 to 50 dollars per cubic yard before delivery, with '
            'dyed and premium types higher. One cubic yard equals about 13.5 bags.'],
  'breakdown_intro': 'The main cost pieces for mulch:',
  'breakdown_table': [['Item', 'Typical range', 'Notes'],
                      ['Bulk hardwood', '$20 to $50 per yd³', 'Standard shredded bark'],
                      ['Bulk dyed / premium', '$30 to $60 per yd³', 'Colored, cedar, or fine'],
                      ['Bagged mulch', '$2 to $5 per bag', '2 ft³ per bag'],
                      ['Delivery', '$50 to $150 per load', 'By distance and volume'],
                      ['Spreading (pro)', 'adds labor', 'If you are not doing it'],
                      ['DIY, material only', 'just the mulch', 'You spread it']],
  'factors': ['Type sets the price. Plain hardwood is cheapest; dyed, cedar, and finely shredded mulches cost '
              'more, and rubber mulch is a separate premium category.',
              'Quantity changes the unit price. Bulk beats bags once you need more than about ten bags.',
              'Delivery is usually a flat fee per load, so small bulk orders carry a high per-yard hauling cost.',
              'Color and quality vary by supplier, and prices rise in spring planting season.'],
  'diy_title': 'Bulk or bags?',
  'diy': ['Spreading mulch is easy do-it-yourself work. For larger beds, bulk delivery is much cheaper and you '
          'move it with a wheelbarrow and rake.',
          'Bags are convenient for small beds and let you buy only what you need with no delivery fee. The '
          'crossover to bulk is around ten bags.'],
  'faqs': [['How much does a yard of mulch cost?',
            'Bulk hardwood mulch is roughly 20 to 50 dollars per cubic yard before delivery. Dyed and premium '
            'types cost more.'],
           ['How much does a bag of mulch cost?',
            'About 2 to 5 dollars for a standard 2 cubic foot bag. Bulk is cheaper per yard once you need more '
            'than about ten bags.'],
           ['How many bags of mulch in a yard?',
            'About 13.5 of the standard 2 cubic foot bags make one cubic yard.'],
           ['How much mulch do I need?',
            'Multiply bed length by width by depth, then convert to cubic yards. The mulch calculator also gives '
            'the bag count.']]}]

GUIDE_FOR = {g["calc_slug"]: g for g in GUIDES}

def guide_link(c):
    g = GUIDE_FOR.get(c["slug"])
    if not g:
        return ""
    return ('<div class="callout"><div class="ctext"><strong>Planning a budget?</strong> '
            'See our ' + esc(g["name"]) + ' guide for price ranges and what drives the cost.</div>'
            '<a class="btn" href="' + g["slug"] + '.html">Read the ' + esc(g["name"]) + ' guide</a></div>')

def guides_section():
    if not GUIDES:
        return ""
    cards = "\n      ".join('<a class="tool" href="%s.html"><div class="tname">%s</div><div class="tdesc">%s</div></a>'
                            % (g["slug"], esc(g["name"]), esc(g["griddesc"])) for g in GUIDES)
    return ('  <section class="tools" id="guides">\n'
            '    <h2 class="blocktitle">Cost guides</h2>\n'
            '    <div class="toolgrid">\n      ' + cards + '\n    </div>\n  </section>\n\n')

def guide_page(g):
    canonical = f"{BASE}/{g['slug']}.html"
    calc_url = g["calc_slug"] + ".html"
    faq_ld = {"@context":"https://schema.org","@type":"FAQPage",
      "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in g["faqs"]]}
    art_ld = {"@context":"https://schema.org","@type":"Article","headline":g["title"],
      "description":g["desc"],"author":{"@type":"Organization","name":SITE},
      "publisher":{"@type":"Organization","name":SITE},"mainEntityOfPage":canonical}
    ld = ('\n<script type="application/ld+json">%s</script>\n<script type="application/ld+json">%s</script>'
          % (json.dumps(art_ld), json.dumps(faq_ld)))
    intro   = "\n    ".join("<p>%s</p>" % esc(p) for p in g["intro"])
    factors = "\n    ".join("<p>%s</p>" % esc(p) for p in g["factors"])
    diy     = "\n    ".join("<p>%s</p>" % esc(p) for p in g["diy"])
    thead = "".join("<th>%s</th>" % esc(h) for h in g["breakdown_table"][0])
    trows = "\n        ".join("<tr>%s</tr>" % "".join("<td>%s</td>" % esc(x) for x in row) for row in g["breakdown_table"][1:])
    faqs = "\n    ".join('<details><summary>%s</summary>\n      <p>%s</p></details>' % (esc(q), esc(a)) for q,a in g["faqs"])
    cta = ('<div class="callout"><div class="ctext"><strong>Need your exact quantity?</strong> '
           'Estimate the materials for your project with the ' + esc(g["calc_name"]) + ' calculator.</div>'
           '<a class="btn" href="' + calc_url + '">Open the ' + esc(g["calc_name"]) + ' calculator</a></div>')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
{head_common(g["title"], g["desc"], canonical)}{ld}
</head>
<body>

{TOPBAR}

<main class="wrap">

  <div class="pagehead">
    <p class="eyebrow">{esc(g["eyebrow"])}</p>
    <h1>{esc(g["h1"])}</h1>
    <p class="lede">{esc(g["lede"])}</p>
  </div>

  <div class="glance">
    <div class="glabel">{esc(g["glance_label"])}</div>
    <div class="grange">{esc(g["glance_range"])}</div>
    <p>{esc(g["glance_note"])}</p>
  </div>

  <p style="font-size:13.5px;color:var(--muted);margin:-6px 0 20px;">Prices are ballpark ranges that vary by region, supplier, and season. Get local quotes before budgeting.</p>

  {cta}

  <section class="block">
    <h2 class="blocktitle"><span class="n">01</span>What it costs</h2>
    {intro}
  </section>

  <section class="block">
    <h2 class="blocktitle"><span class="n">02</span>Cost breakdown</h2>
    <p>{esc(g["breakdown_intro"])}</p>
    <table class="ref">
      <thead><tr>{thead}</tr></thead>
      <tbody>
        {trows}
      </tbody>
    </table>
  </section>

  <section class="block">
    <h2 class="blocktitle"><span class="n">03</span>What affects the cost</h2>
    {factors}
  </section>

  {cta}

  <section class="block">
    <h2 class="blocktitle"><span class="n">04</span>{esc(g["diy_title"])}</h2>
    {diy}
  </section>

  <section class="block faq">
    <h2 class="blocktitle"><span class="n">05</span>Common questions</h2>
    {faqs}
  </section>

  <section class="tools">
    <h2 class="blocktitle">Related calculators</h2>
    <div class="toolgrid">
      {others_grid(g["calc_slug"])}
    </div>
  </section>

</main>

{footer()}

</body>
</html>
'''


if __name__ == "__main__":
    for c in CALCS:
        open(f"{c['slug']}.html","w",encoding="utf-8").write(calc_page(c))
    for g in GUIDES:
        open(f"{g['slug']}.html","w",encoding="utf-8").write(guide_page(g))
    open("index.html","w",encoding="utf-8").write(index_page())
    open("sitemap.xml","w",encoding="utf-8").write(sitemap())
    open("robots.txt","w",encoding="utf-8").write(robots())
    print("built", len(CALCS), "calculators +", len(GUIDES), "guides + index + sitemap + robots")
