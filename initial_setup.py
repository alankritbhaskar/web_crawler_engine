import os

#Each website whic is crawled should be in a separate project directory
def create_project_dir(directory):
    if not os.path.exists(directory): # should make new directory only if it does not exist
        print('Creating Project '+directory) 
        os.makedirs(directory)

# Create queue and crawled files(if not present already)
def create_data_files(project_name,base_url):
    queue = project_name+'/queue.txt' # a list of links waiting to be crawled
    crawled = project_name+'/crawled.txt' # a list of all links crawled so far
    if not os.path.isfile(queue):
        write_file(queue,base_url) # so that at starting queue is not empty 
    if not os.path.isfile(crawled):
        write_file(crawled,'') # should be empty at starting so that crawler initially does not considers any file to be already crawled

# Create a new file
def write_file(path, data):
    file = open(path, 'w') # open file in write mode
    file.write(data) # actually write data in it
    file.close() # close the file after writing data is done 

# create_data_files('thenewdir','https://google.com/')

# Add data on an existing file
def append_to_file(path, data):
    with open(path,'a') as file: # open file in append mode, for adding more links on same page
        file.write(data,'\n')

# Delete the content of a file
def delete_file_contents(path):
    with open(path,'w'): # just create a new file with same name
        pass # do nothing

# Read a file and convert each line to items of a set
def file_to_set(file_name):
    results = set() # an empty set
    with open(file_name, 'rt') as f:
        for line in f: # iterate each line and add 
            results.add(line.replace('\n',''))
    return results

# Iterate through a set, each item will be a new line in the file
def set_to_file(links, file):
    delete_file_contents(file) # we can delete all data in the old file, as complete
                                # new data is present in the set named links
    for link in sorted(links):
        append_to_file(file, link)

