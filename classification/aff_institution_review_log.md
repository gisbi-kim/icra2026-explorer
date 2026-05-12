# Institution Canonicalization Audit

## 1. Executive Summary

`classification/aff_country_table.json` remains the authoritative affiliation-to-country lookup table, but it is not a canonical institution table. Institution-level rankings are distorted when aliases, acronyms, typos, accents, inverted names, lab suffixes, company suffixes, and compound affiliations are counted as separate institutions. This audit adds a conservative layer: raw affiliation string -> canonical institution name(s) -> country.

Be conservative. Merge only when identity is clear. If uncertain, send the case to manual review. Commas are not blindly split, and `X University` is not blindly rewritten as `University of X`.

## 2. Canonical Merge Table

| Canonical Institution | Raw Aliases to Merge | Country | Merge Type | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| AIST | National Institute of Advanced Industrial Science and Technology; National Institute of Advanced Industrial Science and Technology (AIST) | Japan | acronym/full-name, name variant | high | observed in current table |
| Alibaba DAMO Academy | Alibaba; Alibaba Damo Academy; Alibaba Group | China | accent/unaccented, name variant | high | observed in current table |
| Allen Institute for AI | Allen Institute for Artificial Intelligence | USA | name variant | high | observed in current table |
| BIGAI | Beijing Institute for General Artificial Intelligence; Beijing Institute for General Artificial Intelligence (BIGAI) | China | acronym/full-name, name variant | high | observed in current table |
| Beihang University | BeiHang University; Beihang Unverisity | China | accent/unaccented, typo variant | high | observed in current table |
| ByteDance | Bytedance; ByteDance Inc | China | accent/unaccented, lab suffix | high | observed in current table |
| CASIA | Institute of Automation, Chinese Academy of Science; Institute of Automation, Chinese Academy of Sciences; Institute of Automation，Chinese Academy of Sciences | China | name variant, punctuation variant | high | observed in current table |
| CUHK | Chinese University of Hong Kong; CUHK; T-Stone Robotics Institute, the Chinese University of Hong Kong; The Chinese University of Hong Kong; The Chinese University of Hong Kong (CUHK) | China | acronym/full-name, name variant, punctuation variant | high | observed in current table |
| CUHK Shenzhen | Chinese University of Hong Kong (Shenzhen); Chinese University of Hong Kong, Shenzhen; CUHK(SZ); The Chinese University of Hong Kong (Shenzhen); The Chinese University of Hong Kong CUHK (Shenzhen); The Chinese University of Hong Kong, Shenzhen; The Chinese Unviersity of Hong Kong, Shenzhen | China | acronym/full-name, punctuation variant | high | observed in current table |
| Caltech | California Institute of Technology; California Institute of Technology (Caltech); CALTECH | USA | acronym/full-name, name variant | high | observed in current table |
| DGIST | Daegu Gyeongbuk Institute of Science and Technology; Daegu Gyeongbuk Institute of Science and Technology (DGIST); Daegu Gyeongbuk Institute of Science and Technology(DGIST) | South Korea | acronym/full-name, name variant | high | observed in current table |
| EPFL | Ecole Polytechnique Federale De Lausanne; Ecole Polytechnique Fédérale De Lausanne; Ecole Polytechnique Fédérale De Lausanne (EPFL); Epfl; EPFL, Lausanne, Switzerland; École Polytechnique Fédérale De Lausanne; École Polytechnique Fédérale De Lausanne (EPFL); École Polytechnique Fédérale De Lausanne (EPFL), Switzerland | Switzerland | accent/unaccented, acronym/full-name, campus/subunit suffix, name variant | high | observed in current table |
| ETH Zurich | ETH; ETH ZUrich; ETH Zurich, Automatic Control Laboratory (IfA); ETH Zurich, Autonomous Systems Lab; ETH Zurich, Mimic Robotics; ETH Zurich, Robotic Systems Lab; ETH Zürich; ETHZ; Rehabilitation Engineering Laboratory, ETH Zurich; RSL, ETHZ | Switzerland | accent/unaccented, acronym/full-name, campus/subunit suffix, punctuation variant | high | observed in current table |
| FAU Erlangen-Nürnberg | Friedrich-Alexander-University Erlangen-Nurnberg (FAU); Friedrich-Alexander-Universität Erlangen-Nürnberg | Germany | acronym/full-name, name variant | high | observed in current table |
| GIST | Gwangju Institute of Science and Technology; Gwangju Institute of Science and Technology (GIST) | South Korea | acronym/full-name, name variant | high | observed in current table |
| Georgia Tech | Georgia Institute of Technology; The Georgia Institute of Technology | USA | name variant | high | observed in current table |
| HKUST | Hong Kong University of Science and Technology; The Hong Kong University of Science and Technology; The Hong Kong University of Science and Technology (HKUST); The Hong Kong University of Science and Technology, Robotic Institute | China | acronym/full-name, name variant, punctuation variant | high | observed in current table |
| HKUST Guangzhou | Hong Kong University of Science and Technology (Guangzhou); Hong Kong University of Science and Technology (GuangZhou); The Hong Kong University of Science and Technology (Guangzhou); The Hong Kong University of Science and Technology(Guangzhou); The Hong Kong University of Science and Technology(GuangZhou) | China | acronym/full-name | high | observed in current table |
| Heidelberg University | University of Heidelberg | Germany | name variant | potential | potential alias; not observed in current table |
| Honda Research Institute USA | Honda Research Institute, USA | USA | punctuation variant | high | observed in current table |
| Hong Kong Polytechnic University | The Hong Kong Polytechnic University; The Hong Kong Polytechnic University (PolyU) | China | acronym/full-name, article variant | high | observed in current table |
| Huawei | Huawei Noah's Ark Lab; Huawei Technologies | China | lab suffix | high | observed in current table |
| IIIT Hyderabad | International Institute of Information Technology, Hyderabad | India | punctuation variant | high | observed in current table |
| IIT Jodhpur | Indian Institute of Technology, Jodhpur | India | punctuation variant | high | observed in current table |
| Inria | INRIA; Inria Bordeaux; Inria Center at the University of Bordeaux; Inria Center at University of Rennes; Inria centre at the university of Bordeaux, F-33405 Talence, France; INRIA Nancy - Grand Est; Inria Paris; Inria Rennes | France | acronym/full-name, campus/subunit suffix, lab suffix, name variant | high | observed in current table |
| Istituto Italiano di Tecnologia | Istituto Italiano Di Tecnologia; Italian Institute of Technology | Italy | accent/unaccented, name variant | high | observed in current table |
| KAIST | KAIST (Korea Advanced Institute of Science and Technology); Korea Advanced Institute of Science & Technology (KAIST); Korea Advanced Institute of Science and Technology; Korea Advanced Institute of Science and Technology (KAIST); Korea Advanced Institute of Science and Technology, KAIST | South Korea | acronym/full-name, campus/subunit suffix, name variant | high | observed in current table |
| KAUST | KAUST (King Abdullah University of Science and Technology); King Abdullah University of Science and Technology | Saudi Arabia | acronym/full-name, name variant | high | observed in current table |
| KIMM | Korea Institute of Machinery & Materials; Korea Institute of Machinery and Materials | South Korea | name variant | high | observed in current table |
| KITECH | Korea Institute of Industrial Technology | South Korea | name variant | high | observed in current table |
| KRISO | Korea Research Institute of Ships and Ocean Engineering | South Korea | name variant | high | observed in current table |
| KTH Royal Institute of Technology | KTH | Sweden | acronym/full-name | high | observed in current table |
| Karlsruhe Institute of Technology | Karlsruhe Institut of Technology; Karlsruhe Institute of Technology (KIT) | Germany | acronym/full-name, name variant | high | observed in current table |
| King's College London | King’s College London | UK | name variant | high | observed in current table |
| Leibniz University Hannover | Leibniz Universität Hannover | Germany | name variant | high | observed in current table |
| Li Auto | Li Auto Inc; LiAuto | China | lab suffix, spacing/case variant | high | observed in current table |
| Luleå University of Technology | Lulea University of Technology | Sweden | accent/unaccented | high | observed in current table |
| MBZUAI | Mohamed Bin Zayed University of Artificial Intelligence | UAE | name variant | high | observed in current table |
| MIT | Massachusetts Institute of Technology; Massachusetts Institute of Technology (MIT) | USA | acronym/full-name, name variant | high | observed in current table |
| NASA Jet Propulsion Laboratory | Jet Propulsion Laboratory; JPL; NASA JPL; NASA-JPL | USA | acronym/full-name, name variant | high | observed in current table |
| NTNU | Norwegian University of Science and Technology; Norwegian University of Science and Technology (NTNU); NTNU - Norwegian University of Science and Technology; NTNU: Norwegian University of Science and Technology | Norway | acronym/full-name, lab suffix, name variant | high | observed in current table |
| NVIDIA | Nvidia | USA | accent/unaccented | high | observed in current table |
| Nankai University | NanKai University; Nankai University, | China | accent/unaccented, campus/subunit suffix | high | observed in current table |
| Nanyang Technological University | Nanyang Technoligical University; Nanyang Technological University (NTU); Nanyang Technological University, Singapore; Nanyang Technology University; NanyangTechnological University | Singapore | acronym/full-name, campus/subunit suffix, name variant, spacing/case variant, typo variant | high | observed in current table |
| National University of Singapore | National University of Singapore (NUS); NUS | Singapore | acronym/full-name | high | observed in current table |
| Osaka University | The University of Osaka | Japan | name variant | high | observed in current table |
| POSTECH | Pohang University of Science and Technology; Pohang University of Science and Technology ( POSTECH ); Pohang University of Science and Technology (POSTECH); POSTECH, Pohang University of Science and Technology | South Korea | acronym/full-name, campus/subunit suffix, name variant | high | observed in current table |
| Peking University | Advanced Institute of Information Technology (AIIT), Peking University; Institute for Artificial Intelligence, Peking University; Peking Universitiy; Peking University (PKU); Peking University Shenzhen Graduate School; Peking Univesity; State Key Laboratory of General Artificial Inteligence, Peking University, Shenzhen Graduate School; State Key Laboratory of General Artificial Intelligence, Peking University, Shenzhen Graduate School | China | acronym/full-name, campus/subunit suffix, lab suffix, name variant | high | observed in current table |
| SUSTech | Southern University of Science and Technology; Southern University of Science and Technology (SUSTech) | China | acronym/full-name, name variant | high | observed in current table |
| Scuola Superiore Sant'Anna | Scuola Superiore Sant'Anna - SSSA | Italy | lab suffix | high | observed in current table |
| Shanghai AI Laboratory | Shanghai AI Lab; Shanghai Artificial Intelligence Laboratory | China | name variant | high | observed in current table |
| Shanghai Jiao Tong University | Shanghai Jiao Ton University; Shanghai Jiao Tong Univ; ShangHai Jiao Tong University; Shanghai Jiao Tong University, Shanghai Artificial Intelligence Laboratory; Shanghai Jiao Tong University, Shanghai Innovation Institute; Shanghai Jiaotong University; Shanghai JiaoTong University | China | accent/unaccented, campus/subunit suffix, name variant, spacing/case variant | high | observed in current table |
| ShanghaiTech University | Shanghaitech University | China | accent/unaccented | high | observed in current table |
| Shenyang Institute of Automation, Chinese Academy of Sciences | Shenyang Institute of Automation Chinese Academy of Sciences | China | name variant | high | observed in current table |
| Singapore University of Technology and Design | Singapore University of Technology & Design | Singapore | name variant | high | observed in current table |
| Sorbonne University | Sorbonne Université | France | name variant | high | observed in current table |
| Stanford University | Stanford | USA | name variant | high | observed in current table |
| TU Delft | Delft University of Technology | Netherlands | name variant | high | observed in current table |
| Technical University of Berlin | Technische Universität Berlin; TU Berlin | Germany | name variant | high | observed in current table |
| Technical University of Darmstadt | Technische Universität Darmstadt; TU Darmstadt | Germany | name variant | high | observed in current table |
| Technical University of Munich | Tech. Univ. Muenchen TUM; Technical University Munich; Technical University of Munich (TUM); Technische Universitaet Muenchen; Technische Universität München; TU Munich; TUM | Germany | acronym/full-name, name variant | high | observed in current table |
| Tsinghua University | AIR, Tsinghua University; Center for Artificial Intelligence and Robotics, Graduate School at Shenzhen, Tsinghua University, 518055 Shenzhen, China; Institute for AI Industry Research (AIR), Tsinghua University; Institute for AI Industry Research(AIR), Tsinghua University; Shenzhen Graduate School, Tsinghua University; Tsinghua; Tsinghua Shenzhen International Graduate School; Tsinghua Shenzhen International Graduate School, Tsinghua University; Tsinghua Univ; Tsinghua Univeristy; TsingHua University; Tsinghua university; tsinghua university; Tsinghua Unviersity; TsinghuaUniversity; ​Tsinghua University | China | accent/unaccented, campus/subunit suffix, name variant, spacing/case variant, typo variant | high | observed in current table |
| UC Berkeley | Berkeley; UC University of California, Berkeley; UC, Berkeley; UC,Berkeley; Univerisity of California, Berkeley; Univeristy of California, Berkeley; University of California -- Berkeley; University of California at Berkeley; University of California Berkeley; University of California, Berkeley; University of California: Berkeley | USA | name variant, punctuation variant | high | observed in current table |
| UC San Diego | UC San Diego (UCSD); UCSD; University of California - San Diego; University of California at San Diego; University of California San Diego; University of California San Diego (UCSD); University of California, San Diego | USA | acronym/full-name, name variant, punctuation variant | high | observed in current table |
| UCLA | University of California at Los Angeles; University of California Los Angeles; University of California, Los Angeles; University of California, Los Angeles (UCLA) | USA | campus/subunit suffix, name variant, punctuation variant | high | observed in current table |
| UNIST | Ulsan National Institute of Science and Technology; UNIST (Ulsan National Institute of Science and Technology) | South Korea | acronym/full-name, name variant | high | observed in current table |
| University of Bonn | Bonn University | Germany | inverted university-name variant | high | observed in current table |
| University of Bremen | Bremen University | Germany | inverted university-name variant | potential | potential alias; not observed in current table |
| University of California, Davis | UC Davis | USA | name variant | high | observed in current table |
| University of California, Merced | UC Merced; University of California, Merced | USA | campus/subunit suffix, name variant | high | observed in current table |
| University of California, Riverside | UC Riverside; University of California - Riverside; University of California Riverside | USA | name variant | high | observed in current table |
| University of California, Santa Barbara | University of California Santa Barbara | USA | name variant | high | observed in current table |
| University of Edinburgh | The University of Edinburgh; University of Edinburgh, Center for Inflammation Research, | UK | article variant, campus/subunit suffix | high | observed in current table |
| University of Freiburg | Freiburg University | Germany | inverted university-name variant | high | observed in current table |
| University of Hamburg | Hamburg University | Germany | inverted university-name variant | potential | potential alias; not observed in current table |
| University of Hong Kong | Hong Kong University; The University of Hong Kong | China | article variant, inverted university-name variant | high | observed in current table |
| University of Illinois Urbana-Champaign | UIUC; University of Illinois at Urbana Champaign; University of Illinois at Urbana-Champaign; University of Illinois Urbana Champaign; University of Illinois, Urbana-Champaign; University of Illinois-Urbana Champaign | USA | acronym/full-name, name variant, punctuation variant | high | observed in current table |
| University of Kaiserslautern-Landau | Kaiserslautern-Landau University | Germany | inverted university-name variant | potential | potential alias; not observed in current table |
| University of Konstanz | Konstanz University | Germany | inverted university-name variant | potential | potential alias; not observed in current table |
| University of Manchester | The University of Manchester | UK | article variant | high | observed in current table |
| University of Michigan | Univeristy of Michigan; University of Michigan - Ann Arbor; University of Michigan Ann Arbor; University of Michigan, Ann Arbor; University of Michigan-Ann Arbor | USA | campus/subunit suffix, lab suffix, typo variant | high | observed in current table |
| University of Nottingham | University of Nottingham (UoN) | UK | acronym/full-name | high | observed in current table |
| University of Oxford | Oxford University; Responsible Technology Institute, University of Oxford | UK | campus/subunit suffix, inverted university-name variant | high | observed in current table |
| University of Sheffield | The University of Sheffield | UK | article variant | high | observed in current table |
| University of Siena | Siena University | Italy | inverted university-name variant | high | observed in current table |
| University of Stuttgart | Stuttgart University | Germany | inverted university-name variant | potential | potential alias; not observed in current table |
| University of Sydney | The University of Sydney | Australia | article variant | high | observed in current table |
| University of Texas at Austin | The University of Texas at Austin; UT Austin | USA | article variant, name variant | high | observed in current table |
| University of Tokyo | The University of Tokyo; Univ. of Tokyo | Japan | article variant, name variant | high | observed in current table |
| University of Toronto | Univ. of Toronto | Canada | name variant | high | observed in current table |
| University of Wisconsin-Madison | University of Wisconsin - Madison; University of Wisconsin -- Madison; University of Wisconsin Madison; University of Wisconsin, Madison | USA | name variant, punctuation variant, spacing/case variant | high | observed in current table |
| University of Zurich | Zurich University | Switzerland | inverted university-name variant | potential | potential alias; not observed in current table |
| University of the Bundeswehr Munich | Universität Der Bundeswehr München | Germany | name variant | high | observed in current table |
| Waymo | Waymo LLC | USA | lab suffix | high | observed in current table |
| Xiaomi | Xiaomi Coorporation; Xiaomi EV | China | lab suffix, typo variant | high | observed in current table |
| Zhejiang University | Huzhou Institute of Zhejiang University; Zhejiang Univerisity; ZheJiang University; Zhejiang University, Huzhou Institute of Zhejiang University; Zhejiang university, robotics institute; Zhejiang University, Robotics Institute | China | accent/unaccented, campus/subunit suffix, lab suffix, name variant | high | observed in current table |
| École Polytechnique de Montréal | Ecole Polytechnique De Montreal; École Polytechnique De Montréal | Canada | accent/unaccented | high | observed in current table |

