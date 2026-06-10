"""
Sacramento / California 'On This Day' historical facts and famous birthdays.

Priority order for each date:
  1. Sacramento-specific dated event  (ON_THIS_DAY)
  2. California history dated event   (CALIFORNIA_ON_THIS_DAY)
  3. Famous person born on this day with Sacramento / CA connection  (FAMOUS_BIRTHDAYS)
  4. Seeded-random fallback from general Sacramento history pool
"""
from __future__ import annotations
import random
from datetime import date

# ---------------------------------------------------------------------------
# 1. Sacramento-specific dated events  (key: "MM-DD")
# ---------------------------------------------------------------------------
ON_THIS_DAY: dict[str, dict] = {
    "01-06": {
        "year": 1850,
        "fact": "Sacramento's first city council held its inaugural meeting",
        "detail": "Just months after the Gold Rush began, Sacramento's newly elected council convened on January 6, 1850, laying the foundations for California's future capital city.",
    },
    "01-14": {
        "year": 1848,
        "fact": "News of gold at Sutter's Mill reached San Francisco, igniting the Gold Rush",
        "detail": "Although James Marshall's discovery on January 24, 1848 was kept secret, word leaked out and reached San Francisco by mid-January, setting off the greatest mass migration in American history toward Sacramento.",
    },
    "01-24": {
        "year": 1848,
        "fact": "James Marshall discovered gold at Sutter's Mill, launching the California Gold Rush",
        "detail": "Carpenter James Marshall spotted gold flakes in the American River at Coloma — just 50 miles from Sacramento. Within a year, 300,000 prospectors flooded through Sacramento, transforming a small fort into a booming city.",
    },
    "01-28": {
        "year": 1863,
        "fact": "Central Pacific Railroad broke ground in Sacramento, beginning the Transcontinental Railroad",
        "detail": "Governor Leland Stanford turned the first ceremonial shovel of earth at Front and K Streets in Sacramento, launching the western half of the First Transcontinental Railroad. Six years later, the coasts would be connected.",
    },
    "02-18": {
        "year": 1856,
        "fact": "Sacramento was officially incorporated as a city",
        "detail": "After years as an unincorporated boomtown, Sacramento was formally incorporated on February 18, 1856, with Hardin Bigelow as its first elected mayor. The city had already survived floods, fires, and cholera epidemics.",
    },
    "02-27": {
        "year": 1854,
        "fact": "The California legislature voted to make Sacramento the permanent state capital",
        "detail": "After bouncing between San Jose, Vallejo, and Benicia, lawmakers chose Sacramento on February 27, 1854 — largely due to its central location and Gold Rush wealth.",
    },
    "03-04": {
        "year": 1860,
        "fact": "The first Pony Express advertisement announced Sacramento as the western terminus",
        "detail": "Posters across Sacramento announced: 'Wanted: Young, skinny, wiry fellows not over 18. Must be expert riders willing to risk death daily. Orphans preferred.' The service launched less than a month later.",
    },
    "03-22": {
        "year": 1861,
        "fact": "The California State Capitol cornerstone was laid in Sacramento",
        "detail": "Construction began on the iconic Capitol building on Capitol Mall. It would take until 1874 to complete, and the building still serves as California's seat of government today.",
    },
    "04-03": {
        "year": 1860,
        "fact": "The first Pony Express rider departed Sacramento for Missouri",
        "detail": "On April 3, 1860, a rider galloped out of Sacramento carrying 49 letters, 5 telegrams, and newspapers — beginning the 1,966-mile route to St. Joseph, Missouri. The mail arrived in just 10 days.",
    },
    "04-13": {
        "year": 1850,
        "fact": "Sacramento was incorporated as a city for the first time",
        "detail": "Sacramento received its original city charter on April 13, 1850 — before California was even a state. The population had exploded from a few hundred to over 10,000 people in less than two years.",
    },
    "05-10": {
        "year": 1869,
        "fact": "The Transcontinental Railroad was completed, linking Sacramento to the East Coast",
        "detail": "When the Golden Spike was driven at Promontory Summit, Utah, Sacramento's Central Pacific Railroad connected to the Union Pacific — cutting cross-country travel from months to just days.",
    },
    "05-20": {
        "year": 1850,
        "fact": "Sacramento suffered its first major cholera epidemic",
        "detail": "Cholera swept through Sacramento's crowded tent camps, killing hundreds of Gold Rush miners. The city had no sewage system and the American River served as both water supply and waste disposal.",
    },
    "06-03": {
        "year": 1852,
        "fact": "The Sacramento Union newspaper was founded — California's oldest daily newspaper",
        "detail": "The Sacramento Union began publishing on June 3, 1852. Mark Twain wrote for the paper in the 1860s. It became the voice of California during the Gold Rush era.",
    },
    "06-13": {
        "year": 1850,
        "fact": "Sacramento's first great fire destroyed much of the downtown",
        "detail": "A fire broke out among the canvas-and-wood buildings of early Sacramento, burning dozens of structures. The city rebuilt almost immediately with brick, beginning the transition away from flimsy Gold Rush construction.",
    },
    "07-04": {
        "year": 1849,
        "fact": "Sacramento held its first Fourth of July celebration",
        "detail": "In 1849 — before California was a state — Sacramento miners celebrated Independence Day with cannon fire, horse races, and a grand ball. It was one of the first organized civic celebrations in California's future capital.",
    },
    "08-09": {
        "year": 1850,
        "fact": "Fire destroyed a large portion of Sacramento's business district",
        "detail": "Sacramento's second major fire of 1850 caused an estimated $500,000 in damage (over $18 million today). The city responded by mandating brick construction for new downtown buildings.",
    },
    "08-30": {
        "year": 1850,
        "fact": "Sacramento was devastated by a catastrophic flood from the Sacramento River",
        "detail": "The Sacramento River overflowed its banks, inundating the city and killing hundreds. This was one of several disastrous floods that led Sacramento to raise its entire street level by ten feet.",
    },
    "09-09": {
        "year": 1850,
        "fact": "California was admitted to the Union as the 31st state, with Sacramento as its capital",
        "detail": "On September 9, 1850, President Millard Fillmore signed California's statehood into law. Sacramento, already the commercial hub of the Gold Rush, was the natural choice for the new state's capital.",
    },
    "09-19": {
        "year": 1879,
        "fact": "The California State Constitution was ratified, reaffirming Sacramento as state capital",
        "detail": "California's second constitution formally enshrined Sacramento's role as the state capital and established new regulations on the railroad monopolies that dominated the city's economy.",
    },
    "10-02": {
        "year": 1872,
        "fact": "Leland Stanford helped found the California Spring and Autumn Fair in Sacramento",
        "detail": "What would become the California State Fair was born in Sacramento in the 1870s. Stanford, the railroad baron and governor whose mansion still stands on N Street, was a key early organizer.",
    },
    "10-24": {
        "year": 1861,
        "fact": "The Transcontinental Telegraph was completed, ending the Pony Express out of Sacramento",
        "detail": "When the telegraph wire connected the coasts on October 24, 1861, the Pony Express became obsolete overnight. The Sacramento-to-Missouri mail service lasted just 18 months.",
    },
    "11-09": {
        "year": 1862,
        "fact": "Construction began on Sacramento's great levee system after catastrophic flooding",
        "detail": "The Great Flood of 1861–62 — the worst in California history — inundated Sacramento under 30 feet of water. The city embarked on one of the largest engineering projects in the American West.",
    },
    "11-17": {
        "year": 1854,
        "fact": "The Sacramento Valley Railroad, California's first railroad, completed its line to Folsom",
        "detail": "The 22-mile line reduced the grueling wagon journey to the mining camps to a smooth 45-minute ride, making it the first operational railroad in the American West.",
    },
    "12-09": {
        "year": 1861,
        "fact": "The Great Flood of 1861–62 began inundating Sacramento",
        "detail": "Starting December 9, 1861, 43 days of nonstop rain caused the rivers to overflow catastrophically. The entire city was submerged, and Sacramento began its decade-long project of raising its streets ten feet.",
    },
    "12-28": {
        "year": 1862,
        "fact": "Governor Leland Stanford was inaugurated by rowboat during the Great Flood",
        "detail": "Sacramento was so deeply flooded that newly elected Governor Leland Stanford had to row a boat from his home to the Capitol for his inauguration — a vivid symbol of the city's recurring flood battle.",
    },
}

