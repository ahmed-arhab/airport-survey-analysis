
from graphics import *
import csv
import math

data_list = []   # data_list An empty list to load and hold data from csv file

def load_csv(CSV_chosen):
    """
    This function loads any csv file by name (set by the variable 'selected_data_file') into the list "data_list"
    YOU DO NOT NEED TO CHANGE THIS BLOCK OF CODE
    """
    with open(CSV_chosen, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            data_list.append(row)

# Dictationary

air_port= {
        "LHR":"London heathrow",
        "MAD":"Madrid adolfo Suarez-Barajas",
        "CDG":"Charles De Gaulle International",
        "IST":"Istanbul Airport International",
        "AMS":"Amasterdam Schiphol",
        "LIS":"Lisbon Portela",
        "FRA":"Frankfurt Main",
        "FCO":"Rome Fiumicino",
        "MUC":"Munich International",
        "BCN":"Barcelona International"
        }

code_of_air_lines={
                    "BA":"British Airways",
                    "AF":"Air France",
                    "AY":"Finnair",
                    "KL":"KLM",
                    "SK":"Scandinavian Airlines",
                    "TP":"TAP Air Portugal",
                    "TK":"Turkish Airlines",
                    "U2":"easy Jet",
                    "FR":"Ryanair",
                    "A3":"Aegean Airlines",
                    "SN":"Brussels Airlines",
                    "EK":"Emirates",
                    "QR":"Qatar Airways",
                    "IB":"Iberia",
                    "LH":"Lufthansa"
                    }
def get_airport():
    
    display_1="please enter the three-letter city code: "
    while True:
        code_of_airport=input(display_1).upper()
        if code_of_airport not in air_port:
            display_1="unavilable city code - please enter a valid city code: "
            continue
    
        elif len(code_of_airport)!=3:
            display_1="wrong code length - please enter a three-letter city code: "
            continue
        return code_of_airport
    
def get_year():
    
    display_2="please enter the year required in the format yyyy: "
    while True:
        year=input(display_2).strip()       #I am using 'strip' here for merging elements If accidently typing space between the integers 

        if not  year.isdigit() or len(year)!=4 :    #assigning length of year and [year format should be integer'.isdidgit()']
            display_2 = "wrong data type-please enter a four-digit year: "
            continue
        
        
        if not (2000<=(int(year))<=2025):           #assigning range of year between 2000 & 2025
            display_2="out of range-please enter a value from 2000 to 2025"
            continue
        return year
    

def selecting_file(year,airport_code):


    selected_data_file = airport_code + str(year) + ".csv"

    head=f"{selected_data_file} selected - Planes departing {air_port[airport_code]} {year}"
    print("*"*len(head))
    print(head)
    print("*"*len(head))
    load_csv(selected_data_file)
    return head


# Determine Data


def determine_data():
    task_b={}          
    # Total number of departure flights
    total_of_flights = len(data_list)
    print(f"the total number of flights from this airport was {total_of_flights}")
    task_b["total_of_flights"]=total_of_flights

    # Total number of flights departing from Terminal 2
    count_of_terminal_2 = 0
    for terminal_2 in data_list:
        if terminal_2[8] == "2":
            count_of_terminal_2 += 1
    print(f"the total number of flights departing terminal two was {count_of_terminal_2}")
    task_b["count_of_terminal_2"]=count_of_terminal_2

    # Total number of departures of flights that are under 600 miles
    under_600_miles=0
    for miles in data_list:
        if int(miles[5])<600:
            under_600_miles+=1
    print(f"the total number of flights under 600 miles was {under_600_miles}")
    task_b["under_600_miles"]=under_600_miles

    # Total number of departure flights by Air France aircraft
    air_france=0
    for AF_dptr in data_list:
        if AF_dptr [1][0]=="A" and AF_dptr [1][1]=="F":
            air_france += 1
    print(f"there were {air_france} air france flights from this airport")
    task_b["air_france"]=air_france

    # Total number of flights departing in temperatures below 15°C
    temp_below_15=0
    for temp in data_list:
        temp_list=temp[10].split("°")       # '.split("_")' for spliting the elements with '°' for calculation  
        if (temp_list[0])<"15":
            temp_below_15+=1
    print(f"there were {temp_below_15} flights departing in temperature below 15 degrees")
    task_b["temp_below_15"]=temp_below_15

    # Average number of British Airways departures per hour
    flights_of_BA=0
    for BA_dptr in data_list:
        if BA_dptr [1][0]=="B" and BA_dptr [1][1]=="A":
            flights_of_BA += 1
    british_airways_avg_per_hr=round(flights_of_BA/12,2)
    print(f"there was an average of {british_airways_avg_per_hr} british airways flights per hour from this airport")
    task_b["british_airways_avg_per_hr"]=british_airways_avg_per_hr

    # Percentage of total departures that are British Airways aircraft
    percentage_of_BA=round((flights_of_BA/total_of_flights)*100,2)
    print(f"british airways planes made up {percentage_of_BA} % of all departures")
    task_b["percentage_of_BA"]=percentage_of_BA

    # Percentage of Air France flights with a delayed departure
    airfrance_delay_flight=0
    for AF_delay_dptr in data_list:
        if AF_delay_dptr [1][0]=="A" and AF_delay_dptr [1][1]=="F":   
            if AF_delay_dptr[2] < AF_delay_dptr[3]:
                airfrance_delay_flight += 1
    airfrance_delay_flight_percentage=round((airfrance_delay_flight/total_of_flights)*100,2)       
    print(f"{airfrance_delay_flight_percentage} % of Air France departures were delayed")
    task_b["airfrance_delay_flight_percentage"]=airfrance_delay_flight_percentage

    # Total number of hours of rain in the twelve hours
    rainy_hours=set()
    for weather in data_list:
        if "rain" in weather[10]:
            hours=(weather[2].split(":")[0])
            hours=int(hours)
            rainy_hours.add(hours)
    length_of_rainy_hours=len(rainy_hours)
    print(f"There were {length_of_rainy_hours} hours in which rain fell")
    task_b["length_of_rainy_hours"]=length_of_rainy_hours

    # Full name of the least common destination
    count_of_destination={}
    for least_distination in data_list:
        destination=least_distination[4]
        if destination in count_of_destination:
            count_of_destination[destination] += 1
        else:
            count_of_destination[destination] = 1
    least_common_destination = min(count_of_destination, key=lambda l:count_of_destination[l])
    least_common_destination_2=[(air_port.get(least_common_destination))]
    print(f"the least common destination are {least_common_destination_2}")
    task_b["least_common_destination_2"]=least_common_destination_2

    return task_b


# File Handling


def text(airport_code, year, head, task_b):
    # This creates a file named 'report.html' instead of 'results.txt'
    filename = "report.html"
    
    with open(filename, "w") as file:
        # We are writing HTML code into the file
        file.write(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Airport Data Report</title>
            <link rel="stylesheet" type="text/css" href="style.css">
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Airport Analysis Results</h1>
                </div>
                <div class="sub-header">
                    {head}
                </div>
                
                <div class="content">
                    <div class="row">
                        <span class="label">Total Flights:</span>
                        <span class="value">{task_b["total_of_flights"]}</span>
                    </div>
                    <div class="row">
                        <span class="label">Flights from Terminal 2:</span>
                        <span class="value">{task_b["count_of_terminal_2"]}</span>
                    </div>
                    <div class="row">
                        <span class="label">Flights < 600 miles:</span>
                        <span class="value">{task_b["under_600_miles"]}</span>
                    </div>
                    <div class="row">
                        <span class="label">Air France Flights:</span>
                        <span class="value">{task_b["air_france"]}</span>
                    </div>
                    <div class="row">
                        <span class="label">Flights below 15°C:</span>
                        <span class="value">{task_b["temp_below_15"]}</span>
                    </div>
                    <div class="row">
                        <span class="label">Avg BA Flights/Hour:</span>
                        <span class="value">{task_b["british_airways_avg_per_hr"]}</span>
                    </div>
                    <div class="row">
                        <span class="label">British Airways %:</span>
                        <span class="value">{task_b["percentage_of_BA"]}%</span>
                    </div>
                    <div class="row">
                        <span class="label">Air France Delayed %:</span>
                        <span class="value">{task_b["airfrance_delay_flight_percentage"]}%</span>
                    </div>
                    <div class="row">
                        <span class="label">Rainy Hours:</span>
                        <span class="value">{task_b["length_of_rainy_hours"]}</span>
                    </div>
                    <div class="row">
                        <span class="label">Least Common Dest:</span>
                        <span class="value">{task_b["least_common_destination_2"][0]}</span>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """)
    print(f"Report generated successfully: {filename}")

        

# Histogram


def graph(code,year):
    while True:
        airline_histogram = input("Enter a two-character Airline code to plot a histogram: ").upper()
        if len(airline_histogram) != 2:
            print("Airline code should be 2 letters")

        if airline_histogram not in code_of_air_lines :
            print("Unavailable Airline code. Please Try Again")

        else: 
            break

    hour_counts={hour:0 for hour in range(12)}          
    for flight in data_list:
        if airline_histogram in flight[1]:
            
                hour=int(flight[2].split(':')[0])
                hour_counts[hour]+= 1


    # "window = GraphWin(..)"This line creates a new pop-up window
    # it will create window as 900 pixel wide & 900 pixel tall       
    window = GraphWin("Histogram", 900, 900)

    # This line changes the background color of the window 
    window.setBackground("#f0f2f5") # Matches CSS background 

    # I assign that each bar in your chart will be 25 pixels tall
    bar_thickness=25
    # 20-pixel gap between each bar
    gap=20
    maximum_count=max(hour_counts.values()) 

    # It's a scaling factor
    # Here, I have decided I want my longest bar to be 500 pixels wide  
    scale_factor = 500 / maximum_count

    
    for hour, count in hour_counts.items():
        #This is the top edge of the bar
        y_axis1 = hour * (bar_thickness + gap) + 50
        #This is the top edge of the bar
        y_axis2 = y_axis1 + bar_thickness
        #This is the left edge of the bar
        x_axis1 = 150
        #This is the right edge of the bar
        x_axis2 = 150 + (count * scale_factor)


        #bar = Rectangle(...): This defines a new rectangle using 
        #using its top-left corner (Point(x_axis1, y_axis1)) and its bottom-right corner (Point(x_axis2, y_axis2))
        bar = Rectangle (Point(x_axis1, y_axis1), Point(x_axis2, y_axis2))
        #This sets the bar's color to black ("#000000")
        bar.setFill("#3498db")  # Matches CSS Blue
        bar.setOutline("#2c3e50") # Dark border
        #This command makes the bar actually appear
        bar.draw(window)
        #This creates the hour label (bar_space = Text(.....))
        #This formats the hour variable. :02d means "make it 2 digits"
        bar_space = Text(Point(135, (y_axis1 + y_axis2) / 2), f"{hour:02d}")
        bar_space.draw(window)

        #creates the flight count label (count_text = Text(.....))
        count_text = Text(Point(x_axis2 + 12, (y_axis1 + y_axis2) / 2), str(count))
        count_text.draw(window)

    y_axis = Line(Point(150, 50), Point(150, 27 + 12 * (bar_thickness + gap)))
    y_axis.setWidth(1)
    y_axis.draw(window)

    title = Text(Point(400, 20), f"Departures by hour for {code_of_air_lines[airline_histogram]} from {code} {year}")
    title.setSize(18)
    title.setTextColor("#2c3e50") # Dark Blue Text
    title.setStyle("bold")
    title.draw(window)

    subtitle = Text(Point(65, 315), f"HOURS\n\n 00:00\n to\n 12:00\n")
    subtitle.setSize(14)
    subtitle.draw(window)

    window.getMouse()   # window will be appearing until Click the mouse
    window.close()      # As soon as click the mouse, window will close



# ending part


def ask_again():
    while True:
        again=input("do you want to select a new data file?Y/N:").upper()
        if again=="Y":
            data_list.clear()
            break
        elif again=="N":
            print("THANK YOU\nEND OF RUN!")
            exit()
        else:
            print("invalid input.please enter Y or N.")


def main():
    while True:
        code=get_airport()
        year=get_year()
        head=selecting_file(year,code)
        output_of_task_b=determine_data()
        text(code,year,head,output_of_task_b)
        graph(code,year)
        ask_again()

if __name__ == "__main__":
    main()