## 3. Inverted University-Name Variant Table

| Raw Variant | Canonical Institution | Rule |
| --- | --- | --- |
| Bonn University | University of Bonn | explicit alias only |
| Bremen University | University of Bremen | explicit alias only |
| Freiburg University | University of Freiburg | explicit alias only |
| Hamburg University | University of Hamburg | explicit alias only |
| Hong Kong University | University of Hong Kong | explicit alias only |
| Kaiserslautern-Landau University | University of Kaiserslautern-Landau | explicit alias only |
| Konstanz University | University of Konstanz | explicit alias only |
| Oxford University | University of Oxford | explicit alias only |
| Siena University | University of Siena | explicit alias only |
| Stuttgart University | University of Stuttgart | explicit alias only |
| Zurich University | University of Zurich | explicit alias only |

## 4. Comma-Joined / Multi-Institution Affiliation Table

| Raw Affiliation | Canonical Institutions | Paper Count | Status | Notes |
| --- | --- | --- | --- | --- |
| Beijing University of Posts and Telecommunications / Tsinghua University | Beijing University of Posts and Telecommunications; Tsinghua University | 1 | observed | split only by exact multimap lookup |
| Chinese Univ Hong Kong (CUHK) & National Univ Singapore(NUS) | CUHK; National University of Singapore | 6 | observed | split only by exact multimap lookup |
| Dalian Univ. of Tech.; CUHK-Shenzhen | Dalian University of Technology; CUHK Shenzhen | 1 | observed | split only by exact multimap lookup |
| ETH Zurich & IDSIA, USI-SUPSI | ETH Zurich; IDSIA, USI-SUPSI | 1 | observed | split only by exact multimap lookup |
| ETH Zurich & University of Cyprus | ETH Zurich; University of Cyprus | 1 | observed | split only by exact multimap lookup |
| ETH Zurich and EPFL | ETH Zurich; EPFL | 1 | observed | split only by exact multimap lookup |
| ETH Zurich, Stanford | ETH Zurich; Stanford University | 1 | observed | split only by exact multimap lookup |
| Idiap Research Institute and EPFL | Idiap Research Institute; EPFL | 2 | observed | split only by exact multimap lookup |
| Idiap Research Institute, EPFL | Idiap Research Institute; EPFL | 2 | observed | split only by exact multimap lookup |
| Idiap Research Institute; EPFL | Idiap Research Institute; EPFL | 2 | observed | split only by exact multimap lookup |
| JPL, Caltech | NASA Jet Propulsion Laboratory; Caltech | 0 | potential | split only by exact multimap lookup |
| Jet Propulsion Laboratory, California Institute of Technology | NASA Jet Propulsion Laboratory; Caltech | 6 | observed | split only by exact multimap lookup |
| LAAS-CNRS and Université De Toulouse | LAAS-CNRS; Université de Toulouse | 3 | observed | split only by exact multimap lookup |
| MIT, Woods Hole Oceanographic Institution | MIT; Woods Hole Oceanographic Institution | 1 | observed | split only by exact multimap lookup |
| NASA / Caltech Jet Propulsion Laboratory | NASA Jet Propulsion Laboratory; Caltech | 1 | observed | split only by exact multimap lookup |
| NASA Jet Propulsion Laboratory, California Institute of Technology | NASA Jet Propulsion Laboratory; Caltech | 0 | potential | split only by exact multimap lookup |
| NASA-JPL, Caltech | NASA Jet Propulsion Laboratory; Caltech | 2 | observed | split only by exact multimap lookup |
| NVIDIA, UC Berkeley | NVIDIA; UC Berkeley | 1 | observed | split only by exact multimap lookup |
| Nasa's Jet Propulsion Laboratory, Caltech | NASA Jet Propulsion Laboratory; Caltech | 1 | observed | split only by exact multimap lookup |
| National University of Singapore, the University of Hong Kong | National University of Singapore; University of Hong Kong | 1 | observed | split only by exact multimap lookup |
| Noah's Ark Lab, Huawei Technologies | Noah's Ark Lab; Huawei | 6 | observed | split only by exact multimap lookup |
| PICO, ByteDance | PICO; ByteDance | 2 | observed | split only by exact multimap lookup |
| Singapore University of Technology and Design, MIT | Singapore University of Technology and Design; MIT | 1 | observed | split only by exact multimap lookup |
| Stanford & UIUC | Stanford University; University of Illinois Urbana-Champaign | 1 | observed | split only by exact multimap lookup |
| Tencent, Tsinghua University | Tencent; Tsinghua University | 1 | observed | split only by exact multimap lookup |
| The University of Sydney; Vanderbilt University | University of Sydney; Vanderbilt University | 7 | observed | split only by exact multimap lookup |
| The University of Tokyo & RIKEN AIP | University of Tokyo; RIKEN AIP | 1 | observed | split only by exact multimap lookup |
| Tsinghua University; Shanghai Qi Zhi Institute | Tsinghua University; Shanghai Qi Zhi Institute | 1 | observed | split only by exact multimap lookup |
| UC Berkeley / TOYOTA Motor North America | UC Berkeley; Toyota Motor North America | 2 | observed | split only by exact multimap lookup |
| University of Illinois Urbana-Champaign & Instituto Tecnológico Autónomo De México | University of Illinois Urbana-Champaign; Instituto Tecnológico Autónomo de México | 1 | observed | split only by exact multimap lookup |
| University of Illinois Urbana-Champaign & Instituto Tecnológico Autónomo de México | University of Illinois Urbana-Champaign; Instituto Tecnológico Autónomo de México | 2 | observed | split only by exact multimap lookup |
| University of Illinois Urbana-Champaign/NASA Jet Propulsion Laboratory | University of Illinois Urbana-Champaign; NASA Jet Propulsion Laboratory | 2 | observed | split only by exact multimap lookup |
| University of Oxford, NVIDIA | University of Oxford; NVIDIA | 1 | observed | split only by exact multimap lookup |
| University of Sydney, NVIDIA | University of Sydney; NVIDIA | 7 | observed | split only by exact multimap lookup |
| Waabi / University of Toronto | Waabi; University of Toronto | 2 | observed | split only by exact multimap lookup |
| Waabi, University of Toronto | Waabi; University of Toronto | 2 | observed | split only by exact multimap lookup |
| Westlake University, Zhejiang University | Westlake University; Zhejiang University | 1 | observed | split only by exact multimap lookup |
| Zhejiang University, Idiap Research Institute | Zhejiang University; Idiap Research Institute | 1 | observed | split only by exact multimap lookup |
| Zhejiang University, Shanghai AI Laboratory | Zhejiang University; Shanghai AI Laboratory | 1 | observed | split only by exact multimap lookup |
| Zhejiang University, Westlake University | Zhejiang University; Westlake University | 2 | observed | split only by exact multimap lookup |

