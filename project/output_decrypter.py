def bits_to_text(binary_str):
    """
    Convert binary string back to original text
    Reverses the text_to_bits function
    
    Args:
        binary_str: String of '0's and '1's (output from text_to_bits)
        
    Returns:
        Original text string
    """
    # Verify input is binary string
    if not all(c in '01' for c in binary_str):
        # If not, remove non-binary characters
        binary_str = ''.join(c for c in binary_str if c in '01')
    
    # Split into 8-bit chunks
    chunks = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    
    # Convert to characters
    text = ''
    for chunk in chunks:
        # Skip incomplete chunks at the end
        if len(chunk) < 8:
            break
            
        # Convert to decimal then to character
        char_code = int(chunk, 2)
        text += chr(char_code)
    
    return text

# Example usage
if __name__ == "__main__":
    input_path = r'C:/Users/thusa.THUSA/Downloads/New folder (6)/output lora.txt'
    output_path = r'C:/Users/thusa.THUSA/Downloads/New folder (6)/output_text.txt'
    
    # Read input file with error handling
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            binary_str = f.read()
            binary_str = str(binary_str)
        print(f"Read {len(binary_str)} characters from file")
    except Exception as e:
        print(f"Error reading file: {e}")
        exit()
    
    # Convert bits to text
    text_output = bits_to_text(binary_str)
    
    # Save output with UTF-8 encoding
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_output)
        print(f"Decryption complete. Saved to {output_path}")
    except Exception as e:
        print(f"Error writing file: {e}")

    # Print decoded message safely
    print("\nDecoded message preview (first 100 characters):")
    printable_text = ''.join(c if c.isprintable() else f'\\x{ord(c):02x}' for c in text_output[:100])
    print(printable_text)
