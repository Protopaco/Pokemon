
import pickle

def create_file():
    file_name = input("Give full filename: ")
    temp_list = []
    with open(file_name, 'r') as open_file:
        line = open_file.readline()
        temp_list.append(line)
        while line:
            line = open_file.readline()
            temp_list.append(line)

    open_file.close()
    ttemp_list = "".join(temp_list)
    t_file_name = file_name.split(".")
    tt_file_name = t_file_name[0] + '.pok'
    dbfile = open(tt_file_name, 'ab')
    pickle.dump(ttemp_list, dbfile)
    dbfile.close()

if __name__ == "__main__":
    create_file()