## 5. Do-Not-Merge Table

| Institution A | Institution B | Reason |
| --- | --- | --- |
| ETH Zurich | University of Zurich | Different institutions in Zurich. |
| The University of Queensland | Queensland University of Technology | Different Australian universities. |
| University of Washington | Washington University in St. Louis | Different US universities. |
| ShanghaiTech University | Shanghai University | Different Chinese universities. |
| Zhejiang University | Zhejiang University of Technology | Different Chinese universities. |
| Zhejiang University | Zhejiang Sci-Tech University | Different Chinese universities. |
| University of California | UC Berkeley | System-level name should not be automatically mapped to a specific campus. |
| University of California | UC San Diego | System-level name should not be automatically mapped to a specific campus. |
| University of California | UCLA | System-level name should not be automatically mapped to a specific campus. |
| HKUST | HKUST Guangzhou | Same university brand but potentially different campus/entity. |
| CUHK | CUHK Shenzhen | Same university brand but potentially different campus/entity. |
| Northeastern University | Northeastern University, China | Potentially different institutions; requires manual verification. |
| Northwestern University | Northwestern Polytechnical University | Different institutions in different countries. |
| University of Technology Sydney | Singapore University of Technology and Design | Different institutions. |
| Technical University of Munich | LMU Munich | Different Munich universities. |
| Vrije Universiteit Brussel | Vrije Universiteit Amsterdam | Different institutions in different countries. |
| University of Electronic Science and Technology of China | University of Science and Technology of China | Different Chinese universities. |
| Beijing Institute of Technology | Beijing University of Technology | Different Chinese universities. |
| South China University of Technology | South China Normal University | Different Chinese universities. |
| University of York | York University | Different possible institutions depending on country/context. |
| University of Oxford | Oxford Brookes University | Different UK universities despite shared city name. |
| MIT | Mitsubishi Electric Research Laboratories | Substring MIT appears inside unrelated institution/company names. |
| University of California | University of California, Merced | System-level name should not be automatically mapped to a specific campus. |

