"""Parse ICRA 2026 paper title files (tue/wed/thu) into structured JSON."""
from __future__ import annotations
import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "raw" / "paper_titles"
DAYS = {"tue.txt": "Tuesday", "wed.txt": "Wednesday", "thu.txt": "Thursday"}

# Paper start markers, e.g. "09:00-10:30, Paper TuI1I.1" or "17:55-18:05, Paper TuBT4.8"
PAPER_RE = re.compile(r"^\s*(\d{2}:\d{2}-\d{2}:\d{2}),\s*Paper\s+([A-Za-z0-9.]+)")
# Session markers like "TuI1I  Interactive Session, Hall C"
SESSION_RE = re.compile(r"^\s*([A-Z][a-z][A-Za-z0-9]+)\s{2,}([^,]+),\s*(.+?)\s*Add to My Program")

# Country / region inference from affiliation strings (rough but workable)
COUNTRY_HINTS = [
    ("USA", ["MIT", "Stanford", "CMU", "Carnegie Mellon", "Berkeley", "UCLA", "UC ", "Harvard",
             "Princeton", "Cornell", "Columbia University", "Yale", "Caltech", "Georgia Tech",
             "Georgia Institute of Technology", "Michigan", "Illinois", "Texas", "Washington",
             "Penn", "Northwestern", "NYU", "New York University", "Boston", "Purdue", "Rutgers",
             "Maryland", "Wisconsin", "Minnesota", "Notre Dame", "Johns Hopkins", "Duke",
             "Virginia", "North Carolina", "Florida", "Arizona", "Colorado", "Utah",
             "Worcester Polytechnic", "Rensselaer", "Rochester", "Stony Brook", "Buffalo",
             "Iowa", "Tennessee", "Kentucky", "Vanderbilt", "Rice", "USC ", "Southern California",
             "Oregon State", "Pennsylvania", "Massachusetts", "Drexel", "Lehigh",
             "Army Research", "NASA", "Oak Ridge", "Sandia", "JPL", "Jet Propulsion",
             "Meta", "Google", "Microsoft", "Apple", "NVIDIA", "Amazon", "Tesla",
             "Boston Dynamics", "Toyota Research", "Samsung Research America"]),
    ("China", ["Tsinghua", "Peking", "Beihang", "Fudan", "Zhejiang", "Shanghai Jiao Tong",
               "Shanghai Jiaotong", "Sun Yat-Sen", "Xi'an Jiaotong", "Xi’an Jiaotong",
               "Wuhan", "Sichuan", "Harbin Institute", "USTC", "University of Science and Technology of China",
               "SUSTech", "Southern University of Science and Technology", "ShanghaiTech",
               "Tongji", "Nanjing", "Renmin", "Nankai", "Tianjin", "Dalian",
               "Chongqing", "Northeastern University, China", "North China",
               "South China", "East China", "Central South", "Hunan", "Jilin",
               "Lanzhou", "Yunnan", "Sun Yat-sen", "Chinese Academy of Sciences",
               "CASIA", "CAS ", "Institute of Automation", "China University",
               "Beijing", "Shanghai", "Shenzhen", "Hangzhou", "Wuxi",
               "Chengdu", "Westlake", "Great Bay University",
               "Huawei", "Tencent", "Baidu", "Alibaba", "DJI",
               "Chang'an", "Chang’an", "Xidian", "PLA ",
               "National University of Defense Technology"]),
    ("Hong Kong", ["Hong Kong", "HKUST", "HKU ", "PolyU", "CityU", "CUHK"]),
    ("Taiwan", ["Taiwan", "Yang Ming Chiao Tung", "National Taiwan", "NCTU", "NTU "]),
    ("South Korea", ["KAIST", "POSTECH", "Seoul National", "Korea University", "Yonsei",
                     "Hanyang", "Sungkyunkwan", "UNIST", "Pohang", "Korea Advanced",
                     "GIST", "DGIST", "Chungbuk", "Chungnam", "Pusan", "Kyungpook",
                     "Inha", "Ajou", "Sogang", "Konkuk", "Hongik", "Gyeongsang",
                     "Hyundai", "Samsung", "LG ", "Neuromeka",
                     "ETRI", "KIST", "KITECH", "Republic of Korea"]),
    ("Japan", ["Tokyo", "Kyoto", "Osaka", "Kyushu", "Hokkaido", "Tohoku", "Nagoya",
               "Tsukuba", "Waseda", "Keio", "JAXA", "AIST", "Tokai",
               "Ritsumeikan", "Doshisha", "Kobe", "Hiroshima", "Okayama",
               "Ibaraki", "Saitama", "Chiba", "Yokohama", "Kanazawa", "Niigata",
               "OMRON", "Honda", "Sony", "Toyota", "Mitsubishi", "Hitachi",
               "Panasonic", "Fanuc", "Denso", "Bridgestone", "Tokyo Institute",
               "Tokyo University", "Japan"]),
    ("Singapore", ["Singapore", "NUS", "Nanyang Technological", "NTU,",
                   "Agency for Science"]),
    ("Germany", ["Munich", "Berlin", "Karlsruhe", "Stuttgart", "Aachen", "Hamburg",
                 "Heidelberg", "Bonn", "Freiburg", "Tubingen", "Tübingen", "Darmstadt",
                 "Bremen", "Bielefeld", "Bochum", "Dortmund", "Dresden", "Erlangen",
                 "Frankfurt", "Goettingen", "Göttingen", "Hannover", "Kiel", "Leipzig",
                 "Magdeburg", "Mannheim", "Marburg", "Mainz", "Muenster", "Münster",
                 "Nuremberg", "Nürnberg", "Saarland", "Ulm", "Wuerzburg", "Würzburg",
                 "Weimar", "DLR", "Fraunhofer", "Max Planck", "Bosch", "Siemens",
                 "BMW", "Mercedes", "Volkswagen", "Continental", "Aumovio", "Germany",
                 "RWTH", "TUM", "TU Berlin", "TU Munich", "TU Darmstadt", "TU Dresden"]),
    ("UK", ["Oxford", "Cambridge", "Imperial College", "UCL", "King's College", "Edinburgh",
            "Manchester", "Bristol", "Warwick", "Sheffield", "Leeds", "Birmingham",
            "Glasgow", "Liverpool", "Southampton", "Surrey", "Sussex", "York",
            "Loughborough", "Nottingham", "Lancaster", "Durham", "Reading",
            "Strathclyde", "Aberdeen", "St Andrews", "Heriot-Watt", "Bath",
            "Queen Mary", "Essex", "Cardiff", "Newcastle", "United Kingdom",
            "Plymouth", "Bournemouth", "Brunel", "Westminster"]),
    ("France", ["Paris", "Sorbonne", "INRIA", "Inria", "CNRS", "ENS ", "ENSTA",
                "École", "Ecole", "Lyon", "Marseille", "Toulouse", "Grenoble",
                "Lille", "Nice", "Bordeaux", "Strasbourg", "Nantes", "Rennes",
                "Montpellier", "Versailles", "Compiegne", "Compiègne",
                "LAAS", "IRISA", "Mines", "Centrale", "PSL", "France",
                "Institut Polytechnique"]),
    ("Italy", ["Milano", "Milan", "Turin", "Torino", "Roma", "Rome", "Naples",
               "Napoli", "Padova", "Padua", "Pisa", "Bologna", "Firenze",
               "Florence", "Genova", "Genoa", "Trento", "Trieste", "Bari",
               "Catania", "Palermo", "Sicily", "Italy", "Politecnico",
               "Sapienza", "Tor Vergata", "Sant'Anna", "Sant’Anna",
               "Istituto Italiano Di Tecnologia", "IIT "]),
    ("Switzerland", ["ETH ", "EPFL", "Zurich", "Lausanne", "Geneva", "Bern", "Basel",
                     "Idiap", "Switzerland"]),
    ("Netherlands", ["Delft", "TU Delft", "Eindhoven", "Twente", "Wageningen",
                     "Leiden", "Utrecht", "Rotterdam", "Amsterdam", "Groningen",
                     "Maastricht", "Netherlands", "Holland"]),
    ("Spain", ["Madrid", "Barcelona", "Valencia", "Seville", "Zaragoza", "Granada",
               "Bilbao", "Salamanca", "Murcia", "Tenerife", "La Laguna",
               "Spain", "Catalunya", "Catalonia"]),
    ("Sweden", ["KTH", "Stockholm", "Uppsala", "Lund", "Chalmers", "Linköping",
                "Gothenburg", "Sweden"]),
    ("Norway", ["Oslo", "Trondheim", "NTNU", "SINTEF", "Norway", "Bergen", "Tromsø"]),
    ("Denmark", ["Copenhagen", "Aalborg", "Aarhus", "DTU", "Southern Denmark",
                 "Denmark"]),
    ("Finland", ["Aalto", "Helsinki", "Tampere", "Turku", "Oulu", "Finland"]),
    ("Belgium", ["KU Leuven", "Ghent", "Antwerp", "Brussels", "Liege", "Liège",
                 "Belgium"]),
    ("Austria", ["Vienna", "Graz", "Linz", "Innsbruck", "Salzburg", "Austria",
                 "TU Wien", "JKU"]),
    ("Czech", ["Prague", "Czech Technical", "CTU ", "Brno", "Czech"]),
    ("Poland", ["Warsaw", "Krakow", "Cracow", "Wrocław", "Wroclaw", "Gdansk",
                "Poznan", "Poland"]),
    ("Portugal", ["Lisbon", "Lisboa", "Porto", "Coimbra", "Portugal"]),
    ("Greece", ["Athens", "Thessaloniki", "Patras", "Crete", "Greece"]),
    ("Ireland", ["Dublin", "Trinity College", "Cork", "Galway", "Ireland"]),
    ("Canada", ["Toronto", "Waterloo", "McGill", "UBC ", "British Columbia",
                "Alberta", "Calgary", "Montreal", "Ottawa", "Western University",
                "Concordia", "Simon Fraser", "Queen's University", "Dalhousie",
                "Manitoba", "Saskatchewan", "York University", "Carleton", "Canada"]),
    ("Australia", ["Sydney", "Melbourne", "Queensland", "Monash", "ANU ",
                   "Australian National", "UNSW", "New South Wales", "Adelaide",
                   "Western Australia", "Macquarie", "RMIT", "Curtin",
                   "Australia", "CSIRO", "QUT"]),
    ("New Zealand", ["Auckland", "Otago", "Canterbury", "Victoria University of Wellington",
                     "New Zealand", "Massey"]),
    ("India", ["IIT ", "IISc", "Indian Institute", "Delhi", "Mumbai", "Bangalore",
               "Bengaluru", "Chennai", "Madras", "Kolkata", "Calcutta", "Hyderabad",
               "Pune", "Kanpur", "Kharagpur", "Roorkee", "Guwahati", "India",
               "BITS Pilani"]),
    ("Israel", ["Technion", "Tel Aviv", "Hebrew University", "Weizmann", "Bar-Ilan",
                "Ben-Gurion", "Israel"]),
    ("UAE", ["Khalifa", "Mohamed Bin Zayed", "MBZUAI", "UAE", "Emirates",
             "Abu Dhabi", "Dubai"]),
    ("Saudi Arabia", ["KAUST", "King Abdullah", "King Saud", "Riyadh", "Jeddah",
                      "Saudi"]),
    ("Turkey", ["Istanbul", "Ankara", "Bilkent", "Koç", "Sabanci", "METU", "Turkey",
                "Bogazici", "Boğaziçi"]),
    ("Iran", ["Tehran", "Sharif", "Iran", "Isfahan"]),
    ("Brazil", ["São Paulo", "Sao Paulo", "Rio de Janeiro", "Brazil", "Brasil",
                "Brasilia", "USP", "UFRJ", "UFMG", "UFRGS"]),
    ("Mexico", ["UNAM", "Mexico", "México", "Monterrey", "Guadalajara", "Tecnológico"]),
    ("Argentina", ["Buenos Aires", "Argentina", "Cordoba"]),
    ("Chile", ["Santiago", "Chile"]),
    ("South Africa", ["Cape Town", "Johannesburg", "Stellenbosch", "South Africa",
                      "Pretoria"]),
    ("Egypt", ["Cairo", "Egypt", "Alexandria"]),
]


