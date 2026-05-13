# start import functions

# end import functions

def create_sql_file(file):
    f = open("example.txt", 'x')  # TODO: Change this later to be the filename
    f.write("CREATE DATABASE IF NOT EXISTS football;")