## 6. Ambiguous / Needs Manual Review Table

| Raw Affiliation | Paper Count | Country | Reason |
| --- | --- | --- | --- |
| Huazhong University of Science and Technology | 31 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Science and Technology of China | 26 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Beijing University of Posts and Telecommunications | 21 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Harbin Institute of Technology, Shenzhen | 18 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Korea Institute of Science and Technology | 14 | South Korea | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Texas A&M University | 13 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Robotics and AI Institute | 12 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Electronic Science and Technology of China | 11 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Institute of Computing Technology, Chinese Academy of Sciences | 10 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Japan Advanced Institute of Science and Technology | 9 | Japan | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Maryland, College Park | 9 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of California, Riverside | 9 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Singapore University of Technology and Design | 8 | Singapore | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Nanjing University of Science and Technology | 7 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Science and Technology Beijing | 7 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Agency for Science, Technology and Research (A*STAR) | 6 | Singapore | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Shenyang Institute of Automation, Chinese Academy of Sciences | 6 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Nanjing University of Aeronautics and Astronautics | 5 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Minnesota, Twin Cities | 5 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Nevada, Reno | 5 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Beijing Galbot Co., Ltd | 4 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Nara Institute of Science and Technology | 4 | Japan | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of California, Irvine | 4 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| School of Artificial Intelligence, University of Chinese Academy of Sciences | 4 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Mechanical Eng., Sogang University | 4 | South Korea | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| China University of Mining and Technology | 4 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Hefei Institutes of Physical Science, Chinese Academy of Sciences | 4 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Institute of Software, Chinese Academy of Sciences | 3 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Shenzhen Institute of Advanced Technology, Chinese Academy of Sciences | 3 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Wuhan University of Science and Technology | 3 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Electronic Science and Technology | 3 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| East China University of Science and Technology | 3 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Shenzhen Institute of Artificial Intelligence and Robotics for Society | 3 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Beijing Information Science and Technology University | 3 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Zagreb, Faculty of Electrical Engineering and Computing | 3 | Croatia | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| School of Information Engineering, Chang 'an University | 3 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| IIIT, Hyderabad | 3 | India | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Guangdong Laboratory of Artificial Intelligence and Digital Economy (SZ) | 3 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Hong Kong Institute of Science & Innovation, Chinese Academy of Sciences | 3 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Technology, Sydney | 3 | Australia | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Korea Research Institute of Ships & Ocean Engineering (KRISO) | 3 | South Korea | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Twente / Sapienza University of Rome | 3 | Netherlands | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Seoul National University of Science and Technology | 3 | South Korea | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Washington, Seattle | 3 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Institute for Infocomm Research, A*STAR | 3 | Singapore | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Singapore-MIT Alliance for Research and Technology | 3 | Singapore | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| PERCRO Laboratory, TeCIP Institute, Sant’Anna School of Advanced Studies, Pisa | 3 | Italy | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| CTU, CIIRC | 2 | Czech | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Nat. Inst. of Advanced Industrial Science and Technology | 2 | Japan | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Eastern Institute of Technology, Ningbo | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Gwangju Institue of Science and Technology (GIST) | 2 | South Korea | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Chongqing Afari Intelligent Drive Co., Ltd | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Field AI, Inc | 2 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Macau University of Science and Technology | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| CNRS, Lab-STICC | 2 | France | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Technology and Engineering Center for Space Utilization, Chinese Academy of Sciences | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| TU Wien, Austrian Institute of Technology | 2 | Austria | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Pennsylvania, Honda Research Institute USA | 2 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Honda Research Institute USA, Inc | 2 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Beijing University of Aeronautics and Astronautics | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Skolkovo Institute of Science and Technology | 2 | Russia | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Bielefeld University / Fraunhofer IOSB-INA | 2 | Germany | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Macau, Xiaomi EV | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Shanghai Key Laboratory of Flexible Medical Robotics, Tongren Hospital, Institute of Medical Robotics, Shanghai Jiao Tong Univer | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Shenzhen University, | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Institute of Computing Technology, Chinese Academy | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Ruijin Hospital, Shanghai Jiao Tong University School of Medicine | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Trento, Politecnico Di Bari | 2 | Italy | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Indian Institute of Science, Bangalore | 2 | India | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Galaxy General Robot Co., Ltd | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Poznan University of Technology, IDEAS Research Institute, IDEAS NCBR | 2 | Poland | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of California, Santa Barbara | 2 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Honda R&D Co., Ltd | 2 | Japan | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Gyeongsang National University, South Korea | 2 | South Korea | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Sirius University of Science and Technology | 2 | Russia | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Shanghai Flexiv Robotics Technology CO., LTD | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| TU Munich, Institute for Robotics and Systems Intelligence | 2 | Germany | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Leonardo, Innovation Hub | 2 | Italy | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Universität Konstanz & Max Planck Institute of Animal Behavior | 2 | Germany | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Institut De Robòtica I Informàtica Industrial, CSIC-UPC | 2 | Spain | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Guangming Laboratory, Guangdong Laboratory of Artificial Intelligence and Digital Economy (SZ) | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| DGIST (Daegu Gyeongbuk Institute of Science and Technology) | 2 | South Korea | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Nanjing University of Posts and Telecommunications | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| The University of Tennessee, Knoxville | 2 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Korea Institute of Machinery and Materials (KIMM) | 2 | South Korea | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Science and Technology(UST), Korea Research Institute of Ships & Ocean Engineering(KRISO) | 2 | South Korea | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Science and Technology | 2 | South Korea | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| KRISO(Korea Research Institute of Ships and Ocean Engineereing | 2 | South Korea | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Korea Hydro & Nuclear Power Co., Ltd | 2 | South Korea | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Institute of AI for Industries, Chinese Academy of Sciences | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| KITECH(Korea Institute of Industrial Technology), | 2 | South Korea | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Hanoi University of Science and Technology | 2 | Vietnam | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Toyota Motor North America R&D | 2 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| China Ship Development &design Center | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Huawei, Autonomous University of Barcelona, | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Carnegie Mellon University, Robotics Institute | 2 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Singapore-MIT Alliance for Research and Technology (SMART) | 2 | Singapore | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| H.U. Group Research Inst. G. K., Japan | 2 | Japan | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Robotics Research Center, IIIT Hyderabad | 2 | India | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Beijing Univerisity of Aeronautics and Astronautics | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Ceske vysoke uceni technicke v Praze, FEL | 2 | Czech | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| NVIDIA, Carnegie Mellon University | 2 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Interdisciplinary Centre for Security, Reliability and Trust - University of Luxembourg | 2 | Luxembourg | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| N/A | 2 | Unknown | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Université Grenoble Alpes, CEA, Leti | 2 | France | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Université Paris-Saclay, CEA, List | 2 | France | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| USI and SUPSI | 2 | Switzerland | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Honda Research Institute Japan Co., Ltd | 2 | Japan | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| William & Mary | 2 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Northwest A&F University | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Suzhou University of Science and Technology | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Ulsan National Institute of Science and Technology (UNIST) | 2 | South Korea | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Seoul National University, Karlsruhe Institute of Technology | 2 | South Korea | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Toyota Motor North America, InfoTech Labs | 2 | USA | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| University of Modena and Reggio Emilia | 2 | Italy | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Imperial College, London, UK | 2 | UK | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Federal University of Minas Gerais, UFMG, Brazil | 2 | Brazil | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Khalifa University of Science and Technology | 2 | UAE | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| Shanghai Aopeng Medical Technology Co., Ltd | 2 | China | Contains a separator or subunit phrase and is not covered by alias/multimap. |
| TeCIP Institute, Scuola Superiore Sant'Anna | 2 | Italy | Contains a separator or subunit phrase and is not covered by alias/multimap. |