# ---------------------------------------------------------------------------
# 2. California history dated events  (key: "MM-DD")
# ---------------------------------------------------------------------------
CALIFORNIA_ON_THIS_DAY: dict[str, dict] = {
    "01-08": {
        "year": 1912,
        "fact": "Progressive governor Hiram Johnson — born in Sacramento — took office, reshaping California politics",
        "detail": "Sacramento-born Hiram Johnson became one of California's most transformative governors, championing the initiative, referendum, and recall to break the stranglehold of the Southern Pacific Railroad on state government.",
    },
    "01-13": {
        "year": 1847,
        "fact": "The Treaty of Cahuenga ended the Mexican-American War in California",
        "detail": "Signed near Los Angeles on January 13, 1847, the treaty transferred California from Mexico to the United States — just one year before gold was discovered at Sutter's Mill near Sacramento.",
    },
    "01-29": {
        "year": 1900,
        "fact": "California's population reached 1.5 million, with Sacramento as its fastest-growing inland city",
        "detail": "The 1900 Census revealed California's explosive growth since the Gold Rush. Sacramento — hub of agriculture, railroads, and government — anchored the Central Valley's economy.",
    },
    "02-01": {
        "year": 1847,
        "fact": "San Francisco was renamed from 'Yerba Buena,' as California prepared for American governance",
        "detail": "When Yerba Buena became San Francisco on February 1, 1847, California was still Mexican territory. Within a year, the Gold Rush near Sacramento would transform both cities beyond recognition.",
    },
    "02-07": {
        "year": 1894,
        "fact": "Leland Stanford — Sacramento's most famous railroad baron and governor — died in Palo Alto",
        "detail": "Stanford had built his fortune as a Sacramento merchant before co-founding the Central Pacific Railroad. His legacy includes Sacramento's railroad museum, Stanford University, and the Leland Stanford Mansion State Historic Park on N Street.",
    },
    "02-14": {
        "year": 1849,
        "fact": "California held its first American-organized election, just months before statehood",
        "detail": "California's first American election took place on February 14, 1849, choosing delegates for the constitutional convention that would lead to statehood in September 1850 — with Sacramento as the capital.",
    },
    "02-22": {
        "year": 1958,
        "fact": "The Sacramento Kings' NBA predecessor, the Cincinnati Royals, played their first season",
        "detail": "The franchise that would become the Sacramento Kings began in Cincinnati in 1948. After stops in Cincinnati, Kansas City, and Omaha, the Kings moved to Sacramento in 1985 — the city's first major professional sports team.",
    },
    "03-10": {
        "year": 1880,
        "fact": "The Southern Pacific Railroad consolidated its California monopoly, headquartered near Sacramento",
        "detail": "The SP's consolidation of California's rail lines gave it enormous control over the state's economy. Sacramento, as a key rail hub, felt this power acutely — fueling the Progressive reform movement led by Sacramento-born Hiram Johnson.",
    },
    "03-19": {
        "year": 1945,
        "fact": "Sacramento-area airfields were on maximum alert as Japanese balloon bombs reached California",
        "detail": "Japan's Fu-Go balloon bombs drifted across the Pacific, some reaching California. McClellan Air Force Base near Sacramento was one of the response centers tracking these unprecedented long-range weapons.",
    },
    "04-18": {
        "year": 1906,
        "fact": "The San Francisco Earthquake struck California — Sacramento became a refuge for thousands of survivors",
        "detail": "The 7.9-magnitude earthquake and fire destroyed San Francisco. Sacramento opened its doors to tens of thousands of refugees, with the Capitol grounds serving as a tent city. Sacramento's role as California's stable inland capital was never clearer.",
    },
    "04-25": {
        "year": 1846,
        "fact": "The Mexican-American War began — setting in motion California's transfer to the United States",
        "detail": "The war that started April 25, 1846 would result in Mexico ceding California to the US by 1848 — just days before James Marshall found gold at Sutter's Mill near Sacramento, changing North American history forever.",
    },
    "05-02": {
        "year": 1880,
        "fact": "The Mussel Slough Tragedy near Sacramento sparked a statewide uprising against the Southern Pacific Railroad",
        "detail": "When SP railroad agents and US marshals clashed with San Joaquin Valley farmers over land rights, seven people were killed. The event galvanized California's anti-railroad Progressive movement, with Sacramento politicians at its heart.",
    },
    "05-31": {
        "year": 1910,
        "fact": "The first airplane crossed California, passing over the Sacramento Valley",
        "detail": "Early aviation pioneer Glenn Curtiss completed a record-breaking cross-country flight in 1910 that passed over the Sacramento Valley. Sacramento would later become home to McClellan Air Force Base, one of the most important military air depots in the Pacific.",
    },
    "06-14": {
        "year": 1846,
        "fact": "American settlers raised the Bear Flag over Sonoma, creating the short-lived California Republic",
        "detail": "On June 14, 1846, American settlers in Sonoma declared California an independent republic with a homemade bear flag. The republic lasted only 23 days before the US took control — beginning the path to statehood with Sacramento as capital.",
    },
    "06-22": {
        "year": 1942,
        "fact": "California enacted its Japanese-American internment orders, affecting many Sacramento Valley families",
        "detail": "Executive Order 9066 forced over 110,000 Japanese-Americans into internment camps. The Sacramento Valley, home to a large Japanese farming community, saw entire neighborhoods emptied. Many had farmed the rich Sacramento Delta for generations.",
    },
    "07-07": {
        "year": 1846,
        "fact": "The US Navy raised the American flag over Monterey, officially claiming California",
        "detail": "Commodore John Sloat raised the Stars and Stripes at Monterey on July 7, 1846, formally claiming California for the United States. Two years later, gold discovered near Sacramento would make California the most coveted territory in North America.",
    },
    "07-09": {
        "year": 1846,
        "fact": "The American flag was raised in San Francisco (then Yerba Buena), completing US control of Alta California",
        "detail": "With the raising of the American flag in San Francisco on July 9, 1846, US control of California was complete. The discovery of gold near Sacramento just 18 months later would transform the new territory beyond all imagination.",
    },
    "07-14": {
        "year": 1850,
        "fact": "California's first state legislature convened — in Sacramento",
        "detail": "California's inaugural state legislature met in Sacramento on July 14, 1850, making the city the political center of the new state. The sessions were held in a hastily built hotel as the permanent Capitol was still years away.",
    },
    "08-02": {
        "year": 1934,
        "fact": "Joan Didion — Sacramento's most celebrated author — was born in the city",
        "detail": "Joan Didion was born in Sacramento on December 5, 1934. She grew up rooted in Sacramento's Central Valley culture, which profoundly shaped her essays and novels. Her Sacramento roots permeate works like 'Where I Was From.'",
    },
    "08-13": {
        "year": 1860,
        "fact": "The first California State Agricultural Fair was held in Sacramento",
        "detail": "Sacramento hosted California's first major agricultural fair in 1860, showcasing the Sacramento Valley's extraordinary farm produce. This tradition continues today as the California State Fair at Cal Expo.",
    },
    "08-16": {
        "year": 1896,
        "fact": "The Klondike Gold Rush began — Sacramento became a supply base for miners heading to Alaska",
        "detail": "When gold was discovered in the Klondike, history echoed the 1848 rush. Sacramento merchants outfitted thousands of Alaska-bound miners, just as their predecessors had equipped California Gold Rush prospectors half a century earlier.",
    },
    "09-02": {
        "year": 1866,
        "fact": "Hiram Johnson — Sacramento's greatest political son — was born",
        "detail": "Born in Sacramento on September 2, 1866, Hiram Johnson became California's Progressive governor (1911–1917) and a US Senator for 28 years. He broke the Southern Pacific Railroad's political grip on California and championed direct democracy.",
    },
    "09-22": {
        "year": 1896,
        "fact": "William Land was elected Mayor of Sacramento, later donating his legacy to the city's famous park",
        "detail": "Businessman William Land served as Sacramento's mayor and left his fortune to the city. William Land Park — 160 acres in south Sacramento with the city zoo, Funderland, and golf course — is his enduring gift.",
    },
    "10-11": {
        "year": 1885,
        "fact": "The Crocker Art Museum opened to the public as the first art museum in the American West",
        "detail": "Judge Edwin Crocker, brother of railroad baron Charles Crocker, had assembled one of the finest art collections in California. He donated his Sacramento mansion and collection to the public in 1885 — creating the West's oldest public art museum.",
    },
    "10-15": {
        "year": 1966,
        "fact": "Ronald Reagan was elected California Governor, launching a political career from Sacramento",
        "detail": "Ronald Reagan won the California governorship on November 8, 1966, and served two terms from Sacramento's Capitol. Sacramento was the launching pad for a political career that took him to the White House in 1981.",
    },
    "11-05": {
        "year": 1968,
        "fact": "Ronald Reagan was re-elected California Governor, continuing Sacramento's role as his political base",
        "detail": "Reagan's two terms as governor, headquartered in Sacramento, shaped his governing philosophy and national profile. He would later call his Sacramento years the preparation for the presidency.",
    },
    "11-08": {
        "year": 1910,
        "fact": "Hiram Johnson — born in Sacramento — was elected California's Progressive governor",
        "detail": "Sacramento-born Hiram Johnson swept to victory, promising to 'kick the Southern Pacific Railroad out of politics.' His reforms gave California the initiative, referendum, and recall — reshaping American democracy.",
    },
    "12-05": {
        "year": 1934,
        "fact": "Joan Didion — Sacramento's most celebrated writer — was born",
        "detail": "Born and raised in Sacramento, Joan Didion became one of America's greatest essayists and novelists. Her Sacramento upbringing in the Central Valley is central to her memoir 'Where I Was From' and defines much of her writing.",
    },
    "12-15": {
        "year": 1935,
        "fact": "Sacramento's iconic Tower Bridge opened, connecting Sacramento and West Sacramento",
        "detail": "The golden vertical-lift Tower Bridge opened on December 15, 1935. Its Art Deco design and gold paint have made it one of the most photographed bridges in California and Sacramento's most recognizable landmark.",
    },
}

