import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO:get user input for city (chicago,new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while True:
        city=city.casefold()
        if city == 'Chicago'.casefold() or city == 'Washington'.casefold() or city == 'New York'.casefold():
            break
        else:
            city = input("Would you like to see data for Chicago, New York or Washington??   ")

    choice = ''
    while True:
        choice = choice.casefold()
        if choice == 'month'.casefold() or choice == 'day'.casefold() or choice == 'both'.casefold() or choice == 'none'.casefold():
            break
        else:
            choice = input('Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.')

    # TO DO: get user input for month ( january, february, ... , june)
    month = 'none'
    if choice == 'both' or choice == 'month':
        while True:
            month = month.casefold()
            if (month == 'January'.casefold() or month == 'Febreuary'.casefold() or month == 'March'.casefold() or month == 'April'.casefold() or month == 'May'.casefold() or month == 'June'.casefold()):
                break
            else:
                month = input('"Which month do you want to filter data using it??"January,Febreuary,March,April,May,or June    ""')

    DAY_LIST = ['monday'.casefold(), 'tuesday'.casefold(), 'wednesday'.casefold(), 'thursday'.casefold(), 'friday'.casefold(), 'saturday'.casefold(), 'sunday'.casefold()]

    day=''
    # TO DO: get user input for day of week (monday, tuesday, ... sunday)
    if (choice == 'both' or choice == 'day'):
        while True:
            day = input(
                "\nAre you looking for a particular day? If so, kindly enter the day as follows: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday ?\n")
            if day.casefold() not in DAY_LIST:
                print("Sorry, I didn't catch that. Try again.")
                continue
            else:
                break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        frame - Pandas DataFrame containing city data filtered by month and day
    """
    frame = pd.read_csv(CITY_DATA[city])
	# convert the Start Time column to datetime
    frame['Start Time'] = pd.to_datetime(frame['Start Time'])
    frame['End Time'] = pd.to_datetime(frame['End Time'])

    # Making a new hour column.
    frame['Hour'] = frame['Start Time'].dt.hour

    # extract month and day of week from Start Time to create new columns
    frame['month'] = frame['Start Time'].dt.month
    frame['day_of_week'] = frame['Start Time'].dt.weekday_name

    # filter by month
    if month != 'none':
        # use the index of the months list to get the corresponding int
        months = ['january', 'febreuary', 'march', 'april', 'may', 'june']
        ind_mon = months.index(month) + 1
        frame = frame[frame['month'] == ind_mon]

    # filter by day of week if applicable
    if day != '':
        # filter by day of week to create the new dataframe
        frame = frame[frame['day_of_week'] == day.title()]

    return frame


def time_stats(frame,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if month != 'none':
        # display the most common month
        print('Most common month: ', frame['month'].value_counts().index[0])
    if day !='':
        # display the most common day of week
        print('Most common day of week: ', frame['day_of_week'].value_counts().index[0])

        # display the most common start hour
        print('Most common start hour: ',frame['Hour'].value_counts().index[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(frame):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most common start station: ', frame['Start Station'].value_counts().index[0])

    # TO DO: display most commonly used end station
   
    print('Most common end station: ', frame['End Station'].value_counts().index[0])

    # TO DO: display most frequent combination of start station and end station trip
    print(pd.DataFrame(frame.groupby(['Start Station','End Station']).size().sort_values(ascending=False)).iloc[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(frame):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time: ', frame['Trip Duration'].sum())

    # TO DO: display mean travel time
    print('Total travel time: ', frame['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(frame,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Counts of user Types: ",frame['User Type'].value_counts())
    # TO DO: Display counts of gender
    if(city == 'Chicago'.casefold() or city == 'New york'.casefold()):
           print('Counts of gender: ', frame['Gender'].value_counts())
           # TO DO: Display earliest, most recent, and most common year of birth
           print('Most earliest year of birth: ', frame['Birth Year'].sort_values().iloc[0])
           print('Most recent year of birth: ', frame['Birth Year'].sort_values(ascending = False).iloc[0])
           print('Most common year of birth', frame['Birth Year'].value_counts().index[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Function to display the data frame itself as per user request
def display_data(frame):
    """Displays 5 rows of data from the csv file for the selected city.

    Args:
        param1 (frame): The data frame you wish to work with.

    Returns:
        None.
    """
    BIN_RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    #counter variable is initialized as a tag to ensure only details from
    #a particular point is displayed
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        print("\nDo you wish to view the raw data?")
        print("\nAccepted responses:\nYes or yes\nNo or no")
        rdata = input().lower()
        #the raw data from the frame is displayed if user opts for it
        if rdata == "yes":
            print(frame.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print("\nPlease check your input.")
            print("Input does not seem to match any of the accepted responses.")
            print("\nRestarting...\n")

    #Extra while loop here to ask user if they want to continue viewing data
    while rdata == 'yes':
        print("Do you wish to view more raw data?")
        counter += 5
        rdata = input().lower()
        #If user opts for it, this displays next 5 rows of data
        if rdata == "yes":
             print(frame[counter:counter+5])
        elif rdata != "yes":
             break

    print('-'*80)


def main():
    while True:
        city, month, day = get_filters()
        frame = load_data(city, month, day)


        time_stats(frame,month,day)
        station_stats(frame)
        trip_duration_stats(frame)
        user_stats(frame, city)
        display_data(frame)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.casefold() not in 'yes':
            print("Thanks for using our program")
            break



if __name__ == "__main__":
    main()
