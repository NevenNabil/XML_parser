# Implementing comprission algorithm 

# Huffman Coding Algorithm
hashing_table = dict() 

# Creating tree nodes
class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)

# string = test_text # Dummy input
# string = "['def', 'example', 'example', 'synset', 'synsets', 'data']"
# string = "<starttag>value</endtag>"


# Main function implementing huffman coding
def huffman_code_tree(node, left=True, binString=''):
    '''
    Takes a character (a node) from generate_hash_table() function and inserts it in the huffman tree
    based on its number of repetitions
    '''
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d


def generate_hash_table(string):
    '''
    Takes a string as a parameter and calculates the frequency of each character in the given string, it then 
    calls the huffman_code_tree() function to insert that character in the tree based on its frequency.
    Returns a dictionary with each character and its corrosponding hashing value.
    '''
    hashing_table = dict()
    hashing_table.clear()
    # Calculating frequency
    freq = {}
    for c in string:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    nodes = freq

    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))

        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    huffmanCode = huffman_code_tree(nodes[0][0])

    # for (char, frequency) in freq:
    #     print(' %-4r |%12s' % (char, huffmanCode[char]))

    for (char, frequency) in freq:
        hashing_table[char] = huffmanCode[char]

    return hashing_table


# Converting the given text into binary
def string_to_binary(string, unique_characters):
    '''
    Converts the given string into binary based on the hashing table generated by the generate_hash_table() function.
    Takes the string to be converted and unique_characters (hashing_table) as parameters.
    Returns a stream of 0s and 1s #### AS STRING NOT BINARY ### 
    '''
    compressed_data = ""
    for i in range(len(string)):
        compressed_data += str(unique_characters[string[i]])
    #print(string)
    #print (compressed_data)
    return compressed_data
    
# Encoding the binary stream into characters
def encode(bitstring):
    '''
    Takes the bitstring (output of the string_to_binary() function) and maps each 8 bits of it into their 
    corrosponding ASCII character
    returns the encoded string.
    '''
    wholebytes = len(bitstring) // 8
    chars = [chr(int(bitstring[i*8:i*8+8], 2)) for i in range(wholebytes)]
    remainder = bitstring[wholebytes*8:]
    return ''.join(chars)

################
# Now compressing and encoding are done, let's get to the decoding and reconstruction of the data
################

# Converting the encoded string into binary string (huffman binary string)
def decode(encoded_message):
    '''
    Takes the encoded_message() (output of the encode() function)
    and reconstructs the bit stream again
    '''
    output = ""

    for i in encoded_message:
        temp = ""
        if len(bin(ord(i))[2:]) <9: #if the remaining sequence isn't 8 bits long, it would raise an error when trying to convert to ASCII
            temp = '0'*(8-len(bin(ord(i))[2:]))+bin(ord(i))[2:] #add zeros on the left until it's 8 bits
        else:
            temp = bin(ord(i))[2:] #convert the character into binary
            # output of ord() is in format 0b00000000 so we take [2:] to remove the '0b
        output=output +temp

    return output


# Converting the binary stream back into a string
def binary_to_string(compressed_data,unique_characters):
    '''
    Takes the decoded message from the decode() function and the hashing_table as arguments and 
    reconstructs the original string based on the hashing_table.
    Returns the reconstructed data which should be the same as the original data if all went well.
    '''
    extracted_data = ""
    temp = ""

    for i in compressed_data:
        temp += str(i)
        if temp in list(unique_characters.values()):
            extracted_data += list(unique_characters.keys())[list(unique_characters.values()).index(temp)]
            temp = ""
    #    else:
    #        temp = ""
    # print(extracted_data)
    # print("original size = ", len(string)*8 , "bits\n")
    # print("Compressed size = ", len(data), "\n\n", data , type(data))
    return extracted_data


#testing

# c_data = string_to_binary(string)
# # b_data = binary_to_string(c_data)
# encoded_data = encode(c_data)
# print("------\n",encoded_data)
# print(len(encoded_data))
# print(len(string))
# # 11110110111001100001101101000110000110011110111111101011010010111110100111101101111001

# decoded_data = decode(encoded_data)
# reconstructed_data = binary_to_string(decoded_data)
# print(decoded_data)
# print(reconstructed_data)
# print(string)
##########################
# with open('data-sample-medium.xml','r') as fs:
#     small_data = fs.read()

# small_data = small_data.replace("   ","")
# small_data = small_data.replace("\n","")
# hash_dict = generate_hash_table(small_data)

# s_to_r = string_to_binary(small_data,hash_dict)

# enc = encode(s_to_r)

# dec = decode(enc)

# r_to_s = binary_to_string(dec, hash_dict)
# # print(r_to_s)
# with open('data-compressed.txt','w', encoding = 'utf-8') as fsh:
#     fsh.write(enc)

# with open('data-decompressed.txt','w', encoding = 'utf-8') as fsh:
#     fsh.write(r_to_s)

# # Compression
# with open('data-compressed.txt','w', encoding = 'utf-8') as fsh:
#     fsh.write(encode(string_to_binary(small_data,generate_hash_table(small_data))))

# # Decompression
# with open('data-decompressed.txt','w', encoding = 'utf-8') as fsh:
#     fsh.write(binary_to_string(decode(enc), generate_hash_table(small_data)))
