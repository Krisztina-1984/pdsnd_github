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
    while True:
        print('From which city would you like to see data? chicago, new york city, washington')
        city= input().lower()
        if city == 'chicago' or 'new york city' or 'new_york_city' or 'new york' or 'washington':
            break
    # TO DO: get user input for month (all, january, february, ... , june)
    print('From which month would you like to see data? \n Please enter january, february, march, april, may, june; \n if you do not want to select a filter please type all')
    month = input().lower()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('For what day are you intersted? Please give in monday, tuesday, wednesday, thursday, friday, saturday, or sunday \n if you do not want to select a filter please type all')
    day = input().lower()
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
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] =  df['Start Time'].dt.dayofweek

     # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        days_of_week = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day = days_of_week.index(day)
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    popular_month = df['month'].mode()[0]
    if popular_month == 1:
        print('Most popular month: January')
    elif popular_month == 2:
        print('Most popular month: February')
    elif popular_month == 3:
        print('Most popular month: March')
    elif popular_month == 4:
        print('Most popular month: April')
    elif popular_month == 5:
        print('Most popular month: May')
    elif popular_month == 6:
        print('Most popular month: June')

    # display the most common day of week
    popular_day = df['day'].mode()[0]
    if popular_day == 0:
        print('Most popular day of the week: Monday')
    elif popular_day == 1:
        print('Most popular day of the week: Tuesday')
    elif popular_day == 2:
        print('Most popular day of the week: Wednesday')
    elif popular_day == 3:
        print('Most popular day of the week: Thursday')
    elif popular_day == 4:
        print('Most popular day of the week: Friday')
    elif popular_day == 5:
        print('Most popular day of the week: Saturday')
    elif popular_day == 6:
        print('Most popular day of the week: Sunday')

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular start hour:', popular_hour, 'h')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    route = df['Start Station'] + df['End Station']
    popular_route = route.mode()[0]
    print('Most popular combination of start and end stations:', popular_route)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_trip_dur = df['Trip Duration'].sum()
    print('The total trip duration is:', tot_trip_dur/60, 'hours')

    # display mean travel time
    mean_trip_dur = df['Trip Duration'].mean()
    print('The average trip duration is:', mean_trip_dur, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The counts of user types:\n', user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('The count of male/female customers:\n', gender)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        birth_year_of_customer = df['Birth Year']
        print('The youngest customer was born in:', df['Birth Year'].max())
        print('The oldest customer was born in:', df['Birth Year'].min())
        print('The most customers  were born in:', df['Birth Year'].mode()[0])
        typical_age = (2017 - birth_year_of_customer).mode()[0]
        print('The common age of the customers:', typical_age)
        missing_data = birth_year_of_customer.isnull().sum().sum()
        print('There is no birth data from:', missing_data, 'customers')
        false_data_counter=0
        for year in birth_year_of_customer:
            if year < 1930.0:
                false_data_counter+=1
        print('There are:', false_data_counter, 'possibly irrealistic birth years')

def view_data(city, month, day):
    """Presents consecutive five lines of the original data."""

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] =  df['Start Time'].dt.dayofweek
    print('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    present_data = input().lower()
    start_loc=0
    while present_data != 'no':
        print(df.iloc[start_loc:(start_loc+5)])
        start_loc +=5
        print('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
        present_data = input().lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(city, month, day)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' or 'ye':
            break


if __name__ == "__main__":
    main()
