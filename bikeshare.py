import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city
    while True:
        city = input("Enter city: ") # Get string input from user
        city = city.lower() # Change the user input characters to lowercase
        if city in CITY_DATA.keys():
            break
        else:
            print("type one of \'chicago\', \'new york city\', \'washington\'")
    
    # get user input for month
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Enter month: ") # Get string input from user
        month = month.lower() # Change the user input characters to lowercase
        if month in months:
            break
        else:
            print("type one of \'all\', \'january\', \'february\', \'march\', \'april\', \'may\', \'june\'")

    # get user input for day of week
    days = ['all', 'monday', 'tuesday', 'wendsday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Enter day: ") # Get string input from user
        day = day.lower() # Change the user input characters to lowercase
        if day in days:
            break
        else:
            print("type one of \'all\', \'monday\', \'tuesday\', \'wendsday\', \'thursday\', \'friday\', \'saturday\', \'sunday\'")      
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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load datafile into dataframe
    df = pd.read_csv(CITY_DATA[city])

    data_length = df.shape[0] # total data number
    index = 1 # index for showing the data
    break_flag = False # Flag for exciting nested for loop
    
    # Check whether the user want to check the raw data
    while True:
        if break_flag == True:
            break
        
        print("Would you like to see the raw data? Yes, No")
        view_raw_data = input("See the raw data: ") # Get string input from user
        view_raw_data = view_raw_data.lower() # Change the user input characters to lowercase
        
        # User input is yes
        if view_raw_data == "yes":
            print(df[index:].head()) # print the 5 rows of the raw data
            index += 5 # Increase the index for next iteration
            
             # Check whether the user want to check the raw data
            while True:
                print("Would you like to see next raw data? Yes, No")
                view_raw_data = input("See the next raw data: ")
                view_raw_data = view_raw_data.lower()  # Get string input from user

                # User input is yes
                if view_raw_data == "yes": 
                    print(df[index:].head())
                    if index + 5 <= data_length:
                        index += 5
                    else:
                        print("It is last line of data")
                # User input is no
                elif view_raw_data == "no":
                    break_flag = True
                    break
                # Wrong input
                else:
                    print("Please type one of \'Yes\' or \'No\'")
        # If the user input is no
        elif view_raw_data == "no":
            break
        # Wrong input
        else:
            print("Please type one of \'Yes\' or \'No\'")
    
    # Convert 'Start Time' column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract the month, day from the 'Start Time' to create a new column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by month if applicable
    if month != 'all':
        # Get corresponding int using index of month list
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create a new dataframe
        df = df[df['month'] == month]

    # Filter by day of the week, if applicable
    if day != 'all':
        # Create a new dataframe by filtering by day of the week
        df = df[df['day_of_week'] == day.title()]

    return df


def display_data(title, data):
    """Displays the data with title."""
    print('*'*40)
    print(title)
    print(data)
    print('*'*40)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    display_data("most_common_month", most_common_month)

    # display the most common day of week
    most_day_of_week = df['day_of_week'].mode()[0]
    display_data("most_day_of_week", most_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_hour = df['hour'].mode()[0]
    display_data("most_hour", most_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    display_data("most_start_station", most_start_station)

    # display most commonly used end station
    most_end_station = df['End Station'].mode()[0]
    display_data("most_end_station", most_end_station)

    # display most frequent combination of start station and end station trip
    most_start_end_station = df.groupby(['Start Station','End Station']).size().idxmax()
    display_data("most_start_end_station", most_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_duration_sum = df['Trip Duration'].sum()
    display_data("trip_duration_sum", trip_duration_sum)

    # display mean travel time
    trip_duration_mean = trip_duration_sum / df.shape[0]
    display_data("trip_duration_mean", trip_duration_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df['User Type'].value_counts()
    display_data("count_user_type", count_user_type)

    # Display counts of gender
    try:
        count_gender = df['Gender'].value_counts()
        display_data("count_gender", count_gender)
    except:
        print("No \'Gender\' data in this data")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = int(df['Birth Year'].min())
        latest_birth = int(df['Birth Year'].max())
        common_birth = int(df['Birth Year'].mode()[0])
        display_data("earliest_birth", earliest_birth)
        display_data("latest_birth", latest_birth)
        display_data("common_birth", common_birth)
    except:
        print("No \'Birth Year\' data in this data")    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    # Run applicaiton until user stop it.
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
