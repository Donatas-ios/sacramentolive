"""
Sacramento 'On This Day' historical facts.

Keyed by "MM-DD". For days with no specific entry a fallback pool is
used, seeded by the ordinal of today's date (same day = same fact).
"""
from __future__ import annotations
import random
from datetime import date

# ---------------------------------------------------------------------------
# Date-specific facts  (key: "MM-DD")
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
        "detail": "After bouncing between San Jose, Vallejo, and Benicia, lawmakers chose Sacramento as California's permanent capital on February 27, 1854 — largely due to its central location and Gold Rush wealth.",
    },
    "03-04": {
        "year": 1860,
        "fact": "The first Pony Express advertisement appeared, announcing Sacramento as the western terminus",
        "detail": "Posters across Sacramento announced: 'Wanted: Young, skinny, wiry fellows not over 18. Must be expert riders willing to risk death daily. Orphans preferred.' The service would launch less than a month later.",
    },
    "03-22": {
        "year": 1861,
        "fact": "The California State Capitol cornerstone was laid in Sacramento",
        "detail": "Construction began on the iconic Capitol building on Capitol Mall. It would take until 1874 to complete the structure, which still serves as California's seat of government today.",
    },
    "04-03": {
        "year": 1860,
        "fact": "The first Pony Express rider departed Sacramento for Missouri",
        "detail": "On April 3, 1860, a rider galloped out of Sacramento carrying 49 letters, 5 telegrams, and newspapers — beginning the legendary 1,966-mile route to St. Joseph, Missouri. The mail arrived in just 10 days.",
    },
    "04-13": {
        "year": 1850,
        "fact": "Sacramento was incorporated as a city for the first time",
        "detail": "Sacramento received its original city charter on April 13, 1850 — before California was even a state. The population had exploded from a few hundred to over 10,000 people in less than two years.",
    },
    "05-10": {
        "year": 1869,
        "fact": "The Transcontinental Railroad was completed, linking Sacramento to the East Coast",
        "detail": "When the Golden Spike was driven at Promontory Summit, Utah on May 10, 1869, Sacramento's Central Pacific Railroad connected to the Union Pacific — cutting cross-country travel from months to just days.",
    },
    "05-20": {
        "year": 1850,
        "fact": "Sacramento suffered its first major cholera epidemic",
        "detail": "Cholera swept through Sacramento's crowded tent camps in the spring of 1850, killing hundreds of Gold Rush miners. The city had no sewage system and the American River served as both water supply and waste disposal.",
    },
    "06-03": {
        "year": 1852,
        "fact": "The Sacramento Union newspaper was founded — California's oldest daily newspaper",
        "detail": "The Sacramento Union began publishing on June 3, 1852. Mark Twain wrote for the paper in the 1860s. It became the voice of California during the Gold Rush era and remained in print for over 140 years.",
    },
    "06-13": {
        "year": 1850,
        "fact": "Sacramento's first great fire destroyed much of the downtown",
        "detail": "A fire broke out among the canvas-and-wood buildings of early Sacramento, burning dozens of structures. The city rebuilt almost immediately with more brick, beginning the transition away from the flimsy Gold Rush construction.",
    },
    "07-04": {
        "year": 1849,
        "fact": "Sacramento held its first Fourth of July celebration",
        "detail": "In 1849 — before California was a state — Sacramento miners celebrated Independence Day with cannon fire, horse races, and a grand ball. It was one of the first organized civic celebrations in California's future capital.",
    },
    "08-09": {
        "year": 1850,
        "fact": "Fire destroyed a large portion of Sacramento's business district",
        "detail": "Sacramento's second major fire in 1850 caused an estimated $500,000 in damage (over $18 million today). The city responded by mandating brick construction for new downtown buildings.",
    },
    "08-30": {
        "year": 1850,
        "fact": "Sacramento was devastated by a catastrophic flood from the Sacramento River",
        "detail": "The Sacramento River overflowed its banks in August 1850, inundating the city and killing hundreds. This was one of several disastrous floods that led Sacramento to raise the entire street level by ten feet in later decades.",
    },
    "09-09": {
        "year": 1850,
        "fact": "California was admitted to the Union as the 31st state, with Sacramento as its capital city",
        "detail": "On September 9, 1850, President Millard Fillmore signed California's statehood into law. Sacramento, already the commercial hub of the Gold Rush, was the natural choice for the new state's capital.",
    },
    "09-19": {
        "year": 1879,
        "fact": "The California State Constitution was ratified, reaffirming Sacramento as state capital",
        "detail": "California's second constitution, ratified in 1879, formally enshrined Sacramento's role as the state capital. The document also established regulations on railroad monopolies — a huge issue for Sacramento's Central Pacific-dominated economy.",
    },
    "10-02": {
        "year": 1872,
        "fact": "Leland Stanford founded the California Spring and Autumn Fair in Sacramento",
        "detail": "What would become the California State Fair was born in Sacramento in the 1870s. Stanford, the railroad baron and future governor whose mansion still stands on N Street, was a key early organizer.",
    },
    "10-13": {
        "year": 1849,
        "fact": "The first California Constitutional Convention concluded in Monterey, clearing the way for Sacramento's capital status",
        "detail": "Delegates at Monterey completed California's first constitution on October 13, 1849. Sacramento was quickly selected as the seat of government, and the first state legislature convened there in early 1850.",
    },
    "10-24": {
        "year": 1861,
        "fact": "The Transcontinental Telegraph was completed, ending the Pony Express out of Sacramento",
        "detail": "When the telegraph wire connected the coasts on October 24, 1861, the Pony Express became obsolete overnight. The Sacramento-to-Missouri mail service that had captured the nation's imagination lasted just 18 months.",
    },
    "11-09": {
        "year": 1862,
        "fact": "Construction began on Sacramento's great levee system after catastrophic flooding",
        "detail": "The Great Flood of 1861–62 — the worst in California history — inundated Sacramento under 30 feet of water. The city responded by embarking on one of the largest engineering projects in the American West.",
    },
    "11-17": {
        "year": 1854,
        "fact": "The Sacramento Valley Railroad, California's first railroad, completed its line to Folsom",
        "detail": "The Sacramento Valley Railroad — California's first — extended its tracks from Sacramento to Folsom on November 17, 1854. The 22-mile line reduced the grueling wagon journey to the mining camps to a smooth 45-minute ride.",
    },
    "12-09": {
        "year": 1861,
        "fact": "The Great Flood of 1861–62 began inundating Sacramento",
        "detail": "Starting December 9, 1861, 43 days of nonstop rain caused the Sacramento and American rivers to overflow catastrophically. The entire city was submerged, the governor rowed a boat to his inauguration, and Sacramento began its decade-long project of raising its streets ten feet.",
    },
    "12-28": {
        "year": 1862,
        "fact": "Governor Leland Stanford was inaugurated by rowboat during the Great Flood",
        "detail": "Sacramento was so deeply flooded in December 1861 that newly elected Governor Leland Stanford had to row a boat from his Sacramento home to the Capitol for his inauguration — a vivid symbol of the city's recurring flood battle.",
    },
}