## 7. Proposed aff_institution_aliases.json

```json
{
  "National Institute of Advanced Industrial Science and Technology": "AIST",
  "National Institute of Advanced Industrial Science and Technology (AIST)": "AIST",
  "Alibaba": "Alibaba DAMO Academy",
  "Alibaba Damo Academy": "Alibaba DAMO Academy",
  "Alibaba Group": "Alibaba DAMO Academy",
  "Allen Institute for Artificial Intelligence": "Allen Institute for AI",
  "BeiHang University": "Beihang University",
  "Beihang Unverisity": "Beihang University",
  "Beijing Institute for General Artificial Intelligence": "BIGAI",
  "Beijing Institute for General Artificial Intelligence (BIGAI)": "BIGAI",
  "Bytedance": "ByteDance",
  "ByteDance Inc": "ByteDance",
  "California Institute of Technology": "Caltech",
  "California Institute of Technology (Caltech)": "Caltech",
  "CALTECH": "Caltech",
  "Institute of Automation, Chinese Academy of Science": "CASIA",
  "Institute of Automation, Chinese Academy of Sciences": "CASIA",
  "Institute of Automation，Chinese Academy of Sciences": "CASIA",
  "Chinese University of Hong Kong": "CUHK",
  "CUHK": "CUHK",
  "T-Stone Robotics Institute, the Chinese University of Hong Kong": "CUHK",
  "The Chinese University of Hong Kong": "CUHK",
  "The Chinese University of Hong Kong (CUHK)": "CUHK",
  "Chinese University of Hong Kong (Shenzhen)": "CUHK Shenzhen",
  "Chinese University of Hong Kong, Shenzhen": "CUHK Shenzhen",
  "CUHK(SZ)": "CUHK Shenzhen",
  "The Chinese University of Hong Kong (Shenzhen)": "CUHK Shenzhen",
  "The Chinese University of Hong Kong CUHK (Shenzhen)": "CUHK Shenzhen",
  "The Chinese University of Hong Kong, Shenzhen": "CUHK Shenzhen",
  "The Chinese Unviersity of Hong Kong, Shenzhen": "CUHK Shenzhen",
  "Daegu Gyeongbuk Institute of Science and Technology": "DGIST",
  "Daegu Gyeongbuk Institute of Science and Technology (DGIST)": "DGIST",
  "Daegu Gyeongbuk Institute of Science and Technology(DGIST)": "DGIST",
  "Ecole Polytechnique Federale De Lausanne": "EPFL",
  "Ecole Polytechnique Fédérale De Lausanne": "EPFL",
  "Ecole Polytechnique Fédérale De Lausanne (EPFL)": "EPFL",
  "Epfl": "EPFL",
  "EPFL, Lausanne, Switzerland": "EPFL",
  "École Polytechnique Fédérale De Lausanne": "EPFL",
  "École Polytechnique Fédérale De Lausanne (EPFL)": "EPFL",
  "École Polytechnique Fédérale De Lausanne (EPFL), Switzerland": "EPFL",
  "ETH": "ETH Zurich",
  "ETH ZUrich": "ETH Zurich",
  "ETH Zurich, Automatic Control Laboratory (IfA)": "ETH Zurich",
  "ETH Zurich, Autonomous Systems Lab": "ETH Zurich",
  "ETH Zurich, Mimic Robotics": "ETH Zurich",
  "ETH Zurich, Robotic Systems Lab": "ETH Zurich",
  "ETH Zürich": "ETH Zurich",
  "ETHZ": "ETH Zurich",
  "Rehabilitation Engineering Laboratory, ETH Zurich": "ETH Zurich",
  "RSL, ETHZ": "ETH Zurich",
  "Friedrich-Alexander-University Erlangen-Nurnberg (FAU)": "FAU Erlangen-Nürnberg",
  "Friedrich-Alexander-Universität Erlangen-Nürnberg": "FAU Erlangen-Nürnberg",
  "Georgia Institute of Technology": "Georgia Tech",
  "The Georgia Institute of Technology": "Georgia Tech",
  "Gwangju Institute of Science and Technology": "GIST",
  "Gwangju Institute of Science and Technology (GIST)": "GIST",
  "University of Heidelberg": "Heidelberg University",
  "Hong Kong University of Science and Technology": "HKUST",
  "The Hong Kong University of Science and Technology": "HKUST",
  "The Hong Kong University of Science and Technology (HKUST)": "HKUST",
  "The Hong Kong University of Science and Technology, Robotic Institute": "HKUST",
  "Hong Kong University of Science and Technology (Guangzhou)": "HKUST Guangzhou",
  "Hong Kong University of Science and Technology (GuangZhou)": "HKUST Guangzhou",
  "The Hong Kong University of Science and Technology (Guangzhou)": "HKUST Guangzhou",
  "The Hong Kong University of Science and Technology(Guangzhou)": "HKUST Guangzhou",
  "The Hong Kong University of Science and Technology(GuangZhou)": "HKUST Guangzhou",
  "Honda Research Institute, USA": "Honda Research Institute USA",
  "The Hong Kong Polytechnic University": "Hong Kong Polytechnic University",
  "The Hong Kong Polytechnic University (PolyU)": "Hong Kong Polytechnic University",
  "Huawei Noah's Ark Lab": "Huawei",
  "Huawei Technologies": "Huawei",
  "International Institute of Information Technology, Hyderabad": "IIIT Hyderabad",
  "Indian Institute of Technology, Jodhpur": "IIT Jodhpur",
  "INRIA": "Inria",
  "Inria Bordeaux": "Inria",
  "Inria Center at the University of Bordeaux": "Inria",
  "Inria Center at University of Rennes": "Inria",
  "Inria centre at the university of Bordeaux, F-33405 Talence, France": "Inria",
  "INRIA Nancy - Grand Est": "Inria",
  "Inria Paris": "Inria",
  "Inria Rennes": "Inria",
  "Istituto Italiano Di Tecnologia": "Istituto Italiano di Tecnologia",
  "Italian Institute of Technology": "Istituto Italiano di Tecnologia",
  "KAIST (Korea Advanced Institute of Science and Technology)": "KAIST",
  "Korea Advanced Institute of Science & Technology (KAIST)": "KAIST",
  "Korea Advanced Institute of Science and Technology": "KAIST",
  "Korea Advanced Institute of Science and Technology (KAIST)": "KAIST",
  "Korea Advanced Institute of Science and Technology, KAIST": "KAIST",
  "Karlsruhe Institut of Technology": "Karlsruhe Institute of Technology",
  "Karlsruhe Institute of Technology (KIT)": "Karlsruhe Institute of Technology",
  "KAUST (King Abdullah University of Science and Technology)": "KAUST",
  "King Abdullah University of Science and Technology": "KAUST",
  "Korea Institute of Machinery & Materials": "KIMM",
  "Korea Institute of Machinery and Materials": "KIMM",
  "King’s College London": "King's College London",
  "Korea Institute of Industrial Technology": "KITECH",
  "Korea Research Institute of Ships and Ocean Engineering": "KRISO",
  "KTH": "KTH Royal Institute of Technology",
  "Leibniz Universität Hannover": "Leibniz University Hannover",
  "Li Auto Inc": "Li Auto",
  "LiAuto": "Li Auto",
  "Lulea University of Technology": "Luleå University of Technology",
  "Mohamed Bin Zayed University of Artificial Intelligence": "MBZUAI",
  "Massachusetts Institute of Technology": "MIT",
  "Massachusetts Institute of Technology (MIT)": "MIT",
  "NanKai University": "Nankai University",
  "Nankai University,": "Nankai University",
  "Nanyang Technoligical University": "Nanyang Technological University",
  "Nanyang Technological University (NTU)": "Nanyang Technological University",
  "Nanyang Technological University, Singapore": "Nanyang Technological University",
  "Nanyang Technology University": "Nanyang Technological University",
  "NanyangTechnological University": "Nanyang Technological University",
  "Jet Propulsion Laboratory": "NASA Jet Propulsion Laboratory",
  "JPL": "NASA Jet Propulsion Laboratory",
  "NASA JPL": "NASA Jet Propulsion Laboratory",
  "NASA-JPL": "NASA Jet Propulsion Laboratory",
  "National University of Singapore (NUS)": "National University of Singapore",
  "NUS": "National University of Singapore",
  "Norwegian University of Science and Technology": "NTNU",
  "Norwegian University of Science and Technology (NTNU)": "NTNU",
  "NTNU - Norwegian University of Science and Technology": "NTNU",
  "NTNU: Norwegian University of Science and Technology": "NTNU",
  "Nvidia": "NVIDIA",
  "The University of Osaka": "Osaka University",
  "Advanced Institute of Information Technology (AIIT), Peking University": "Peking University",
  "Institute for Artificial Intelligence, Peking University": "Peking University",
  "Peking Universitiy": "Peking University",
  "Peking University (PKU)": "Peking University",
  "Peking University Shenzhen Graduate School": "Peking University",
  "Peking Univesity": "Peking University",
  "State Key Laboratory of General Artificial Inteligence, Peking University, Shenzhen Graduate School": "Peking University",
  "State Key Laboratory of General Artificial Intelligence, Peking University, Shenzhen Graduate School": "Peking University",
  "Pohang University of Science and Technology": "POSTECH",
  "Pohang University of Science and Technology ( POSTECH )": "POSTECH",
  "Pohang University of Science and Technology (POSTECH)": "POSTECH",
  "POSTECH, Pohang University of Science and Technology": "POSTECH",
  "Scuola Superiore Sant'Anna - SSSA": "Scuola Superiore Sant'Anna",
  "Shanghai AI Lab": "Shanghai AI Laboratory",
  "Shanghai Artificial Intelligence Laboratory": "Shanghai AI Laboratory",
  "Shanghai Jiao Ton University": "Shanghai Jiao Tong University",
  "Shanghai Jiao Tong Univ": "Shanghai Jiao Tong University",
  "ShangHai Jiao Tong University": "Shanghai Jiao Tong University",
  "Shanghai Jiao Tong University, Shanghai Artificial Intelligence Laboratory": "Shanghai Jiao Tong University",
  "Shanghai Jiao Tong University, Shanghai Innovation Institute": "Shanghai Jiao Tong University",
  "Shanghai Jiaotong University": "Shanghai Jiao Tong University",
  "Shanghai JiaoTong University": "Shanghai Jiao Tong University",
  "Shanghaitech University": "ShanghaiTech University",
  "Shenyang Institute of Automation Chinese Academy of Sciences": "Shenyang Institute of Automation, Chinese Academy of Sciences",
  "Singapore University of Technology & Design": "Singapore University of Technology and Design",
  "Sorbonne Université": "Sorbonne University",
  "Stanford": "Stanford University",
  "Southern University of Science and Technology": "SUSTech",
  "Southern University of Science and Technology (SUSTech)": "SUSTech",
  "Technische Universität Berlin": "Technical University of Berlin",
  "TU Berlin": "Technical University of Berlin",
  "Technische Universität Darmstadt": "Technical University of Darmstadt",
  "TU Darmstadt": "Technical University of Darmstadt",
  "Tech. Univ. Muenchen TUM": "Technical University of Munich",
  "Technical University Munich": "Technical University of Munich",
  "Technical University of Munich (TUM)": "Technical University of Munich",
  "Technische Universitaet Muenchen": "Technical University of Munich",
  "Technische Universität München": "Technical University of Munich",
  "TU Munich": "Technical University of Munich",
  "TUM": "Technical University of Munich",
  "AIR, Tsinghua University": "Tsinghua University",
  "Center for Artificial Intelligence and Robotics, Graduate School at Shenzhen, Tsinghua University, 518055 Shenzhen, China": "Tsinghua University",
  "Institute for AI Industry Research (AIR), Tsinghua University": "Tsinghua University",
  "Institute for AI Industry Research(AIR), Tsinghua University": "Tsinghua University",
  "Shenzhen Graduate School, Tsinghua University": "Tsinghua University",
  "Tsinghua": "Tsinghua University",
  "Tsinghua Shenzhen International Graduate School": "Tsinghua University",
  "Tsinghua Shenzhen International Graduate School, Tsinghua University": "Tsinghua University",
  "Tsinghua Univ": "Tsinghua University",
  "Tsinghua Univeristy": "Tsinghua University",
  "TsingHua University": "Tsinghua University",
  "Tsinghua university": "Tsinghua University",
  "tsinghua university": "Tsinghua University",
  "Tsinghua Unviersity": "Tsinghua University",
  "TsinghuaUniversity": "Tsinghua University",
  "​Tsinghua University": "Tsinghua University",
  "Delft University of Technology": "TU Delft",
  "Berkeley": "UC Berkeley",
  "UC University of California, Berkeley": "UC Berkeley",
  "UC, Berkeley": "UC Berkeley",
  "UC,Berkeley": "UC Berkeley",
  "Univerisity of California, Berkeley": "UC Berkeley",
  "Univeristy of California, Berkeley": "UC Berkeley",
  "University of California -- Berkeley": "UC Berkeley",
  "University of California at Berkeley": "UC Berkeley",
  "University of California Berkeley": "UC Berkeley",
  "University of California, Berkeley": "UC Berkeley",
  "University of California: Berkeley": "UC Berkeley",
  "UC San Diego (UCSD)": "UC San Diego",
  "UCSD": "UC San Diego",
  "University of California - San Diego": "UC San Diego",
  "University of California at San Diego": "UC San Diego",
  "University of California San Diego": "UC San Diego",
  "University of California San Diego (UCSD)": "UC San Diego",
  "University of California, San Diego": "UC San Diego",
  "University of California at Los Angeles": "UCLA",
  "University of California Los Angeles": "UCLA",
  "University of California, Los Angeles": "UCLA",
  "University of California, Los Angeles (UCLA)": "UCLA",
  "Ulsan National Institute of Science and Technology": "UNIST",
  "UNIST (Ulsan National Institute of Science and Technology)": "UNIST",
  "Bonn University": "University of Bonn",
  "Bremen University": "University of Bremen",
  "UC Davis": "University of California, Davis",
  "UC Merced": "University of California, Merced",
  "University of California, Merced": "University of California, Merced",
  "UC Riverside": "University of California, Riverside",
  "University of California - Riverside": "University of California, Riverside",
  "University of California Riverside": "University of California, Riverside",
  "University of California Santa Barbara": "University of California, Santa Barbara",
  "The University of Edinburgh": "University of Edinburgh",
  "University of Edinburgh, Center for Inflammation Research,": "University of Edinburgh",
  "Freiburg University": "University of Freiburg",
  "Hamburg University": "University of Hamburg",
  "Hong Kong University": "University of Hong Kong",
  "The University of Hong Kong": "University of Hong Kong",
  "UIUC": "University of Illinois Urbana-Champaign",
  "University of Illinois at Urbana Champaign": "University of Illinois Urbana-Champaign",
  "University of Illinois at Urbana-Champaign": "University of Illinois Urbana-Champaign",
  "University of Illinois Urbana Champaign": "University of Illinois Urbana-Champaign",
  "University of Illinois, Urbana-Champaign": "University of Illinois Urbana-Champaign",
  "University of Illinois-Urbana Champaign": "University of Illinois Urbana-Champaign",
  "Kaiserslautern-Landau University": "University of Kaiserslautern-Landau",
  "Konstanz University": "University of Konstanz",
  "The University of Manchester": "University of Manchester",
  "Univeristy of Michigan": "University of Michigan",
  "University of Michigan - Ann Arbor": "University of Michigan",
  "University of Michigan Ann Arbor": "University of Michigan",
  "University of Michigan, Ann Arbor": "University of Michigan",
  "University of Michigan-Ann Arbor": "University of Michigan",
  "University of Nottingham (UoN)": "University of Nottingham",
  "Oxford University": "University of Oxford",
  "Responsible Technology Institute, University of Oxford": "University of Oxford",
  "The University of Sheffield": "University of Sheffield",
  "Siena University": "University of Siena",
  "Stuttgart University": "University of Stuttgart",
  "The University of Sydney": "University of Sydney",
  "The University of Texas at Austin": "University of Texas at Austin",
  "UT Austin": "University of Texas at Austin",
  "Universität Der Bundeswehr München": "University of the Bundeswehr Munich",
  "The University of Tokyo": "University of Tokyo",
  "Univ. of Tokyo": "University of Tokyo",
  "Univ. of Toronto": "University of Toronto",
  "University of Wisconsin - Madison": "University of Wisconsin-Madison",
  "University of Wisconsin -- Madison": "University of Wisconsin-Madison",
  "University of Wisconsin Madison": "University of Wisconsin-Madison",
  "University of Wisconsin, Madison": "University of Wisconsin-Madison",
  "Zurich University": "University of Zurich",
  "Waymo LLC": "Waymo",
  "Xiaomi Coorporation": "Xiaomi",
  "Xiaomi EV": "Xiaomi",
  "Huzhou Institute of Zhejiang University": "Zhejiang University",
  "Zhejiang Univerisity": "Zhejiang University",
  "ZheJiang University": "Zhejiang University",
  "Zhejiang University, Huzhou Institute of Zhejiang University": "Zhejiang University",
  "Zhejiang university, robotics institute": "Zhejiang University",
  "Zhejiang University, Robotics Institute": "Zhejiang University",
  "Ecole Polytechnique De Montreal": "École Polytechnique de Montréal",
  "École Polytechnique De Montréal": "École Polytechnique de Montréal"
}
```