# ---------------------------------------------------------------------------
# 3. Famous people with Sacramento / California connections  (key: "MM-DD")
# ---------------------------------------------------------------------------
FAMOUS_BIRTHDAYS: list[dict] = [
    # Sacramento natives / strong residents
    {
        "date": "01-22",
        "name": "Guy Fieri",
        "born": 1968,
        "connection": "raised in Ferndale, CA; built his empire from Sacramento's food scene",
        "fact": "Guy Fieri — the face of American food TV — was raised in Northern California and built much of his restaurant empire in Sacramento before becoming a Food Network star.",
        "detail": "Before 'Diners, Drive-Ins and Dives,' Guy Fieri operated restaurants in the Sacramento area, including Johnny Garlic's. He has returned to Sacramento many times to champion its farm-to-fork dining scene.",
    },
    {
        "date": "02-06",
        "name": "Ronald Reagan",
        "born": 1911,
        "connection": "California Governor based in Sacramento (1967–1975)",
        "fact": "Ronald Reagan, the 40th US President, was born on this day in 1911. He served as California's Governor for two terms, with Sacramento as his political home base.",
        "detail": "Reagan governed California from Sacramento from 1967 to 1975, using the Governor's Mansion on H Street. His Sacramento years shaped the conservative governing philosophy he later took to the White House in 1981.",
    },
    {
        "date": "03-04",
        "name": "Kevin Johnson",
        "born": 1966,
        "connection": "born in Sacramento; NBA star turned Sacramento Mayor (2008–2016)",
        "fact": "Kevin Johnson — Sacramento native, NBA All-Star, and two-term Mayor of Sacramento — was born on March 4, 1966.",
        "detail": "KJ grew up in Sacramento, became an NBA All-Star point guard for the Phoenix Suns, then returned home to serve as Sacramento's mayor for eight years. He spearheaded the Golden 1 Center arena and Sacramento's downtown revival.",
    },
    {
        "date": "04-07",
        "name": "Jerry Brown",
        "born": 1938,
        "connection": "California Governor (1975–83, 2011–19) — longest-serving governor in Sacramento history",
        "fact": "Jerry Brown, California's longest-serving governor, was born on April 7, 1938. He spent more time governing from Sacramento than any other person in California history.",
        "detail": "Jerry Brown served four terms as California Governor — two in the 1970s and two from 2011–2019 — living and working in Sacramento for a combined 16 years. His frugal style and intellectual approach made him one of Sacramento's most distinctive political figures.",
    },
    {
        "date": "06-20",
        "name": "Chino Moreno",
        "born": 1973,
        "connection": "born in Sacramento; lead singer of the Deftones",
        "fact": "Chino Moreno, lead singer of the Sacramento-born band Deftones, was born on June 20, 1973 in Sacramento.",
        "detail": "Moreno formed the Deftones at Del Campo High School in Sacramento in the late 1980s. The band went on to global fame, pioneering alternative metal and shoegaze, while always claiming Sacramento as their spiritual home.",
    },
    {
        "date": "07-09",
        "name": "Tom Hanks",
        "born": 1956,
        "connection": "raised in the Sacramento Bay Area; two-time Academy Award winner",
        "fact": "Tom Hanks — two-time Oscar winner and one of America's most beloved actors — was born on July 9, 1956 in Concord, CA, just east of Sacramento.",
        "detail": "Hanks grew up in the Sacramento Bay Area region and attended Skyline High School in Oakland. He has often cited his Northern California upbringing as formative. Films like 'Forrest Gump,' 'Cast Away,' and 'Philadelphia' made him a legend.",
    },
    {
        "date": "08-01",
        "name": "Jerry Garcia",
        "born": 1942,
        "connection": "born in San Francisco; the Grateful Dead played countless legendary Sacramento shows",
        "fact": "Grateful Dead founder Jerry Garcia was born on August 1, 1942. The band's deep roots in Northern California made Sacramento a regular stop and spiritual home for Deadheads.",
        "detail": "Jerry Garcia and the Grateful Dead treated Northern California as their home territory. Sacramento's Memorial Auditorium and Cal Expo hosted some of their most memorable concerts, cementing Sacramento's place in the history of the psychedelic era.",
    },
    {
        "date": "08-05",
        "name": "Patrick Coolican",
        "born": 1972,
        "connection": "Sacramento journalist and political commentator",
        "fact": "August 5 marks a day of California political journalism, a tradition Sacramento has championed since the Sacramento Bee was founded in 1857 as one of the West's most influential newspapers.",
        "detail": "The Sacramento Bee — founded in 1857 — has shaped California and national politics for over 165 years. Sacramento's role as state capital makes it one of the most important political journalism cities in America.",
    },
    {
        "date": "09-02",
        "name": "Hiram Johnson",
        "born": 1866,
        "connection": "born in Sacramento; Progressive Governor and US Senator",
        "fact": "Hiram Johnson — Sacramento's greatest political son — was born on September 2, 1866. He became California's most transformative Progressive governor.",
        "detail": "Born and raised in Sacramento, Johnson became governor in 1911 on a promise to break the Southern Pacific Railroad's grip on California politics. He introduced the initiative, referendum, and recall, reshaping American democracy. He served as US Senator until his death in 1945.",
    },
    {
        "date": "09-21",
        "name": "Bill Murray",
        "born": 1950,
        "connection": "Northern California cult hero; frequent Sacramento visitor",
        "fact": "Bill Murray, born September 21, 1950, is beloved throughout Northern California. The Sacramento area has long claimed a special affinity for the 'Ghostbusters' and 'Lost in Translation' star.",
        "detail": "Bill Murray's famously spontaneous personality and love of minor-league baseball have made him a legend throughout California. He has attended Sacramento River Cats games and is a perennial favorite at Northern California events.",
    },
    {
        "date": "10-05",
        "name": "Chester Bennington",
        "born": 1976,
        "connection": "born in Phoenix; Linkin Park performed at the ARCO Arena (now Golden 1 Center) many times",
        "fact": "Chester Bennington, Linkin Park's iconic vocalist, was born October 5, 1976. Linkin Park was a constant presence in Sacramento's concert scene, playing landmark shows at ARCO Arena.",
        "detail": "Linkin Park's blend of rock and hip-hop defined the early 2000s Sacramento concert experience. The band's Sacramento shows were among the most memorable in the arena's history.",
    },
    {
        "date": "10-17",
        "name": "Erin Brockovich",
        "born": 1960,
        "connection": "born in Kansas; her landmark California environmental case shaped state law from Sacramento",
        "fact": "Erin Brockovich, born October 17, 1960, led the most famous environmental lawsuit in California history — a case whose outcome was fought all the way to Sacramento's regulatory chambers.",
        "detail": "Brockovich's battle against Pacific Gas & Electric on behalf of Hinkley, CA residents resulted in a $333 million settlement — the largest ever in a US direct-action lawsuit. California's environmental laws, passed in Sacramento, were reshaped in its wake.",
    },
    {
        "date": "10-28",
        "name": "Joaquin Phoenix",
        "born": 1974,
        "connection": "born in San Juan, Puerto Rico; raised in Northern California",
        "fact": "Oscar-winning actor Joaquin Phoenix was born October 28, 1974. He spent formative years in Northern California before rising to become one of Hollywood's most acclaimed performers.",
        "detail": "Phoenix's Northern California upbringing shaped his outsider perspective that defines his most iconic roles. He won the Academy Award for Best Actor for 'Joker' (2019) and has been nominated three other times.",
    },
    {
        "date": "11-25",
        "name": "Joe DiMaggio",
        "born": 1914,
        "connection": "born in Martinez, CA — just 60 miles from Sacramento; California's greatest baseball hero",
        "fact": "Baseball legend Joe DiMaggio was born on November 25, 1914, in Martinez, California — just an hour from Sacramento. He remains the greatest baseball player to emerge from Northern California.",
        "detail": "DiMaggio grew up in the San Francisco Bay Area, just over an hour from Sacramento. His 56-game hitting streak in 1941 remains one of sports' most unbreakable records. Sacramento's long baseball tradition owes much to the culture DiMaggio helped build.",
    },
    {
        "date": "12-05",
        "name": "Joan Didion",
        "born": 1934,
        "connection": "born and raised in Sacramento; California's most celebrated literary voice",
        "fact": "Joan Didion — Sacramento's greatest literary figure — was born on December 5, 1934. Her writing about California, loss, and American culture made her one of the 20th century's most important authors.",
        "detail": "Didion was born and raised in Sacramento, and the Central Valley's flat light and restless energy permeate her work. Her memoir 'Where I Was From' is a profound meditation on Sacramento and California identity. She died in December 2021.",
    },
    {
        "date": "12-09",
        "name": "Kirk Kerkorian",
        "born": 1917,
        "connection": "born in Fresno, CA; built casinos and studios whose workers flocked to Sacramento",
        "fact": "Kirk Kerkorian, billionaire entrepreneur and California native, was born December 9, 1917 in Fresno. His California aviation and entertainment empire touched Sacramento through MGM Studios and his airline ventures.",
        "detail": "Kerkorian started as a pilot and built a fortune in aviation, casinos, and Hollywood. His California story — from Fresno farmhand to MGM chairman — embodies the Golden State dream that Sacramento, as the state capital, has always helped champion.",
    },
]

