import os

def convert_dmm_to_dd(dmm):
    return int(dmm[:2]) + (float(dmm[2:]) / 60)

def convert_raw_file(file_path, temp_file_path): # example line: $GNRMC,   151011.800,      A,        5231.91008,N,  00605.51763,E,   1.12   ,138.32   ,100125,     ,           , A,       V         *09
                                                                       #         <--time-->  <data status>  <---lat---->   <----lon---->   <speed> <course>  <date> <<magnetic data>> <mode> <nav status> <checksum>
    try:
        if not os.path.exists(self.temp_file_foder):
            os.mkdir(self.temp_file_foder)

        if os.path.exists(temp_file_path):
            return False

        with open(temp_file_path, "w") as temp_file:
            with open(file_path, "r") as raw_file:
                for line in raw_file:
                    if line.startswith("$GNRMC"):
                        line = line.strip()
                        line_string = line.split(",")

                        time = line_string[1]
                        lat_dmm = line_string[3]
                        lat_dir = line_string[4]
                        lon_dmm = line_string[5]
                        lon_dir = line_string[6]

                        lat_dd = convert_dmm_to_dd(lat_dmm)
                        lon_dd = convert_dmm_to_dd(lon_dmm)

                        if lat_dir == "S":
                            lat_dd = -lat_dd
                        if lon_dir == "W":
                            lon_dd = -lon_dd

                        temp_file.write(f"{time}, {lat_dd}, {lon_dd}\n")

        print(f'processed "{file_path}" -> "{temp_file_path}"')
        return True
    except Exception as e:
        print(f'error processing "{file_path}": {e}')
        return False