Potential aliases not observed in the current table are retained in the JSON because they are high-confidence guards from the instruction, but the merge table marks them as potential.

## 8. Proposed aff_institution_multimap.json

```json
{
  "Beijing University of Posts and Telecommunications / Tsinghua University": [
    "Beijing University of Posts and Telecommunications",
    "Tsinghua University"
  ],
  "Chinese Univ Hong Kong (CUHK) & National Univ Singapore(NUS)": [
    "CUHK",
    "National University of Singapore"
  ],
  "Dalian Univ. of Tech.; CUHK-Shenzhen": [
    "Dalian University of Technology",
    "CUHK Shenzhen"
  ],
  "ETH Zurich & IDSIA, USI-SUPSI": [
    "ETH Zurich",
    "IDSIA, USI-SUPSI"
  ],
  "ETH Zurich & University of Cyprus": [
    "ETH Zurich",
    "University of Cyprus"
  ],
  "ETH Zurich and EPFL": [
    "ETH Zurich",
    "EPFL"
  ],
  "ETH Zurich, Stanford": [
    "ETH Zurich",
    "Stanford University"
  ],
  "Idiap Research Institute and EPFL": [
    "Idiap Research Institute",
    "EPFL"
  ],
  "Idiap Research Institute, EPFL": [
    "Idiap Research Institute",
    "EPFL"
  ],
  "Idiap Research Institute; EPFL": [
    "Idiap Research Institute",
    "EPFL"
  ],
  "Jet Propulsion Laboratory, California Institute of Technology": [
    "NASA Jet Propulsion Laboratory",
    "Caltech"
  ],
  "JPL, Caltech": [
    "NASA Jet Propulsion Laboratory",
    "Caltech"
  ],
  "LAAS-CNRS and Université De Toulouse": [
    "LAAS-CNRS",
    "Université de Toulouse"
  ],
  "MIT, Woods Hole Oceanographic Institution": [
    "MIT",
    "Woods Hole Oceanographic Institution"
  ],
  "NASA / Caltech Jet Propulsion Laboratory": [
    "NASA Jet Propulsion Laboratory",
    "Caltech"
  ],
  "NASA Jet Propulsion Laboratory, California Institute of Technology": [
    "NASA Jet Propulsion Laboratory",
    "Caltech"
  ],
  "Nasa's Jet Propulsion Laboratory, Caltech": [
    "NASA Jet Propulsion Laboratory",
    "Caltech"
  ],
  "NASA-JPL, Caltech": [
    "NASA Jet Propulsion Laboratory",
    "Caltech"
  ],
  "National University of Singapore, the University of Hong Kong": [
    "National University of Singapore",
    "University of Hong Kong"
  ],
  "Noah's Ark Lab, Huawei Technologies": [
    "Noah's Ark Lab",
    "Huawei"
  ],
  "NVIDIA, UC Berkeley": [
    "NVIDIA",
    "UC Berkeley"
  ],
  "PICO, ByteDance": [
    "PICO",
    "ByteDance"
  ],
  "Singapore University of Technology and Design, MIT": [
    "Singapore University of Technology and Design",
    "MIT"
  ],
  "Stanford & UIUC": [
    "Stanford University",
    "University of Illinois Urbana-Champaign"
  ],
  "Tencent, Tsinghua University": [
    "Tencent",
    "Tsinghua University"
  ],
  "The University of Sydney; Vanderbilt University": [
    "University of Sydney",
    "Vanderbilt University"
  ],
  "The University of Tokyo & RIKEN AIP": [
    "University of Tokyo",
    "RIKEN AIP"
  ],
  "Tsinghua University; Shanghai Qi Zhi Institute": [
    "Tsinghua University",
    "Shanghai Qi Zhi Institute"
  ],
  "UC Berkeley / TOYOTA Motor North America": [
    "UC Berkeley",
    "Toyota Motor North America"
  ],
  "University of Illinois Urbana-Champaign & Instituto Tecnológico Autónomo de México": [
    "University of Illinois Urbana-Champaign",
    "Instituto Tecnológico Autónomo de México"
  ],
  "University of Illinois Urbana-Champaign & Instituto Tecnológico Autónomo De México": [
    "University of Illinois Urbana-Champaign",
    "Instituto Tecnológico Autónomo de México"
  ],
  "University of Illinois Urbana-Champaign/NASA Jet Propulsion Laboratory": [
    "University of Illinois Urbana-Champaign",
    "NASA Jet Propulsion Laboratory"
  ],
  "University of Oxford, NVIDIA": [
    "University of Oxford",
    "NVIDIA"
  ],
  "University of Sydney, NVIDIA": [
    "University of Sydney",
    "NVIDIA"
  ],
  "Waabi / University of Toronto": [
    "Waabi",
    "University of Toronto"
  ],
  "Waabi, University of Toronto": [
    "Waabi",
    "University of Toronto"
  ],
  "Westlake University, Zhejiang University": [
    "Westlake University",
    "Zhejiang University"
  ],
  "Zhejiang University, Idiap Research Institute": [
    "Zhejiang University",
    "Idiap Research Institute"
  ],
  "Zhejiang University, Shanghai AI Laboratory": [
    "Zhejiang University",
    "Shanghai AI Laboratory"
  ],
  "Zhejiang University, Westlake University": [
    "Zhejiang University",
    "Westlake University"
  ]
}
```

