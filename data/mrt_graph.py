# MRT station lists for each line

north_south_line = [
"Jurong East","Bukit Batok","Bukit Gombak","Choa Chu Kang",
"Yew Tee","Kranji","Marsiling","Woodlands","Admiralty",
"Sembawang","Canberra","Yishun","Khatib","Yio Chu Kang",
"Ang Mo Kio","Bishan","Braddell","Toa Payoh","Novena",
"Newton","Orchard","Somerset","Dhoby Ghaut","City Hall",
"Raffles Place","Marina Bay","Marina South Pier"
]

east_west_line = [
"Pasir Ris","Tampines","Simei","Tanah Merah","Bedok",
"Kembangan","Eunos","Paya Lebar","Aljunied","Kallang",
"Lavender","Bugis","City Hall","Raffles Place",
"Tanjong Pagar","Outram Park","Tiong Bahru","Redhill",
"Queenstown","Commonwealth","Buona Vista","Dover",
"Clementi","Jurong East","Chinese Garden","Lakeside",
"Boon Lay","Pioneer","Joo Koon","Gul Circle",
"Tuas Crescent","Tuas West Road","Tuas Link"
]

north_east_line = [
"HarbourFront","Outram Park","Chinatown","Clarke Quay",
"Dhoby Ghaut","Little India","Farrer Park","Boon Keng",
"Potong Pasir","Woodleigh","Serangoon","Kovan",
"Hougang","Buangkok","Sengkang","Punggol"
]

circle_line = [
"Dhoby Ghaut","Bras Basah","Esplanade","Promenade",
"Nicoll Highway","Stadium","Mountbatten","Dakota",
"Paya Lebar","MacPherson","Tai Seng","Bartley",
"Serangoon","Lorong Chuan","Bishan","Marymount",
"Caldecott","Botanic Gardens","Farrer Road",
"Holland Village","Buona Vista","one-north",
"Kent Ridge","Haw Par Villa","Pasir Panjang",
"Labrador Park","Telok Blangah","HarbourFront"
]

downtown_line = [
"Bukit Panjang","Cashew","Hillview","Hume",
"Beauty World","King Albert Park","Sixth Avenue",
"Tan Kah Kee","Botanic Gardens","Stevens","Newton",
"Little India","Rochor","Bugis","Promenade",
"Bayfront","Downtown","Telok Ayer","Chinatown",
"Fort Canning","Bencoolen","Jalan Besar",
"Bendemeer","Geylang Bahru","Mattar","MacPherson",
"Ubi","Kaki Bukit","Bedok North","Bedok Reservoir",
"Tampines West","Tampines","Tampines East",
"Upper Changi","Expo"
]

thomson_east_coast_line = [
"Woodlands North","Woodlands","Woodlands South","Springleaf",
"Lentor","Mayflower","Bright Hill","Upper Thomson",
"Caldecott","Stevens","Napier","Orchard Boulevard",
"Orchard","Great World","Havelock","Outram Park",
"Maxwell","Shenton Way","Marina Bay",
"Gardens by the Bay","Tanjong Rhu","Katong Park",
"Tanjong Katong","Marine Parade","Marine Terrace",
"Siglap","Bayshore","Bedok South","Sungei Bedok"
]

def add_line(graph, stations, weight=2):
    for i in range(len(stations)-1):

        a = stations[i]
        b = stations[i+1]

        if a not in graph:
            graph[a] = {}
        if b not in graph:
            graph[b] = {}

        graph[a][b] = weight
        graph[b][a] = weight

# Initialize the graph
graph = {}

# Add all lines to the graph
add_line(graph, north_south_line)
add_line(graph, east_west_line)
add_line(graph, north_east_line)
add_line(graph, circle_line)
add_line(graph, downtown_line)
add_line(graph, thomson_east_coast_line)