# ---------------------------------------------------------------------------
# Fallback pool — used when no date-specific fact exists
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
        "detail": "In the Gold Rush era, steamboats carried thousands of miners and tons of supplies from San Francisco Bay up the Sacramento River to the city. The journey took about 12 hours — compared to days overland.",
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
        "detail": "The four men who financed and built the Central Pacific Railroad all began their fortunes as Sacramento merchants. Their mansions on 'Nob Hill' (now Capitol Park area) defined Sacramento's Gilded Age grandeur.",
    },
    {
        "year": None,
        "fact": "Sacramento had a thriving Chinatown in the 1800s, home to thousands of Chinese railroad workers",
        "detail": "Over 10,000 Chinese laborers built the Central Pacific Railroad's treacherous Sierra Nevada section. Many settled in Sacramento's Chinatown afterward — one of the largest in California outside San Francisco.",
    },
    {
        "year": None,
        "fact": "The Crocker Art Museum was the first public art museum west of the Mississippi",
        "detail": "Judge Edwin Crocker (brother of railroad baron Charles Crocker) assembled an extraordinary European art collection and donated his Sacramento mansion and artworks to the city in 1885.",
    },
    {
        "year": None,
        "fact": "Sacramento was a key stop on the Underground Railroad in the 1850s",
        "detail": "Despite California entering as a free state in 1850, the Fugitive Slave Act still applied. Sacramento's African-American community actively helped freedom seekers, and Mary Ellen Pleasant — Sacramento's most famous Black abolitionist — raised funds to help people escape slavery.",
    },
    {
        "year": None,
        "fact": "The Sacramento Bee has been publishing since 1857, making it one of California's oldest newspapers",
        "detail": "Founded by James McClatchy in 1857, the Sacramento Bee grew into one of the most influential newspapers in the American West, shaping California politics for over 160 years.",
    },
    {
        "year": None,
        "fact": "Sacramento hosted some of the first professional baseball games in California in the 1860s",
        "detail": "The Sacramento Base Ball Club played organized games as early as 1860, making Sacramento one of the first cities west of the Rockies with an organized baseball team. The city has supported professional baseball almost continuously since.",
    },
    {
        "year": None,
        "fact": "During World War II, Sacramento's McClellan Air Field became one of the most important military depots in the Pacific",
        "detail": "McClellan Air Force Base near Sacramento served as a major overhaul and supply depot during WWII and the Cold War, employing tens of thousands and transforming Sacramento into a military city.",
    },
    {
        "year": None,
        "fact": "The Tower Bridge connecting Sacramento to West Sacramento opened in 1935",
        "detail": "Sacramento's iconic golden Tower Bridge — a vertical-lift bridge — opened on December 15, 1935. Its distinctive art deco style and gold paint make it one of the most photographed bridges in California.",
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
        "detail": "Beginning as an agricultural exhibition in 1854, the California State Fair grew into one of the largest state fairs in the nation. It moved to its current Cal Expo location in 1968 and draws nearly half a million visitors annually.",
    },
]


def get_fact_for_date(today: date) -> dict:
    """Return the best fact for the given date.

    Prefers a date-specific event; falls back to a seeded-random pick from
    the general pool so the same calendar day always shows the same fact.
    """
    key = today.strftime("%m-%d")
    if key in ON_THIS_DAY:
        entry = ON_THIS_DAY[key].copy()
        entry["is_anniversary"] = True
        entry["date_label"] = (
            f"On this day in {entry['year']}" if entry["year"] else "Sacramento History"
        )
        return entry

    # Fallback: seed by month+day so it's stable within a calendar date
    rng = random.Random(today.month * 100 + today.day)
    entry = rng.choice(FALLBACK_FACTS).copy()
    entry["is_anniversary"] = False
    entry["date_label"] = "Sacramento History"
    return entry
