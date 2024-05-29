class Test:
    def firstTest(self, filename):

        # Task 2: Read the text file from "sample.txt"
        with open(filename, 'r') as file:
            print("\n Task 2:")
            for text in file:
                print(text.strip())
        
        # Task 3: Get the text number (index) and text string for each text
        tuple_list = [(index, text.strip()) for index, text in enumerate(open(filename))]
        print("\n Task 3:")
        for index, text in tuple_list:
            print(f"Line {index}: {text}")
        
        # Task 4: Make a list of tuples [(index, string)]
        list_of_tuples = tuple_list
        
        # Task 5: Make a list of dictionaries with keys and values like [{"index": index, "text": "textstring", "total_words": total words count in each string}]
        dict_list = [
            {
                "index": index,
                "text": text,
                "total_words": len(text.split())
            }
            for index, text in tuple_list
        ]
        
        return list_of_tuples, dict_list

if __name__ == "__main__":

    # Task 1: Save the text line-wise in one file with name sample.txt
    text = """Python is a general-purpose interpreted, interactive, object-oriented and high-level programming language.
    it was created by Guido van Rossum during 1985-1990.
    like Perl, Python source code is also available under the GNU General Public
    License (GPL). This tutorial gives you enough understanding on python Programming Language."""
    
    with open('sample.txt', 'w') as file:
        file.write(text)
        print("Task 1:creation of sample.txt is done ")
    
    test = Test()
    filename = 'sample.txt'
    list_of_tuples, dictionary_list = test.firstTest(filename)
    
    print("\n Task 4: List of Tuples:")
    print(list_of_tuples)
    
    print("\n Task 5: List of Dictionaries:")
    print(dictionary_list)