Counting-policy recommendation: full counting with per-paper deduplication. A paper contributes at most one count to each canonical institution after exact multimap splitting and alias canonicalization.

## 9. Proposed aff_institution_do_not_merge.json

```json
[
  {
    "a": "ETH Zurich",
    "b": "University of Zurich",
    "reason": "Different institutions in Zurich."
  },
  {
    "a": "The University of Queensland",
    "b": "Queensland University of Technology",
    "reason": "Different Australian universities."
  },
  {
    "a": "University of Washington",
    "b": "Washington University in St. Louis",
    "reason": "Different US universities."
  },
  {
    "a": "ShanghaiTech University",
    "b": "Shanghai University",
    "reason": "Different Chinese universities."
  },
  {
    "a": "Zhejiang University",
    "b": "Zhejiang University of Technology",
    "reason": "Different Chinese universities."
  },
  {
    "a": "Zhejiang University",
    "b": "Zhejiang Sci-Tech University",
    "reason": "Different Chinese universities."
  },
  {
    "a": "University of California",
    "b": "UC Berkeley",
    "reason": "System-level name should not be automatically mapped to a specific campus."
  },
  {
    "a": "University of California",
    "b": "UC San Diego",
    "reason": "System-level name should not be automatically mapped to a specific campus."
  },
  {
    "a": "University of California",
    "b": "UCLA",
    "reason": "System-level name should not be automatically mapped to a specific campus."
  },
  {
    "a": "HKUST",
    "b": "HKUST Guangzhou",
    "reason": "Same university brand but potentially different campus/entity."
  },
  {
    "a": "CUHK",
    "b": "CUHK Shenzhen",
    "reason": "Same university brand but potentially different campus/entity."
  },
  {
    "a": "Northeastern University",
    "b": "Northeastern University, China",
    "reason": "Potentially different institutions; requires manual verification."
  },
  {
    "a": "Northwestern University",
    "b": "Northwestern Polytechnical University",
    "reason": "Different institutions in different countries."
  },
  {
    "a": "University of Technology Sydney",
    "b": "Singapore University of Technology and Design",
    "reason": "Different institutions."
  },
  {
    "a": "Technical University of Munich",
    "b": "LMU Munich",
    "reason": "Different Munich universities."
  },
  {
    "a": "Vrije Universiteit Brussel",
    "b": "Vrije Universiteit Amsterdam",
    "reason": "Different institutions in different countries."
  },
  {
    "a": "University of Electronic Science and Technology of China",
    "b": "University of Science and Technology of China",
    "reason": "Different Chinese universities."
  },
  {
    "a": "Beijing Institute of Technology",
    "b": "Beijing University of Technology",
    "reason": "Different Chinese universities."
  },
  {
    "a": "South China University of Technology",
    "b": "South China Normal University",
    "reason": "Different Chinese universities."
  },
  {
    "a": "University of York",
    "b": "York University",
    "reason": "Different possible institutions depending on country/context."
  },
  {
    "a": "University of Oxford",
    "b": "Oxford Brookes University",
    "reason": "Different UK universities despite shared city name."
  },
  {
    "a": "MIT",
    "b": "Mitsubishi Electric Research Laboratories",
    "reason": "Substring MIT appears inside unrelated institution/company names."
  },
  {
    "a": "University of California",
    "b": "University of California, Merced",
    "reason": "System-level name should not be automatically mapped to a specific campus."
  }
]
```