def country_for(aff: str) -> str:
    s = aff
    for country, hints in COUNTRY_HINTS:
        for h in hints:
            if h in s:
                return country
    return "Other"


def parse_file(path: Path, day: str):
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    papers = []
    cur_session_code = None
    cur_session_title = None
    cur_session_room = None

    i = 0
    while i < len(lines):
        line = lines[i]
        # Session header
        m_sess = SESSION_RE.match(line)
        if m_sess:
            cur_session_code = m_sess.group(1)
            cur_session_room = m_sess.group(2).strip()
            # Session title is on the next non-empty line (often)
            # Use the part after the comma plus next line as full title
            # The third group already captures the rest of header line
            tail = m_sess.group(3).strip()
            # Try next line for session topic
            j = i + 1
            topic = ""
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and not PAPER_RE.match(lines[j]) and not SESSION_RE.match(lines[j]):
                topic = lines[j].strip()
            cur_session_title = topic or tail
            i += 1
            continue

        m_paper = PAPER_RE.match(line)
        if m_paper:
            time_slot = m_paper.group(1)
            paper_code = m_paper.group(2)
            # Title is on next non-empty line
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            title = lines[j].strip() if j < len(lines) else ""
            # Authors follow until blank or next paper/session
            authors = []
            k = j + 1
            while k < len(lines):
                ln = lines[k]
                if not ln.strip():
                    break
                if PAPER_RE.match(ln) or SESSION_RE.match(ln):
                    break
                # Author lines have a tab between name and affiliation
                if "\t" in ln:
                    name, aff = ln.split("\t", 1)
                    authors.append({"name": name.strip(), "aff": aff.strip()})
                else:
                    # Could be a continuation; tolerate
                    parts = re.split(r"\s{2,}", ln.strip(), maxsplit=1)
                    if len(parts) == 2:
                        authors.append({"name": parts[0].strip(), "aff": parts[1].strip()})
                k += 1
            if title and authors:
                papers.append({
                    "id": f"{day[:3]}-{paper_code}",
                    "code": paper_code,
                    "day": day,
                    "time": time_slot,
                    "session": cur_session_code,
                    "session_title": cur_session_title,
                    "room": cur_session_room,
                    "title": title,
                    "authors": authors,
                })
            i = k
            continue
        i += 1
    return papers


def main():
    all_papers = []
    for fname, day in DAYS.items():
        p = SRC / fname
        all_papers.extend(parse_file(p, day))
    # Stats
    aff_counter = Counter()
    country_counter = Counter()
    author_counter = Counter()
    for p in all_papers:
        first_aff = p["authors"][0]["aff"] if p["authors"] else ""
        seen_affs = set()
        for a in p["authors"]:
            if a["aff"] not in seen_affs:
                aff_counter[a["aff"]] += 1
                seen_affs.add(a["aff"])
            author_counter[a["name"]] += 1
        # country: union of unique countries in this paper
        seen_countries = set()
        for a in p["authors"]:
            seen_countries.add(country_for(a["aff"]))
        for c in seen_countries:
            country_counter[c] += 1

    out = {
        "papers": all_papers,
        "n_papers": len(all_papers),
    }
    out_path = ROOT / "output" / "papers.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(f"Parsed {len(all_papers)} papers")
    print("Top affiliations:")
    for a, c in aff_counter.most_common(15):
        print(f"  {c:4d}  {a}")
    print("Top countries:")
    for a, c in country_counter.most_common(15):
        print(f"  {c:4d}  {a}")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