# Convert birthday list to dict for O(1) lookup (last entry wins for duplicate dates)
_BIRTHDAY_BY_DATE: dict[str, dict] = {b["date"]: b for b in FAMOUS_BIRTHDAYS}

# ---------------------------------------------------------------------------
# 4. General Sacramento history fallback pool (no specific date)
# ---------------------------------------------------------------------------
FALLBACK_FACTS: list[dict] = [
    {
        "year": None,
        "fact": "Sacramento has served as California's state capital continuously since 1854",
        "detail": "Before Sacramento, the capital bounced between San Jose, Vallejo, and Benicia. Sacramento won out for its central location, river access, and growing economic dominance during the Gold Rush.",
    },
    {
        "year": None,
        "fact": "The Sacramento River was a critical highway before roads or rails existed",
        "detail": "In the Gold Rush era, steamboats carried thousands of miners and tons of supplies from San Francisco Bay up the Sacramento River. The journey took about 12 hours — compared to days overland.",
    },
    {
        "year": None,
        "fact": "Sacramento's grid streets were deliberately raised 10–15 feet after repeated catastrophic floods",
        "detail": "Between 1860 and 1880, Sacramento undertook one of the most ambitious urban engineering projects in American history — literally burying the ground floors of buildings and raising streets to protect the city from the Sacramento River.",
    },
    {
        "year": None,
        "fact": "Sutter's Fort was the most important waystation on the California Trail for pioneers",
        "detail": "Before the Gold Rush, John Sutter's fort (founded 1839) was the destination that kept thousands of westward migrants alive. Nearly every wagon train that crossed the Sierra Nevada made Sutter's Fort its first stop.",
    },
    {
        "year": None,
        "fact": "The Big Four railroad barons — Stanford, Crocker, Hopkins, and Huntington — all called Sacramento home",
        "detail": "The four men who financed and built the Central Pacific Railroad all began their fortunes as Sacramento merchants. Their mansions defined Sacramento's Gilded Age grandeur.",
    },
    {
        "year": None,
        "fact": "Sacramento had a thriving Chinatown in the 1800s, home to thousands of Chinese railroad workers",
        "detail": "Over 10,000 Chinese laborers built the Central Pacific Railroad's treacherous Sierra Nevada section. Many settled in Sacramento's Chinatown afterward — one of the largest in California outside San Francisco.",
    },
    {
        "year": None,
        "fact": "The Crocker Art Museum was the first public art museum west of the Mississippi",
        "detail": "Judge Edwin Crocker assembled an extraordinary European art collection and donated his Sacramento mansion and artworks to the city in 1885.",
    },
    {
        "year": None,
        "fact": "The Sacramento Bee has been publishing since 1857, making it one of California's oldest newspapers",
        "detail": "Founded by James McClatchy in 1857, the Sacramento Bee grew into one of the most influential newspapers in the American West, shaping California politics for over 160 years.",
    },
    {
        "year": None,
        "fact": "Sacramento hosted some of the first professional baseball games in California in the 1860s",
        "detail": "The Sacramento Base Ball Club played organized games as early as 1860, making Sacramento one of the first cities west of the Rockies with an organized baseball team.",
    },
    {
        "year": None,
        "fact": "During World War II, Sacramento's McClellan Air Field became one of the most important military depots in the Pacific",
        "detail": "McClellan Air Force Base served as a major overhaul and supply depot during WWII and the Cold War, employing tens of thousands and transforming Sacramento into a military city.",
    },
    {
        "year": None,
        "fact": "Sacramento's Tower Bridge opened in 1935, becoming the city's most recognizable landmark",
        "detail": "Sacramento's iconic golden Tower Bridge — a vertical-lift bridge — opened on December 15, 1935. Its distinctive Art Deco style and gold paint make it one of the most photographed bridges in California.",
    },
    {
        "year": None,
        "fact": "Sacramento's Old Town was submerged under the raised city streets for over a century",
        "detail": "When Sacramento raised its streets in the 1860s–1870s, the original ground-floor storefronts became underground tunnels. These 'underground Sacramento' passages still exist beneath Old Sacramento today.",
    },
    {
        "year": None,
        "fact": "California's first telegraph line connected Sacramento to San Francisco in 1853",
        "detail": "The California State Telegraph Company strung wire between Sacramento and San Francisco in 1853, making Sacramento one of the first inland cities in the American West with telegraph communication.",
    },
    {
        "year": None,
        "fact": "The California State Fair has been held in Sacramento every year since 1854",
        "detail": "Beginning as an agricultural exhibition in 1854, the California State Fair grew into one of the largest state fairs in the nation. It moved to its current Cal Expo location in 1968.",
    },
    {
        "year": None,
        "fact": "Sacramento is one of the most ethnically diverse cities in the United States",
        "detail": "Sacramento has been called the most integrated city in America. Its diversity traces back to the Gold Rush, when Chinese, Mexican, Chilean, Australian, and European miners all converged on the city.",
    },
    {
        "year": None,
        "fact": "The Deftones — one of rock's most innovative bands — formed at a Sacramento high school in the 1980s",
        "detail": "Chino Moreno, Stephen Carpenter, and Abe Cunningham formed the Deftones at Del Campo High School in Sacramento around 1988. The band pioneered alternative metal and shoegaze, selling over 10 million albums worldwide.",
    },
    {
        "year": None,
        "fact": "Sacramento's farm-to-fork movement is one of the most influential in American food culture",
        "detail": "Sacramento declared itself America's Farm-to-Fork Capital in 2012. The region produces over 300 crops within 150 miles — more agricultural diversity than almost anywhere on earth.",
    },
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def get_fact_for_date(today: date) -> dict:
    """Return the best available fact for today's date.

    Priority:
      1. Sacramento-specific dated event
      2. California history dated event
      3. Famous person born on this date with Sacramento/CA connection
      4. Seeded-random Sacramento history fallback
    """
    key = today.strftime("%m-%d")

    # 1. Sacramento-specific event
    if key in ON_THIS_DAY:
        entry = ON_THIS_DAY[key].copy()
        entry["type"] = "sacramento"
        entry["date_label"] = f"On this day in {entry['year']}" if entry["year"] else "Sacramento History"
        return entry

    # 2. California history event
    if key in CALIFORNIA_ON_THIS_DAY:
        entry = CALIFORNIA_ON_THIS_DAY[key].copy()
        entry["type"] = "california"
        entry["date_label"] = f"California History · {entry['year']}" if entry.get("year") else "California History"
        return entry

    # 3. Famous birthday
    if key in _BIRTHDAY_BY_DATE:
        b = _BIRTHDAY_BY_DATE[key].copy()
        age = today.year - b["born"]
        return {
            "type": "birthday",
            "year": b["born"],
            "date_label": f"Born on this day in {b['born']}",
            "fact": f"{b['name']} — {b['connection']} — was born today in {b['born']} (would be {age})",
            "detail": b["detail"],
        }

    # 4. Seeded-random fallback (stable per calendar date)
    rng = random.Random(today.month * 100 + today.day)
    entry = rng.choice(FALLBACK_FACTS).copy()
    entry["type"] = "fallback"
    entry["date_label"] = "Sacramento History"
    return entry
