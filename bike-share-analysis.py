import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Introduction:
# This script analyzes bike share data from different cities, specifically Chicago, New York City, and Washington.
# It loads data, cleans it, calculates statistics, and generates visualizations.
def load_data(city):
    """Load data from CSV file based on city name."""
    city = city.lower().replace(" ", "_")
    file_path = f"{city}.csv"
    logging.info(f"Loading data for {city}")
    try:
        df = pd.read_csv(file_path)
        logging.info("Data loaded successfully")
        return df
    except FileNotFoundError:
        logging.error("File not found. Please check the file path.")
        return None

def clean_data(df):
    """Clean data by handling missing values and filtering data."""
    logging.info("Cleaning data")
    df.dropna(inplace=True)
    df = df[df['Trip Duration'] > 0]  # Filtering invalid trip durations
    return df
def get_filters():
    """Get user input for city, month, and day with error handling."""
    cities = ['chicago', 'new york city', 'washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    
    while True:
        city = input("Enter the city (Chicago, New York City, Washington): ").strip().lower()
        if city in cities:
            break
        print("Invalid city. Please enter a valid city name.")
    
    while True:
        month = input("Enter the month (January to June) or 'all': ").strip().lower()
        if month in months:
            break
        print("Invalid month. Please enter a valid month name.")
    
    while True:
        day = input("Enter the day (Monday to Sunday) or 'all': ").strip().lower()
        if day in days:
            break
        print("Invalid day. Please enter a valid day name.")
    
    return city, month, day
def filter_data(df, month, day):
    """Filter the data by month and day if applicable."""
    if month != 'all':
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df = df[df['Start Time'].dt.month_name().str.lower() == month]
    if day != 'all':
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df = df[df['Start Time'].dt.day_name().str.lower() == day]
    return df

def display_raw_data(df):
    """Ask the user if they want to see raw data and display it in chunks of 5 rows."""
    row_index = 0
    while True:
        show_data = input("Would you like to see 5 rows of raw data? Enter yes or no: ").strip().lower()
        if show_data != 'yes':
            break
        print(df.iloc[row_index: row_index + 5])
        row_index += 5
        if row_index >= len(df):
            print("No more data to display.")
            break
def time_stats(df):
    """Calculate and display the most common month, day, and hour."""
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    common_month = df['Start Time'].dt.month_name().mode()[0]
    common_day = df['Start Time'].dt.day_name().mode()[0]
    common_hour = df['Start Time'].dt.hour.mode()[0]
    print(f"Most Common Month: {common_month}")
    print(f"Most Common Day: {common_day}")
    print(f"Most Common Hour: {common_hour}")
    
    # Visualization for Time Stats
    df['month'] = df['Start Time'].dt.month_name()
    df['hour'] = df['Start Time'].dt.hour

    # Monthly trip distribution
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='month', order=['January', 'February', 'March', 'April', 'May', 'June'])
    plt.title('Number of Trips per Month')
    plt.xlabel('Month')
    plt.ylabel('Number of Trips')
    plt.xticks(rotation=45)
    plt.show()

    # Hourly trip distribution
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='hour')
    plt.title('Number of Trips per Hour')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Trips')
    plt.show()

def station_stats(df):
    """Calculate and display station statistics."""
    common_start_station = df['Start Station'].mode()[0]
    common_end_station = df['End Station'].mode()[0]
    df['Route'] = df['Start Station'] + " -> " + df['End Station']
    common_route = df['Route'].mode()[0]
    print(f"Most Common Start Station: {common_start_station}")
    print(f"Most Common End Station: {common_end_station}")
    print(f"Most Common Trip: {common_route}")
    
    # Visualization for Station Stats
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Start Station', order=df['Start Station'].value_counts().index[:10])
    plt.title('Top 10 Most Common Start Stations')
    plt.xlabel('Start Station')
    plt.ylabel('Number of Trips')
    plt.xticks(rotation=45)
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='End Station', order=df['End Station'].value_counts().index[:10])
    plt.title('Top 10 Most Common End Stations')
    plt.xlabel('End Station')
    plt.ylabel('Number of Trips')
    plt.xticks(rotation=45)
    plt.show()

def trip_duration_stats(df):
    """Calculate trip duration statistics."""
    total_duration = df['Trip Duration'].sum()
    mean_duration = df['Trip Duration'].mean()
    print(f"Total Trip Duration: {total_duration}")
    print(f"Average Trip Duration: {mean_duration}")
    
    # Visualization for Trip Duration
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Trip Duration'], kde=True, color='blue', bins=50)
    plt.title('Trip Duration Distribution')
    plt.xlabel('Trip Duration (Seconds)')
    plt.ylabel('Frequency')
    plt.show()

def user_stats(df):
    """Display user statistics including User Types, Gender, and Birth Year."""
    print("User Type Counts:")
    print(df['User Type'].value_counts())
    
    # Visualization for User Type
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='User Type')
    plt.title('User Type Distribution')
    plt.xlabel('User Type')
    plt.ylabel('Number of Users')
    plt.show()
    
    if 'Gender' in df.columns:
        print("Gender Counts:")
        print(df['Gender'].value_counts())
        
        # Visualization for Gender
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df, x='Gender')
        plt.title('Gender Distribution')
        plt.xlabel('Gender')
        plt.ylabel('Number of Users')
        plt.show()
        
    if 'Birth Year' in df.columns:
        print(f"Earliest Birth Year: {int(df['Birth Year'].min())}")
        print(f"Most Recent Birth Year: {int(df['Birth Year'].max())}")
        print(f"Most Common Birth Year: {int(df['Birth Year'].mode()[0])}")
def main():
    """Main function to run the analysis script."""
    city, month, day = get_filters()
    df = load_data(city)
    if df is not None:
        df = clean_data(df)
        df = filter_data(df, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
    else:
        print("Failed to load data.")

if __name__ == "__main__":
    main()
