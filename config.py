import ujson

def json_read(DATA):
    # grab config from json
    write_values=0
    try:
        json_data_file = open('config.json', 'r')
        DATA = ujson.loads(json_data_file.read())
        json_data_file.close()
        print(DATA)
        return DATA
    except:
        print("Cloud not read config file")
        json_write(DATA)

# Setup Json Write
def json_write(DATA):
    """ Writes global data value to config file """
    try:
        json_data_file = open('config.json', 'w')
        json_data_file.write(ujson.dumps(DATA))
        json_data_file.close()
    except Exception as e:
        print("Could not update config file %s" % e)
