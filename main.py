import pandas as pd 
import sys
import matplotlib
matplotlib.use('Agg')
import io
import matplotlib.pyplot as plt4
from health import Health
import os
import requests

def main():
  health_file_path = "health.csv" #Set the csv file as a variable
  clear_csv_file(health_file_path) #Reset the current csv file to its initial state
  directory = "."  # Delete PNG files in the current directory
  delete_png_files(directory)

  # Start a loop to collect data
  while True:
    health = get_user_health()

    save_health_to_file(health, health_file_path)

    df = pd.read_csv("health.csv", index_col=False)

    print(df) 

    # Plot the DataFrame
    df.plot(kind='scatter', x='day', y='steps') #Graphs the data
    plt4.savefig('steps_plot.png') # Save the plot to a file
    download_plot_option('steps_plot.png') #Option to download the plot file
    
    df.plot(kind='scatter', x='day', y='calories') 
    plt4.savefig('calories_burned_plot.png')
    download_plot_option('calories_burned_plot.png')
    
    df.plot(kind='scatter', x='day', y='sleep') 
    plt4.savefig('sleep_plot.png')
    download_plot_option('sleep_plot.png')

    average_steps = df['steps'].mean()
    average_calories = df['calories'].mean()
    average_sleep = df['sleep'].mean()
    print(f"\nAverage steps: {average_steps}")
    print(f"Average calories burned: {average_calories}")
    print(f"Average sleep: {average_sleep} \n")
    std_steps = df['steps'].std()
    std_calories = df['calories'].std()
    std_sleep = df['sleep'].std()
    print(f"Standard Deviation of Steps: {std_steps}")
    print(f"Standard Deviation of Calories Burned: {std_calories}")
    print(f"Standard Deviation of Sleep: {std_sleep} \n")

    # Ask the user if they want to continue                                                                                                                                
    continue_input = input("Do you want to enter more data? (yes/no): ")
    if continue_input.lower() != 'yes':  
      # Calculate the correlation matrix
      correlation_matrix = df.corr()
      print("\nCorrelation Matrix:")
      print(correlation_matrix)
      if average_steps < 10000:
        print("\nYou need to get more active!\n")
      else:
        print("\nYou walk a healthy amount of steps! Keep it up!\n")
      if average_calories < 2000:
        print("You need to do more exercise!\n")
      else:
        print("You burn a healthy amount of calories! Keep it up!\n")
      if average_sleep < 420:
        print("You need to get more sleep!")
      else:
        print("You get a healthy amount of sleep! Keep it up!\n")
      break # Exit the loop if the user enters anything other than 'yes'

def get_user_health():
  #Collect health data from the user
  day_number = int(input("Enter the day number(+1 to the last day): "))
  number_of_steps_taken = int(input("Enter the number of steps taken: "))
  number_of_calories_burned = int(input("Enter the number of calories burned: "))
  minutes_of_sleep = int(input("Enter the number of minutes of sleep: "))
  #Set these variables equal to the class variables
  new_health = Health(
    day=day_number, steps=number_of_steps_taken, calories=number_of_calories_burned, sleep=minutes_of_sleep
  )
  return new_health

def save_health_to_file(health, health_file_path):
  #Saves the health data to the csv file
  with open(health_file_path, "a") as f:
    f.write(f"{health.day},{health.steps},{health.calories},{health.sleep}\n")

def clear_csv_file(health_file_path):
  #Clears the contents of a CSV file.
  with open(health_file_path, "w") as f:
    f.write("day,steps,calories,sleep\n") 
 
def delete_png_files(directory):
  #Deletes all PNG files in a given   directory.
  for filename in os.listdir(directory):
    if filename.endswith(".png"):
      file_path = os.path.join(directory, filename)
      os.remove(file_path)

def download_plot_option(plot_filename):
  #Asks the user if they want to download the plot and saves it if they choose yes.
  download_choice = input(f"\nDo you want to download the {plot_filename} plot? (yes/no): ")
  if download_choice.lower() == 'yes':
      download_and_save_plot(plot_filename)

def download_and_save_plot(plot_filename):
  #Downloads the plot from the Replit file system and saves it locally.
  url = f"https://replit.com/@{os.environ['REPL_OWNER']}/{os.environ['REPL_SLUG']}/files/{plot_filename}"
  response = requests.get(url)
  with open(plot_filename, "wb") as f:
      f.write(response.content)     
      
if __name__ == "__main__":
  main() 