## 10. Implementation Guideline

Use this order: Unicode NFKC normalization -> whitespace and punctuation normalization -> exact multimap lookup -> exact alias lookup -> suspicious separator detection -> canonical institution name(s) -> canonical institution country lookup -> fallback country hints -> manual review log.

Do not split commas, slashes, ampersands, semicolons, `and`, or `with` automatically. Split only when the exact raw string is in `aff_institution_multimap.json`.

## 11. Suggested Tests

- `ETH Zürich -> ETH Zurich`
- `ETH Zurich, Robotic Systems Lab -> ETH Zurich`
- `University of Zurich -> University of Zurich`
- `Bonn University -> University of Bonn`
- `Technical University of Munich (TUM) -> Technical University of Munich`
- `TUM -> Technical University of Munich`
- `Korea Advanced Institute of Science and Technology (KAIST) -> KAIST`
- `Daegu Gyeongbuk Institute of Science and Technology(DGIST) -> DGIST`
- `NASA-JPL, Caltech -> NASA Jet Propulsion Laboratory + Caltech`
- `University of California, Berkeley -> UC Berkeley`
- `University of Michigan, Ann Arbor -> University of Michigan`
- `Washington University in St. Louis` remains unchanged.
- `Shanghai Jiaotong University -> Shanghai Jiao Tong University`
- `Institute of Automation，Chinese Academy of Sciences -> CASIA`
- `NanyangTechnological University -> Nanyang Technological University`

## 12. Remaining Risks

1. Some affiliation strings are compound affiliations and require an explicit split policy.
2. Some company labs can be counted either at lab level or parent-company level.
3. Some campuses can be counted separately or merged into university-system-level entities.
4. Inverted names such as `Bonn University` are handled only by explicit alias mapping.
5. Comma-containing strings are not split automatically.
6. Ambiguous strings are logged instead of silently normalized.
