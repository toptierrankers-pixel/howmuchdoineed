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
BUILD = "2026-07-26 v3 - 10 calculators + SEO"   # favicon cache-buster; bump when the icon changes

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
]

BY_SLUG = {c["slug"]: c for c in CALCS}

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
    cards = []
    for c in CALCS:
        if c["slug"] == current: continue
        cards.append('<a class="tool" href="%s.html"><div class="tname">%s</div><div class="tdesc">%s</div></a>'
                     % (c["slug"], esc(c["name"]), esc(c["grid"])))
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
<link rel="stylesheet" href="assets/styles.css">'''

TOPBAR = f'''<header class="topbar">
  <div class="wrap">
    <a class="brand" href="index.html">{MARK}{SITE}</a>
    <nav>
      <a href="gravel.html">Aggregates</a>
      <a href="concrete.html">Concrete</a>
      <a href="paint.html">Paint</a>
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
    <h2 class="blocktitle">Other material calculators</h2>
    <div class="toolgrid">
      {others_grid(c["slug"])}
    </div>
  </section>

</main>

{footer()}

<script src="assets/engine.js"></script>
<script>
window.CALC = {{
  fields: {fields_js(c["fields"])},
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

  <section class="block" style="margin-top:20px;">
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
    urls = [f"{BASE}/"] + [f"{BASE}/{c['slug']}.html" for c in CALCS]
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
if __name__ == "__main__":
    for c in CALCS:
        open(f"{c['slug']}.html","w",encoding="utf-8").write(calc_page(c))
    open("index.html","w",encoding="utf-8").write(index_page())
    open("sitemap.xml","w",encoding="utf-8").write(sitemap())
    open("robots.txt","w",encoding="utf-8").write(robots())
    print("built", len(CALCS), "calculators + index + sitemap + robots")
