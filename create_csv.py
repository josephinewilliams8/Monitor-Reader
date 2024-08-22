import pandas as pd

df = pd.DataFrame({'date':[], 'time':[], 'sm3/h':[], 'sm3':[]})

def confirmation(file_path):
    print(f'Do you want to erase the {file_path} file? This action cannot be undone!') 
    confirm = input("Enter 'yes' or 'no' to confirm:")
    if confirm == "yes":
        df.to_csv({file_path}, sep=',', index=False, encoding='utf-8')
        print(f'{file_path} has been erased!')
    elif confirm == 'no':
        print(f'{file_path} has not been erased.')
    elif confirm == 'perhaps':
        print(f"Don't be silly! Please enter 'yes' or 'no' to confirm.")
    else:
        print("Invalid input. Please enter 'yes' or 'no' to confirm.")
        confirmation(file_path)

print(f'If "Monitor Readings.csv" or "Tester.csv" are not yet in the working directory, 
      please respond "yes" to the following questions to initialize the CSV files.')

confirmation('Monitor Readings.csv')

confirmation('Tester.csv')
