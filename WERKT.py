from PyGnuplot import gp
import os

class DataPlotter:
    def __init__(self, input_file="0015_output", debug=False):
        self.input_file = input_file
        self.debug = debug
        self.f1 = gp()
        self.temp_file = f"temp/{self.input_file}.dat"
        self.data = None
        if self.debug:
            print(f"[DEBUG] Initialized DataPlotter with input_file: {self.input_file}")
            print(f"[DEBUG] Temporary file will be: {self.temp_file}")
    
    def load_data(self):
        try:
            with open(f"{self.temp_file}", 'w') as output_file:
                with open(f"{self.input_file}.txt", 'r') as input_file:
                    for line in input_file:
                        if line.startswith(">23|01:"):
                            processed_line = line.removeprefix(">23|01:").strip()
                            processed_line = ' '.join(['None' if segment == '' else segment for segment in processed_line.split(',')])
                            output_file.write(processed_line + "\n")
            
            print(f"Processed {self.input_file}.txt -> {self.temp_file}.dat")
        
        except FileNotFoundError:
            print(f"Error: One of the files not found.")
        except Exception as e:
            print(f"An error occurred: {e}")


#    def validate_column_numbers(self, column_numbers):
#        """Validate the column numbers against the data shape."""
#        if self.debug:
#            print(f"[DEBUG] Validating column numbers: {column_numbers}")
#        valid = all(1 <= num <= self.data.shape[0] for num in column_numbers)
#        if self.debug:
#            if valid:
#                print(f"[DEBUG] All column numbers are valid.")
#            else:
#                print(f"[DEBUG] Some column numbers are invalid.")
#        return valid

    def plot_data(self):
        """Prompt user for column numbers and plot the data."""

        try:
            while True:
                column_numbers = input("Enter the column numbers to plot (e.g., 2,6,7), or enter nothing to quit: ")
                if self.debug:
                    print(f"[DEBUG] User input for column numbers: '{column_numbers}'")
                if column_numbers.lower() == "":
                    print("Exiting the plotting interface.")
                    break

                try:
                    column_numbers = [int(num) for num in column_numbers.split(',')]
                    if self.debug:
                        print(f"[DEBUG] Parsed column numbers: {column_numbers}")
                    #if not self.validate_column_numbers(column_numbers):
                    #    print("Invalid column number(s). Please try again.")
                    #    continue

                    plot_command = ', '.join([f'"{self.temp_file}" u 1:{num} w lp' for num in column_numbers])
                    if self.debug:
                        print(f"[DEBUG] Plot command: plot {plot_command}")
                    self.f1.c(f'plot {plot_command}')  # Plot the data
                    print("Plot command executed successfully.")

                except ValueError:
                    print("Please enter valid integers for column numbers.")
                    if self.debug:
                        print("[DEBUG] ValueError encountered while parsing column numbers.")

        finally:
            self.cleanup()

    def cleanup(self):
        """Remove the temporary file if it exists."""
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
            if self.debug:
                print(f"[DEBUG] Temporary file {self.temp_file} removed.")
            print(f"Temporary file {self.temp_file} removed.")
        else:
            if self.debug:
                print(f"[DEBUG] Temporary file {self.temp_file} does not exist, no cleanup needed.")

    def run(self):
        """Run the data loading and plotting process."""
        if self.debug:
            print("[DEBUG] Starting the run process.")
        self.load_data()
        self.plot_data()
if __name__ == "__main__":
    input_file = input("file path: ")
    debug_mode = input("Enable debug mode? (y/N): ").lower() == 'y'
    plotter = DataPlotter(input_file, debug=debug_mode)
    plotter.run()